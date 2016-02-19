# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import redis

from app.settings import Redis


_KEY_NUM = '2L:gold:num'
_KEY_GOLD = '2L:gold:gold'

conn = redis.StrictRedis(**Redis['gold'])


def set(num, gold):
    conn.set(_KEY_NUM, num)
    conn.set(_KEY_GOLD, gold)


def get(func):
    """Use Redis optimistic locking."""
    gold = 0
    with conn.pipeline() as pipe:
        while 1:
            try:
                pipe.watch(_KEY_NUM, _KEY_GOLD)

                left_num = int(pipe.get(_KEY_NUM) or 0)
                left_gold = int(pipe.get(_KEY_GOLD) or 0)

                if left_num == 0 and left_gold == 0:
                    return gold

                left_num -= 1
                gold = func(left_num, left_gold)
                left_gold -= gold

                pipe.multi()
                pipe.set(_KEY_NUM, left_num)
                pipe.set(_KEY_GOLD, left_gold)
                pipe.execute()
            except redis.WatchError:
                continue
            else:
                return gold
