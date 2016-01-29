# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json, authenticated
from app.models import Subscription
from app.services.api import exceptions


class SubscribedTopicAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def get(self):
        username = self.current_user
        subs = yield self.async_task(Subscription.list_by_user, username)
        result = {
            'total': len(subs),
            'topics': [s.to_dict() for s in subs],
        }
        raise gen.Return(result)


class SubscribeTopicAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def post(self, topic_id):
        username = self.current_user
        s = yield self.async_task(Subscription.get_by_user_topic,
                                  username, topic_id)
        if s:
            raise exceptions.TopicAlreadySubscribed()
        else:
            yield self.async_task(Subscription.create, username, topic_id)


class UnsubscribeTopicAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def delete(self, topic_id):
        username = self.current_user
        s = yield self.async_task(Subscription.get_by_user_topic,
                                  username, topic_id)
        if s:
            yield self.async_task(s.delete)
        else:
            raise exceptions.TopicHasNotBeenSubscribed()


urls = [
    # For authenticated user:

    #  `GET /api/subscription/topics`, get all subscribed topic.
    (r'/api/subscribed/topics', SubscribedTopicAPIHandler),
    #  `POST /api/subscription/subscribe/:topic_id`,
    #   subscribe a new topic.
    (r'/api/subscribe/topic/(\d+)', SubscribeTopicAPIHandler),
    #  `DELETE /api/subscription/unsubscribe/:topic_id`,
    #   unsubscribe a topic.
    (r'/api/unsubscribe/topic/(\d+)', UnsubscribeTopicAPIHandler),
]
