# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import functools
import json
import time
from datetime import datetime

from tornado import gen

from app.base.exceptions import HTTPError
from app.base.exceptions import ValidationError
from app.models import User
from app.base.roles import Roles


class _DatetimeEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return json.JSONEncoder.default(self, obj)


def json_encode(value):
    # http://stackoverflow.com/questions/1580647/json-why-are-forward-slashes-escaped
    return json.dumps(value, cls=_DatetimeEncoder).replace("</", "<\\/")


def as_json(method):
    @functools.wraps(method)
    @gen.coroutine
    def wrapper(self, *args, **kwargs):
        start = time.time()
        api_name = "{0}.{1}".format(self.__class__.__name__, method.__name__)
        timed = "{0}.timed".format(api_name)
        success = "{0}.success".format(api_name)
        permission_err = "{0}.permission_error".format(api_name)
        http_err = "{0}.http_error".format(api_name)
        internal_err = "{0}.internal_error".format(api_name)

        try:
            result = yield gen.maybe_future(method(self, *args, **kwargs))
            # Wait future complete.
            if isinstance(result, gen.Future):
                result = yield result
                # result = result.result()
        except (HTTPError, ValidationError) as e:
            self.log.error('Error: %s', e)
            self.finish(json_encode({
                'status': 0,
                'code': e.status_code,
                'reason': e.reason,
            }))
            if e.status_code == 403:
                self.statsd_client.incr(permission_err, 1)
            else:
                self.statsd_client.incr(http_err, 1)
        except Exception:
            self.log.error('Unexpected error', exc_info=True)
            self.finish({
                'status': 0,
                'code': 500,
                'reason': 'Unknown server error.',
            })
            self.statsd_client.incr(internal_err, 1)
        else:
            result = result or dict()
            result.update({'status': 1})
            self.finish(json_encode(result))
            self.statsd_client.incr(success, 1)
        finally:
            self.statsd_client.timing_since(timed, start)
    return wrapper


def authenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper


def need_permissions(*permissions):
    def decorator(method):

        @functools.wraps(method)
        @gen.coroutine
        def wrapper(self, *args, **kwargs):
            username = self.current_user
            if not username:
                raise HTTPError(403)

            user = yield gen.maybe_future(User.get_by_name(username))
            for permission in permissions:
                if (args and args[0] and
                        permission in (Roles.TopicEdit, Roles.PostEdit)):
                    permission = permission.format(args[0])

                has_permission = yield gen.maybe_future(
                    user.has_permission(permission))
                if not has_permission:
                    raise HTTPError(403)

            raise gen.Return(method(self, *args, **kwargs))

        return wrapper
    return decorator
