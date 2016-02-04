# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import functions, expression

from app.models.base import Model
from app.models.user import User
from app.libs.db import db_session


class Topic(Model):
    name = Column('name', String(30), unique=True, nullable=False)
    admin_id = Column('admin_id', Integer(), default=1)
    avatar = Column('avatar', String(100), nullable=False)
    description = Column('description', String(420), nullable=False)
    rules = Column('rules', Text(), nullable=False)

    @classmethod
    def list_all(cls):
        return cls.query.all()

    @classmethod
    def list_by_user(cls, username):
        user = User.get_by_name(username)
        return cls.query.filter(cls.admin_id==user.id).all()

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter(cls.name==name).first()

    @classmethod
    def create(cls, name, created_name, avatar, description, rules):
        user = User.get_by_name(created_name)
        t = Topic(name=name, admin_id=user.id, avatar=avatar,
                  description=description, rules=rules)
        db_session.add(t)
        db_session.commit()
        return t

    def update(self, description=None, rules=None, avatar=None):
        if description:
            self.description = description
        if rules:
            self.rules = rules
        db_session.add(self)
        db_session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'avatar': self.avatar,
            'administer': self.administer.username,
            'description': self.description,
            'rules': self.rules,
        }

    @property
    def administer(self):
        return User.get(self.admin_id)


class Post(Model):
    topic_id = Column('topic_id', Integer(), index=True, nullable=False)
    author_id = Column('author_id', Integer(), index=True, nullable=False)
    title = Column('title', String(120), unique=True, nullable=False)
    created_date = Column('created_date', DateTime(timezone=True),
                          default=functions.now())
    update_date = Column('update_date', DateTime(timezone=True),
                         default=functions.now(), onupdate=functions.now())
    comment_date = Column('comment_date', DateTime(timezone=True),
                          default=functions.now())
    keywords = Column('keywords', String(120), nullable=False)
    content = Column('content', Text(), default='')
    keep_silent = Column('keep_silent', Boolean(), default=False)
    is_draft = Column('is_draft', Boolean(), default=False)

    @classmethod
    def get_by_title(cls, title):
        return cls.query.filter(cls.title==title).first()

    @classmethod
    def page_list(cls, page, per_page):
        q = cls.query.order_by(expression.desc(cls.comment_date))
        return q.paginate(page, per_page)

    @classmethod
    def page_list_by_user(cls, username, page, per_page):
        user = User.get_by_name(username)
        q = cls.query.filter(cls.author_id==user.id).order_by(
            expression.desc(cls.comment_date))
        return q.paginate(page, per_page)

    @classmethod
    def page_list_by_topic(cls, topic_id, page, per_page):
        q = cls.query.filter(cls.topic_id==topic_id).order_by(
            expression.desc(cls.comment_date))
        return q.paginate(page, per_page)

    @classmethod
    def create(cls, author_name, topic_id, title, keywords,
               content='', keep_silent=False, is_draft=False):
        p = cls(
            topic_id=topic_id,
            author_id=User.get_by_name(author_name).id,
            title=title,
            keywords=keywords,
            content=content,
            keep_silent=keep_silent,
            is_draft=is_draft,
        )
        db_session.add(p)
        db_session.commit()
        return p

    def update(self, keywords=None, content=None,
               keep_silent=None, is_draft=None):
        if keywords:
            self.keywords = keywords
        if content:
            self.content = content
        if keep_silent:
            self.keep_silent = keep_silent
        if is_draft:
            self.is_draft = is_draft
        db_session.add(self)
        db_session.commit()

    def to_dict(self):
        latest_comment = Comment.latest_by_post(self.id)
        comment_count = Comment.count_by_post(self.id)
        if latest_comment:
            latest_comment_user = User.get(latest_comment.author_id).username
            latest_comment_date = latest_comment.date
        else:
            latest_comment_user = None
            latest_comment_date = None
        return {
            'id': self.id,
            'author_name': self.author.username,
            'author_avatar': self.author.profile.avatar,
            'topic_id': self.topic_id,
            'topic_name': self.topic.name,
            'title': self.title,
            'keywords': self.keywords,
            'content': self.content,
            'keep_silent': self.keep_silent,
            'created_date': self.created_date,
            'update_date': self.update_date,
            'latest_comment_user': latest_comment_user,
            'latest_comment_date': latest_comment_date,
            'comment_count': comment_count,
        }

    def _new_comment(self, now):
        self.comment_date = now
        db_session.add(self)

    @property
    def author(self):
        return User.get(self.author_id)

    @property
    def topic(self):
        return Topic.get(self.topic_id)


class Comment(Model):
    post_id = Column('post_id', Integer(), index=True, nullable=False)
    author_id = Column('author_id', Integer(), index=True, nullable=False)
    date = Column('date', DateTime(timezone=True), default=functions.now())
    content = Column('content', Text(), nullable=False)

    @classmethod
    def latest_by_post(cls, post_id):
        cs = cls.query.filter(cls.post_id==post_id).order_by(
            expression.desc(cls.date)).limit(1)
        return cs.first()

    @classmethod
    def page_list(cls, page, per_page):
        p = cls.query.order_by(expression.asc(cls.date))
        return p.paginate(page, per_page)

    @classmethod
    def count_by_user(cls, username):
        user = User.get_by_name(username)
        return cls.query.filter(cls.author_id==user.id).count()

    @classmethod
    def count_by_post(cls, post_id):
        return cls.query.filter(cls.post_id==post_id).count()

    @classmethod
    def page_list_by_user(cls, username, page, per_page):
        user = User.get_by_name(username)
        p = cls.query.order_by(
            expression.asc(cls.date)).filter(cls.author_id==user.id)
        return p.paginate(page, per_page)

    @classmethod
    def page_list_by_post(cls, post_id, page, per_page):
        p = cls.query.order_by(
            expression.asc(cls.date)).filter(cls.post_id==post_id)
        return p.paginate(page, per_page)

    @classmethod
    def create(cls, author_name, post_id, content):
        user = User.get_by_name(author_name)
        now = functions.now()
        Post.get(post_id)._new_comment(now)
        c = cls(author_id=user.id, post_id=post_id, content=content, date=now)
        db_session.add(c)
        db_session.commit()
        return c

    def update(self, content):
        self.content = content
        db_session.add(self)
        db_session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author.username,
            'date': self.date,
            'content': self.content,
        }

    @property
    def author(self):
        return User.get(self.author_id)

    @property
    def post(self):
        return Post.get(self.post_id)
