# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, String, event
from sqlalchemy.sql import select, functions
from sqlalchemy.orm import load_only

from app.models.base import Model


class Permission(Model):
    bit = Column('number', Integer, index=True)
    role = Column('role', String(24), index=True, nullable=False)

    @classmethod
    def get_by_role(cls, role):
        r = cls.query.options(load_only('bit')).filter(cls.role==role)
        return r.first()


@event.listens_for(Permission, 'before_insert')
def bit_generater(mapper, connection, target):
    # SELECT max(bit) as max_bit from permission
    # bit = max_bit << 1
    s = select([functions.max(Permission.bit).label('max_bit')])
    result = connection.execute(s).fetchone()
    target.bit = (result.max_bit << 1) if result.max_bit else 1
