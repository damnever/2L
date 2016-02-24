# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import time

import redis

from app.settings import Redis


_SUBJECT_NOTIFICATION = 'subject:notification:{0}'

conn = redis.StrictRedis(**Redis['notification'])
pubsubs = dict()


def channel_matched(channel, username):
    return channel.rsplit(':', 1)[1] == username


def subscribe(username):
    pubsub = conn.pubsub()
    pubsub.subscribe(_SUBJECT_NOTIFICATION.format(username))
    pubsubs[username] = pubsub


def publish(target, msg):
    conn.publish(_SUBJECT_NOTIFICATION.format(target), msg)


def iter_message(username):
    pubsub = pubsubs.get(username, None)
    if pubsub is None:
        raise KeyError('"{0}" not subscribed a channel!'.format(username))

    while 1:
        msg = pubsub.get_message()
        if msg and channel_matched(msg['channel'], username):
            yield msg['data']
        time.sleep(0.001)
