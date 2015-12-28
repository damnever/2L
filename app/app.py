#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import signal

from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options

from app.base.handlers import DefaultHandler
from app.services import urls
from app.libs.db import init_db, drop_db, shutdown_session
from app.settings import Tornado


define('port', default=8888, help='run on the given port', type=int)
define('init', default=False, help='initialize database', type=bool)
define('clear', default=False, help='drop database if exists', type=bool)


class App(Application):

    def __init__(self):
        settings = {
            'default_handler_class': DefaultHandler,
        }
        settings.update(**Tornado)
        super(Application, self).__init__(urls, **settings)


def signal_handler(signum, frame):
    shutdown_session()


def run_server():
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, signal_handler)
    http_server = HTTPServer(App(), xheaders=True)
    http_server.listen(options.port)
    IOLoop.instance().start()


def run():
    options.parse_command_line()
    if options.init:
        init_db()
    elif options.clear:
        drop_db()
    else:
        run_server()


if __name__ == '__main__':
    run()
