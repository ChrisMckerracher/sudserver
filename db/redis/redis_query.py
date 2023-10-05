from typing import Optional, TypeVar

from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass
from redis.client import Redis

# 10 minutes
# ToDo: makes this configurable potentially... you dont want session persist time to actually be 10 minutes
persist_time = 60 * 10

T = TypeVar("T", bound=ModelMetaclass)


class RedisQuery(BaseModel):
    client: Redis
    # I hate this I hate this I hate this
    type: ModelMetaclass

    def get(self, key: str) -> Optional[T]:
        data = self.client.get(key)

        if (data):
            # ToDo: test case this on data string
            return self.type.model_validate_json(data)

    def save(self, value: T):
        self.client.set(value.id, value.json(), ex=persist_time)

    class Config:
        arbitrary_types_allowed = True
