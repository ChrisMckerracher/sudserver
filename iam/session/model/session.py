from db.redis.redis_entity import RedisEntity


class Session(RedisEntity):
    index = "session"
    #secure string
    sec_string: str
    #id will be user_id
