#coding=utf-8

from celery_test_module.celery_tasks import add,manage_redis


# add.delay(5,7)
# manage_redis.delay()

import time
for i in xrange(50):
    add.delay(i+1, 0)
    time.sleep(1)
