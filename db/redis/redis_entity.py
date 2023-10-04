from pydantic import BaseModel
from redis.client import Redis

from db.redis.redis_query import RedisQuery

ExcludeFields =["key", "index"]


class RedisEntity(BaseModel):
    id: str
    index: str = ""

    @classmethod
    def query(cls, client: Redis) -> RedisQuery:
        return RedisQuery(client=client, type=cls)

    def dump(self):
        return self.model_dump(mode="json", exclude=set(ExcludeFields))
