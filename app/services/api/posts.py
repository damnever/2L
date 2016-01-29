# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json, authenticated, need_permissions
from app.base.roles import Roles
from app.services.api import exceptions
from app.models import Post, Comment, PostUpVote, PostDownVote, Favorite


def _post_info(post):
    info = post.to_dict()
    comments = Comment.count_by_post(post.id)
    favorites = Favorite.count_by_post(post.id)
    up_votes = PostUpVote.count_by_post(post.id)
    down_votes = PostDownVote.count_by_post(post.id)
    info.update({
        'up_votes': up_votes,
        'down_votes': down_votes,
        'favorites': favorites,
        'comments': comments,
        'comments_url': '/api/comments/post/{0}'.format(post.id),
    })
    return info


class PostsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, hot):
        if hot:
            pass
        else:
            page = self.get_argument('page', 1)
            per_page = self.get_argument('per_page', 20)
            pagination = yield self.async_task(Post.page_list, page, per_page)
            posts = list()
            for post in pagination.items:
                info = yield self.async_task(_post_info, post)
                posts.append(info)
            result = {
                'page': page,
                'has_prev': pagination.has_prev,
                'has_next': pagination.has_next,
                'pages': pagination.pages,
                'total': pagination.total,
                'posts': posts,
            }
            raise gen.Return(result)


class TopicPostsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, topic_id):
        page = self.get_argument('page', 1)
        per_page = self.get_argument('per_page', 20)
        pagination = yield self.async_task(Post.page_list_by_topic,
                                           topic_id, page, per_page)
        posts = list()
        for post in pagination.items:
            info = yield self.async_task(_post_info, post)
            pagination.append(info)
        result = {
            'page': page,
            'pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
            'posts': posts,
        }
        raise gen.Return(result)

    @as_json
    @need_permissions(Roles.Comment)
    @authenticated
    @gen.coroutine
    def post(self, topic_id):
        title = self.get_argument('title', None)
        keywords = self.get_argument('keywords', None)
        content = self.get_argument('content', '')
        keep_silent = self.get_argument('keep_silent', False)

        if title is None or keywords is None:
            raise exceptions.EmptyFields()
        else:
            exists = yield self.async_task(Post.get_by_title, title)
            if exists:
                raise exceptions.PostTitleAlreadyExists()
            else:
                username = self.current_user
                yield self.async_task(
                    Post.create, username, topic_id, title,
                    keywords, content, keep_silent=keep_silent)


class UserPostsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, username):
        page = self.get_argument('page', 1)
        per_page = self.get_argument('per_page', 20)
        pagination = yield gen.async_task(Post.page_list_by_user,
                                          username, page, per_page)
        posts = list()
        for post in pagination.items:
            info = yield self.async_task(_post_info, post)
            posts.append(info)
        result = {
            'page': page,
            'pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
            'posts': posts,
        }
        raise gen.Return(result)


class PostAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, post_id):
        post = yield self.async_task(Post.get, post_id)
        info = yield self.async_task(_post_info, post)
        raise gen.Return(info)

    @as_json
    @need_permissions(Roles.PostEdit)
    @authenticated
    @gen.coroutine
    def patch(self, post_id):
        keywords = self.get_argument('keywords', None)
        content = self.get_argument('content', None)
        keep_silent = self.get_argument('keep_silent', None)

        if keywords is None and content is None and keep_silent is None:
            raise exceptions.EmptyFields()
        else:
            post = yield self.async_task(Post.get, post_id)
            yield self.async_task(post.update, keywords, content, keep_silent)

    @as_json
    @need_permissions(Roles.PostEdit)
    @authenticated
    @gen.coroutine
    def delete(self, post_id):
        p = yield self.async_task(Post.get, post_id)
        yield self.async_task(p.delete)


urls = [
    # `GET /api/posts/all`, get all posts.
    # `GET /api/posts/hot`, get hot posts.
    (r'/api/posts/(w+)', PostsAPIHandler),
    # `GET /api/posts/topic/:topic_id`, get all posts of the topic.
    # For authenticated user:
    #  `POST /api/posts/topic/:topic_id`, create a new post for
    #   the topic.
    (r'/api/posts/topic/(\d+)', TopicPostsAPIHandler),
    # `GET /api/posts/topic/:username, get all posts of the user.
    (r'/api/posts/user/(\w+)', UserPostsAPIHandler),
    # `GET /api/posts/post/:post_id`, get information of the post.
    # For the post owner:
    #  `PATCH /api/posts/post/:post_id`, update information of the post.
    #  `DELETE /api/posts/post/:post_id`, delete the post.
    (r'/api/posts/post/(\d+)', PostAPIHandler),
]
