# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from celery import Celery
from tzlocal import get_localzone

from app.settings import Redis


BROKER_URL = 'redis://:{password}@{host}:{port}/{db}'.format(**Redis['task'])

app = Celery('2L', broker=BROKER_URL, include=['app.tasks.tasks'])


app.conf.update(
    CELERY_TIMEZONE=get_localzone(),
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json', 'yaml'],
)


if __name__ == '__main__':
    app.start()
