# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json, authenticated, need_permissions
from app.models import Announcement, Notification
from app.base.roles import Roles
from app.services.api import exceptions


class AnnouncementAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self):
        count = int(self.get_argument('count', 4))

        ans = yield gen.maybe_future(Announcement.list_by_count(count))
        raise gen.Return({
            'total': len(ans),
            'announcements': [(yield gen.maybe_future(an.to_dict()))
                              for an in ans]
        })

    @as_json
    @need_permissions(Roles.Admin)
    @gen.coroutine
    def post(self):
        content = self.get_argument('content', None)
        username = self.current_user

        if content is None:
            raise exceptions.EmptyFields()
        yield gen.maybe_future(Announcement.create(username, content))


class CommentNotificationsAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def get(self):
        type_ = self.get_argument('type', None)
        unread = bool(self.get_argument('unread', True))
        username = self.current_user

        ntfs = yield gen.maybe_future(
            Notification.list_by_user_and_type(username, type_, unread))
        result = {
            'total': len(ntfs),
            'messages': [n.to_dict() for n in ntfs],
        }
        raise gen.Return(result)


urls = [
    (r'/api/notifications/announcement', AnnouncementAPIHandler),
    (r'/api/notifications/comments', CommentNotificationsAPIHandler),
]
