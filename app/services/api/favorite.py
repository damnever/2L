# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import APIHandler
from app.base.decorators import as_json


class FavoritePostsAPIHandler(APIHandler):

    @as_json
    def get(self):
        return []


class FavoritePostAPIHandler(APIHandler):

    @as_json
    def post(self, post_id):
        pass


class UnfavoritePostAPIHandler(APIHandler):

    @as_json
    def delete(self, post_id):
        pass


urls = [
    # For authenticated user:

    # `GET /api/favorite/posts`, get all favorite posts.
    (r'/api/favorite/posts', FavoritePostsAPIHandler),
    # `POST /api/favorite/post/:post_id`, favorite a new post.
    (r'/api/favorite/post/(\d+)', FavoritePostAPIHandler),
    # `DELETE /api/unfavorite/post/:post_id`, unfavorite a post.
    (r'/api/unfavorite/post/(\d+)', UnfavoritePostAPIHandler),

]
