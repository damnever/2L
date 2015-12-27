# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import os.path


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


MySQL = {
    'username': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 3306,
    'db': '2L',
}

Redis = {
    'password': '',
    'host': '127.0.0.1',
    'port': 6379,
    'cache_db': 0,
    'session_db': 1,
    'gold_db': 2,
}

Level = {
    'Gold': {
        'Register': 50,
        'TopicCreation': 500,
        'Vote': 100,
    },
    'Time': {
        'Comment': 18000,  # 5 hours
    }
}

Accounts = {
    'GitHub': {
        'login': True,
        'token': '',
    },
    'Weibo': {
        'login': True,
        'token': '',
    },
    'QQ': {
        'login': True,
        'token': '',
    },
    'Gmail': {
        'login': True,
        'token': '',
    },
}


EMail = {
    'username': '',
    'password': '',
    'verify': True,
    'smtp': {
        'server': '',
        'port': 25,
    },
}


Tornado = {
    'debug': True,
    'static_path': os.path.join(ROOT_DIR, 'static'),
    'template_path': os.path.join(ROOT_DIR, 'templates'),
    'cookie_secret': '',
}
