from unittest.mock import patch, MagicMock

import pytest

redis_mock = MagicMock()
from module.redis.redis_client import is_redis_ready, check_redis, acquire_lock, release_lock, wait_til_redis_ready


def test_is_redis_ready_ok():
    with patch('redis.Redis.ping'):
        assert is_redis_ready() is True


def test_is_redis_ready_fail():
    def raise_error():
        raise Exception

    with patch('redis.Redis.ping', side_effect=raise_error):
        assert is_redis_ready() is False


def test_check_redis():
    with patch('utils.redis_client.is_redis_ready', return_value='tested'):
        assert check_redis()[0] == 'tested'


def test_acquire_lock_timeout():
    with patch('redis.Redis.setnx', return_value=False):
        with pytest.raises(TimeoutError):
            acquire_lock('test_lock', timeout=0.03, sleep_time=0.01)


def test_acquire_lock_success():
    with patch('redis.Redis.setnx', return_value=True), patch('redis.Redis.expire', return_value=True):
        acquire_lock('test_lock', timeout=1, ttl=1)


def test_release_lock():
    with patch('redis.Redis.delete') as mock:
        release_lock('test_lock')
        mock.assert_called_with('test_lock')


def test_wait_til_redis_ready_timeout():
    with patch('utils.redis_client.is_redis_ready', return_value=False):
        with pytest.raises(TimeoutError):
            wait_til_redis_ready(timeout=0.03, sleep_time=0.01)
