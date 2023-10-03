from db.redis.redis_entity import RedisEntity


class Session(RedisEntity):
    index = "session"
    #id will be user_id
