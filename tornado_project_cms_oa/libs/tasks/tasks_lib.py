# -*- coding:utf-8 -*-
from libs.flash.flash_lib import flash
from libs.db.dbsession import dbSession
from models.tasks.tasks_publisher_accept_models import Tasks,CategoryTasks

def save_tasks_messages(self,content,current_user,category):

    if content is not None:
        content_task = Tasks.by_name(content)
        # task_category = CategoryTasks.by_name(category)
        print content_task
        # if task_category is not None:
        #     print '**********++++++++'
        #     return {'status': False, 'msg': '该分类已经存在'}
        if content_task is not None:
            print '+++++++++++'
            return {'status': False, 'msg': '任务已经存在'}
        else:

            task = Tasks()
            task.content = content
            task.users.append(current_user)
            task.category_id = category
            # task.category_content = category
            self.db.add(task)

            self.db.commit()

            self.conn.sadd('tasks:%s'%category,content)
            return {'status': True, 'msg': '任务发布成功'}

    else:
        return {'status': False, 'msg': '不能发布空任务'}

def save_category(self,category):
    if category is not None:
        category_task = CategoryTasks.by_name(category)
        print category_task
        if category_task is not None:
            print "+++++++"
            return {'status': False, 'msg': '分类已经存在'}

        category_task = CategoryTasks()
        category_task.name = category
        self.db.add(category_task)
        self.db.commit()
        return {'status': True, 'msg': '任务发布成功'}
    else:
        print "*****"
        return {'status': False, 'msg': '请输入分类'}








 # def save_category(self,category):
 #    if category is not None:
 #         category_task  = CategoryTasks.by_name(category)
 #         if category_task is not None:
 #             return {'status': False, 'msg': '分类已经存在'}
 #
 #         category_task = CategoryTasks()
 #         category_task.name = category
 #
 #         self.db.add(category_task)
 #         self.db.commit()
 #         return {'status': True, 'msg': '任务发布成功'}
 #     else:
 #         return {'status': False, 'msg': '请输入不同的分类'}
 #
 #
 #
 #



