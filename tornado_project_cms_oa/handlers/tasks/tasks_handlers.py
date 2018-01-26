# -*- coding:utf-8 -*-
from handlers.base.base_handler import BaseHandler
from models.tasks.tasks_publisher_accept_models import Tasks,CategoryTasks
from libs.tasks.tasks_lib import save_tasks_messages,save_category

class TaskPublishHanlder(BaseHandler):
    def get(self):
        task = Tasks()

        tasks_name = task.content
        user_name = self.get_current_user().name
        kw = {
            'tasks_name':tasks_name,
            'user_name':user_name,
        }

        self.render('tasks/tasks_publisher.html',**kw)

    def post(self):
        content = self.get_argument('content',None)
        category =self.get_argument('category',None)
        print content,category
        current_user = self.get_current_user()
        current_user_name = current_user.name

        result = save_tasks_messages(self,content,current_user_name)


        if result['status'] is True:
            return self.write('发送成功')
        else:
            return self.write({'status': 400, 'msg': result['msg']})






class TasksAcceptHanlder(BaseHandler):
    def get(self):

        tasks = Tasks.all()
        current_uer = self.get_current_user().name
        task = Tasks()


        print '**********'
        print task.category_id

        kw = {
            'tasks':tasks,
            'current_uer':current_uer,

        }
        self.render('tasks/tasks_accept.html',**kw)


class UserAcceptHandler(BaseHandler):
    def get(self):
        '''
        根据task id 取出任务
        :return:
        '''

        current_user = self.get_current_user()
        user_name = current_user.name
        task_id = self.get_argument('id','')

        tasks = Tasks.by_id(task_id)
        # if tasks is not None:
        #     tasks_content = tasks.content
        str_task_id = str(task_id)
        current_user.tasks.append(tasks)
        print '**************'
        print current_user.tasks

        # self.conn.setex('tasks:%s'%user_name,tasks_content,2000)
        self.write('成功接受任务')

class MyTasksHandler(BaseHandler):
    def get(self):
        current_user = self.get_current_user()
        user_id = self.get_argument('user_id','')
        tasks = current_user.tasks
        kw = {
            'current_user':current_user,
            'tasks':tasks,
        }
        return self.render('tasks/my_doing_tasks.html',**kw)




