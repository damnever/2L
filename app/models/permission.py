# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, String, event
from sqlalchemy.sql import select, functions
from sqlalchemy.exc import DataError, IntegrityError, ProgrammingError

from app.base.roles import Roles
from app.models.base import Model
from app.libs.db import db_session


class Permission(Model):
    bit = Column('number', Integer)
    role = Column('role', String(24), index=True, nullable=False)

    @classmethod
    def root_permission(cls):
        r = cls.query.with_entities(functions.sum(Permission.bit).label('a'))
        return r.first().a

    @classmethod
    def get_by_role(cls, role):
        r = cls.query.with_entities(cls.bit).filter(cls.role==role)
        return r.first()

    @classmethod
    def create(cls, role):
        p = cls(role=role)
        try:
            db_session.add(p)
            db_session.commit()
        except (DataError, IntegrityError, ProgrammingError):
            db_session.rollback()
            raise
        return p


@event.listens_for(Permission, 'before_insert')
def bit_generater(mapper, connection, target):
    # SELECT max(bit) as max_bit from permission
    # bit = max_bit << 1
    s = select([functions.max(Permission.bit).label('max_bit')])
    result = connection.execute(s).fetchone()
    target.bit = (result.max_bit << 1) if result.max_bit else 1


@event.listens_for(Permission, 'after_insert')
def update_permission(mapper, connection, target):
    from app.models import User
    print('UPDATE PERMISSION')
    for user in User.list_all():
        if any(map(user.has_permission, [Roles.Root, Roles.Admin])):
            user.role |= target.bit
            print('PERMISSION: {0} -> {1}'.format(target.bit, user.role))
            db_session.add(user)
