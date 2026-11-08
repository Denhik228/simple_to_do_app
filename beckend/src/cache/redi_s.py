from redis import Redis


class RedisCache:
    def __init__(self, redis: ):
        self.redis = redis

    def set(self, key: str, value: dict):
        ...
    def get(self):
        ...
    def delete(self):
        ...
