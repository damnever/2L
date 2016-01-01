# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import json

import mox

from app.models import Topic, User
from app.base.handlers import APIHandler

from tests.base import BaseTestCase


USER = {
    'username': 'XXX',
    'password': 'werqwds34',
    'email': 'XXX@2L.com',
}

TOPIC = {
    'name': '2L',
    'avatar': '',
    'description': 'Good to go',
    'rules': ('## Best practice to be a XXX\n'
              '- Sleep like a XXX\n'
              '- Eat like a XXX\n'
              '- Walk like a XXX\n'
              '- Talk like a XXX\n'),
}


class TopicsTests(BaseTestCase):

    _path = '/api/topics{0}'

    def setUp(self):
        super(TopicsTests, self).setUp(self)
        self._me = USER
        self._topic = TOPIC
        self._topic.update({'admin_id': 1})
        User.create(**self._me)
        Topic.create(**self._topic)

    def test_get_all(self):
        r = self.get(self._path.format(''))
        data = self._topic
        data.pop('admin_id')
        data.update({'id': 1, 'admin': self._me['username']})
        self.assertEqual(r.code, 200)
        self.assertDictEqual(
            json.loads(r.body),
            {'total': 1, 'topics': [data]}
        )

    def test_get_one(self):
        r = self.get(self._path.format('/1'))
        data = self._topic
        data.pop('admin_id')
        data.update({'status': 1, 'id': 1, 'admin': self._me['username']})
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), data)


class TopicTests(BaseTestCase):

    _path = '/api/topic{0}'

    def setUp(self):
        super(TopicTests, self).setUp()
        self._mox = mox.Mox()
        self._me = USER
        User.create(**self._me)
        self._mox.StubOutWithMock(APIHandler,
                                  'get_current_user', use_mock_anything=True)
        APIHandler.get_current_user().AndReturn(self._me['username'])
        self._mox.ReplayAll()

    def tearDown(self):
        super(TopicTests, self).tearDown()
        self._mox.UnsetStubs()

    def test_post(self):
        r = self.post(self._path.format(''), body=TOPIC)
        data = TOPIC
        data.update({
            'id': 1,
            'admin': self._me['username'],
        })
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), {'status': 1})
        topic = Topic.get(1)
        self.assertDictEqual(topic.to_dict(), data)
        self._mox.VerifyAll()

    def test_patch(self):
        tdata = TOPIC
        tdata.update({'admin_id', 1})
        Topic.create(**tdata)
        data = {'description': 'Broken bad'}
        r = self.patch(self._path.format(1), body=data)
        body = TOPIC
        body.update(data)
        body.update({'status': 1, 'id': 1, 'admin': self._me['username']})
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), body)
        self._mox.VerifyAll()
