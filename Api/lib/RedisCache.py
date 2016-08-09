#coding=utf-8

import redis

RedisCache = redis.Redis(host='127.0.0.1', port=6379, db=2)
