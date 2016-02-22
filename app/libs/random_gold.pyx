# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import random


cpdef int random_gold(left_num, left_gold):
    if left_num <= 0:
        return 0
    if left_num == 1:
        return left_gold

    min_gold = 1
    max_gold = left_gold / left_num * 2
    gold = int(random.random() * max_gold)

    if gold > min_gold:
        return gold
    return min_gold
