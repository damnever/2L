# -*- coding: utf-8 -*-

#TODO:  get by unread, FUCK...

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, DateTime, String, Boolean
from sqlalchemy.sql import functions

from app.models.base import Model
from app.models.user import User
from app.libs.db import db_session


class Notification(Model):
    sender_id = Column('sender_id', Integer(), index=True, nullable=False)
    recipient_id = Column('recipient_id', Integer(), index=True, nullable=False)
    activity_type = Column('activity_type', String(50), nullable=False)
    content_url = Column('content_url', String(100), nullable=False)
    unread = Column('unread', Boolean(), nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def count_by_recipient(cls, username):
        user = User.get_by_name(username)
        return cls.query.filter(cls.recipient_id==user.id).count()

    @classmethod
    def count_by_type(cls, type_):
        return cls.query.filter(cls.activity_type==type_).count()

    @classmethod
    def get_by_recipient(cls, username):
        user = User.get_by_name(username)
        return cls.query.filter(cls.recipient_id==user.id).all()

    @classmethod
    def get_by_activity_type(cls, type_):
        return cls.query.filter(cls.activity_type==type_).all()

    @classmethod
    def create(cls, sender_name, recipient_name, activity_type, content_url):
        sender = User.get_by_name(sender_name)
        recipient = User.get_by_name(recipient_name)
        n = cls(sender_id=sender.id, recipient_id=recipient.id,
                activity_type=activity_type, content_url=content_url)
        db_session.add(n)

    def mark_as_read(self):
        self.unread = True
        db_session.add(self)

    def sender(self):
        return User.get(self.sender_id)

    def recipient(self):
        return User.get(self.recipient_id)


class Announcement(Model):
    sender_id = Column('sender_id', Integer(), index=True, nullable=False)
    recipient_id = Column('recipient_id', Integer(), index=True, nullable=False)
    activity_type = Column('activity_type', String(50), nullable=False)
    content_url = Column('content_url', String(100), nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())
    expire = Column('expire', DateTime(timezone=True), default=functions.now())

    @classmethod
    def get_by_recipient(cls, username):
        user = User.get_by_name(username)
        return cls.query.filter(cls.recipient_id==user.id).all()

    @classmethod
    def expired(cls, id_):
        announcement = cls.get(id_)
        return announcement.expire <= announcement.date

    def sender(self):
        return User.get(self.sender_id)

    def recipient(self):
        return User.get(self.recipient_id)


class PrivateMessage(Model):
    sender_id = Column('sender_id', Integer(), index=True, nullable=False)
    recipient_id = Column('recipient_id', Integer(), index=True, nullable=False)
    message = Column('message', Integer(), nullable=False)
    unread = Column('unread', Boolean(), nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def get_by_sender(cls, username):
        user = User.get_by_name(username)
        return cls.query.filter(cls.sender_id==user.id).all()

    @classmethod
    def get_by_recipient(cls, username):
        user = User.get_by_name(username)
        return cls.query.filter(cls.recipient_id==user.id).all()

    def sender(self):
        return User.get(self.sender_id)

    def recipient(self):
        return User.get(self.recipient_id)
