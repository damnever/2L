# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import json

from app.libs.db import init_db, drop_db
from app.models import User

from tests.base import BaseTestCase


class UsersTests(BaseTestCase):

    _path = '/api/users/{0}'

    def setUp(self):
        super(RegisterTests, self).setUp()
        init_db()
        self._data = {
            'username': 'godfather',
            'password': '1donotknow',
            'email': 'god@father.com',
        }
        User.create(**self._data)

    def tearDown(self):
        super(RegisterTests, self).tearDown()
        drop_db()

    def test_get_user_info(self):
        r = self.get(self._path.format(self._data['username']))
        self.assertEqual(r.code, 200)

