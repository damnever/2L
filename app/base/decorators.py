# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import functools

from tornado.escape import json_encode
from tornado.web import HTTPError

from app.service.api.exceptions import ValidationError


def as_json(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            result = method(self, *args, **kwargs)
        except (HTTPError, ValidationError) as e:
            self.write(json_encode({
                'status': 0,
                'code': e.status_code,
                'reason': e.reason,
            }))
        else:
            result.update({'status': 1})
            self.write(json_encode(result))
        self.flush()
        return None
    return wrapper


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        pass
    return wrapper
