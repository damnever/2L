# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.sql import functions

from app.models.base import Model


class Subscription(Model):
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    topic_id = Column('topic_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())


class Favorite(Model):
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())


class PostView(Model):
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), default=0)
    agent = Column('agent', String(50), default='')
    ip = Column('ip', String(15), default='')


class PostUpVote(Model):
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())


class PostDownVote(Model):
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())


class CommentUpVote(Model):
    comment_id = Column('comment_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())


class CommentDownVote(Model):
    comment_id = Column('comment_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())
