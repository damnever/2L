# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, DateTime, String, Boolean, Text
from sqlalchemy.sql import functions, expression
from sqlalchemy.exc import DataError, IntegrityError, ProgrammingError

from app.models.base import Model
from app.models.user import User
from app.libs.db import db_session


class Notification(Model):
    """activity_type: comment, at, follow..."""

    sender_id = Column('sender_id', Integer(), index=True, nullable=False)
    recipient_id = Column('recipient_id', Integer(), index=True, nullable=False)
    activity_type = Column('activity_type', String(50), nullable=False)
    header = Column('header', Text(), nullable=False)
    content = Column('content', Text(), nullable=False)
    unread = Column('unread', Boolean(), default=True)
    date = Column('date', DateTime(timezone=True), default=functions.now())

    @classmethod
    def list_by_recipient(cls, username, unread=None):
        user = User.get_by_name(username)
        cond = [cls.recipient_id==user.id]
        if unread is not None:
            cond.append(cls.unread==unread)
        return cls.query.filter(expression.and_()).all()

    @classmethod
    def list_by_type(cls, type_, unread=None):
        cond = [cls.activity_type==type_]
        if unread is not None:
            cond.append(cls.unread==unread)
        return cls.query.filter(expression.and_(cond)).all()

    @classmethod
    def list_by_user_and_type(cls, username, type_, unread=None):
        user = User.get_by_name(username)
        cond = [cls.activity_type==type_, cls.recipient_id==user.id]
        if unread is not None:
            cond.append(cls.unread==unread)
        return cls.query.filter(expression.and_(*cond)).all()

    @classmethod
    def create(cls, sender_name, recipient_name,
               activity_type, header, content):
        sender = User.get_by_name(sender_name)
        recipient = User.get_by_name(recipient_name)
        n = cls(sender_id=sender.id, recipient_id=recipient.id,
                activity_type=activity_type, header=header,
                content=content, unread=True)
        try:
            db_session.add(n)
            db_session.commit()
        except (DataError, IntegrityError, ProgrammingError):
            db_session.rollback()
            raise
        return n

    def to_dict(self):
        return {
            'id': self.id,
            'header': self.header,
            'content': self.content,
        }

    def mark_as_read(self):
        self.unread = False
        try:
            db_session.add(self)
            db_session.commit()
        except (DataError, IntegrityError, ProgrammingError):
            db_session.rollback()
            raise

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
        return cls.query.filter(cls.recipient_id==user.id).all()

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
        try:
            db_session.add(a)
            db_session.commit()
        except (DataError, IntegrityError, ProgrammingError):
            db_session.rollback()
            raise
        return a

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
        return cls.query.filter(stmt).all()

    @classmethod
    def list_by_recipient(cls, username, unread=None):
        user = User.get_by_name(username)
        stmt = cls.recipient_id==user.id
        if unread is not None:
            stmt = expression.and_(stmt, cls.unread==unread)
        return cls.query.filter().all()

    @classmethod
    def create(cls, sender_name, recipient_name, message):
        sender = User.get_by_name(sender_name)
        recipient = User.get_by_name(recipient_name)
        pm = cls(sender_id=sender.id, recipient_id=recipient.id,
                 message=message)
        try:
            db_session.add(pm)
            db_session.commit()
        except (DataError, IntegrityError, ProgrammingError):
            db_session.rollback()
            raise
        return pm

    def mark_as_read(self):
        self.unread = False
        try:
            db_session.add(self)
            db_session.commit()
        except (DataError, IntegrityError, ProgrammingError):
            db_session.rollback()
            raise

    def sender(self):
        return User.get(self.sender_id)

    def recipient(self):
        return User.get(self.recipient_id)
