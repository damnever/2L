# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

try:  # Py2
    from httplib import responses
    from urlparse import urlparse
except ImportError:  # Py3
    from http.client import responses
    from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor

from tornado.concurrent import run_on_executor
from tornado.web import RequestHandler, decode_signed_value
from tornado.log import app_log

from app.base.exceptions import HTTPError
from app.base.decorators import as_json
from app.cache import session
from app.settings import ThreadPoolMaxWorkers, DefaultAvatar
from app.libs.db import db_session
from app.libs.statsd import statsd_client


class AsyncTaskMixIn(object):
    """Making a synchronous method asynchronously on a executor.

    The ``IOLoop`` and executor to be used are determined by the
    ``io_loop`` and ``executor`` attributes of ``self``.

    TODO: MAKE IT WORK WITH SCOPED SQLALCHEMY SESSION!!!
    MAYBE USE THREAD IDENTIFY.
    """
    executor = ThreadPoolExecutor(max_workers=ThreadPoolMaxWorkers)

    @run_on_executor
    def async_task(self, callback, *args, **kwargs):
        return callback(*args, **kwargs)


class BaseHandler(AsyncTaskMixIn, RequestHandler):

    @property
    def statsd_client(self):
        return statsd_client

    @property
    def log(self):
        return self.settings.get('log', app_log)

    @property
    def session(self):
        return session

    @property
    def default_avatar(self):
        return DefaultAvatar

    def prepare(self):
        pass

    def on_finish(self):
        db_session.remove()

    # Reference:
    #  - https://github.com/jupyter/notebook/blob/master/notebook/base/handlers.py
    @property
    def allow_origin(self):
        """Normal Access-Control-Allow-Origin"""
        return self.settings.get('allow_origin', '')

    @property
    def allow_origin_pat(self):
        """Regular expression version of allow_origin"""
        return self.settings.get('allow_origin_pat', None)

    # origin_to_satisfy_tornado is present because tornado requires
    # check_origin to take an origin argument, but we don't use it
    def check_origin(self, origin_to_satisfy_tornado=""):
        """Check Origin for cross-site API requests, including websockets

        Copied from WebSocket with changes:

        - allow unspecified host/origin (e.g. scripts)
        """
        if self.allow_origin == '*':
            return True

        host = self.request.headers.get('Host')
        origin = self.request.headers.get('Origin')

        # If no header is is provided, assume it comes from a
        # script, curl, httpie, etc.
        # We are only concerned with cross-site browser stuff here.
        if origin is None or host is None:
            return True

        origin = origin.lower()
        origin_host = urlparse(origin).netloc

        # OK if origin matches host
        if origin_host == host:
            return True

        # Check CORS headers
        if self.allow_origin:
            allow = self.allow_origin == origin
        elif self.allow_origin_pat:
            allow = bool(self.allow_origin_pat.match(origin))
        else:
            # No CORS headers deny the request
            allow = False
            if not allow:
                self.log.warn("Blocking Cross Origin API request."
                              "  Origin: %s, Host: %s", origin, host,)
            return allow

    def _decode_user_token(self, value, max_age_days=31, min_version=None):
        return decode_signed_value(self.application.settings['cookie_secret'],
                                   'token', value, max_age_days=max_age_days,
                                   min_version=min_version)

    def get_current_user(self):
        token = self.get_secure_cookie('token')
        if token is None:
            value = self.get_argument('token', None)
            if value is None:
                return None
            token = self._decode_user_token(value)

        if token:
            username = self.session.get(token)
            return username
        return None

    def write_error(self, status_code, **kwargs):
        message = ''
        if status_code:
            reason = responses.get(status_code, 'Unkonwn Error')
            message = '{0} {1}.'.format(status_code, reason)
        else:
            message = '500 Internal Server Error.'
        self.render('error.html', message=message)


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
        self.render('error.html', message='Nothing For You.')
