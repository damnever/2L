# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json, authenticated
from app.models import Notification


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
    (r'/api/notifications/comments', CommentNotificationsAPIHandler),
]
