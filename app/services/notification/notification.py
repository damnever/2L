# -*- coding: utf-8 -*-

"""Simple push service use WebSocket and Redis Pub-Sub, no BB!"""

from __future__ import print_function, division, absolute_import

import os
import multiprocessing

try:
    from urllib.parse import urlparse  # Py3
except ImportError:
    from urlparse import urlparse  # Py2

from tornado.websocket import WebSocketHandler

from app.base.handlers import BaseHandler


class PushService(object):

    def __init__(self):
        self._manager = multiprocessing.Manager()
        self._connections = self._manager.dict()
        self._lock = multiprocessing.Lock()

    def add_connection(self, username, connection):
        with self._lock:
            self._connections[username] = connection

    def remove_connection(self, username):
        with self._lock:
            if username in self._connections:
                del self._connections[username]

    def start(self):
        try:
            pid = os.fork()
            if pid == 0:
                self.push_msg()
        except OSError as e:
            print('[PUSH SERVICE]: \x1b[33;01m{0}\x1b[39;49;00m'.format(e))

    def push_msg(self):
        pass


class NotifyHandler(BaseHandler, WebSocketHandler):

    # Borrow from:
    #  https://github.com/jupyter/notebook/blob/master/notebook/base/zmqhandlers.py
    def check_origin(self, origin=None):
        """Check Origin == Host or Access-Control-Allow-Origin.

        Tornado >= 4 calls this method automatically,
        raising 403 if it returns False.
        """
        if self.allow_origin == '*':
            return True

        host = self.request.headers.get("Host")
        if origin is None:
            origin = self.get_origin()

        # If no header is provided, assume we can't verify origin
        if origin is None:
            self.log.warning(("Missing Origin header, "
                              "rejecting WebSocket connection."))
            return False
        if host is None:
            self.log.warning(("Missing Host header, "
                              "rejecting WebSocket connection."))
            return False

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
            self.log.warning(("Blocking Cross Origin WebSocket Attempt. "
                              "Origin: %s, Host: %s"), origin, host)
        return allow

    def open(self):
        self.log.info('New WebSocket connect in...')

    def on_close(self):
        self.log.info('WebSocket closed...')
