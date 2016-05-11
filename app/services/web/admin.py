# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import BaseHandler
from app.base.decorators import need_permissions
from app.base.roles import Roles


class AdminIndexHandler(BaseHandler):

    @need_permissions(Roles.Admin)
    def get(self):
        self.render('admin/index.html',
                    keywords=None,
                    description=None,
                    title='后台管理')


class NewAnnouncementHandler(BaseHandler):

    @need_permissions(Roles.Admin)
    def get(self):
        self.render('admin/new_announcement.html',
                    keywords=None,
                    description=None,
                    title='广播')


urls = [
    (r'/admin', AdminIndexHandler),
    (r'/admin/announcement/new', NewAnnouncementHandler),
]
