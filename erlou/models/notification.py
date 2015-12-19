# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, Float

from .base import Model


class Announcement(Model):
    recv_user = Column('recv_user', Integer(), index=True, nullable=False)
    message = Column('message', Integer(), nullable=False)
    date = Column('date', Float(), nullable=False)


class PrivateMessage(Model):
    send_user = Column('send_user', Integer(), index=True, nullable=False)
    recv_user = Column('recv_user', Integer(), index=True, nullable=False)
    message = Column('message', Integer(), nullable=False)
    date = Column('date', Float(), nullable=False)


class PostComment(Model):
    send_user = Column('send_user', Integer(), index=True, nullable=False)
    recv_user = Column('recv_user', Integer(), index=True, nullable=False)
    post_id = Column('post_id', Integer(), nullable=False)
    comment_id = Column('comment_id', Integer(), nullable=False)
    date = Column('date', Float(), nullable=False)


class CommentComment(Model):
    send_user = Column('send_user', Integer(), index=True, nullable=False)
    recv_user = Column('recv_user', Integer(), index=True, nullable=False)
    post_id = Column('post_id', Integer(), nullable=False)
    comment_id = Column('comment_id', Integer(), nullable=False)
    date = Column('date', Float(), nullable=False)
