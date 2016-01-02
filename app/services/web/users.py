# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import BaseHandler


class LoginHandler(BaseHandler):

    def get(self):
        self.render('login.html')


class RegisterHandler(BaseHandler):

    def get(self):
        self.render('register.html')


class UserHandler(BaseHandler):

    def get(self, username):
        self.render('profile.html', username=username)


urls = [
    (r'/login', LoginHandler),
    (r'/register', RegisterHandler),
    (r'/user/(w+)', UserHandler),
]
