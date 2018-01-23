#coding=utf-8
from datetime import datetime
import tornado.escape
from handlers.base.base_handler import BaseWebSocket,BaseHandler
from models.permission.permission_model import Role




class SendMessageHandler(BaseHandler):
    def get(self):
        kw = {
            'user_msg': self.get_redis_json_to_dict('user'),
            'role_msg': self.get_redis_json_to_dict('role'),
            'system_msg': self.get_redis_json_to_dict('system'),
            'roles': Role.all(),
        }
        self.render('message/message_send_message.html', **kw)

    def get_redis_json_to_dict(self, target):
        msgs = self.conn.lrange('message:%s'%target, -2, -1)
        msgs.reverse()
        dict_list = []
        for c in msgs:
            msg = tornado.escape.json_decode(c)
            dict_list.append(msg)
        return dict_list


    def post(self):
        content = self.get_argument('content', '')
        send_type = self.get_argument('send_type', '')
        roleid = self.get_argument('roleid', '')
        user = self.get_argument('user', '')
        if send_type == "system":
            MessageWebSocket.send_system_message(self,content,send_type,)
        if send_type == "role":
            MessageWebSocket.send_role_message(self,content,send_type,roleid)
        if send_type == "user":
            MessageWebSocket.send_user_message(self,content,send_type,user)
        self.redirect('/message/send_message')


class MessageHandler(BaseHandler):
    def get(self):
        cache = self.conn.lrange('message:list', -5 , -1)  #['','']
        cache.reverse()
        cache_list = []
        for c in cache:
            msg = tornado.escape.json_decode(c)
            cache_list.append(msg)

        user_list = self.conn.lrange('message:user_list',0, -1)
        kw = {'cache': cache_list,'user_list':user_list}
        self.render('message/message_chat.html', **kw)


class MessageWebSocket(BaseWebSocket): #zhangsan  lishi

    users = {}# {'zhangsan': MessageWebSocket(), 'lishi': MessageWebSocket()}

    @classmethod
    def send_system_message(cls,self ,content,send_type):
        target = 'system'
        redis_msg = cls.dict_to_json(self, content, send_type, target)
        self.conn.rpush('message:%s'%send_type,redis_msg)
        for f, v in MessageWebSocket.users.iteritems():
            v.write_message(redis_msg)


    @classmethod
    def dict_to_json(cls, self, content, send_type, target):
        msg = {
            "content": content,
            "send_type": send_type,
            "sender": self.current_user.name,
            "target": target,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return tornado.escape.json_encode(msg)


    @classmethod
    def send_role_message(cls, self,content,send_type,roleid):
        role = Role.by_id(roleid)
        redis_msg = cls.dict_to_json(self, content, send_type, role.name)
        self.conn.rpush('message:%s' % send_type, redis_msg)
        role_users = role.users #[zhangsan, lishi , wangwu]  [zhangsan, lishi]
        for user in role_users:
            if MessageWebSocket.users.get(user.name, None) is not None:
                MessageWebSocket.users[user.name].write_message(redis_msg)
            else:
                #self.conn.lpush("ws:role_off_line",message)
                pass

    @classmethod
    def send_user_message(cls, self,content,send_type,user):
        redis_msg = cls.dict_to_json(self, content, send_type, user)
        self.conn.rpush('message:%s' % send_type, redis_msg)
        if cls.users.get(user, None) is not None:
            cls.users[user].write_message(redis_msg)
        else:
            #self.conn.lpush("ws:user_off_line",message)
            pass

    def open(self):
        print '----------------open------------------'
        MessageWebSocket.users[self.current_user.name] = self
        self.conn.rpush('message:user_list', self.current_user.name)
        # users['zhangsan'] = self
        # users['lishi'] =self
        print MessageWebSocket.users
        MessageWebSocket.send_system_message(
            self, "%s:上线了" % self.current_user.name.encode('utf-8'), "system", )


    def on_close(self):
        print '---------------close------------------'
        del MessageWebSocket.users[self.current_user.name]
        print MessageWebSocket.users
        MessageWebSocket.send_system_message(
            self, "%s:下线了" % self.current_user.name.encode('utf-8'), "system", )

    def on_message(self, message):
        print '---------------on_message------------------'
        print message
        msg = tornado.escape.json_decode(message)
        msg.update({
            "name": self.current_user.name,
            "useravatar": self.current_user.avatar,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        message = tornado.escape.json_encode(msg)

        self.conn.rpush('message:list', message)

        for f, v in MessageWebSocket.users.iteritems():
            v.write_message(msg)