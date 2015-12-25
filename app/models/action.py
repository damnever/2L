# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import functions, expression

from app.models.base import Model
from app.models.user import User
from app.libs.db import db_session


class Subscription(Model):
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    topic_id = Column('topic_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def count_by_user(cls, username):
        user = User.get_by_name(username)
        return cls.query.filter(cls.user_id==user.id).count()

    @classmethod
    def count_by_topic(cls, topic_id):
        return cls.query.filter(cls.topic_id==topic_id).count()

    @classmethod
    def get_by_topic(cls, topic_id):
        return cls.query.filter(cls.topic_id==topic_id).all()

    @classmethod
    def get_by_user(cls, username):
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
        db_session.add(s)


class Favorite(Model):
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def count_by_user(cls, username):
        user = User.get_by_name(username)
        return cls.query.filter(cls.user_id==user.id).count()

    @classmethod
    def count_by_post(cls, post_id):
        return cls.query.count()

    @classmethod
    def get_by_user(cls, username):
        user = User.get_by_name(username)
        return cls.query.filter(cls.user_id==user.id).all()

    @classmethod
    def get_by_post(cls, post_id):
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
        db_session.add(f)


class PostView(Model):
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), default=0)
    system = Column('system', String(30), default='')
    agent = Column('agent', String(30), default='')
    ip = Column('ip', String(15), default='')

    @classmethod
    def create(cls, username, post_id, system, agent, ip):
        user = User.get_by_name(username)
        p = cls(post_id=post_id, user_id=user.id, system=system,
                agent=agent, ip=ip)
        db_session.add(p)


class PostUpVote(Model):
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def count_by_post(cls, post_id):
        return cls.query.filter(cls.post_id==post_id).count()

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
        db_session.add(pu)


class PostDownVote(Model):
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def count_by_post(cls, post_id):
        return cls.query.filter(cls.post_id==post_id).count()

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
        db_session.add(pd)


class CommentUpVote(Model):
    comment_id = Column('comment_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def count_by_comment(cls, comment_id):
        return cls.query.filter(cls.comment_id==comment_id).count()

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
        db_session.add(cu)


class CommentDownVote(Model):
    comment_id = Column('comment_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def count_by_comment(cls, comment_id):
        return cls.query.filter(cls.comment_id==comment_id).count()

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
        db_session.add(cd)
