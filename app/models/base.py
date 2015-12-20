# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer




class _Base(object):

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
    }

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def id(cls):
        return Column('id', Integer(), primary_key=True, autoincrement=True)


Base = declarative_base(cls=_Base)
Model = Base


class Roles(object):
    # head of the site
    GodFather = 'GodFather'
    Admin = 'Admin'
    Vote = 'Vote'
    User = 'User'
    # Topic administer, such as, the administer of the Python topic
    TopicAdmin = 'Topic:{0}:Admin'

