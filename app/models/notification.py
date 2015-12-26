# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, DateTime, String, Boolean
from sqlalchemy.sql import functions, expression

from app.models.base import Model
from app.models.user import User
from app.libs.db import db_session


class Notification(Model):
    sender_id = Column('sender_id', Integer(), index=True, nullable=False)
    recipient_id = Column('recipient_id', Integer(), index=True, nullable=False)
    activity_type = Column('activity_type', String(50), nullable=False)
    content_url = Column('content_url', String(100), nullable=False)
    unread = Column('unread', Boolean(), nullable=True)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def list_by_recipient(cls, username, unread=None):
        user = User.get_by_name(username)
        stmt = cls.recipient_id==user.id
        if unread is not None:
            stmt = expression.and_(stmt, cls.unread==unread)
        return cls.query.filter(stmt)

    @classmethod
    def list_by_type(cls, type_, unread=None):
        stmt = cls.activity_type==type_
        if unread is not None:
            stmt = expression.and_(stmt, cls.unread==unread)
        return cls.query.filter(stmt)

    @classmethod
    def create(cls, sender_name, recipient_name, activity_type, content_url):
        sender = User.get_by_name(sender_name)
        recipient = User.get_by_name(recipient_name)
        n = cls(sender_id=sender.id, recipient_id=recipient.id,
                activity_type=activity_type, content_url=content_url)
        db_session.add(n)
        db_session.commit()

    def mark_as_read(self):
        self.unread = False
        db_session.add(self)
        db_session.commit()

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
    def list_by_recipient(cls, username):
        user = User.get_by_name(username)
        return cls.query.filter(cls.recipient_id==user.id)

    @classmethod
    def expired(cls, id_):
        announcement = cls.get(id_)
        return announcement.expire <= announcement.date

    @classmethod
    def create(cls, sender_name, recipient_name, activity_type,
               content_url, expire):
        sender = User.get_by_name(sender_name)
        recipient = User.get_by_name(recipient_name)
        a = cls(
            sender_id=sender.id,
            recipient_id=recipient.id,
            activity_type=activity_type,
            content_url=content_url,
            expire=expire
        )
        db_session.add(a)
        db_session.commit()

    def sender(self):
        return User.get(self.sender_id)

    def recipient(self):
        return User.get(self.recipient_id)


class PrivateMessage(Model):
    sender_id = Column('sender_id', Integer(), index=True, nullable=False)
    recipient_id = Column('recipient_id', Integer(), index=True, nullable=False)
    message = Column('message', Integer(), nullable=False)
    unread = Column('unread', Boolean(), nullable=True)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def list_by_sender(cls, username, unread=None):
        user = User.get_by_name(username)
        stmt = cls.sender_id==user.id
        if unread is not None:
            stmt = expression.and_(stmt, cls.unread==unread)
        return cls.query.filter(stmt)

    @classmethod
    def list_by_recipient(cls, username, unread=None):
        user = User.get_by_name(username)
        stmt = cls.recipient_id==user.id
        if unread is not None:
            stmt = expression.and_(stmt, cls.unread==unread)
        return cls.query.filter()

    @classmethod
    def create(cls, sender_name, recipient_name, message):
        sender = User.get_by_name(sender_name)
        recipient = User.get_by_name(recipient_name)
        pm = cls(sender_id=sender.id, recipient_id=recipient.id,
                 message=message)
        db_session.add(pm)
        db_session.commit()

    def mark_as_read(self):
        self.unread = False
        db_session.add(self)

    def sender(self):
        return User.get(self.sender_id)

    def recipient(self):
        return User.get(self.recipient_id)
