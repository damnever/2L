# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import os.path


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def read_img(path):
    path = os.path.join(ROOT_DIR, path)
    with open(path, 'rb') as f:
        return f.read()


MySQL = {
    'username': 'root',
    'password': 'DXC',
    'host': '127.0.0.1',
    'port': 3306,
    'db': '2L',
}

Redis = {
    'cache': {
        'password': '',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
    },
    'session': {
        'password': '',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 1,
    },
    'gold': {
        'password': '',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 2,
    },
    'task': {
        'password': '',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 3,
    },
    'notification': {
        'password': '',
        'host': '127.0.0.1',
        'port': 6379,
        'db': 4,
    },
}

Level = {
    'gold': {
        'register': 50,
        'topic_creation': 500,
        'vote': 100,
    },
    'time': {
        'comment': 1800,  # 30 minutes
        'proposal': 1200,  # 20 minutes
    }
}

Gold = {
    'rob': [2, 22],
    'register': 50,
    '2L': [2, 22],
    'new_proposal': -50,
    'proposal_accepted': +60,
    'proposal_rejected': +10,
    'new_post': -10,
    'delete_post': -30,
    'post_be_favorite': 10,
    'comment': -1,
    'be_comment': 1,
    'up_vote': -5,
    'be_up_vote': 5,
    'down_vote': -8,
    'be_down_vote': -5,
    'report': -15,
    'report_confirm': 30,
    'be_report': 0,
    'be_report_confirm': -30,
}

ResetGoldTime = 14

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
        'password': 'youguess',
        'email': 'dxc.wolf@gmail.com',
        'avatar': read_img('static/imgs/damnever.png.txt'),
        'role': 'root',
    },
    {
        'username': 'Root',
        'password': 'RootRoot',
        'email': 'Root@2L.SB',
        'avatar': read_img('static/imgs/anonymous.png.txt'),
        'role': 'admin',
    },
    {
        'username': 'Admin',
        'password': 'AdminAdmin',
        'email': 'Admin@2L.SB',
        'avatar': read_img('static/imgs/admin.png.txt'),
        'role': 'admin',
    }
]

Topics = [
    {
        'name': '2L',
        'created_name': Admins[0]['username'],
        'avatar': read_img('static/imgs/2L.png.txt'),
        'description': '关于本站（2L）的所有事务都可以在这里讨论，拒绝灌水。',
        'rules': '  \n# 2',
        'why': 'No BB',
        'state': 1,
    },
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


ThreadPoolMaxWorkers = 10


DefaultAvatar = read_img('static/imgs/anonymous.png.txt')


Tornado = {
    'debug': True,
    'static_path': os.path.join(ROOT_DIR, 'static'),
    'template_path': os.path.join(ROOT_DIR, 'templates'),
    'xsrf_cookies': True,
    # base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)[:-1] + 'x'
    'cookie_secret': 'mv69eaIlTPWUsSwCQMhMYO36uX6MM0uMiJ2D6rRjOdE4',
    'allow_origin': '*',
    'allow_origin_pat': '.+',
}
