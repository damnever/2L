# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import BaseHandler
from app.base.decorators import authenticated
from app.base.exceptions import HTTPError


class UserHandler(BaseHandler):

    @authenticated
    def get(self, username):
        self.render(
            'user.html',
            title=username,
            keywords='profile, 个人信息, {0}'.format(username),
            description='{0}的个人信息, {0}\'s profile'.format(username),
        )


class ProfileEditHandler(BaseHandler):

    @authenticated
    def get(self, username):
        if self.current_user != username:
            raise HTTPError(403)
        self.render('edit_profile.html',
                    title=username,
                    keywords='profile, 个人信息, {0}'.format(username),
                    description='{0}的个人信息, {0}\'s profile'.format(username),
                    )


urls = [
    (r'/user/(\w+[^/])$', UserHandler),
    (r'/edit/profile/(\w+[^/])$', ProfileEditHandler),
]
