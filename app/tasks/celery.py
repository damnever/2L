# -*- coding: utf-8 -*-

from __future__ import print_function, division, absolute_import

from celery import Celery
from celery.schedules import crontab
from tzlocal import get_localzone

from app.settings import Redis, ResetGoldTime


BROKER_URL = 'redis://:{password}@{host}:{port}/{db}'.format(**Redis['task'])

app = Celery('2L', broker=BROKER_URL, include=['app.tasks.tasks'])


app.conf.update(
    CELERY_TIMEZONE=get_localzone(),
    CELERY_TASK_SERIALIZER='pickle',
    CELERY_RESULT_SERIALIZER='pickle',
    CELERY_ACCEPT_CONTENT=['pickle', 'json'],
    CELERYBEAT_SCHEDULE={
        'reset-gold-every-day-{0}am'.format(ResetGoldTime): {
            'task': 'reset_gold',
            'schedule': crontab(hour=17, minute=7),
        }
    },
)


if __name__ == '__main__':
    app.start()
