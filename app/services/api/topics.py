# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json, authenticated, need_permissions
from app.base.roles import Roles
from app.services.api import exceptions
from app.models import Topic


class TopicsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, topic_id):
        if topic_id:
            topic = yield gen.maybe_future(Topic.get(topic_id))
            raise gen.Return(topic.to_dict())
        else:
            topics = yield gen.maybe_future(Topic.list_all())
            result = {
                'total': len(topics),
                'topics': [topic.to_dict() for topic in topics],
            }
            raise gen.Return(result)


class TopicAPIHandler(APIHandler):

    @as_json
    @need_permissions(Roles.TopicCreation)
    @authenticated
    @gen.coroutine
    def post(self):
        name = self.get_argument('name', None)
        description = self.get_argument('description', None)
        rules = self.get_argument('rules', None)
        avatar = self.get_argument('avatar', None)

        if name is None or description is None or rules is None:
            raise exceptions.EmptyFields()
        else:
            exists = yield gen.maybe_future(Topic.get_by_name(name))
            if exists:
                raise exceptions.TopicNameAlreadyExists()
            else:
                created_user = self.current_user
                yield gen.maybe_future(
                    Topic.create(name, created_user, avatar,
                                 description, rules))

    @as_json
    @need_permissions(Roles.TopicEdit)
    @authenticated
    @gen.coroutine
    def patch(self, topic_id):
        fields = dict()
        for key in ('description', 'rules', 'avatar'):
            value = self.get_argument(key, None)
            if value is not None:
                fields[key] = value

        if not fields:
            raise exceptions.EmptyFields()
        else:
            topic = yield gen.maybe_future(Topic.get(topic_id))
            yield gen.maybe_future(topic.update(**fields))


urls = [
    # `GET /api/topics`, return all topics.
    # `GET /api/topics/:topic_id`, return information of the topic.
    (r'/api/topics(?:/(\d+))?', TopicsAPIHandler),
    # For the topic administer or GodFather...
    #  `POST /api/topic`, create a new topic.
    #  `PATCH /api/topic/:topic_id`, update information of the topic.
    (r'/api/topic(?:/(\d+))?', TopicAPIHandler),
]
