# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

try:
    from urllib import urlencode  # Py2
except ImportError:
    from urllib.parse import urlencode  # Py3

from tornado.testing import AsyncHTTPTestCase

from app.app import App
from app.settings import Tornado


class BaseTestCase(AsyncHTTPTestCase):

    _headers = {
        'Accept': 'application/json',
        'X-Xsrftoken': Tornado['cookie_secret']
    }

    def get_app(self):
        return App()

    def get(self, path):
        return self.fetch(path, method='GET', headers=self._headers)

    def post(self, path, body=None):
        body = urlencode(body) if body else None
        return self.fetch(path, method='POST', body=body, headers=self._headers)

    def delete(self, path):
        return self.fetch(path, method='DELETE', headers=self._headers)

    def put(self, path, body=None, callback=None):
        body = urlencode(body) if body else None
        return self.fetch(path, method='PUT', body=body, headers=self._headers)

    def patch(self, path, body=None):
        body = urlencode(body) if body else None
        return self.fetch(path, method='PATCH', body=body, headers=self._headers)
