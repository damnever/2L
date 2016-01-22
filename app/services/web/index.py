# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from app.base.handlers import BaseHandler


class IndexHandler(BaseHandler):

    def get(self):
        self.render('index.html',
                    #  current_user='Damnever',
                    keywords=None,
                    description=None,
                    title=None)


urls = [(r'/', IndexHandler)]
