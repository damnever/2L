# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import


class ValidationError(Exception):

    __slots__ = ('status_code', 'reason')

    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason
