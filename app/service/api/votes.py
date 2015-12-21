# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import APIHandler
from app.base.decorators import as_json


class PostUpVoteAPIHanlder(APIHandler):

    @as_json
    def get(self, post_id):
        return 0

    @as_json
    def post(self, post_id):
        pass

    @as_json
    def delete(self, post_id):
        pass


class PostDownVoteAPIHandler(APIHandler):

    @as_json
    def get(self, post_id):
        return 0

    @as_json
    def post(self, post_id):
        pass

    @as_json
    def delete(self, post_id):
        pass


class CommentUpVoteAPIHandler(APIHandler):

    @as_json
    def get(self, comment_id):
        return 0

    @as_json
    def post(self, comment_id):
        pass

    @as_json
    def delete(self, comment_id):
        pass


class CommentDownVoteAPIHandler(APIHandler):

    @as_json
    def get(self, comment_id):
        return 0

    @as_json
    def post(self, comment_id):
        pass

    @as_json
    def delete(self, comment_id):
        pass


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
