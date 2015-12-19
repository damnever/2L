# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import httplib
import functools

from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_encode


class BaseHandler(RequestHandler):

    def get_current_user(self):
        return None

    def write_error(self, status_code, **kwargs):
        message = ''
        if status_code:
            reason = httplib.responses.get(status_code, 'Unkonwn Error')
            message = '{0} {1}.'.format(status_code, reason)
        else:
            message = '500 Internal Server Error.'
        self.render('error.html', message)


def as_json(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        try:
            result = method(self, *args, **kwargs)
        except HTTPError as e:
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


class APIHandler(BaseHandler):
    """get, post, patch, put, head, delete, options methods
    must has return value, and do not use write, render, etc.
    """

    def set_default_headers(self):
        super(APIHandler, self).set_default_headers()
        self.set_header('Content-Type', 'application/json')

    @as_json
    def get(self, *args, **kwargs):
        raise HTTPError(405)

    @as_json
    def post(self, *args, **kwargs):
        raise HTTPError(405)

    @as_json
    def put(self, *args, **kwargs):
        raise HTTPError(405)

    @as_json
    def patch(self, *args, **kwargs):
        raise HTTPError(405)

    @as_json
    def delete(self, *args, **kwargs):
        raise HTTPError(405)

    @as_json
    def head(self, *args, **kwargs):
        raise HTTPError(405)

    @as_json
    def options(self, *args, **kwargs):
        raise HTTPError(405)


class DefaultHandler(BaseHandler):

    def get(self):
        self.render('error.html', 'Nothing For You.')
