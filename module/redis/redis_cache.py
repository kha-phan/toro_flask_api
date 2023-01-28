from redis_client import redis_client


class RedisCache():
    @staticmethod
    def get(name, key):
        if isinstance(key, list):
            return redis_client.hmget(name, key)
        return redis_client.hget(name, key)

    @staticmethod
    def set(name, key, value):
        return redis_client.hset(name, key, value)

    @staticmethod
    def bulk_set(name, items):
        data = []
        for k, v in items.items():
            data.extend((k, v))
        return redis_client.execute_command('HSET', name, *data)

    @staticmethod
    def exists(name, key=None):
        return bool((key is None or redis_client.hexists(name, key)) and redis_client.exists(name))

    @staticmethod
    def invalidate(name, key=None):
        if not key:
            return redis_client.delete(name)
        else:
            return redis_client.hdel(name, key)

    @staticmethod
    def delete(*name):
        return redis_client.delete(*name)

    @staticmethod
    def scan_iter(match=None, count=None):
        return redis_client.scan_iter(match, count)
