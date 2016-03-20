#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

#  import signal
import os
import atexit

from tornado.web import Application
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.log import enable_pretty_logging

from app.libs.db import shutdown_session, ping_db
from app.settings import Tornado, PID_FILE
from app.cache import session, gold


class App(Application):

    def __init__(self):
        from app.services import urls
        from app.base.handlers import DefaultHandler
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
    print(' Stoping...')
    IOLoop.current().stop()
    shutdown_session()
    session.delete_all()
    gold.delete_all()
    with open(PID_FILE, 'rb') as f:
        os.kill(9, int(f.read()))


def run_server(host='127.0.0.1', port=9487):
    enable_pretty_logging()
    #  for sig in (signal.SIGINT, signal.SIGTERM):
    #      signal.signal(sig, signal_handler)
    os.environ['NO_SERVICE_HOST'] = host
    os.environ['NO_SERVICE_PORT'] = str(port + 1)
    atexit.register(exit_func)

    # Do not make MySQL goaway.
    PeriodicCallback(ping_db, 3600 * 1000).start()

    http_server = HTTPServer(App(), xheaders=True)
    http_server.listen(port, address=host)

    ioloop = IOLoop.instance()
    # For debuging.
    ioloop.set_blocking_log_threshold(0.5)
    ioloop.start()
