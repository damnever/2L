# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import functions

from .base import Model


class Topic(Model):
    name = Column('name', String(30), index=True, unique=True, nullable=False)
    avatar = Column('avatar', String(100), nullable=False)
    description = Column('description', String(420), nullable=True)
    rules = relationship('TopicRules', back_populates='topic')


class TopicRules(Model):
    index = Column('index', Integer, nullable=False)
    rule = Column('rule', String(300), nullable=False)


class Post(Model):
    topic_id = Column('topic_id', Integer(), index=True, nullable=False)
    author_id = Column('author_id', Integer(), index=True, nullable=False)
    title = Column('title', Text(120), nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())
    keywords = Column('keywords', String(120), nullable=False)
    content = Column('content', Text(), default='')
    keep_silent = Column('keep_silent', Boolean(), default=False)


class Comment(Model):
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    author_id = Column('author_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())
    content = Column('content', Text(), nullable=False)
