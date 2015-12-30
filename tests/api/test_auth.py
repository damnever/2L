# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import json

from app.libs.db import init_db, drop_db
from app.models import User

from tests.base import BaseTestCase


class RegisterTests(BaseTestCase):

    _path = '/api/register'

    def setUp(self):
        super(RegisterTests, self).setUp()
        init_db()
        User.create(
            username='exists',
            password='newpassword',
            email='exists@exists.com'
        )

    def tearDown(self):
        super(RegisterTests, self).tearDown()
        drop_db()

    def test_register_success(self):
        body = {
            'username': 'abc',
            'password': '12345678',
            'email': 'abc@123.com',
        }
        r = self.post(self._path, body)
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), {'status': 1})

    def test_empty_fields_error(self):
        body = {
            'username': 'bcd',
        }
        r = self.post(self._path, body)
        self.assertEqual(r.code, 200)
        self.assertDictEqual(
            json.loads(r.body),
            {'status': 0, 'reason': 'Empty fields'}
        )

    def test_username_exists_error(self):
        body = {
            'username': 'exists',
            'password': '987654321',
            'email': 'cde@987.com',
        }
        r = self.post(self._path, body)
        self.assertEqual(r.code, 200)
        self.assertDictEqual(
            json.loads(r.body),
            {'status': 0, 'reason': 'Username already exists'}
        )

    def test_email_exists_error(self):
        body = {
            'username': 'cde',
            'password': '347862340',
            'email': 'exists@exists.com',
        }
        r = self.post(self._path, body)
        self.assertEqual(r.code, 200)
        self.assertDictEqual(
            json.loads(r.body),
            {'status': 0, 'reason': 'E-mail already exists'}
        )


class LoginTests(BaseTestCase):

    _path = '/api/login'

    def setUp(self):
        super(RegisterTests, self).setUp()
        init_db()
        self._data = {
            'username': 'exists',
            'password': 'newpassword',
            'email': 'exists@exists.com',
        }
        User.create(**self._data)

    def tearDown(self):
        super(RegisterTests, self).tearDown()
        drop_db()

    def test_login_success(self):
        r = self.post(self._path, body=self._data)
        self.assertEqual(r.code, 200)
        self.assertDictEqual(json.loads(r.body), {'status': 1})

    def test_empty_fields_error(self):
        body = {'username': 'exists'}
        r = self.post(self._path, body=body)
        self.assertEqual(r.code, 200)
        self.assertDictEqual(
            json.loads(r.body),
            {'status': 0, 'reason': 'Empty fields'}
        )

    def test_username_no_exists_error(self):
        body = self._data
        body['username'] = 'notexists'
        r = self.post(self._path, body=body)
        self.assertEqual(self._path, body=body)
        self.assertDictEqual(
            json.loads(r.body),
            {'status': 0, 'reason': 'Username does not exists'}
        )

    def test_password_wrong_error(self):
        body = self._data
        body['password'] = 'wrongpassword'
        r = self.post(self._path, body=body)
        self.assertEqual(r.code, 200)
        self.assertDictEqual(
            json.loads(r.body),
            {'status': 0, 'reason': 'Password wrong'}
        )
