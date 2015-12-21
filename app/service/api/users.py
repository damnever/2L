# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import APIHandler
from app.base.decorators import authenticated, as_json


class UsersAPIHandler(APIHandler):

    @as_json
    def get(self, username):
        return None


class AuthedUserAPIHandler(APIHandler):

    @authenticated
    @as_json
    def get(self):
        return None

    @authenticated
    @as_json
    def patch(self):
        return None


class AuthedFollowingAPIHandler(APIHandler):

    @authenticated
    @as_json
    def get(self, username):
        return None

    @authenticated
    @as_json
    def post(self):
        return None

    @authenticated
    @as_json
    def delete(self):
        return None


class AuthedBlockedAPIHandler(APIHandler):

    @authenticated
    @as_json
    def get(self):
        return None

    @authenticated
    @as_json
    def post(self):
        return None

    @authenticated
    @as_json
    def delete(self):
        return None


urls = [
    # `GET /api/users/:username`, get information of username.
    (r'/api/users/(\w+)', UsersAPIHandler),
    # For the current user:
    #  `GET /api/user`, get user information.
    #  `PATCH /api/user`, update user information.
    (r'/api/user', AuthedUserAPIHandler),
    # For the current user:
    #  `GET /api/user/following`, get all following users.
    #  `POST /api/user/following`, follow a new user.
    #  `DELETE /api/user/following`, unfollow a user.
    (r'/api/user/following', AuthedFollowingAPIHandler),
    # For the current user:
    #  `GET /api/user/blocked`, get all bloacked users.
    #  `POST /api/user/blocked`, blocked a new user.
    #  `DELETE /api/user/blocked`, unblock a user.
    (r'/api/user/blocked', AuthedBlockedAPIHandler),
]
