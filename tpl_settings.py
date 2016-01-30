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

Admins = [
    {
        'username': 'Damnever',
        'password': 'you guess',
        'email': 'dxc.wolf@gmail.com',
        'role': 'GodFather',
    },
    {
        'username': 'Root',
        'password': 'Root',
        'email': 'Root@2L.SB',
        'role': 'Admin',
    },
    {
        'username': 'Admin',
        'password': 'Admin',
        'email': 'Admin@2L.SB',
        'role': 'Admin',
    }
]


EMail = {
    'username': '',
    'password': '',
    'verify': True,
    'smtp': {
        'server': '',
        'port': 25,
    },
}


ThreadPoolMaxWorkers = 5


Tornado = {
    'debug': True,
    'static_path': os.path.join(ROOT_DIR, 'static'),
    'template_path': os.path.join(ROOT_DIR, 'templates'),
    'xsrf_cookies': True,
    # base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)[:-1] + 'x'
    'cookie_secret': 'mv69eaIlTPWUsSwCQMhMYO36uX6MM0uMiJ2D6rRjOdE4',
}
