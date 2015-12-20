# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, DateTime, String, Boolean
from sqlalchemy.sql import functions

from app.models.base import Model


class Notification(Model):
    sender = Column('sender', Integer(), index=True, nullable=False)
    recipient = Column('recipient', Integer(), index=True, nullable=False)
    activity_type = Column('activity_type', String(50), nullable=False)
    content_url = Column('content_url', String(100), nullable=False)
    unread = Column('unread', Boolean(), nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())


class Announcement(Model):
    sender = Column('sender', Integer(), index=True, nullable=False)
    recipient = Column('recipient', Integer(), index=True, nullable=False)
    activity_type = Column('activity_type', String(50), nullable=False)
    content_url = Column('content_url', String(100), nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())
    expire = Column('expire', DateTime(timezone=True), default=functions.now())


class PrivateMessage(Model):
    sender = Column('sender', Integer(), index=True, nullable=False)
    recipient = Column('recipient', Integer(), index=True, nullable=False)
    message = Column('message', Integer(), nullable=False)
    unread = Column('unread', Boolean(), nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())
