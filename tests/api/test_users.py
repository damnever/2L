# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import json

import mox

from app.libs.db import init_db, drop_db
from app.models import User, Following, Blocked
from app.settings import Level
from app.base.handlers import APIHandler

from tests.base import BaseTestCase


DATA = {
    'username': 'godfather',
    'password': '1donotknow',
    'email': 'god@father.com',
    'introduce': 'I am God Father',
    'location': 'ChangSha',
    'wiki': ('## God\n You do not know God.\n'
                '## Father\n Yes, I am a father, my son is God'),
    'blog': 'http://damnever.github.io/',
    'github': 'https://github.com/Damnever',
    'google': 'https://plus.google.com/u/0/112029405049071050730',
    'weibo': 'http://weibo.com/u/1977691952',
    'twitter': 'https://twitter.com/WolfDxc',
}


class UsersTests(BaseTestCase):

    _path = '/api/users/{0}'

    def setUp(self):
        super(UsersTests, self).setUp()
        init_db()
        self._data = DATA
        User.create(**self._data)

    def tearDown(self):
        super(UsersTests, self).tearDown()
        drop_db()

    def test_get_user_info(self):
        r = self.get(self._path.format(self._data['username']))
        data = self._data
        data.update({
            'status': 1,
            'id': 1,
            'avatar': '',
            'gold': Level['Gold']['Register'],
        })
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), data)

    def test_username_not_exists_error(self):
        r = self.get(self._path.format('notexists'))
        self.assertEqual(r.code, 200)
        self.assertDictEqual(
            json.loads(r.body),
            {'status': 0, 'reason': 'Username does not exists'},
        )


class UserTests(BaseTestCase):

    _path = '/api/user'

    def setUp(self):
        super(UsersTests, self).setUp()
        self._mox = mox.Mox()
        init_db()
        self._me = DATA
        User.create(**self._me)
        self._mox.StubOutWithMock(APIHandler,
                                  'get_current_user', use_mock_anything=True)
        APIHandler.get_current_user().AndReturn(self._me['username'])
        self._mox.ReplayAll()

    def tearDown(self):
        super(UsersTests, self).tearDown()
        self._mox.UnsetStubs()
        drop_db()

    def test_get_self_info(self):
        r = self.get(self._path)
        data = self._me
        data.update({
            'status': 1,
            'id': 1,
            'avatar': '',
            'gold': Level['Gold']['Register'],
            'following': 0,
            'blocked': 0,
            'following_url': '/api/user/following',
            'blocked_url': '/api/user/blocked',
        })
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), data)
        self._mox.VerifyAll()

    def test_update_self_info(self):
        data = {
            'introduce': 'GodFather is me',
            'location': 'ChangSha, China',
        }
        r = self.patch(self._path, body=data)
        body = self._other
        body.update(data)
        body.update({
            'status': 1,
            'id': 1,
            'avatar': '',
            'gold': Level['Gold']['Register'],
            'following': 0,
            'blocked': 0,
            'following_url': '/api/user/following',
            'blocked_url': '/api/user/blocked',
        })
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), body)
        self._mox.VerifyAll()


class FollowingTests(BaseTestCase):

    _path = '/api/user/following'

    def setUp(self):
        super(UsersTests, self).setUp()
        self._mox = mox.Mox()
        init_db()
        self._other = DATA
        self._me = {
            'username': 'root',
            'password': 'utellme',
            'email': 'root@os.com',
        }
        User.create(**self._me)
        User.create(**self._other)
        Following.create(self._me['username'], self._other['username'])
        self._mox.StubOutWithMock(APIHandler,
                                  'get_current_user', use_mock_anything=True)
        APIHandler.get_current_user().AndReturn(self._me['username'])
        self._mox.ReplayAll()

    def tearDown(self):
        super(UsersTests, self).tearDown()
        self._mox.UnsetStubs()
        drop_db()

    def get_followings(self):
        body = self._other
        body.update({
            'status': 1,
            'id': 1,
            'avatar': '',
            'gold': Level['Gold']['Register'],
            'following': 0,
            'blocked': 0,
            'following_url': '/api/user/following',
            'blocked_url': '/api/user/blocked',
        })
        r = self.get(self._path)
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), body)
        self._mox.VerifyAll()


class FollowOneTests(BaseTestCase):

    _path = '/api/user/follow/{0}'

    def setUp(self):
        super(UsersTests, self).setUp()
        self._mox = mox.Mox()
        init_db()
        self._other = DATA
        self._me = {
            'username': 'root',
            'password': 'utellme',
            'email': 'root@os.com',
        }
        User.create(**self._me)
        User.create(**self._other)
        self._mox.StubOutWithMock(APIHandler,
                                  'get_current_user', use_mock_anything=True)
        APIHandler.get_current_user().AndReturn(self._me['username'])
        self._mox.ReplayAll()

    def tearDown(self):
        super(UsersTests, self).tearDown()
        self._mox.UnsetStubs()
        drop_db()

    def test_follow_one(self):
        r = self.post(self._path.format(self._other['username']))
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), {'status': 1})
        exists = Following.get_by_user_following(
            self._me['username'], self._other['username'])
        self.assertIsNotNone(exists)
        self._mox.VerifyAll()


