# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import APIHandler
from app.base.decorators import as_json


class LatestPostsAPIHandler(APIHandler):

    @as_json
    def get(self, post_id):
        return []


class TopicPostsAPIHandler(APIHandler):

    @as_json
    def get(self, topic_id):
        return []


class UserPostsAPIHandler(APIHandler):

    @as_json
    def get(self, username):
        return []


class PostAPIHandler(APIHandler):

    @as_json
    def get(self, post_id):
        return None

    @as_json
    def patch(self, post_id):
        return None

    @as_json
    def delete(self, post_id):
        return None


urls = [
    # `GET /api/posts/latest`, get all latest posts.
    (r'/api/posts/latest', LatestPostsAPIHandler),
    # `GET /api/posts/topic/:topic_id`, get all posts of the topic.
    (r'/api/posts/topic/(\d+)', TopicPostsAPIHandler),
    # `GET /api/posts/topic/:username, get all posts of the user.
    (r'/api/posts/user/(\w+)', UserPostsAPIHandler),
    # `GET /api/posts/post/:post_id`, get information of the post.
    # For the post owner:
    #  `PATCH /api/posts/post/:post_id`, update information of the post.
    #  `DELETE /api/posts/post/:post_id`, delete the post.
    (r'/api/posts/post/(\d+)', PostAPIHandler),
]
