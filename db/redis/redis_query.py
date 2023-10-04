from pydantic import BaseModel
from pydantic._internal._model_construction import ModelMetaclass
from redis.client import Redis
from typing import Optional, Generic, TypeVar, ForwardRef, Union, get_args

# 10 minutes
# ToDo: makes this configurable potentially... you dont want session persist time to actually be 10 minutes
persist_time = 60 * 10

# bound=RedisEntity but then we have a cicular dependency
# also... absolutely dont do this, modelmetaclass is not supposed to be referenced directly. its not a gaurantee of pydantic's api and is an internal implementation
T = TypeVar("T", bound=ModelMetaclass)


#ToDo: keeping this generic stuff so i can take more of a look at it later
class RedisQuery(BaseModel, Generic[T]):
    client: Redis
    type: ModelMetaclass

    def get(self, key: str) -> Optional[T]:
        data = self.client.get(key)

        if (data):
            # ToDo: test case this on data string
            return self.type.model_validate_json(data)

    def save(self, key: str, value: T):
        self.client.set(key, value.json(), ex=persist_time)

    def get_t(self):
        return self.__orig_bases__[0]


    class Config:
        arbitrary_types_allowed = True
