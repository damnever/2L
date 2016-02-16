# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.exceptions import HTTPError
from app.base.handlers import BaseHandler
from app.models import (
    Topic, Post, User,
    PostUpVote, PostDownVote, TopicUpVote, TopicDownVote,
)


class TopicHandler(BaseHandler):

    @gen.coroutine
    def get(self, topic_id):
        topic = yield gen.maybe_future(Topic.get(topic_id))
        if not topic:
            raise HTTPError(404)
        admin = yield gen.maybe_future(User.get(topic.admin_id))
        self.render(
            'topic.html',
            title=topic.name,
            keywords=topic.name + ', 2L',
            description=topic.description,
            topic_id=topic_id,
            admin=admin.username,
            avatar=topic.avatar,
            rules=topic.rules,
        )


class NewTopicHandler(BaseHandler):

    def get(self):
        self.render('new_topic.html',
                    title='新建主题',
                    keywords='新建主题, 2L',
                    description='新建主题, 2L')


class ProposalHandler(BaseHandler):

    @gen.coroutine
    def get(self, topic_id):
        topic = yield gen.maybe_future(Topic.get(topic_id))
        if not topic:
            raise HTTPError(404)
        user = yield gen.maybe_future(User.get(topic.admin_id))
        up_votes = yield gen.maybe_future(TopicUpVote.count_by_topic(topic_id))
        down_votes = yield gen.maybe_future(
            TopicDownVote.count_by_topic(topic_id))

        up_voted, down_voted = False, False
        username = self.current_user
        if username is not None:
            up_voted = bool((yield gen.maybe_future(
                TopicUpVote.get_by_user_topic(username, topic_id))))
            down_voted = bool((yield gen.maybe_future(
                TopicDownVote.get_by_user_topic(username, topic_id))))
        self.render(
            'proposal.html',
            title=topic.name,
            keywords=topic.name + ', 2L',
            description=topic.description,
            id=topic.id,
            avatar=topic.avatar,
            rules=topic.rules,
            why=topic.why,
            state=topic.state,
            date=topic.date,
            user=user.username,
            #  user_avatar=user.profile.avatar,
            up_votes=up_votes,
            down_votes=down_votes,
            up_voted=int(up_voted),
            down_voted=int(down_voted),
        )


class PostHandler(BaseHandler):

    @gen.coroutine
    def get(self, post_id):
        post = yield gen.maybe_future(Post.get(post_id))
        if not post:
            raise HTTPError(404)
        author = yield gen.maybe_future(User.get(post.author_id))
        up_votes = yield gen.maybe_future(PostUpVote.count_by_post(post_id))
        down_votes = yield gen.maybe_future(PostDownVote.count_by_post(post_id))
        self.render(
            'post.html',
            title=post.title,
            keywords=post.keywords,
            description=post.title,
            topic_id=post.topic_id,
            post_id=post_id,
            author=author.username,
            avatar=author.profile.avatar,
            date=post.created_date,
            content=post.content,
            up_votes=up_votes,
            down_votes=down_votes,
        )


class NewPostHandler(BaseHandler):

    @gen.coroutine
    def get(self, topic_id):
        topic = yield gen.maybe_future(Topic.get(topic_id))
        if not topic:
            raise HTTPError(404)
        admin = yield gen.maybe_future(User.get(topic.admin_id))
        self.render('new_post.html',
                    title=topic.name,
                    keywords=topic.name + ', 2L',
                    description=topic.description,
                    topic_id=topic_id,
                    rules=topic.rules,
                    admin=admin.username,
                    avatar=topic.avatar)


class NotificationsHandler(BaseHandler):

    def get(self, username):
        self.render('notifications.html',
                    title='通知',
                    description='通知',
                    keywords='通知')


urls = [
    (r'/topic/(\d+)', TopicHandler),
    (r'/post/(\d+)', PostHandler),
    (r'/topic/new', NewTopicHandler),
    (r'/proposal/(\d+)', ProposalHandler),
    (r'/topic/(\d+)/new/post', NewPostHandler),
    (r'/notifications/(\w+)', NotificationsHandler),
]
