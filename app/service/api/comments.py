# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import APIHandler
from app.base.decorators import as_json


class PostCommentsAPIHandler(APIHandler):

    @as_json
    def get(self, post_id):
        return []

    @as_json
    def post(self, post_id):
        return None


class UserCommentsAPIHandler(APIHandler):

    @as_json
    def get(self, username):
        return []


urls = [
    # NOTE: comment can not be deleted...
    # `GET /api/comments/post/:post_id`, get all comments of the post.
    # For authenticated user:
    #   `POST /api/comments/post/:post_id`, add a new comments to post.
    (r'/api/comments/post/(\d+)', PostCommentsAPIHandler),
    # `GET /api/comments/user/:username`, get all comments of the user.
    (r'/api/comments/user/(\w+)', UserCommentsAPIHandler),
]
