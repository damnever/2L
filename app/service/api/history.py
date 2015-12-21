# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import APIHandler
from app.base.decorators import as_json


class TopicEditHistoryAPIHandler(APIHandler):

    @as_json
    def get(self, topic_id):
        return []


class PostEditHistoryAPIHandler(APIHandler):

    @as_json
    def get(self, post_id):
        return []


urls = [
    # `GET /api/history/topic/:topic_id`, get all edit history of the topic.
    (r'/api/history/topic/(\d+)', TopicEditHistoryAPIHandler),
    # `GET /api/history/post/:post_id`, get all edit history of the post.
    (r'/api/history/post/(\d+)', PostEditHistoryAPIHandler),
]
