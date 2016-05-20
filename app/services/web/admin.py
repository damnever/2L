# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import BaseHandler
from app.base.decorators import need_permissions
from app.base.roles import Roles


class AdminIndexHandler(BaseHandler):

    @need_permissions(Roles.Admin)
    def get(self):
        self.redirect('/admin/announcement')


class NewAnnouncementHandler(BaseHandler):

    @need_permissions(Roles.Admin)
    def get(self):
        self.render('admin/new_announcement.html',
                    keywords=None,
                    description=None,
                    title='后台管理·广播')


class UsersHandler(BaseHandler):

    @need_permissions(Roles.Admin)
    def get(self):
        self.render('admin/users.html',
                    keywords=None,
                    description=None,
                    title='后台管理·用户')


class TopicsHandler(BaseHandler):

    @need_permissions(Roles.Admin)
    def get(self):
        self.render('admin/topics.html',
                    keywords=None,
                    description=None,
                    title='后台管理·用户')


class PostsHandler(BaseHandler):

    @need_permissions(Roles.Admin)
    def get(self):
        self.render('admin/posts.html',
                    keywords=None,
                    description=None,
                    title='后台管理·帖子')


class CommentsHandler(BaseHandler):

    @need_permissions(Roles.Admin)
    def get(self):
        self.render('admin/comments.html',
                    keywords=None,
                    description=None,
                    title='后台管理·评论')


urls = [
    (r'/admin', AdminIndexHandler),
    (r'/admin/announcement', NewAnnouncementHandler),
    (r'/admin/users', UsersHandler),
    (r'/admin/topics', TopicsHandler),
    (r'/admin/posts', PostsHandler),
    (r'/admin/comments', CommentsHandler),
]
