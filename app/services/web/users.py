# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import BaseHandler


class UserHandler(BaseHandler):

    def get(self, username):
        self.render(
            'user.html',
            title=username,
            keywords='profile, 个人信息, {0}'.format(username),
            description='{0}的个人信息, {0}\'s profile'.format(username),
        )


class UserProfileEditHandler(BaseHandler):

    def get(self):
        username = self.current_user
        self.render(
            'profile.html',
            title=username,
            keywords='profile, 个人信息, {0}'.format(username),
            description='{0}的个人信息, {0}\'s profile'.format(username),
        )


urls = [
    (r'/user/(\w+[^/])$', UserHandler),
    (r'/user/profile/edit', UserProfileEditHandler),
]
