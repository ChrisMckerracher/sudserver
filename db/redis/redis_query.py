from redis.client import Redis
from pydantic import Generic, TypeVar
from typing import Optional

from db.redis.redis_entity import RedisEntity

T = TypeVar("T", bound=RedisEntity)

# 10 minutes
persist_time = 60 * 10


class RedisQuery(Generic[T]):
    client: Redis
    type: T

    def get(self, key: str) -> Optional[T]:
        data = self.client.get(key)

        if (data):
            # ToDo: test case this on data string
            T.parse_raw(data)

    def save(self, key: str, value: T):
        self.client.set(key, value, ex=persist_time, keepttl=True)