class UnfollowOneTests(BaseTestCase):

    _path = '/api/user/follow/{0}'

    def setUp(self):
        super(UsersTests, self).setUp()
        self._mox = mox.Mox()
        init_db()
        self._other = DATA
        self._me = {
            'username': 'root',
            'password': 'utellme',
            'email': 'root@os.com',
        }
        User.create(**self._me)
        User.create(**self._other)
        Following.create(self._me['username'], self._other['username'])
        self._mox.StubOutWithMock(APIHandler,
                                  'get_current_user', use_mock_anything=True)
        APIHandler.get_current_user().AndReturn(self._me['username'])
        self._mox.ReplayAll()

    def tearDown(self):
        super(UsersTests, self).tearDown()
        self._mox.UnsetStubs()
        drop_db()

    def test_unfollow_one(self):
        r = self.delete(self._path.format(self._other['username']))
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), {'status': 1})
        exists = Following.get_by_user_following(
            self._me['username'], self._other['username'])
        self.assertIsNone(exists)
        self._mox.VerifyAll()


class BlockedTests(BaseTestCase):

    _path = '/api/user/blocked'

    def setUp(self):
        super(UsersTests, self).setUp()
        self._mox = mox.Mox()
        init_db()
        self._other = DATA
        self._me = {
            'username': 'root',
            'password': 'utellme',
            'email': 'root@os.com',
        }
        User.create(**self._me)
        User.create(**self._other)
        Blocked.create(self._me['username'], self._other['username'])
        self._mox.StubOutWithMock(APIHandler,
                                  'get_current_user', use_mock_anything=True)
        APIHandler.get_current_user().AndReturn(self._me['username'])
        self._mox.ReplayAll()

    def tearDown(self):
        super(UsersTests, self).tearDown()
        self._mox.UnsetStubs()
        drop_db()

    def get_followings(self):
        body = self._other
        body.update({
            'status': 1,
            'id': 1,
            'avatar': '',
            'gold': Level['Gold']['Register'],
            'following': 0,
            'blocked': 0,
            'following_url': '/api/user/following',
            'blocked_url': '/api/user/blocked',
        })
        r = self.get(self._path)
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), body)
        self._mox.VerifyAll()


class BlockOneTests(BaseTestCase):

    _path = '/api/user/block/{0}'

    def setUp(self):
        super(UsersTests, self).setUp()
        self._mox = mox.Mox()
        init_db()
        self._other = DATA
        self._me = {
            'username': 'root',
            'password': 'utellme',
            'email': 'root@os.com',
        }
        User.create(**self._me)
        User.create(**self._other)
        self._mox.StubOutWithMock(APIHandler,
                                  'get_current_user', use_mock_anything=True)
        APIHandler.get_current_user().AndReturn(self._me['username'])
        self._mox.ReplayAll()

    def tearDown(self):
        super(UsersTests, self).tearDown()
        self._mox.UnsetStubs()
        drop_db()

    def test_follow_one(self):
        r = self.post(self._path.format(self._other['username']))
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), {'status': 1})
        exists = Blocked.get_by_user_blocked(
            self._me['username'], self._other['username'])
        self.assertIsNotNone(exists)
        self._mox.VerifyAll()


class UnblockOneTests(BaseTestCase):

    _path = '/api/user/unblock/{0}'

    def setUp(self):
        super(UsersTests, self).setUp()
        self._mox = mox.Mox()
        init_db()
        self._other = DATA
        self._me = {
            'username': 'root',
            'password': 'utellme',
            'email': 'root@os.com',
        }
        User.create(**self._me)
        User.create(**self._other)
        Blocked.create(self._me['username'], self._other['username'])
        self._mox.StubOutWithMock(APIHandler,
                                  'get_current_user', use_mock_anything=True)
        APIHandler.get_current_user().AndReturn(self._me['username'])
        self._mox.ReplayAll()

    def tearDown(self):
        super(UsersTests, self).tearDown()
        self._mox.UnsetStubs()
        drop_db()

    def test_unblock_one(self):
        r = self.delete(self._path.format(self._other['username']))
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), {'status': 1})
        exists = Blocked.get_by_user_blocked(
            self._me['username'], self._other['username'])
        self.assertIsNone(exists)
        self._mox.VerifyAll()
