# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json, authenticated
from app.models import Favorite
from app.services.api import exceptions


class FavoritePostsAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def get(self):
        username = self.current_user
        fs = yield gen.maybe_future(Favorite.list_by_user(username))
        result = {
            'total': len(fs),
            'posts': [f.to_dict() for f in fs],
        }
        raise gen.Return(result)


class FavoritePostAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def post(self, post_id):
        username = self.current_user
        f = yield gen.maybe_future(Favorite.get_by_user_post(username, post_id))
        if f:
            raise exceptions.PostAlreadyFavorited()
        else:
            yield gen.maybe_future(Favorite.create(username, post_id))


class UnfavoritePostAPIHandler(APIHandler):

    @as_json
    def delete(self, post_id):
        username = self.current_user
        f = yield gen.maybe_future(Favorite.get_by_user_post(username, post_id))
        if f:
            yield gen.maybe_future(f.delete())
        else:
            raise exceptions.PostHasNotBeenFavorited()


urls = [
    # For authenticated user:

    #  `GET /api/favorite/posts`, get all favorite posts.
    (r'/api/favorite/posts', FavoritePostsAPIHandler),
    #  `POST /api/favorite/post/:post_id`, favorite a new post.
    (r'/api/favorite/post/(\d+)', FavoritePostAPIHandler),
    #  `DELETE /api/unfavorite/post/:post_id`, unfavorite a post.
    (r'/api/unfavorite/post/(\d+)', UnfavoritePostAPIHandler),
]
