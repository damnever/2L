# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr

from app.libs.db import Base, db_session


class MixIn(object):

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

    @classmethod
    def get(cls, id_):
        return cls.query.filter(cls.id==id_).first()

    @classmethod
    def get_multi(cls, *ids):
        return [cls.get(id_) for id_ in ids]

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Model(MixIn, Base):

    __abstract__ = True
    query = db_session.query_property()


class Roles(object):
    # head of the site
    GodFather = 'GodFather'
    Admin = 'Admin'
    Vote = 'Vote'
    User = 'User'
    # Topic administer, such as, the administer of the Python topic
    TopicAdmin = 'Topic:{0}:Admin'
