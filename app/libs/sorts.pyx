# -*- coding: utf-8 -*-

# Borrow from reddit:
#  https://github.com/reddit/reddit/blob/master/r2/r2/lib/db/_sorts.pyx

from __future__ import print_function, division, absolute_import

import math
from datetime import datetime

from tzlocal import get_localzone


#----------------------------------------------------------------------
# Post ranking.
#----------------------------------------------------------------------
epoch = datetime(1970, 1, 1, tzinfo=get_localzone())


cdef double epoch_seconds(date):
    td = date - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


cdef int score(ups, downs):
    return ups - downs


cdef hot(ups, downs, date):
    s = score(ups, downs)
    order = math.log10(max(abs(s), 1))

    if s > 0:
        sign = 1
    elif s < 0:
        sign = -1
    else:
        sign = 0
    seconds = epoch_seconds(date) - 1134028003
    return round(sign * order + seconds / 45000, 7)


#----------------------------------------------------------------------
# Comment ranking.
#----------------------------------------------------------------------
cdef _confidence(ups, downs):
    n = ups + downs

    if n == 0:
        return 0

    z = 1.281551565545  # 80% confidence
    p = ups / n
    left = p + 1/(2*n)*z*z
    right = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))
    under = 1+1/n*z*z

    return (left - right) / under


up_range, down_range = 400, 100
_confidences = list()
for ups in range(up_range):
    for downs in range(down_range):
        _confidences.append(_confidence(ups, downs))


cdef confidence(ups, downs):
    if ups + downs == 0:
        return 0
    elif ups < up_range and downs < down_range:
        return _confidences[downs + ups*down_range]
    else:
        return _confidence(ups, downs)
