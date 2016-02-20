# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import redis

from app.settings import Redis


_KEY_NUM = '2L:gold:num'
_KEY_GOLD = '2L:gold:gold'
_KEY_USERS = '2L:gold:robed-users'

conn = redis.StrictRedis(**Redis['gold'])


def delete_all():
    # conn.delete(_KEY_NUM, _KEY_GOLD, _KEY_USERS)
    conn.flushdb()


def set(num, gold):
    delete_all()
    conn.set(_KEY_NUM, num)
    conn.set(_KEY_GOLD, gold)


def get(username, func):
    """Use Redis optimistic locking.

     0  no more gold today
     -1 can not rob again
    """
    with conn.pipeline() as pipe:
        while 1:
            try:
                pipe.watch(_KEY_NUM, _KEY_GOLD)

                if pipe.hexists(_KEY_USERS, username):
                    return -1

                left_num = int(pipe.get(_KEY_NUM) or 0)
                left_gold = int(pipe.get(_KEY_GOLD) or 0)
                if left_num == 0 and left_gold == 0:
                    return 0

                left_num -= 1
                gold = func(left_num, left_gold)
                left_gold -= gold

                pipe.multi()
                pipe.hmset(_KEY_USERS, username, 1)
                pipe.set(_KEY_NUM, left_num)
                pipe.set(_KEY_GOLD, left_gold)
                pipe.execute()
            except redis.WatchError:
                continue
            else:
                return gold
