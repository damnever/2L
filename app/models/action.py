# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import functions, expression

from app.models.base import Model
from app.models.user import User
from app.models.content import Topic, Post


class Subscription(Model):
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    topic_id = Column('topic_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def list_by_topic(cls, topic_id):
        return cls.query.filter(cls.topic_id==topic_id).all()

    @classmethod
    def list_by_user(cls, username):
        user = User.get_by_name(username)
        return cls.query.filter(cls.user_id==user.id).all()

    @classmethod
    def get_by_user_topic(cls, username, topic_id):
        user = User.get_by_name(username)
        r = cls.query.filter(expression.and_(cls.user_id==user.id,
                                             cls.topic_id==topic_id))
        return r.first()

    @classmethod
    def create(cls, username, topic_id):
        user = User.get_by_name(username)
        s = cls(user_id=user.id, topic_id=topic_id)
        cls.session.add(s)
        cls.session.commit()
        return s

    def to_dict(self):
        return {
            'id': self.id,
            'topic': self.topic.to_dict(),
            'date': self.date,
        }

    @property
    def topic(self):
        return Topic.get(self.topic_id)


class Favorite(Model):
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def count_by_post(cls, post_id):
        return cls.query.filter(cls.post_id==post_id).count()

    @classmethod
    def list_by_user(cls, username):
        user = User.get_by_name(username)
        return cls.query.filter(cls.user_id==user.id).all()

    @classmethod
    def list_by_post(cls, post_id):
        return cls.query.filter(cls.post_id==post_id).all()

    @classmethod
    def get_by_user_post(cls, username, post_id):
        user = User.get_by_name(username)
        r = cls.query.filter(expression.and_(cls.user_id==user.id,
                                             cls.post_id==post_id))
        return r.first()

    @classmethod
    def create(cls, username, post_id):
        user = User.get_by_name(username)
        f = cls(user_id=user.id, post_id=post_id)
        cls.session.add(f)
        cls.session.commit()
        return f

    def to_dict(self):
        return {
            'id': self.id,
            'post': self.post.to_dict(),
            'date': self.date,
        }

    @property
    def post(self):
        return Post.get(self.post_id)


class PostUpVote(Model):
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def count_by_post(cls, post_id):
        return cls.query.filter(cls.post_id==post_id).count()

    @classmethod
    def list_by_post(cls, post_id):
        return cls.query.filter(cls.post_id==post_id).all()

    @classmethod
    def get_by_user_post(cls, username, post_id):
        user = User.get_by_name(username)
        r = cls.query.filter(expression.and_(cls.post_id==post_id,
                                             cls.user_id==user.id))
        return r.first()

    @classmethod
    def create(cls, username, post_id):
        user = User.get_by_name(username)
        pu = cls(user_id=user.id, post_id=post_id)
        cls.session.add(pu)
        cls.session.commit()
        return pu

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.username,
            'date': self.date,
        }

    @property
    def user(self):
        return User.get(self.user_id)


class PostDownVote(Model):
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def count_by_post(cls, post_id):
        return cls.query.filter(cls.post_id==post_id).count()

    @classmethod
    def list_by_post(cls, post_id):
        return cls.query.filter(cls.post_id==post_id).all()

    @classmethod
    def get_by_user_post(cls, username, post_id):
        user = User.get_by_name(username)
        r = cls.query.filter(expression.and_(cls.post_id==post_id,
                                             cls.user_id==user.id))
        return r.first()

    @classmethod
    def create(cls, username, post_id):
        user = User.get_by_name(username)
        pd = cls(user_id=user.id, post_id=post_id)
        cls.session.add(pd)
        cls.session.commit()
        return pd


class CommentUpVote(Model):
    comment_id = Column('comment_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def count_by_comment(cls, comment_id):
        return cls.query.filter(cls.comment_id==comment_id).count()

    @classmethod
    def list_by_comment(cls, comment_id):
        return cls.query.filter(cls.comment_id==comment_id).all()

    @classmethod
    def get_by_user_comment(cls, username, comment_id):
        user = User.get_by_name(username)
        r = cls.query.filter(expression.and_(cls.comment_id==comment_id,
                                             cls.user_id==user.id))
        return r.first()

    @classmethod
    def create(cls, username, comment_id):
        user = User.get_by_name(username)
        cu = cls(user_id=user.id, comment_id=comment_id)
        cls.session.add(cu)
        cls.session.commit()
        return cu


class CommentDownVote(Model):
    comment_id = Column('comment_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def count_by_comment(cls, comment_id):
        return cls.query.filter(cls.comment_id==comment_id).count()

    @classmethod
    def list_by_comment(cls, comment_id):
        return cls.query.filter(cls.comment_id==comment_id).all()

    @classmethod
    def get_by_user_comment(cls, username, comment_id):
        user = User.get_by_name(username)
        r = cls.query.filter(expression.adn_(cls.comment_id==comment_id,
                                             cls.user_id==user.id))
        return r.first()

    @classmethod
    def create(cls, username, comment_id):
        user = User.get_by_name(username)
        cd = cls(user_id=user.id, comment_id=comment_id)
        cls.session.add(cd)
        cls.session.commit()
        return cd
