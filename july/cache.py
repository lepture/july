from time import time as sys_time
from tornado.options import options


class _Cache(object):
    """python-memcahe compatable instance cache
    """
    def __init__(self):
        self._app_cache = {}

    @classmethod
    def create_instance(cls):
        if hasattr(cls, '_instance'):
            return cls._instance

        if hasattr(options, 'memcache_clients') and options.memcache_clients:
            try:
                import pylibmc
                cache = pylibmc.Client(options.memcache_clients,
                                       **options.memcache_kwargs)
                cls._instance = cache
                return cls._instance
            except ImportError:
                import memcache
                cache = memcache.Client(options.memcache_clients,
                                        **options.memcache_kwargs)
                cls._instance = cache
                return cls._instance
            except ImportError:
                cls._instance = cls()
                return cls._instance
        else:
            cls._instance = cls()
            return cls._instance

    def flush_all(self):
        self._app_cache = {}

    def set(self, key, val, time=0):
        key = str(key)
        if time < 0:
            time = 0

        self._app_cache[key] = (val, sys_time(), time)
        return val

    def get(self, key):
        key = str(key)
        _store = self._app_cache.get(key, None)
        if not _store:
            return None
        value, begin, seconds = _store
        if seconds and sys_time() > begin + seconds:
            del self._app_cache[key]
            return None
        return value

    def add(self, key, val, time=0):
        key = str(key)
        if key not in self._app_cache:
            return self.set(key, val, time)
        return self.get(key)

    def delete(self, key, time=0):
        key = str(key)
        if key in self._app_cache:
            del self._app_cache[key]
        return None

    def incr(self, key, delta=1):
        key = str(key)
        _store = self._app_cache.get(key, None)
        if not _store:
            return None

        value, begin, seconds = _store
        if seconds and sys_time() > begin + seconds:
            del self._app_cache[key]
            return None

        if isinstance(value, basestring):
            value = int(value)

        value = value + delta
        self.set(key, value)
        return value

    def decr(self, key, delta=1):
        return self.incr(key, -delta)

    def set_multi(self, mapping, time=0, key_prefix=''):
        for key, value in mapping.items():
            self.set('%s%s' % (key_prefix, key), value, time)

        return True

    def get_multi(self, keys, key_prefix=''):
        dct = {}
        for key in keys:
            value = self.get('%s%s' % (key_prefix, key))
            dct[key] = value

        return dct

    def delete_multi(self, keys, time=0, key_prefix=''):
        for key in keys:
            self.delete('%s%s' % (key_prefix, key))

        return None


cache = _Cache.create_instance()
