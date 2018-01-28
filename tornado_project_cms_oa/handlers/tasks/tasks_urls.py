# -*- coding:utf-8 -*-
from handlers.tasks.tasks_handlers import TaskPublishHanlder,TasksAcceptHanlder,UserAcceptHandler,MyTasksHandler,QuitTaskHandler,HaveDoneTasksHandler,CategoryTasksHandler,CategoryManageHandler

tasks_urls = [
    (r'/tasks/publisher',TaskPublishHanlder),
    (r'/tasks/accept',TasksAcceptHanlder),
    # (r'/tasks/category',TasksCategoryHanlder)
    (r'/tasks/accept_tasks',UserAcceptHandler),
    (r'/tasks/my_doing_tasks',MyTasksHandler),
    (r'/tasks/delete',QuitTaskHandler),
    (r'/tasks/havedone',HaveDoneTasksHandler),
    (r'/tasks/category_by_tasks',CategoryTasksHandler),
    (r'/tasks/category_manage',CategoryManageHandler),
]