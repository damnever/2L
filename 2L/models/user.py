# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import Model


class User(Model):
    username = Column('username', String(24), index=True, unique=True, nullable=False)
    password = Column('password', String(20), nullable=False)
    email = Column('email', String(100), unique=True, default='')
    role = Column('role', Integer(), nullable=False)
    profile = relationship('Profile', uselist=False, back_populates='user')


class Profile(Model):
    user_id = Column('user_id', Integer(), ForeignKey('user.id'))
    gold = Column('gold', Integer(), index=True, nullable=False)
    introduce = Column('introduce', Text(300))
    avatar = Column('avatar', String(100))
    location = Column('location', String(120))
    wiki = Column('wiki', Text())
    blog = Column('blog', String(100))
    github = Column('github', String(100))
    google = Column('google', String(100))
    weibo = Column('weibo', String(100))
    twitter = Column('twitter', String(100))


class Followers(Model):
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    follower_id = Column('follower_id', Integer(), index=True, nullable=False)


class Blocked(Model):
    user_id = Column('user_id', Integer(), index=True, nullable=False)
    blocked_id = Column('blocked_id', Integer(), index=True, nullable=False)
