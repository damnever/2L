# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.tasks.celery import app


class Strategy(object):

    def __call__(self, type_, *args):
        method = getattr(self, type_, None)
        if method is not None:
            method(*args)


@app.task(name='reset_gold', max_retries=5)
def reset_gold():
    import random
    from app.models import User
    from app.cache import gold
    from app.settings import Gold

    users = User.count() // 2
    count = random.randint(*Gold['rob']) * users
    gold.set(users, count)


@app.task(name='update_permission', max_retries=5)
def update_permission(user, role):
    from app.libs.db import db_session
    from app.models import Permission

    user.role |= Permission.get_by_role(role).bit
    db_session.add(user)
    db_session.commit()


@app.task(name='check_proposal', max_retries=5)
def check_proposal(topic_id):
    from app.libs.db import db_session
    from app.models import Topic, User, TopicUpVote, TopicDownVote
    from app.settings import Gold

    user_count = User.count()
    topic = Topic.get(topic_id)
    user = User.get(topic.admin_id)
    up_votes = TopicUpVote.count_by_topic(topic_id)
    down_votes = TopicDownVote.count_by_topic(topic_id)

    # Check if the proposal can be accepted or rejected.
    if (up_votes - down_votes) > (user_count / 2):
        topic.state = 1
        user.profile.gold += Gold['proposal_accepted']
    else:
        topic.state = -1
        user.profile.gold += Gold['proposal_rejected']

    db_session.add(user)
    db_session.add(topic)
    db_session.commit()


@app.task(name='update_gold', max_retries=5)
def update_gold(type_, *args):
    import random
    from app.models import User, Post, Comment
    from app.settings import Gold

    class _UpdateProposal(Strategy):

        def sb_2l(self, username, post_id):
            count, comment = Comment.last_with_count(post_id)
            user = User.get(comment.author_id)
            if count == 2 and username == user.username:
                gold = random.randint(*Gold['2L'])
                user.update(gold=gold)

        def new_proposal(self, username):
            user = User.get_by_name(username)
            user.update(gold=Gold['new_proposal'])

        def new_post(self, username):
            user = User.get_by_name(username)
            user.update(gold=Gold['new_post'])

        def delete_post(self, username):
            user = User.get_by_name(username)
            user.update(gold=Gold['delete_post'])

        def post_be_favorite(self, post_id, symbol=1):
            post = Post.get(post_id)
            user = User.get(post.author_id)
            user.update(gold=(Gold['post_be_favorite'] * symbol))

        def cancel_post_be_favorite(self, post_id):
            self.post_be_favorite(post_id, symbol=-1)

        def comment(self, username):
            user = User.get_by_name(username)
            user.update(gold=Gold['comment'])

        def be_comment(self, usernames):
            for username in usernames:
                user = User.get_by_name(username)
                user.update(gold=Gold['be_comment'])

        def vote(self, username, id_, category, vote_type, symbol=1):
            v = None
            if category == 'topic':
                return
            elif category == 'post':
                v = Post.get(id_)
            elif category == 'comment':
                v = Comment.get(id_)
            if v is None:
                return

            vote_user = User.get_by_name(username)
            vote_user.update(gold=(Gold['{0}_vote'.format(vote_type)]*symbol))
            be_vote_user = User.get(v.author_id)
            be_vote_user.update(
                gold=(Gold['be_{0}_vote'.format(vote_type)]*symbol))

        def cancel_vote(self, username, id_, category, vote_type):
            self.vote(username, id_, category, vote_type, symbol=-1)

    _UpdateProposal()(type_, *args)


@app.task(name='send_email', max_retries=4)
def send_email(to_name, to_addr, subject, message):
    pass


@app.task(name='notify', max_retries=10)
def notify(type_, *args):
    from tornado.escape import json_encode
    from app.models import User, Notification, Post
    from app.cache import notification

    class _Notification(Strategy):
        _comment_header = (u'<a href="/user/{0}">{0}</a> 回复了你的帖子'
                           u' <a href="/post/{1}">{2}</a>:')
        _at_header = (u'<a href="/user/{0}">{0}</a> 在回复 '
                      u'<a href="/post/{1}">{2}</a> 时提到了你:')

        def comment(self, sender_name, post_id, content):
            post = Post.get(post_id)
            user = User.get(post.author_id)
            header = self._comment_header.format(
                sender_name, post.id, post.title)
            Notification.create(
                sender_name, user.username, 'comment', header, content)
            notification.publish(user.username, json_encode({'unread': 1}))

        def at(self, sender_name, usernames, post_id, content):
            post = Post.get(post_id)

            for username in usernames:
                header = self._at_header.format(
                    sender_name, post.id, post.title)
                Notification.create(
                    sender_name, username, 'at', header, content)
                notification.publish(username, json_encode({'unread': 1}))

    _Notification()(type_, *args)
