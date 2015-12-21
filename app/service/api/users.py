# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import APIHandler
from app.base.decorators import as_json


class UsersAPIHandler(APIHandler):

    @as_json
    def get(self, username):
        return None


class UserAPIHandler(APIHandler):

    @as_json
    def get(self):
        return None

    @as_json
    def patch(self):
        return None


class FollowingAPIHandler(APIHandler):

    @as_json
    def get(self):
        return None


class FollowOneAPIHandler(APIHandler):

    @as_json
    def post(self, username):
        return None


class UnfollowOneAPIHandler(APIHandler):

    @as_json
    def delete(self, username):
        return None


class BlockedAPIHandler(APIHandler):

    @as_json
    def get(self):
        return None


class BlockOneAPIHandler(APIHandler):

    @as_json
    def post(self):
        return None


class UnblockOneAPIHandler(APIHandler):

    @as_json
    def delete(self):
        return None


urls = [
    # `GET /api/users/:username`, get information of username.
    (r'/api/users/(\w+)', UsersAPIHandler),

    # For the current user:

    #  `GET /api/user`, get user information.
    #  `PATCH /api/user`, update user information.
    (r'/api/user', UserAPIHandler),
    #  `GET /api/user/following`, get all following users.
    (r'/api/user/following', FollowingAPIHandler),
    #  `POST /api/user/follow/:username`, follow a new user.
    (r'/api/user/follow/(\w+)', FollowOneAPIHandler),
    #  `DELETE /api/user/unfollow/:username`, unfollow a user.
    (r'/api/user/unfollow/(\w+)', UnfollowOneAPIHandler),
    #  `GET /api/user/blocked`, get all bloacked users.
    (r'/api/user/blocked', BlockedAPIHandler),
    #  `POST /api/user/block/:username`, blocked a new user.
    (r'/api/user/block/(\w+)', BlockOneAPIHandler),
    #  `DELETE /api/user/unblock/:username`, unblock a user.
    (r'/api/user/unblock/(\w+)',UnblockOneAPIHandler),
]
