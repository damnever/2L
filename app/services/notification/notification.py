# -*- coding: utf-8 -*-

"""Simple push service, as simple as possible...

XXX: PICKLE IS A BIG PROBLE, celery, multiprocessing...
"""

from __future__ import print_function, division, absolute_import

import json
import time
import threading
try:
    from urllib.parse import urlparse  # Py3
except ImportError:
    from urlparse import urlparse  # Py2

import redis
from tornado.websocket import WebSocketHandler, WebSocketClosedError

from app.base.handlers import BaseHandler
from app.settings import Redis


Number = (type(1), type(1L))


class PushService(object):

    _subject_notification = 'subject:notification:{0}'

    def __init__(self):
        self._conns = dict()
        self._lock = threading.Lock()
        self._redis = redis.StrictRedis(**Redis['notification'])
        self._pubsub = self._redis.pubsub()

    def add_conn(self, username, conn):
        self._pubsub.subscribe(self._subject_notification.format(username))
        with self._lock:
            self._conns[username] = conn

    def remove_conn(self, username):
        self._pubsub.unsubscribe(self._subject_notification.format(username))
        with self._lock:
            if username in self._conns:
                del self._conns[username]

    def start(self):
        self._thread = threading.Thread(
            target=self._push_msg,
            name='push_forever',
            args=(),
        )
        self._thread.daemon = True
        self._thread.start()

    def republish(self, target, msg):
        self._redis.publish(self._subject_notification.format(target), msg)

    def _push_msg(self):
        while 1:
            try:
                message = self._pubsub.get_message()
            except AttributeError:
                # no one subscribed!
                pass
            else:
                if message and not isinstance(message['data'], Number):
                    username = self._parse_username(message['channel'])
                    msg = message['data']
                    with self._lock:
                        conn = self._conns.get(username, None)

                    if conn is not None:
                        try:
                            conn.write_message(msg)
                        except WebSocketClosedError:
                            self.republish(username, msg)
                            self.remove_conn(username)

            time.sleep(0.001)

    def _parse_username(self, channel):
        try:
            return channel.rsplit(':', 1)[1]
        except IndexError:
            return None


push_service = PushService()
push_service.start()


class NotifyHandler(WebSocketHandler, BaseHandler):

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

    username = None

    def open(self):
        self.log.info('New WebSocket connect in...')

    def on_message(self, message):
        try:
            msg = json.loads(message)
        except json.JSONDecoder:
            self.log.error("WebSocket: ", exc_info=True)
            return

        if not isinstance(msg, dict):
            self.log.error('message format is not dict like.')
            return

        token = msg.get('token', '')
        token = self._decode_user_token(token)
        self.username = self.session.get(token)
        if self.username is None:
            self.log.error('"token" wrong')
            return
        push_service.add_conn(self.username, self)

    def on_close(self):
        self.log.info('WebSocket closed...')
        self.close()
        push_service.remove_conn(self.username)


# Make load_module_attrs ignore this...
no_urls = [
    (r'/', NotifyHandler),
]
