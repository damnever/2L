# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer


Base = declarative_base()


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


class Model(MixIn, Base):
    pass
