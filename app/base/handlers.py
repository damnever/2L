# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

try:
    from http.client import responses  # Py3
except ImportError:
    from httplib import responses

from tornado.web import RequestHandler, HTTPError
from tornado.log import app_log

from app.base.decorators import as_json
from app.libs.db.database import db_session
from app.cache import session


class BaseHandler(RequestHandler):

    @property
    def log(self):
        return self.settings.get('log', app_log)

    @property
    def db_session(self):
        return db_session

    @property
    def session(self):
        return session

    def get_current_user(self):
        username = self.get_secure_cookie('username')
        if username and self.session.get(username) is not None:
            return username
        return None

    def write_error(self, status_code, **kwargs):
        message = ''
        if status_code:
            reason = responses.get(status_code, 'Unkonwn Error')
            message = '{0} {1}.'.format(status_code, reason)
        else:
            message = '500 Internal Server Error.'
        self.render('error.html', message)


class APIHandler(BaseHandler):
    """get, post, patch, put, head, delete, options methods
    must has return value(gen.Return in Py2, return, whatever),
    and do not use write, render, etc.
    """

    def prepare(self):
        pass

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

    @as_json
    def write_error(self, status_code, **kwargs):
        if status_code:
            raise HTTPError(status_code)
        else:
            raise HTTPError(500)


class DefaultHandler(BaseHandler):

    def get(self):
        self.render('error.html', 'Nothing For You.')
