# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.exceptions import HTTPError
from app.base.handlers import BaseHandler
from app.models import Topic, Post, User, PostUpVote, PostDownVote


class TopicsHandler(BaseHandler):

    def get(self):
        self.render(
            'topics.html',
            title='主题',
            keywords='所有主题, topics',
            description='2L 所有主题',
        )


class TopicHandler(BaseHandler):

    @gen.coroutine
    def get(self, topic_id):
        topic = yield gen.maybe_future(Topic.get(topic_id))
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
                    keywords='新建主题',
                    description='新建主题')


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
    (r'/topics', TopicsHandler),
    (r'/topic/(\d+)', TopicHandler),
    (r'/post/(\d+)', PostHandler),
    (r'/topic/new', NewTopicHandler),
    (r'/topic/(\d+)/new/post', NewPostHandler),
    (r'/notifications/(\w+)', NotificationsHandler),
]
