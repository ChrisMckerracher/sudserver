from db.redis.redis_entity import RedisEntity


class RedisAdminWSSession(RedisEntity):
    sid: any
    id: str = "admin_ws"


