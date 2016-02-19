# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import APIHandler
from app.base.decorators import as_json, authenticated
from app.cache import gold
from app.libs.random_gold import random_gold
from app.services.api import exceptions
from app.models import User


class RobGoldAPIHandler(APIHandler):

    @as_json
    @authenticated
    @gen.coroutine
    def post(self):
        username = self.current_user

        robed = gold.get(username, random_gold)
        if robed == -1:
            raise exceptions.CanNotRobAgain()
        elif robed == 0:
            raise exceptions.NoMoreGoldToday()
        user = yield gen.maybe_future(User.get_by_name(username))
        yield gen.maybe_future(user.update(gold=robed))
        raise gen.Return({'gold': robed})


urls = [
    (r'/rob/gold', RobGoldAPIHandler),
]
