# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

try:
    from urllib.parse import urlparse  # Py3
except ImportError:
    from urlparse import urlparse  # Py2

from tornado.websocket import WebSocketHandler

from app.base.handlers import BaseHandler


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
