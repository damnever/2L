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


class LatestPostsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self):
        posts = yield gen.maybe_future(Post.list_all())
        infos = list()
        for post in posts:
            info = yield gen.maybe_future(_post_info(post))
            infos.append(info)
        result = {
            'total': len(posts),
            'posts': infos,
        }
        raise gen.Return(result)


class TopicPostsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, topic_id):
        posts = yield gen.maybe_future(Post.list_by_topic(topic_id))
        result = {
            'total': len(posts),
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
            exists = yield gen.maybe_future(Post.get_by_title(title))
            if exists:
                raise exceptions.PostTitleAlreadyExists()
            else:
                username = self.current_user
                yield gen.maybe_future(
                    Post.create(username, topic_id, title, keywords,
                                content, keep_silent=keep_silent))


class UserPostsAPIHandler(APIHandler):

    @as_json
    @gen.coroutine
    def get(self, username):
        posts = yield gen.maybe_future(Post.list_by_user(username))
        infos = list()
        for post in posts:
            info = yield gen.maybe_future(_post_info(post))
            infos.append(info)
        result = {
            'total': len(posts),
            'posts': infos,
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
    @authenticated
    @gen.coroutine
    def patch(self, post_id):
        keywords = self.get_argument('keywords', None)
        content = self.get_argument('content', None)
        keep_silent = self.get_argument('keep_silent', None)

        if keywords is None and content is None and keep_silent is None:
            raise exceptions.EmptyFields()
        else:
            post = yield gen.maybe_future(Post.get(post_id))
            yield gen.maybe_future(post.update(keywords, content, keep_silent))

    @as_json
    @need_permissions(Roles.PostEdit)
    @authenticated
    @gen.coroutine
    def delete(self, post_id):
        yield gen.maybe_future(Post.get(post_id).delete())


urls = [
    # `GET /api/posts/latest`, get all latest posts.
    (r'/api/posts/latest', LatestPostsAPIHandler),
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
