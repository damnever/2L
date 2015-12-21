# -*- coding: utf-8 -*-

#TODO: sth.?? I have no idea... limit API access rate, OAuth???

from __future__ import print_function, division, absolute_import

from app.base.handlers import APIHandler
from app.base.decorators import as_json


class LoginHandler(APIHandler):

    @as_json
    def post(self):
        pass


class RegisterHandler(APIHandler):

    @as_json
    def post(self):
        pass


urls = [
    (r'/api/login', LoginHandler),
    (r'/api/register', RegisterHandler),
]
