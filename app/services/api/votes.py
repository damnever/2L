# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json, authenticated, need_permissions
from app.base.roles import Roles
from app.models import PostUpVote, PostDownVote, CommentUpVote, CommentDownVote
from app.services.api import exceptions


class BaseVoteAPIHandler(APIHandler):
    """
    The following Class attribute(or instance attribute) required:
      table: the table class
      category: POST or COMMENT or what else
      vote_type: UP or DOWN
    """

    def _list_by_category(self, id_):
        category = self.category.lower()
        clsmethod = getattr(self.table, 'list_by_{0}'.format(category))
        return clsmethod(self.table, id_)

    def _get_by_user_category(self, username, id_):
        category = self.category.lower()
        clsmethod = getattr(self.table, 'get_by_user_{0}'.format(category))
        return clsmethod(self.table, username, id_)

    @as_json
    @gen.coroutine
    def get(self, id_):
        votes = yield self.async_task(self._list_by_category, id_)
        sk = '{0}_votes'.format(self.vote_type.lower())
        result = {
            'total': len(votes),
            sk: [v.to_dict() for v in votes],
        }
        raise gen.Return(result)

    @as_json
    @need_permissions(Roles.Vote)
    @authenticated
    @gen.coroutine
    def post(self, id_):
        username = self.current_user
        v = yield self.async_task(self._get_by_user_category, username, id_)
        if v:
            vote_type = self.vote_type.capitalize()
            exception = getattr(exceptions,
                                'CanNotVote{0}Again'.format(vote_type))
            raise exception()
        else:
            yield self.async_task(self.table.create, username, id_)

    @as_json
    @need_permissions(Roles.Vote)
    @authenticated
    @gen.coroutine
    def delete(self, id_):
        username = self.current_user
        v = yield self.async_task(self._get_by_user_category, username, id_)
        if v:
            yield self.async_task(v.delete)
        else:
            raise exceptions.NoVoteCanBeCancel()


class PostUpVoteAPIHanlder(BaseVoteAPIHandler):

    table = PostUpVote
    category = 'post'
    vote_type = 'up'


class PostDownVoteAPIHandler(BaseVoteAPIHandler):

    table = PostDownVote
    category = 'post'
    vote_type = 'down'


class CommentUpVoteAPIHandler(BaseVoteAPIHandler):

    table = CommentUpVote
    category = 'comment'
    vote_type = 'up'


class CommentDownVoteAPIHandler(BaseVoteAPIHandler):

    table = CommentDownVote
    category = 'comment'
    vote_type = 'down'


urls = [
    # NOTE: post vote include topic creation vote and normal post vote.
    # `GET /api/votes/post/:post_id/up`, get all up votes of the post.
    # For authenticated user:
    #  `POST /api/votes/post/:post_id/up`, vote up the post.
    #  `DELETE /api/votes/post/:post_id/down`, cancel up vote of the
    #   post.
    (r'/api/votes/post/(\d+)/up', PostUpVoteAPIHanlder),
    # `GET /api/votes/post/:post_id/down`, get all down votes of the
    #  post.
    # For authenticated user:
    #  `POST /api/votes/post/:post_id/down`, vote down the post.
    #  `DELETE /api/votes/post/:post_id/down`, cancel down vote of
    #   the post.
    (r'/api/votes/post/(\d+)/down', PostDownVoteAPIHandler),
    # `GET /api/votes/comment/:comment_id/up`, get all up votes of
    #  the comment.
    # For authenticated user:
    #  `comment /api/votes/comment/:comment_id/up`, vote up the
    #   comment.
    #  `DELETE /api/votes/comment/:comment_id/down`, cancel up
    #   vote of the comment.
    (r'/api/votes/comment/(\d+)/up', CommentUpVoteAPIHandler),
    # `GET /api/votes/comment/:comment_id/down`, get all down votes
    #  of the comment.
    # For authenticated user:
    #  `comment /api/votes/comment/:comment_id/down`, vote down the
    #   comment.
    #  `DELETE /api/votes/comment/:comment_id/down`, cancel down vote
    #   of the comment.
    (r'/api/votes/comment/(\d+)/down', CommentDownVoteAPIHandler),
]
