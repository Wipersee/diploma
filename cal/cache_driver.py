import redis
from config.settings import REDIS_TTL


class RedisDriver:
    def __init__(self):
        self.conn = redis.Redis(host="localhost", port=6379, db=0)

    def get(self, key):
        return self.conn.get(key)

    def update(self, key, value):
        if not self.conn.set(key, value, ex=REDIS_TTL):
            return False
        return True

    def delete(self, key):
        if not self.conn.delete(key):
            return False
        return True


cache_driver = RedisDriver()
