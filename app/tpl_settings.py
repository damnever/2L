# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import


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
    'db': 0,
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
    'static_path': 'static',
    'template_path': 'templates',
    'cookie_secret': '',
}
