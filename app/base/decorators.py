# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import functools

from tornado import gen
from tornado.escape import json_encode
from tornado.web import HTTPError

from app.base.exceptions import ValidationError
from app.models import User
from app.base.roles import Roles


def as_json(method):
    @functools.wraps(method)
    @gen.coroutine
    def wrapper(self, *args, **kwargs):
        try:
            result = yield gen.maybe_future(method(self, *args, **kwargs))
        except (HTTPError, ValidationError) as e:
            self.log.error('Error: %s', e)
            self.write(json_encode({
                'status': 0,
                'code': e.status_code,
                'reason': e.reason,
            }))
        except Exception:
            self.log.error('Unexpected error', exc_info=True)
            self.write({
                'status': 0,
                'code': 500,
                'reason': 'Unknown server error.',
            })
        else:
            if result is None:
                result = dict()
            result.update({'status': 1})
            self.write(json_encode(result))
        self.flush()
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
        def wrapper(self, id_):
            username = self.current_user
            if not username:
                raise HTTPError(403)

            user = yield gen.maybe_future(User.get_by_name(username))
            for permission in permissions:
                if id_ and permission == Roles.TopicEdit:
                    permission = permission.format(id_)
                if not user.has_permission(permission):
                    raise HTTPError(403)
            raise gen.Return(method(self, id_))

        return wrapper
    return decorator
