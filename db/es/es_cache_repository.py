from typing import TypeVar, Generic, Optional, cast, get_args

from elasticsearch import Elasticsearch
from pydantic import BaseModel
from redis.client import Redis

from db.es.es_repository import EsRepository
from db.redis.redis_entity import RedisEntity

import logging

T = TypeVar("T", bound=RedisEntity)
logger = logging.getLogger("EsCacheRepository")


# This is kind of insane becaue I'm using ES as if it's a regular row store with unique ids. Technically works, VERY awkward
class EsCacheRepository(EsRepository, Generic[T]):
    redis: Redis

    def __init__(self, es: Elasticsearch, redis: Redis):
        # there HAS to be a better way
        t_class: T = get_args(self.__orig_bases__[0])

        # ToDo: NO WAY this is the right way to do this...
        index = t_class[0].model_fields['index'].default
        super().__init__(es, index)
        self.redis = redis

    def save(self, id: str, document: BaseModel) -> None:
        #ToDo: write to Redis store and async queue a write to ES task
        self.es.index(index=self.index, id=id, document=document.model_dump_json())

    def get(self, id: str) -> Optional[T]:
        cls = self.get_t()
        val = cls.query(client=self.redis).get(id)

        if not val:
            json_string = self.search(id)
            if (json_string):
                val = cls.model_validate(json_string)
                cls.query(self.redis).save(id, val)
                return val
            return None

    # there's no constraints that theres only 1 response. this is a self imposed requirement that i can totally accidentally break lol
    # ToDo: you can actually just search the actual document by id instead of searching bro
    def search(self, id: str) -> Optional[T]:
        responses = self.es.search(index="user", query={
            "bool": {
                "must": [
                    {
                        "query_string": {
                            "fields": ["id"],
                            "query": id
                        }
                    },
                ]
            }})

        responses = [x["_source"] for x in responses["hits"]["hits"]]

        response_len = len(responses)

        if response_len > 1:
            logger.warning(f"responses: {responses} greater than 1", responses)

        if responses:
            return responses[0]

        return None

    def get_t(self):
        return get_args( self.__orig_bases__[0])[0]
