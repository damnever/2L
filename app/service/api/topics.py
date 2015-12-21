# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import APIHandler
from app.base.decorators import as_json


class TopicsAPIHandler(APIHandler):

    @as_json
    def get(self, topic_id):
        if topic_id:
            return self._one_topic(topic_id)
        else:
            return self._all_topics

    def _all_topics(self):
        return None

    def _one_topic(self, topic_id):
        return None


class TopicAPIHandler(APIHandler):

    @as_json
    def post(self):
        return None

    @as_json
    def patch(self, topic_id):
        return None


urls = [
    # `GET /api/topics`, return all topics.
    # `GET /api/topics/:topic_id`, return information of the topic.
    (r'/api/topics(?:/(\d+))?', TopicsAPIHandler),
    # For the topic administer or GodFather...
    #  `POST /api/topic`, build a new topic.
    #  `PATCH /api/topic/:topic_id`, update information of the topic.
    (r'/api/topic(?:/(\d+))?', TopicAPIHandler),
]
