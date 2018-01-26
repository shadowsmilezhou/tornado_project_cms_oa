# -*- coding:utf-8 -*-
from handlers.tasks.tasks_handlers import TaskPublishHanlder,TasksAcceptHanlder,UserAcceptHandler,MyTasksHandler

tasks_urls = [
    (r'/tasks/publisher',TaskPublishHanlder),
    (r'/tasks/accept',TasksAcceptHanlder),
    # (r'/tasks/category',TasksCategoryHanlder)
    (r'/tasks/accept_tasks',UserAcceptHandler),
    (r'/tasks/my_doing_tasks',MyTasksHandler),
]