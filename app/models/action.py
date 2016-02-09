# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, DateTime, UniqueConstraint
from sqlalchemy.sql import functions, expression
from sqlalchemy.exc import DataError, IntegrityError, ProgrammingError

from app.models.base import Model
from app.models.user import User
from app.models.content import Topic, Post
from app.libs.db import db_session


class Subscription(Model):

    __table_args__ = (
        UniqueConstraint('user_id', 'topic_id', name='s_usr_tpc'),
    )

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
        try:
            db_session.add(s)
            db_session.commit()
        except (DataError, IntegrityError, ProgrammingError):
            db_session.rollback()
            raise
        return s

    def to_dict(self):
        return {
            'id': self.id,
            'topic': Topic.get(self.topic_id).to_dict(),
            'date': self.date,
        }


class Favorite(Model):

    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='f_usr_pst'),
    )

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
        try:
            db_session.add(f)
            db_session.commit()
        except (DataError, IntegrityError, ProgrammingError):
            db_session.rollback()
            raise
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

    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='up_usr_pst'),
    )

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
        try:
            db_session.add(pu)
            db_session.commit()
        except (DataError, IntegrityError, ProgrammingError):
            db_session.rollback()
            raise
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

    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='dn_usr_pst'),
    )

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
        try:
            db_session.add(pd)
            db_session.commit()
        except (DataError, IntegrityError, ProgrammingError):
            db_session.rollback()
            raise
        return pd


class CommentUpVote(Model):

    __table_args__ = (
        UniqueConstraint('user_id', 'comment_id', name='up_usr_cmt'),
    )

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
        try:
            db_session.add(cu)
            db_session.commit()
        except (DataError, IntegrityError, ProgrammingError):
            cls.rollback()
            raise
        return cu


class CommentDownVote(Model):

    __table_args__ = (
        UniqueConstraint('user_id', 'comment_id', name='dn_usr_cmt'),
    )

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
        try:
            db_session.add(cd)
            db_session.commit()
        except (DataError, IntegrityError, ProgrammingError):
            db_session.rollback()
            raise
        return cd
