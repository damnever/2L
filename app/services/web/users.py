# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import BaseHandler
from app.base.decorators import authenticated


class UserHandler(BaseHandler):

    @authenticated
    def get(self, username):
        self.render(
            'user.html',
            title=username,
            keywords='profile, 个人信息, {0}'.format(username),
            description='{0}的个人信息, {0}\'s profile'.format(username),
        )


urls = [
    (r'/user/(\w+[^/])$', UserHandler),
]
