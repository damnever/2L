#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

#  import signal
import atexit

from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.log import enable_pretty_logging

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
        super(App, self).__init__(urls, **settings)


#  def signal_handler(signum, frame):
    #  shutdown_session()
    #  print(' Stoping...')
    #  IOLoop.instance().stop()

def exit_func():
    shutdown_session()
    print(' Stoping...')
    IOLoop.instance().stop()


def run_server(host='127.0.0.1', port=8888):
    enable_pretty_logging()
    #  for sig in (signal.SIGINT, signal.SIGTERM):
    #      signal.signal(sig, signal_handler)
    atexit.register(exit_func)

    http_server = HTTPServer(App(), xheaders=True)
    http_server.listen(port, address=host)

    ioloop = IOLoop.instance()
    # For debuging.
    ioloop.set_blocking_log_threshold(0.5)
    ioloop.start()
