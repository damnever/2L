# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json
from app.models import User, Topic, Post, Comment


class CountStatusAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self):
        users = yield self.async_task(User.count)
        topics = yield self.async_task(Topic.count)
        posts = yield self.async_task(Post.count)
        comments = yield self.async_task(Comment.count)
        raise gen.Return({
            'users_count': users,
            'topics_count': topics,
            'posts_count': posts,
            'comments_count': comments,
        })


urls = [
    (r'/api/status/count', CountStatusAPIHandler),
]
