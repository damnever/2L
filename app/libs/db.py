# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

import math
import functools

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import DataError, IntegrityError, ProgrammingError

from app.settings import MySQL, ThreadPoolMaxWorkers


class Pagination(object):
    """
    Borrow from: flask_sqlalchemy
    Internal helper class returned by `BaseQuery.paginate`.  You
    can also construct it from any other SQLAlchemy query object if
    you are working with other libraries. Additionally it is possible
    to pass `None` as query object in which case the `prev` and `next`
    will no longer work.
    """

    def __init__(self, query, page, per_page, total, items):
        # the unlimited query object that was used to create
        # this pagination object.
        self.query = query
        # the current page number, 1 indexed.
        self.page = page
        # the number of items to be displayed on a page.
        self.per_page = per_page
        # the total number of items match the query.
        self.total = total
        # the items for the current page.
        self.items = items

    @property
    def pages(self):
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(math.ceil(self.total / self.per_page))
        return pages

    def prev(self):
        """Return a `Pagination` object for the previous page."""
        return self.query.paginate(self.page - 1, self.per_page)

    @property
    def prev_num(self):
        """Number of the previous page."""
        return self.page - 1

    @property
    def has_prev(self):
        """True if previous page exists."""
        return self.page > 1

    def next(self):
        """Returns a Pagination object for the next page."""
        return self.query.paginate(self.page + 1, self.per_page)

    @property
    def has_next(self):
        """True if next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page."""
        return self.page + 1


class BaseQuery(Query):

    def paginate(self, page=None, per_page=None):
        """Returns `per_page` items from page `page`."""
        page = page or 1
        per_page = per_page or 20

        items = self.limit(per_page).offset((page - 1) * per_page).all()
        if not items and page != 1:
            return None
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = self.order_by(None).count()

        return Pagination(self, page, per_page, total, items)


class Scope(object):

    pass


url = ('mysql://{username}:{password}@{host}:{port}/{db}'
       '?charset=utf8').format(**MySQL)
engine = create_engine(url, pool_size=ThreadPoolMaxWorkers,
                       pool_recycle=3600, echo=True)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        query_cls=BaseQuery
    )
)

Base = declarative_base()


def ping_db():
    db_session.excute('show variables')


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.
    # from app.models import *
    _engine = create_engine(url.rsplit('/', 1)[0], echo=True)
    _engine.execute('CREATE DATABASE IF NOT EXISTS {0}'.format(MySQL['db']))
    Base.metadata.create_all(bind=engine)


def drop_db():
    _engine = create_engine(url.rsplit('/', 1)[0], echo=True)
    _engine.execute('DROP DATABASE IF EXISTS {0}'.format(MySQL['db']))


def shutdown_session():
    db_session.remove()


def catch_integrity_errors(session):
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(self, *args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (DataError, IntegrityError, ProgrammingError) as e:
                print(e)
                session.rollback()
        return _wrapper
