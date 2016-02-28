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
        user = yield gen.maybe_future(User.get_by_name(username))
        if user is None:
            raise exceptions.UsernameDoesNotExists()
        else:
            info = user.information()
            followed, blocked = False, False

            if self.current_user != username:
                me = yield gen.maybe_future(User.get_by_name(self.current_user))
                followed = yield gen.maybe_future(
                    Following.followed(me.id, user.id))
                blocked = yield gen.maybe_future(
                    Blocked.blocked(me.id, user.id))

            info.update({'followed': followed, 'blocked': blocked})
            raise gen.Return(info)


class UserAPIHandler(APIHandler):

    _fields = ("password role gold introduce avatar location "
               "wiki blog github google weibo twitter")

    @as_json
    @authenticated
    @gen.coroutine
    def get(self):
        username = self.current_user
        user = yield gen.maybe_future(User.get_by_name(username))
        raise gen.Return(user.information())

    @as_json
    @authenticated
    @gen.coroutine
    def patch(self):
        fields = dict()
        for key in self._fields.split():
            value = self.get_argument(key, None)
            if value:
                fields[key] = value

        if not fields:
            raise exceptions.EmptyFields()
        else:
            username = self.current_user
            user = yield gen.maybe_future(User.get_by_name(username))
            yield gen.maybe_future(user.update(**fields))


class FollowingAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def get(self):
        username = self.current_user
        users = yield gen.maybe_future(Following.list_following(username))
        followings = list()
        if users:
            ids = [user.following_id for user in users]
            users = yield gen.maybe_future(User.get_multi(*ids))
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
        yield gen.maybe_future(Following.create(me, username))


class UnfollowOneAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def delete(self, username):
        me = self.current_user
        r = yield gen.maybe_future(Following.get_by_user_following(me, username))
        yield gen.maybe_future(r.delete())


class BlockedAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def get(self):
        username = self.current_user
        users = yield gen.maybe_future(Blocked.list_blocked(username))
        blockeds = list()
        if users:
            ids = [user.blocked_id for user in users]
            users = yield gen.maybe_future(User.get_multi(*ids))
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
        yield gen.maybe_future(Blocked.create(me, username))


class UnblockOneAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def delete(self, username):
        me = self.current_user
        r = yield gen.maybe_future(Blocked.get_by_user_blocked(me, username))
        yield gen.maybe_future(r.delete())


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
