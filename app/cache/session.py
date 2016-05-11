# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import redis

from app.settings import Redis


_KEY_FMT = '2L:session:{0}'
conn = redis.StrictRedis(**Redis['session'])


def set(key, value, expires_days=1):
    conn.set(_KEY_FMT.format(key), value)
    conn.expire(key, expires_days * 86400)

def get(key):
    return conn.get(_KEY_FMT.format(key))

def delete(key):
    conn.delete(_KEY_FMT.format(key))

def delete_all():
    conn.flushdb()
