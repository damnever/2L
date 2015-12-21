# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import APIHandler
from app.base.decorators import as_json


class SubscribedTopicAPIHandler(APIHandler):

    @as_json
    def get(self):
        return []


class SubscribeTopicAPIHandler(APIHandler):

    @as_json
    def post(self, topic_id):
        pass


class UnsubscribeTopicAPIHandler(APIHandler):

    @as_json
    def delete(self, topic_id):
        pass


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
