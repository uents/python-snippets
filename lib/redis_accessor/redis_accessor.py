# -*- coding: utf-8 -*-
"""redis accessor

Redis accessor class
"""

import redis

_CHARSET = 'utf-8'
_DEFAULT_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'db': 0
}


class RedisAccessor():
    """Redis accessor"""

    def __init__(self, config=None, max_retry_count=0, logger=None):
        if config is None:
            config = _DEFAULT_CONFIG
        self.__redis = redis.StrictRedis(host=config['host'],
                                         port=config['port'],
                                         db=config['db'],
                                         socket_timeout=5,
                                         encoding=_CHARSET)
        self.__max_retry_count = max_retry_count
        self.__logger = logger if logger else LocalLogger()
        self.__pipe = None

    def __del__(self):
        self.__logger.info('__del__')

    def __enter__(self):
        self.__logger.info('__enter__')
        self.__pipe = self.__redis.pipeline()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__logger.info('__exit__')
        if self.__pipe:
            self.__pipe.execute()
        self.__pipe = None

    def set(self, *props):
        """set key-value pair"""
        # TODO リトライ
        return self.__set(*props)

    def __set(self, *props):
        if isinstance(props[0], dict):
            return self.__redis.mset(props[0])
        elif isinstance(props[0], str) and (props[1], str):
            return self.__redis.set(props[0], props[1])
        elif isinstance(props[0], str) and (props[1], dict):
            return self.__redis.hmset(props[0], props[1])
        raise TypeError('unexpected property: {}'.format(*props))

    def get(self, key):
        """retrieve value from the key"""
        # TODO リトライ
        return self.__get(key)

    def __get(self, key):
        if isinstance(key, list):
            value = self.__redis.mget(key)
            return {k: v.decode(_CHARSET) if v else None for k, v in zip(key, value)}
        elif self.__redis.type(key) == b'string':
            value = self.__redis.get(key)
            return value.decode(_CHARSET) if value else None
        elif self.__redis.type(key) == b'hash':
            value = self.__redis.hgetall(key)
            return {k.decode(_CHARSET): v.decode(_CHARSET) for k, v in value.items()}
        elif self.__redis.type(key) == b'none':
            return None
        raise KeyError('unexpected key: {}'.format(key))

    def push(self, key, value):
        """push value to queue"""
        # TODO リトライ
        return self.__push(key, value)

    def __push(self, key, value):
        return self.__redis.lpush(key, value)

    def pop(self, key, timeout=5):
        """pop value from queue (with block wait)"""
        # TODO リトライ
        return self.__pop(key, timeout)

    def __pop(self, key, timeout):
        pair = self.__redis.brpop(key, timeout=timeout)
        if isinstance(pair, tuple):
            return pair[1].decode(_CHARSET)
        return None

    def peek(self, key):
        # XXX いまのところ実装不要
        raise NotImplementedError


class LocalLogger():
    def error(self, *args, **kwargs):
        print(*args, **kwargs)

    def info(self, *args, **kwargs):
        print(*args, **kwargs)


if __name__ == '__main__':
    pass
