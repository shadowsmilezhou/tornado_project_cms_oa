# -*- coding:utf-8 -*-
from time import sleep
from celery import Celery


backend = 'redis://127.0.0.1:6379/0'
broker = 'redis://127.0.0.1:6379/1'

app = Celery('tasks', backend=backend, broker=broker)


@app.task
def task_1():
    sleep(5)
    return 'this is task 1'

@app.task
def task_2():
    sleep(2)
    return 'this is task 2'


@app.task
def task_3():
    sleep(3)
    return 'this is task 3'


@app.task
def task_4():
    sleep(4)
    return 'this is task 4'


@app.task
def task_5():
    return 'this is task 5'


