import redis


redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True,
    protocol=2
)


def get_redis():

    return redis_client