# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json, authenticated, need_permissions
from app.base.roles import Roles
from app.models import Comment, CommentUpVote, CommentDownVote
from app.services.api import exceptions


def _comment_info(comment):
    info = comment.to_dict()
    up_votes = CommentUpVote.count_by_comment(comment.id)
    down_votes = CommentDownVote.count_by_comment(comment.id)
    info.update({
        'up_votes': up_votes,
        'down_votes': down_votes,
    })
    return info


class PostCommentsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, post_id):
        page = self.get_argument('page', 1)
        per_page = self.get_argument('per_page', 20)
        pagination = yield gen.maybe_future(
            Comment.page_list_by_post(post_id, page, per_page))
        comments = list()
        for comment in pagination.items:
            info = yield gen.maybe_future(_comment_info(comment))
            comments.append(info)
        result = {
            'page': page,
            'pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
            'comments': comments,
        }
        raise gen.Return(result)

    @as_json
    @need_permissions(Roles.Comment)
    @authenticated
    @gen.coroutine
    def post(self, post_id):
        content = self.get_argument('content', None)

        if content is None:
            raise exceptions.EmptyFields()
        else:
            username = self.current_user
            yield gen.maybe_future(Comment.create(username, post_id, content))


class UserCommentsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, username):
        page = self.get_argument('page', 1)
        per_page = self.get_argument('per_page', 20)
        pagination = yield gen.maybe_future(
            Comment.page_list_by_user(username, page, per_page))
        comments = list()
        for comment in pagination.items:
            info = yield gen.maybe_future(_comment_info(comment))
            comments.append(info)
        result = {
            'page': page,
            'pages': pagination.pages,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'total': pagination.total,
            'comments': comments,
        }
        raise gen.Return(result)


urls = [
    # NOTE: comment can not be modified and deleted...
    # `GET /api/comments/post/:post_id`, get all comments of the post.
    # For authenticated user:
    #   `POST /api/comments/post/:post_id`, add a new comments to post.
    (r'/api/comments/post/(\d+)', PostCommentsAPIHandler),
    # `GET /api/comments/user/:username`, get all comments of the user.
    (r'/api/comments/user/(\w+)', UserCommentsAPIHandler),
]
