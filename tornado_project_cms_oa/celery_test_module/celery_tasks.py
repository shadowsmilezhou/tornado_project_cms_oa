#coding=utf-8
from __future__ import absolute_import
import time
import redis
from celery_test_module.celery import celery_test
conn = redis.Redis()


@celery_test.task
def add(a, b):
    time.sleep(2)
    return a+b

@celery_test.task
def manage_redis():
    msg_len = conn.llen('message:system')
    print msg_len
    if msg_len>5:
        conn.ltrim('message:system', msg_len-5, msg_len)
    print conn.llen('message:system')
