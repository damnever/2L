# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json, need_permissions
from app.base.roles import Roles
from app.services.api import exceptions
from app.libs.utils import at_content
from app.tasks.tasks import update_gold, notify
from app.models import (
    Comment,
    CommentUpVote,
    CommentDownVote,
    User,
)


def _comment_info(username, comment):
    info = comment.to_dict()
    up_votes = CommentUpVote.count_by_comment(comment.id)
    down_votes = CommentDownVote.count_by_comment(comment.id)
    avatar = User.get(comment.author_id).profile.avatar
    up_voted, down_voted = False, False
    if username:
        up_voted = CommentUpVote.get_by_user_comment(username, comment.id)
        down_voted = CommentDownVote.get_by_user_comment(username, comment.id)
    info.update({
        'avatar': avatar,
        'up_votes': up_votes,
        'down_votes': down_votes,
        'up_voted': bool(up_voted),
        'down_voted': bool(down_voted),
    })
    return info


class PostCommentsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, post_id):
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('per_page', 20))
        username = self.current_user

        pagination = yield gen.maybe_future(
            Comment.page_list_by_post(post_id, page, per_page))
        comments = list()
        for comment in pagination.items:
            info = yield gen.maybe_future(_comment_info(username, comment))
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
    @gen.coroutine
    def post(self, post_id):
        content = self.get_argument('content', None)

        if content is None:
            raise exceptions.EmptyFields()
        else:
            users, content = at_content(content)
            username = self.current_user
            comment = yield gen.maybe_future(
                Comment.create(username, post_id, content))

            # Update gold.
            update_gold.apply_async(('sb_2l', username, post_id))
            update_gold.apply_async(('comment', username))
            if users:
                update_gold.apply_async(('be_comment', users))

            # TODO: Notify users: be comment, someone @you.
            notify.apply_async(('comment', username, post_id, content))
            if users:
                notify.apply_async(('at', username, users, post_id, content))

            raise gen.Return(comment.to_dict())


class UserCommentsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, username):
        page = int(self.get_argument('page', 1))
        per_page = int(self.get_argument('per_page', 20))
        username = self.current_user

        pagination = yield gen.maybe_future(
            Comment.page_list_by_user(username, page, per_page))
        comments = list()
        for comment in pagination.items:
            info = yield gen.maybe_future(_comment_info(username, comment))
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
