# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json, need_permissions
from app.base.roles import Roles
from app.services.api import exceptions
from app.tasks.tasks import update_gold
from app.models import (
    Topic,
    Post,
    Comment,
    PostUpVote,
    PostDownVote,
    Favorite,
    User,
)


def _post_info(post):
    info = post.to_dict()
    favorites = Favorite.count_by_post(post.id)
    up_votes = PostUpVote.count_by_post(post.id)
    down_votes = PostDownVote.count_by_post(post.id)
    latest_comment = Comment.latest_by_post(post.id)
    comment_count = Comment.count_by_post(post.id)
    if latest_comment:
        latest_comment_user = User.get(latest_comment.author_id).username
        latest_comment_date = latest_comment.date
    else:
        latest_comment_user = None
        latest_comment_date = None
    info.update({
        'up_votes': up_votes,
        'down_votes': down_votes,
        'favorites': favorites,
        'latest_comment_user': latest_comment_user,
        'latest_comment_date': latest_comment_date,
        'comment_count': comment_count,
    })
    return info


class PostsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self):
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('per_page', 20))
        username = self.current_user

        pagination = yield gen.maybe_future(
            Post.page_list(username, page, per_page))
        posts = list()
        for post in pagination.items:
            info = yield gen.maybe_future(_post_info(post))
            posts.append(info)
        result = {
            'page': page,
            'per_page': per_page,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'pages': pagination.pages,
            'total': pagination.total,
            'posts': posts,
        }
        raise gen.Return(result)


class HotPostsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self):
        num = int(self.get_argument('num', 30))

        hots = yield gen.maybe_future(Post.hot_list(num))
        posts = list()
        for post in hots:
            info = yield gen.maybe_future(_post_info(post))
            posts.append(info)
        result = {
            'total': len(posts),
            'posts': posts,
        }
        raise gen.Return(result)


class TopicPostsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, topic_id):
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('per_page', 20))

        pagination = yield gen.maybe_future(
            Post.page_list_by_topic(topic_id, page, per_page))
        posts = list()
        for post in pagination.items:
            info = yield gen.maybe_future(_post_info(post))
            posts.append(info)
        result = {
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
            'posts': posts,
        }
        raise gen.Return(result)

    @as_json
    @need_permissions(Roles.Comment)
    @gen.coroutine
    def post(self, topic_id):
        title = self.get_argument('title', None)
        keywords = self.get_argument('keywords', None)
        content = self.get_argument('content', '')
        keep_silent = bool(self.get_argument('keep_silent', False))
        is_draft = bool(self.get_argument('is_draft', False))

        if not all([title, keywords]):
            raise exceptions.EmptyFields()
        else:
            can_post = yield gen.maybe_future(Topic.can_post(topic_id))
            if not can_post:
                raise exceptions.TopicIsNotAccepted
            exists = yield gen.maybe_future(Post.get_by_title(title))
            if exists:
                raise exceptions.PostTitleAlreadyExists()
            else:
                username = self.current_user
                yield gen.maybe_future(
                    Post.create(username, topic_id,
                                title, keywords, content,
                                keep_silent=keep_silent, is_draft=is_draft))

                # Update gold.
                update_gold.apply_async(('new_post', username))


class UserPostsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, username):
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('per_page', 20))

        pagination = yield gen.maybe_future(
            Post.page_list_by_user(username, page, per_page))
        posts = list()
        for post in pagination.items:
            info = yield gen.maybe_future(_post_info(post))
            posts.append(info)
        result = {
            'page': page,
            'per_page': per_page,
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
        post = yield gen.maybe_future(Post.get(post_id))
        info = yield gen.maybe_future(_post_info(post))
        raise gen.Return(info)

    @as_json
    @need_permissions(Roles.PostEdit)
    @gen.coroutine
    def patch(self, post_id):
        keywords = self.get_argument('keywords', None)
        content = self.get_argument('content', None)
        keep_silent = self.get_argument('keep_silent', None)
        is_draft = self.get_argument('is_draft', None)

        if keywords is None and content is None and keep_silent is None:
            raise exceptions.EmptyFields()
        else:
            post = yield gen.maybe_future(Post.get(post_id))
            yield gen.maybe_future(
                post.update(keywords, content, keep_silent, is_draft))

    @as_json
    @need_permissions(Roles.PostEdit)
    @gen.coroutine
    def delete(self, post_id):
        p = yield gen.maybe_future(Post.get(post_id))
        yield gen.maybe_future(p.delete())

        # Update gold.
        update_gold.apply_async(('delete_post', self.current_user))


urls = [
    # `GET /api/posts/all`, get all posts.
    (r'/api/posts/all', PostsAPIHandler),
    # `GET /api/posts/hot`, get hot posts.
    (r'/api/posts/hot', HotPostsAPIHandler),
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
