# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import


from app.base.handlers import BaseHandler


class TopicsHandler(BaseHandler):

    def get(self):
        self.render(
            'topics.html',
            title='主题',
            keywords='所有主题, topics',
            description='2L 所有主题',
        )


class TopicHandler(BaseHandler):

    def get(self, topic_id):
        self.render(
            'topic.html',
            title='扯淡',
            keywords='扯淡, 2L',
            description='扯淡，no how，no when，start now.',
            id=1,
            admin='Damnever',
            avatar='/static/2L.png',
            rules='Fuck youself.|Good for everyone.',
        )


class PostHandler(BaseHandler):

    def get(self, post_id):
        self.render(
            'post.html',
            title='古语有云，二楼煞笔',
            keywords='Damnever, 二楼, 煞笔',
            description='古语有云，二楼煞笔',
            author='Damnever',
            avatar='/static/2L.png',
            date='2016-01-06 20:35:23',
            content=('自古二楼出傻逼，想必大家都已经知道了\n---\n'
                     '- 主贴：11区老是争钓鱼岛，天朝到底怎么样才能彻底解决钓鱼岛问题？\n'
                     '- 二楼：操，还犹豫个屁！直接用核武把11区核平了，把小日本炸到太平洋里就解决了。\n'
                     '- 吐槽：自古二楼出傻逼！！'),
        )


urls = [
    (r'/topics', TopicsHandler),
    (r'/topic/(\d+)', TopicHandler),
    (r'/post/(\d+)', PostHandler),
]
