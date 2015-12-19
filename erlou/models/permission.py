# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, String, event
from sqlalchemy.sql import select, functions

from .base import Model


class Roles(object):
    # head of the site
    GodFather = 'GodFather'
    Admin = 'Admin'
    User = 'User'
    # Topic administer, such as, the administer of the Python topic
    TopicAdmin = 'Topic:{0}:Admin'


class Permission(Model):
    bit = Column('number', Integer, index=True)
    role = Column('role', String(24), index=True, nullable=False)


@event.listens_for(Permission, 'before_insert')
def bit_generater(mapper, connection, target):
    # SELECT max(bit) as max_bit from permission
    # bit = max_bit << 1
    s = select([functions.max(Permission.bit).label('max_bit')])
    result = connection.execute(s).fetchone()
    target.bit = (result.max_bit << 1) if result.max_bit else 1
