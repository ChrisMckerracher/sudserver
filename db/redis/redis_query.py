from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass
from redis.client import Redis
from typing import Optional, Generic, TypeVar, ForwardRef, Union

# 10 minutes
# ToDo: makes this configurable potentially... you dont want session persist time to actually be 10 minutes
persist_time = 60 * 10

# bound=RedisEntity but then we have a cicular dependency
# also... absolutely dont do this, modelmetaclass is not supposed to be referenced directly. its not a gaurantee of pydantic's api and is an internal implementation
T = TypeVar("T", bound=ModelMetaclass)


class RedisQuery(BaseModel, Generic[T]):
    client: Redis
    type: T

    def get(self, key: str) -> Optional[T]:
        data = self.client.get(key)

        if (data):
            # ToDo: test case this on data string
            T.parse_raw(data)

    def save(self, key: str, value: T):
        self.client.set(key, value.json(), ex=persist_time)

    class Config:
        arbitrary_types_allowed = True
