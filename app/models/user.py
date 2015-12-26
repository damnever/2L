# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, expression
from sqlalchemy.sql import functions

from app.models.base import Model
from app.models.permission import Permission
from app.libs.db import db_session


class User(Model):
    username = Column('username', String(24), index=True,
                      unique=True, nullable=False)
    password = Column('password', String(20), nullable=False)
    email = Column('email', String(100), unique=True, default='')
    role = Column('role', Integer(), nullable=False)
    profile = relationship('Profile', uselist=False, back_populates='user')

    @classmethod
    def get_by_name(cls, username):
        return cls.query.filter(cls.username==username).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(cls.email==email).first()

    @classmethod
    def create(cls, **kwargs):
        user_attrs = dict()
        profile_attrs = dict()
        for k, v in kwargs.items():
            if hasattr(cls, k):
                user_attrs[k] = v
            elif hasattr(Profile, k):
                profile_attrs[k] = v
        profile = Profile(**profile_attrs)
        user_attrs.update({'profile': profile})
        user = cls(**user_attrs)
        db_session.add(user)
        db_session.add(profile)
        db_session.commit()

    def delete(self):
        db_session.delete(self.profile)
        db_session.delete(self)
        db_session.commit()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
            elif hasattr(self.profile, k):
                setattr(self.profile, k, v)
        db_session.add(self)
        db_session.commit()

    def has_permission(self, role):
        return self.query.filter(self.role&Permission.get_by_role(role))

    def permissions(self):
        r = self.query.join(Permission).filter(
                self.role&Permission.bit).filter(self.__class__.id==self.id)
        return r.all()

    def information(self):
        info = {
            'id': self.id,
            'username': self.username,
            'role': self.permissions(),
            'gold': self.profile.gold,
            'intorduce': self.profile.join_date,
            'avatar': self.profile.avatar,
            'location': self.profile.avatar,
            'wiki': self.profile.wiki,
            'blog': self.profile.blog,
            'github': self.profile.github,
            'google': self.profile.google,
            'weibo': self.profile.weibo,
            'twitter': self.profile.twitter,
        }
        return info

    def following_count(self):
        return Following.get_count_by_userid(self.id)

    def blocked_count(self):
        return Blocked.get_count_by_userid(self.id)


class Profile(Model):
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    gold = Column('gold', Integer(), index=True, nullable=False, default=50)
    join_date = Column('join_date', DateTime(timezone=True),
                       default=functions.now())
    introduce = Column('introduce', Text(300), default='You know, 2L~')
    avatar = Column('avatar', String(100))
    location = Column('location', String(120), default='Earth')
    wiki = Column('wiki', Text(), default='')
    blog = Column('blog', String(100), default='')
    github = Column('github', String(100), default='')
    google = Column('google', String(100), default='')
    weibo = Column('weibo', String(100), default='')
    twitter = Column('twitter', String(100), default='')


class Following(Model):
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    following_id = Column('following_id', Integer(), index=True, nullable=False)

    @classmethod
    def list_following(cls, username):
        user = User.get_by_name(username)
        return cls.query.with_entities(
            cls.following_id).filter(cls.user_id==user.id)

    @classmethod
    def create(cls, username, following_name):
        user = User.get_by_name(username)
        following = User.get_by_name(following_name)
        f = Following(user_id=user.id, following_id=following.id)
        db_session.add(f)
        db_session.commit()

    @classmethod
    def get_by_user_following(cls, username, following_name):
        user = User.get_by_name(username)
        following = User.get_by_name(following_name)
        r = cls.query.filter(expression.and_(cls.user_id==user.id,
                                             cls.following_id==following.id))
        return r.first()


class Blocked(Model):
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    blocked_id = Column('blocked_id', Integer(), index=True, nullable=False)

    @classmethod
    def list_blocked(cls, username):
        user = User.get_by_name(username)
        return cls.query.with_entities(
            cls.blocked_id).filter(cls.user_id==user.id)

    @classmethod
    def create(cls, username, blocked_name):
        user = User.get_by_name(username)
        blocked = User.get_by_name(blocked_name)
        f = Blocked(user_id=user.id, blocked_id=blocked.id)
        db_session.add(f)
        db_session.commit()

    @classmethod
    def get_by_user_blocked(cls, username, blocked_name):
        user = User.get_by_name(username)
        blocked = User.get_by_name(blocked_name)
        r = cls.query.filter(expression.and_(cls.user_id==user.id,
                                             cls.blocked_id==blocked.id))
        return r.first()
