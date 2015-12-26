# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import sys
import traceback
import functools

from tornado import gen
from tornado.escape import json_encode
from tornado.web import HTTPError

from app.base.exceptions import ValidationError


def as_json(method):
    @functools.wraps(method)
    @gen.coroutine
    def wrapper(self, *args, **kwargs):
        try:
            result = yield gen.maybe_future(method(self, *args, **kwargs))
        except (HTTPError, ValidationError) as e:
            self.write(json_encode({
                'status': 0,
                'code': e.status_code,
                'reason': e.reason,
            }))
        except Exception:
            self.log.error('Unexpected error', exc_info=True)
            tb_text = ''.join(traceback.format_exception(*sys.exc_info()))
            self.write({
                'status': 0,
                'code': 500,
                'reason': 'Unknown server error.\n' + tb_text,
            })
        else:
            result.update({'status': 1})
            self.write(json_encode(result))
        self.flush()
    return wrapper


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        pass
    return wrapper


def need_permissions(*permissions):
    def decorator(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            pass
        return wrapper
    return decorator
