# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import redis

from app.settings import Redis


conn = redis.StrictRedis(
    host=Redis['host'],
    port=Redis['port'],
    db=Redis['session_db'],
)


def set(key, value, expires_days=1):
    conn.set(key, value)
    conn.expire(key, expires_days * 86400)

def get(key):
    return conn.get(key)

def delete(key):
    conn.delete(key)

def delete_all(key):
    conn.flushdb()
