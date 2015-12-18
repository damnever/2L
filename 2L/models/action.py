# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, Float

from .base import Model


class Subscription(Model):
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    date = Column('date', Float(), nullable=False)


class Favorite(Model):
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    comment_id = Column('comment_id', Integer(), index=True, nullable=False)
    date = Column('date', Float(), nullable=False)


class PostUpVote(Model):
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', Float(), nullable=False)


class PostDownVote(Model):
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', Float(), nullable=False)


class CommentUpVote(Model):
    comment_id = Column('comment_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', Float(), nullable=False)


class CommentDownVote(Model):
    comment_id = Column('comment_id', Integer(), index=True, nullable=False)
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    date = Column('date', Float(), nullable=False)
