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
        users = yield gen.maybe_future(User.count())
        topics = yield gen.maybe_future(Topic.count())
        posts = yield gen.maybe_future(Post.count())
        comments = yield gen.maybe_future(Comment.count())
        raise gen.Return({
            'users_count': users,
            'topics_count': topics,
            'posts_count': posts,
            'comments_count': comments,
        })


urls = [
    (r'/api/status/count', CountStatusAPIHandler),
]
