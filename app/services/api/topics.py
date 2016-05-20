# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from datetime import datetime, timedelta

from tornado import gen
from tzlocal import get_localzone

from app.base.handlers import APIHandler
from app.base.decorators import as_json, authenticated, need_permissions
from app.base.roles import Roles
from app.services.api import exceptions
from app.models import Topic, Subscription
from app.tasks.tasks import check_proposal, update_gold
from app.settings import Level


def _topic_info(username, topic):
    is_subed = False
    if username is not None:
        exists = Subscription.get_by_user_topic(username, topic.id)
        if exists:
            is_subed = True

    info = topic.to_dict()
    info.update({'is_subscribed': is_subed})
    return info


class AllTopicsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self):
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('per_page', 20))

        pagination = yield gen.maybe_future(
            Topic.page_list_all(page, per_page))
        result = {
            'page': page,
            'per_page': per_page,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'pages': pagination.pages,
            'total': pagination.total,
            'topics': [(yield gen.maybe_future(item.to_dict()))
                       for item in pagination.items],
        }
        raise gen.Return(result)


class AcceptedTopicsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self):
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('per_page', 20))
        username = self.current_user

        pagination = yield gen.maybe_future(
            Topic.page_list_all_accepted(page, per_page))
        result = {
            'page': page,
            'per_page': per_page,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'pages': pagination.pages,
            'total': pagination.total,
            'topics': [(yield gen.maybe_future(_topic_info(username, item)))
                       for item in pagination.items],
        }
        raise gen.Return(result)


class TopicsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, topic_id):
        username = self.current_user

        if topic_id:
            topic = yield gen.maybe_future(Topic.get(topic_id))
            info = yield gen.maybe_future(_topic_info(username, topic))
            raise gen.Return(info)
        else:
            page = int(self.get_argument('page', 1))
            per_page = int(self.get_argument('per_page', 20))

            pagination = yield gen.maybe_future(
                Topic.page_list_all(page, per_page))
            result = {
                'page': page,
                'per_page': per_page,
                'has_prev': pagination.has_prev,
                'has_next': pagination.has_next,
                'pages': pagination.pages,
                'total': pagination.total,
                'topics': [(yield gen.maybe_future(item.to_dict()))
                           for item in pagination.items],
            }
            raise gen.Return(result)


class TopicAPIHandler(APIHandler):

    @as_json
    @need_permissions(Roles.TopicCreation)
    @gen.coroutine
    def post(self, topic_id):
        name = self.get_argument('name', None)
        description = self.get_argument('description', None)
        rules = self.get_argument('rules', None)
        avatar = self.get_argument('avatar', None)
        why = self.get_argument('why', None)

        if not all([name, description, rules, why]):
            raise exceptions.EmptyFields()
        else:
            exists = yield gen.maybe_future(Topic.get_by_name(name))
            if exists:
                raise exceptions.TopicNameAlreadyExists()
            else:
                created_user = self.current_user
                topic = yield gen.maybe_future(
                    Topic.create(name, created_user, avatar,
                                 description, rules, why))

                # Update Gold.
                update_gold.apply_async(('new_proposal', created_user))

                # Update proposal state.
                seconds = Level['time']['proposal']
                wait = datetime.now(get_localzone()) + timedelta(seconds=seconds)
                check_proposal.apply_async((topic.id,), eta=wait)

    @as_json
    @need_permissions(Roles.TopicEdit)
    @authenticated
    @gen.coroutine
    def patch(self, topic_id):
        fields = dict()
        for key in ('description', 'rules', 'avatar', 'state'):
            value = self.get_argument(key, None)
            if value is not None:
                fields[key] = value

        if not fields:
            raise exceptions.EmptyFields()
        else:
            topic = yield gen.maybe_future(Topic.get(topic_id))
            yield gen.maybe_future(topic.update(**fields))

    @as_json
    @need_permissions(Roles.TopicEdit)
    @authenticated
    @gen.coroutine
    def delete(self, topic_id):
        topic = yield gen.maybe_future(Topic.get(topic_id))
        if topic:
            yield gen.maybe_future(topic.delete())


urls = [
    # `GET /api/topics/all`, return all topics
    (r'/api/topics/all$', AllTopicsAPIHandler),
    # `GET /api/topics/accepted`,
    # return all accepted topics, those can be subscrined.
    (r'/api/topics/accepted$', AcceptedTopicsAPIHandler),
    # `GET /api/topics`, return all topics.
    # `GET /api/topics/:topic_id`, return information of the topic.
    (r'/api/topics(?:/(\d+))?', TopicsAPIHandler),
    # For the topic administer or GodFather...
    #  `POST /api/topic`, create a new topic.
    #  `PATCH /api/topic/:topic_id`, update information of the topic.
    #  `DELETE /api/topic/:topic_id`, delete topic
    (r'/api/topic(?:/(\d+))?', TopicAPIHandler),
]
