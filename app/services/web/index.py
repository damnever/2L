# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import BaseHandler
from app.base.decorators import authenticated


class IndexHandler(BaseHandler):

    def get(self):
        self.render('index.html',
                    #  current_user='Damnever',
                    keywords=None,
                    description=None,
                    title=None)


class HotHandler(BaseHandler):

    def get(self):
        self.render('hot.html',
                    keywords=None,
                    description=None,
                    title="最热")


class TopicsHandler(BaseHandler):

    def get(self):
        self.render(
            'topics.html',
            title='主题',
            keywords='所有主题, topics',
            description='2L 所有主题',
        )


class ProposalHandler(BaseHandler):

    def get(self):
        self.render('proposals.html',
                    title='我要',
                    keywords='我要, 2L',
                    description=('如果在 2L 没有找到相关的主题，'
                                 '你可以在此发帖表达想要创建主题的意愿。'),
                    rules=('请注明新主题名称\n请注明新主题相关的描述信息\n'
                           '请注明新主题的发帖规则'))


class NotificationsHandler(BaseHandler):

    @authenticated
    def get(self, username):
        self.render('notifications.html',
                    title='通知',
                    description='通知',
                    keywords='通知')


urls = [
    (r'/', IndexHandler),
    (r'/hot', HotHandler),
    (r'/topics', TopicsHandler),
    (r'/proposal', ProposalHandler),
    (r'/notifications/(\w+)', NotificationsHandler),
]
