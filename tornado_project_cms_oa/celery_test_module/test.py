# -*- coding:utf-8 -*-
from time import sleep
from tasks import task_1,task_2,task_3,task_4,task_5

task_list = [task_1,task_2,task_3,task_4,task_5]

result = task_1.delay()

sleep(5)
# print result.status
# print result.ready()
# print result.result

