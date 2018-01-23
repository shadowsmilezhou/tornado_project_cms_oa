#coding=utf-8
from __future__ import absolute_import
from datetime import timedelta
from celery.schedules import crontab

BROKER_URL = 'redis://127.0.0.1/2'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1/3'

CELERY_TIMEZONE='Asia/Shanghai'


CELERYBEAT_SCHEDULE = {
    'redis_manage':{
        'task':'celery_test_module.celery_tasks.manage_redis',
        'schedule': timedelta(seconds=5)
    },
    'redis_manage2': {
        'task': 'celery_test_module.celery_tasks.manage_redis',
        'schedule': crontab(minute=50)
    }
}