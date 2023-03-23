from unittest.mock import patch

from module.redis.redis_cache import RedisCache as CacheService

dummy = None


def test_get():
    class TestCache:
        @classmethod
        def get(cls, name, key):
            return 'tested', name, key

    CacheService.cache = TestCache
    assert CacheService.get('name', 'key') == ('tested', 'name', 'key')


def test_get_error():
    class TestCache:
        @classmethod
        def get(cls, name, key):
            raise

    CacheService.cache = TestCache
    assert CacheService.get('name', 'key') is None


def test_set():
    class TestCache:
        @classmethod
        def set(cls, name, key, value):
            global dummy
            dummy = (name, key, value)

    CacheService.cache = TestCache
    assert CacheService.set('name', 'key', 'value') is True
    assert dummy == ('name', 'key', 'value')


def test_set_error():
    class TestCache:
        @classmethod
        def set(cls, name, key, value):
            raise

    CacheService.cache = TestCache
    assert CacheService.set('name', 'key', 'value') is False


def test_bulk_set():
    class TestCache:
        @classmethod
        def bulk_set(cls, name, items):
            global dummy
            dummy = (name, items)

    CacheService.cache = TestCache
    assert CacheService.bulk_set('name', {'a': 'value'}) is True
    assert dummy == ('name', {'a': 'value'})


def test_bulk_set_error():
    class TestCache:
        @classmethod
        def set(cls, name, items):
            raise

    CacheService.cache = TestCache
    assert CacheService.bulk_set('name', {'a': 'value'}) is False


def test_exists():
    class TestCache:
        @classmethod
        def exists(cls, name, key):
            return 'tested', name, key

    CacheService.cache = TestCache
    assert CacheService.exists('name', 'key') == ('tested', 'name', 'key')


def test_exists_raise():
    class TestCache:
        @classmethod
        def exists(cls, name, key):
            raise

    CacheService.cache = TestCache
    assert CacheService.exists('name', 'key') is None


def test_scan_iter():
    class TestCache:
        @classmethod
        def scan_iter(cls, name, count):
            return 'tested', name

    CacheService.cache = TestCache
    assert CacheService.scan_iter('name') == ('tested', 'name')


def test_scan_iter_raise():
    class TestCache:
        @classmethod
        def scan_iter(cls, name, count):
            raise

    CacheService.cache = TestCache
    assert CacheService.scan_iter('name') == ()


def test_delete():
    class TestCache:
        @classmethod
        def delete(cls, name):
            return 'tested', name

    CacheService.cache = TestCache
    assert CacheService.delete('name') == ('tested', 'name')


def test_delete_raise():
    class TestCache:
        @classmethod
        def delete(cls, name):
            raise

    CacheService.cache = TestCache
    assert CacheService.delete('name') is False


def test_invalidate():
    class TestCache:
        @classmethod
        def invalidate(cls, name, key):
            return 'tested', name, key

    CacheService.cache = TestCache
    assert CacheService.invalidate('name', 'key') == ('tested', 'name', 'key')


def test_invalidate_raise():
    class TestCache:
        @classmethod
        def invalidate(cls, name, key):
            raise

    CacheService.cache = TestCache
    assert CacheService.invalidate('name', 'key') is False


def test_license_info_exists():
    def custom_fn(name, key):
        if name != 'license:some_id' or key not in ('str', 'exp'):
            raise
        return True

    with patch('services.cache_service.CacheService.exists', side_effect=custom_fn):
        assert CacheService.license_info_exists('some_id') is True


def test_get_license_info():
    with patch('services.cache_service.CacheService.get', return_value=('lic str', '10000.0')) as cache_mock:
        assert CacheService.get_license_info('some_id') == ('lic str', 10000)
        cache_mock.assert_called_with('license:some_id', ['str', 'exp'])


def test_set_license_info():
    with patch('services.cache_service.CacheService.bulk_set') as set_mock:
        CacheService.set_license_info('some_id', '34dhf01', '32194')
        set_mock.assert_called_with('license:some_id', {
            'str': '34dhf01',
            'exp': '32194'
        })
