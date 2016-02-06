# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json
from app.services.api import exceptions
from app.models import User, Following, Blocked
from app.base.decorators import authenticated


class UsersAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, username):
        user = yield self.async_task(User.get_by_name, username)
        if user is None:
            raise exceptions.UsernameDoesNotExists()
        else:
            raise gen.Return(user.information())


class UserAPIHandler(APIHandler):

    _fields = ("password role gold intorduce avatar location "
               "wiki blog github google weibo twitter")

    @as_json
    @authenticated
    @gen.coroutine
    def get(self):
        username = self.current_user
        user = yield self.async_task(User.get_by_name, username)
        raise gen.Return(user.information())

    @as_json
    @authenticated
    @gen.coroutine
    def patch(self):
        fields = dict()
        for key in self._fields.split():
            value = self.get_argument(key, None)
            if value is not None:
                fields[key] = value

        if not fields:
            raise exceptions.EmptyFields()
        else:
            username = self.current_user
            user = yield self.async_task(User.get_by_name, username)
            yield self.async_task(user.update, fields)
            info = user.information()
            following = yield self.async_task(Following.count_by_user, username)
            blocked = yield self.async_task(Blocked.count_by_user, username)
            info.update({
                'following': following,
                'blocked': blocked,
                'following_url': '/api/user/following',
                'blocked_url': '/api/user/blocked',
            })
            raise gen.Return(info)


class FollowingAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def get(self):
        username = self.current_user
        ids = yield self.async_task(Following.list_following, username)
        if ids:
            users = yield self.async_task(User.get_multi, sorted(ids))
            followings = [user.information() for user in users]
            raise gen.Return({
                'followings': followings,
                'total': len(followings),
            })


class FollowOneAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def post(self, username):
        me = self.current_user
        yield self.async_task(Following.create, me, username)


class UnfollowOneAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def delete(self, username):
        me = self.current_user
        r = yield self.async_task(Following.get_by_user_following, me, username)
        yield self.async_task(r.delete)


class BlockedAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def get(self):
        username = self.current_user
        ids = yield self.async_task(Blocked.list_blocked, username)
        if ids:
            users = yield self.async_task(User.get_multi, sorted(ids))
            blockeds = [user.information() for user in users]
            raise gen.Return({
                'blockeds': blockeds,
                'total': len(blockeds),
            })


class BlockOneAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def post(self, username):
        me = self.current_user
        yield self.async_task(Blocked.create, me, username)


class UnblockOneAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def delete(self, username):
        me = self.current_user
        r = yield self.async_task(Blocked.get_by_user_following, me, username)
        yield self.async_task(r.delete)


urls = [
    # `GET /api/users/:username`, get information of username.
    (r'/api/users/(\w+)', UsersAPIHandler),

    # For authenticated user:

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
    (r'/api/user/unblock/(\w+)', UnblockOneAPIHandler),
]
