from typing import TypeVar, Generic, Optional

from elasticsearch import Elasticsearch
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
        super().__init__(es, T.index)
        self.redis = redis

    def save(self, id: str, document) -> None:
        #ToDo: write to Redis store and async queue a write to ES task
        self.es.index(index=self.index, id=id, document=document)

    def get(self, id: str) -> Optional[T]:
        val = T.query(self.redis).get(id)

        if not val:
            json_string = self.search(id)
            if (json_string):
                val = T.model_validate_json(json_string)
                T.query.save(id, val)
                return val
            return None

    # there's no constraints that theres only 1 response. this is a self imposed requirement that i can totally accidentally break lol
    def search(self, id: str) -> Optional[T]:
        responses = self.es.search(index="entity", query={
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
