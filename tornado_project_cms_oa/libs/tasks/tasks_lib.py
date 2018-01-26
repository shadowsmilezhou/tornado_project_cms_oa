# -*- coding:utf-8 -*-
from libs.flash.flash_lib import flash
from libs.db.dbsession import dbSession
from models.tasks.tasks_publisher_accept_models import Tasks,CategoryTasks

def save_tasks_messages(self,content,current_user_name):

    if content is not None:
        content_task = Tasks.by_name(content)
        if content_task is not None:
            return {'status': False, 'msg': '任务已经存在'}
        else:

            task = Tasks()
            task.content = content

            self.db.add(task)
            self.db.commit()
            return {'status': True, 'msg': '任务发布成功'}

    else:
        return {'status': False, 'msg': '不能发布空任务'}

def save_category(self,category):
    if category is not None:
        category_task  = CategoryTasks.by_name(category)
        if category_task is not None:
            return {'status': False, 'msg': '任务已经存在'}

        category_task = CategoryTasks()
        category_task.name = category

        self.db.add(category_task)
        self.db.commit()
        return {'status': True, 'msg': '任务发布成功'}
    else:
        return {'status': False, 'msg': '请输入不同的分类'}







