# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.settings import MySQL


url = 'mysql://{username}:{password}@{host}:{port}/{db}'.format(**MySQL)
engine = create_engine(url, echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.
    from app.models import *
    Base.metadata.create_all(bind=engine)


def drop_db():
    from app.models import *
    Base.metadata.drop_all(bind=engine)


def shutdown_session():
    db_session.remove()
