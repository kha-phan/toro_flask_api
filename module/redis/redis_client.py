import time
import redis

from utils import config, logger


redis_client = redis.Redis(
    host=config.get('redis.host'),
    port=config.get('redis.port'),
    db=config.get('redis.db'),
    password=config.get('redis.password'),
    decode_responses=True
)


def is_redis_ready():
    try:
        redis_client.ping()
        return True
    except Exception:
        return False


def check_redis():
    begin = time.time()
    return is_redis_ready(), time.time() - begin


if is_redis_ready():
    logger.info(f'Redis is ready.')
else:
    logger.warning('Redis is NOT ready!')


def acquire_lock(lock_name: str, timeout: float = None, sleep_time: float = 0.1, ttl: int = None):
    """
    Simple distributed lock
    :param lock_name:
    :param timeout:
    :param sleep_time:
    :param ttl:
    :return:
    """
    begin = time.time()
    while not redis_client.setnx(lock_name, 1):
        if timeout is not None and time.time() - begin >= timeout:
            raise TimeoutError
        time.sleep(sleep_time)
    if ttl:
        redis_client.expire(lock_name, ttl)


def release_lock(lock_name: str):
    """
    Release distributed lock
    :param lock_name:
    :return:
    """
    redis_client.delete(lock_name)


def wait_til_redis_ready(timeout: float = None, sleep_time: float = 0.5):
    begin = time.time()
    while not is_redis_ready():
        if timeout is not None and time.time() - begin >= timeout:
            raise TimeoutError
        time.sleep(sleep_time)
