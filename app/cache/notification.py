# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import redis

from app.settings import Redis


_SUBJECT_NOTIFICATION = 'subject:notification:{0}'

conn = redis.StrictRedis(**Redis['notification'])

def publish(target, msg):
    conn.publish(_SUBJECT_NOTIFICATION.format(target), msg)
