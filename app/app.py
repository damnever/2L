#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import signal

from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from app.base.handlers import DefaultHandler
from app.services import urls
from app.libs.db import shutdown_session
from app.settings import Tornado


class App(Application):

    def __init__(self):
        settings = {
            'default_handler_class': DefaultHandler,
        }
        settings.update(Tornado)
        super(Application, self).__init__(urls, **settings)


def signal_handler(signum, frame):
    shutdown_session()


def run_server(host='localhost', port=8888):
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, signal_handler)
    http_server = HTTPServer(App(), xheaders=True)
    http_server.listen(port, address=host)
    IOLoop.instance().start()
