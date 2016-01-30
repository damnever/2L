# -*- coding: utf-8 -*-

# TODO: sth.?? I have no idea... limit API access rate, OAuth???

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json
from app.services.api import exceptions
from app.models import User
from app.libs.utils import encrypt_password, gen_token


class LoginHandler(APIHandler):

    @as_json
    @gen.coroutine
    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        expire = int(self.get_argument('expire', 1))

        if username is None or password is None:
            raise exceptions.EmptyFields()
        else:
            user = yield self.async_task(User.get_by_name, username)
            if user is None:
                raise exceptions.UsernameDoesNotExists()
            if encrypt_password(password) != user.password:
                raise exceptions.PasswordWrong()
            token = gen_token()
            self.set_secure_cookie('token', token, expire)
            self.session.set(token, username, expire)
            raise gen.Return({'username': username})


class LogoutHandler(APIHandler):

    @as_json
    @gen.coroutine
    def post(self):
        username = self.current_user
        token = self.get_cookie('token')

        if username == self.session.get(token):
            self.clear_cookie('token')
            self.session.delete(token)


class RegisterHandler(APIHandler):

    @as_json
    @gen.coroutine
    def post(self):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        email = self.get_argument('email', None)

        if username is None or password is None or email is None:
            raise exceptions.EmptyFields()
        else:
            user = yield self.async_task(User.get_by_name, username)
            if user is not None:
                raise exceptions.UsernameAlreadyExists()
            user = yield self.async_task(User.get_by_email, email)
            if user is not None:
                raise exceptions.EmailAlreadyExists()
            password = encrypt_password(password)
            self.async_task(User.create, username=username,
                            password=password, email=email)


urls = [
    (r'/api/login', LoginHandler),
    (r'/api/logout', LogoutHandler),
    (r'/api/register', RegisterHandler),
]
