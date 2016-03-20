# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import os

from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from app.libs.daemonize import daemonize_app
from app.services.notification.notification import no_urls
from app.settings import Tornado, PID_FILE


class DaemonApp(object):

    def __init__(self, host, port):
        web_app = Application(no_urls, Tornado)
        http_server = HTTPServer(web_app, xheaders=True)
        http_server.listen(port, address=host)
        ioloop = IOLoop.instance()

        self._ioloop = ioloop

    def start(self):
        self._ioloop.start()

    def stop(self):
        self._ioloop.stop()


host = os.getenv('NO_SERVICE_HOST')
port = int(os.getenv('NO_SERVICE_PORT'))

pid = os.fork()
if pid == 0:
    daemonize_app(DaemonApp(host, port), PID_FILE)
