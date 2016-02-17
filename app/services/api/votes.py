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
    TopicUpVote, TopicDownVote,
    PostUpVote, PostDownVote,
    CommentUpVote, CommentDownVote,
)


class BaseVoteAPIHandler(APIHandler):
    """
    The following Class attribute(or instance attribute) required:
      table: the table class
      category: POST or COMMENT or what else
      vote_type: UP or DOWN
    """

    def _list_by_category(self, id_):
        return self._cls_method('list_by_')(id_)

    def _get_by_user_category(self, username, id_):
        return self._cls_method('get_by_user_')(username, id_)

    def _count_by_category(self, id_):
        return self._cls_method('count_by_')(id_)

    def _cls_method(self, prefix):
        category = self.category
        return getattr(self.table, prefix + category)

    @as_json
    @gen.coroutine
    def get(self, id_):
        votes = yield gen.maybe_future(self._list_by_category(id_))
        sk = '{0}_votes'.format(self.vote_type.lower())
        result = {
            'total': len(votes),
            sk: [v.to_dict() for v in votes],
        }
        raise gen.Return(result)

    @as_json
    @need_permissions(Roles.Vote)
    @gen.coroutine
    def post(self, id_):
        if self.category == 'topic':
            t = yield gen.maybe_future(Topic.get(id_))
            if t and t.state in (-1, 1):
                raise exceptions.TopicVoteTimeHasPassed()

        username = self.current_user
        v = yield gen.maybe_future(self._get_by_user_category(username, id_))
        if v:
            vote_type = self.vote_type.capitalize()
            exception = getattr(exceptions,
                                'CanNotVote{0}Again'.format(vote_type))
            raise exception()
        else:
            yield gen.maybe_future(self.table.create(username, id_))
            count = yield gen.maybe_future(self._count_by_category(id_))

            # Update gold.
            update_gold.apply_async(
                ('vote', username, id_, self.category, self.vote_type))
            raise gen.Return({'count': count})

    @as_json
    @need_permissions(Roles.Vote)
    @gen.coroutine
    def delete(self, id_):
        if self.category == 'topic':
            t = yield gen.maybe_future(Topic.get(id_))
            if t and t.state in (-1, 1):
                raise exceptions.TopicVoteTimeHasPassed()

        username = self.current_user
        v = yield gen.maybe_future(self._get_by_user_category(username, id_))
        if v:
            yield gen.maybe_future(v.delete())
            count = yield gen.maybe_future(self._count_by_category(id_))
            # Update gold.
            update_gold.apply_async(
                ('cancel_vote', username, id_, self.category, self.vote_type))
            raise gen.Return({'count': count})
        else:
            raise exceptions.NoVoteCanBeCancel()


class TopicUpVoteAPIHandler(BaseVoteAPIHandler):

    table = TopicUpVote
    category = 'topic'
    vote_type = 'up'


class TopicDownVoteAPIHandler(BaseVoteAPIHandler):

    table = TopicDownVote
    category = 'topic'
    vote_type = 'down'


class PostUpVoteAPIHandler(BaseVoteAPIHandler):

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
    # `GET /api/votes/topic/:topic_id/up`, get all up votes of the proposal.
    # For authenticated user:
    #  `topic /api/votes/topic/:topic_id/up`, vote up the topic.
    #  `DELETE /api/votes/topic/:topic_id/down`, cancel up vote of the
    #   topic.
    (r'/api/votes/topic/(\d+)/up', TopicUpVoteAPIHandler),
    # `GET /api/votes/topic/:topic_id/down`, get all down votes of the
    #  topic.
    # For authenticated user:
    #  `topic /api/votes/topic/:topic_id/down`, vote down the topic.
    #  `DELETE /api/votes/topic/:topic_id/down`, cancel down vote of
    #   the topic.
    (r'/api/votes/topic/(\d+)/down', TopicDownVoteAPIHandler),
    # NOTE: post vote include topic creation vote and normal post vote.
    # `GET /api/votes/post/:post_id/up`, get all up votes of the post.
    # For authenticated user:
    #  `POST /api/votes/post/:post_id/up`, vote up the post.
    #  `DELETE /api/votes/post/:post_id/down`, cancel up vote of the
    #   post.
    (r'/api/votes/post/(\d+)/up', PostUpVoteAPIHandler),
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
