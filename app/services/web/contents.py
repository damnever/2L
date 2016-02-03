# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from tornado import gen

from app.base.handlers import BaseHandler
from app.models import Topic, User


class TopicsHandler(BaseHandler):

    def get(self):
        self.render(
            'topics.html',
            title='主题',
            keywords='所有主题, topics',
            description='2L 所有主题',
        )


class TopicHandler(BaseHandler):

    @gen.coroutine
    def get(self, topic_id):
        topic = yield self.async_task(Topic.get, topic_id)
        admin = yield self.async_task(User.get, topic.admin_id)
        self.render(
            'topic.html',
            title=topic.name,
            keywords=topic.name + ', 2L',
            description=topic.description,
            id=topic_id,
            admin=admin.username,
            avatar=topic.avatar,
            rules=topic.rules,
        )


class PostHandler(BaseHandler):

    def get(self, post_id):
        self.render(
            'post.html',
            title='古语有云，二楼煞笔',
            keywords='Damnever, 二楼, 煞笔',
            description='古语有云，二楼煞笔',
            topic_id=1,
            post_id=post_id,
            author='Damnever',
            avatar='/static/2L.png',
            date='2016-01-06 20:35:23',
            content='''自古二楼出傻逼，想必大家都已经知道了:

- 主贴：11区老是争钓鱼岛，天朝到底怎么样才能彻底解决钓鱼岛问题？
- 二楼：操，还犹豫个屁！直接用核武把11区核平了，把小日本炸到太平洋里就解决了。
- 吐槽：自古二楼出傻逼！！

```python
from __future__ import print_function

print("Python is the best language!")
```

![picture](http://127.0.0.1:8888/static/2L.png)
'''
        )


class TopicEditHandler(BaseHandler):

    @gen.coroutine
    def get(self, topic_id):
        topic = yield self.async_task(Topic.get, topic_id)
        admin = yield self.async_task(User.get, topic.admin_id)
        self.render('newpost.html',
                    title=topic.name,
                    keywords=topic.name + ', 2L',
                    description=topic.description,
                    topic_id=topic_id,
                    rules=topic.rules,
                    admin=admin.username,
                    avatar=topic.avatar)


urls = [
    (r'/topics', TopicsHandler),
    (r'/topic/(\d+)', TopicHandler),
    (r'/post/(\d+)', PostHandler),
    (r'/topic/(\d+)/new/post', TopicEditHandler),
]
