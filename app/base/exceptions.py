# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

try:  # Py2
    from httplib import responses
except ImportError:  # Py3
    from http.client import responses

import tornado.web


class ValidationError(Exception):

    __slots__ = ('status_code', 'reason')

    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason

    def __str__(self):
        return '{0} {1}'.format(self.status_code, self.reason)

    __repr__ = __str__


class HTTPError(tornado.web.HTTPError):

    def __init__(self, code, **kwargs):
        super(HTTPError, self).__init__(code, **kwargs)
        if self.reason is None:
            self.reason = responses.get(code, 'Unkonwn')
