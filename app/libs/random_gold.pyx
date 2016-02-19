# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import math
import random


cdef extern from "math.h":
    double floor(double)


cpdef int random_gold(left_num, left_gold):
    if left_num == 1:
        return left_gold

    cdef int min_gold = 1
    cdef double max_gold = left_gold / left_num * 1
    gold = int(floor(random.random() * max_gold))
    return gold if gold > min_gold else min_gold
