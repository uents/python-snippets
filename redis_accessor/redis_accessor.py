# -*- coding: utf-8 -*-
"""redis accessor

Redis accessor class
"""

import redis

_CHARSET = 'utf-8'


class RedisAccessor():
    """Redis accessor"""

    def __init__(self, host='localhost', port=6379, db=0):
        self.__redis = redis.StrictRedis(host=host, port=port, db=db)
        self.__pipeline = None

    def __del__(self):
        print('__del__')

    def __enter__(self):
        print('__enter__')
        self.__pipeline = self.__redis.pipeline()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('__exit__')
        self.__pipeline.execute()
        self.__pipeline = None

    def set(self, key, value):
        """set a key-value pair"""
        if isinstance(value, dict):
            return self.__redis.hmset(key, value)
        return self.__redis.set(key, value)

    def get(self, key):
        """get value for the key"""
        try:
            value = self.__redis.hgetall(key)
        except redis.ResponseError:
            pass
        else:
            if value is None:
                return None
            return {k.decode(_CHARSET): v.decode(_CHARSET)
                    for k, v in value.items()}
        try:
            value = self.__redis.get(key)
        except redis.ResponseError:
            pass
        else:
            if value is None:
                return None
            return value.decode(_CHARSET)
        return None

    def push(self, key, values):
        pass

    def pop(self, key):
        pass
