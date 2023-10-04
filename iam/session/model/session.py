from db.redis.redis_entity import RedisEntity


class Session(RedisEntity):
    index: str = "session"
    #secure string is id
    user_id: str
