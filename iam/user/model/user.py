from db.redis.redis_entity import RedisEntity
from iam.user.model.user_role import UserRole


class User(RedisEntity):
    role: UserRole
    index: str = "user"
