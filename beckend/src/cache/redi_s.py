from redis import Redis
import json


class RedisCache:
    def __init__(self, redis_url: str, redis_time_to_live_seconds: int):
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.redis_time_to_live_seconds = redis_time_to_live_seconds

    def set(self, key: str, value: dict):
        self.redis.set(key, json.dumps(value), ex=self.redis_time_to_live_seconds)

    def get(self, key: str) -> dict:
        value = self.redis.get(key)
        if value is not None:
            return json.loads(self.redis.get(key))

    def delete(self, key: str):
        self.redis.delete(key)

