from typing import Literal, get_args

from pydantic import BaseModel
from redis.client import Redis

from db.redis.RedisQuery import RedisQuery

ExcludeFields = Literal["key", "index"]


class RedisEntity(BaseModel):
    key: str
    index: str

    @classmethod
    @property
    def query(cls, client: Redis) -> RedisQuery:
        return RedisQuery(type=cls)

    def dump(self):
        return self.model_dump(mode="json", exclude=set(get_args(ExcludeFields)))