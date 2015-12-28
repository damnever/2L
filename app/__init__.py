# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import sys


# Speed up...
if sys.version_info[0] < 3:
    import __builtin__
    __builtin__.range = __builtin__.xrange
