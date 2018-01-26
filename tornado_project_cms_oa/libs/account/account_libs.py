#coding=utf-8
import json
import traceback
from uuid import uuid4
from random import choice
from string import printable
from datetime import datetime
from libs.common.send_email.send_email_libs import send_qq_html_email
from models.account.account_user_model import User

def edit_profile(self, name, password):
    """编辑个人信息"""
    if password == "":
        return {'status': False, 'msg': "密码不能为空"}

    if name == "":
        return {'status': False, 'msg': "姓名不能为空"}
    user = self.current_user
    user.name = name
    user.password = password
    user.update_time = datetime.now()
    self.db.add(user)
    self.db.commit()
    return {'status': True, 'msg': "修改成功"}

def send_email_libs(self, email):
    """发送邮件"""
    email_code = ''.join([choice(printable[:62]) for i in xrange(4)])
    u = str(uuid4())
    text_dict = {
        u: self.current_user.id,
        'email_code': email_code
    }
    redis_text = json.dumps(text_dict)

    content = """
          <p>html 邮箱验证 </p>
          <p>请点击以下邮箱进行验证<a href="http://192.168.206.129:8000/account/auth_email_code?code={}&email={}&user_id={}">邮箱绑定链接</a></p>
      """.format(email_code, email, u)

    send_fail = send_qq_html_email("630551760@qq.com", [email], "邮箱验证", content)
    if send_fail:
        return {'status': False, 'msg': "邮箱发送失败"}
    self.conn.setex('email:%s' % email, redis_text, 500)
    return {'status': True, 'msg': "邮箱发送成功"}


def auth_email_libs(self, email, email_code, u):
    """验证邮箱验证码"""
    redis_text = self.conn.get('email:%s' % email)
    if redis_text:
        text_dict = json.loads(redis_text)
        if text_dict and text_dict['email_code'] == email_code:
            user = self.current_user
            if not user:
                user = User.by_id(text_dict[u])
            print user
            user.email = email
            user.update_time =datetime.now()
            self.db.add(user)
            self.db.commit()
            return {'status': True, 'msg': "邮箱修改成功"}
        return {'status': False, 'msg': "验证码错误"}
    return {'status': False, 'msg': "验证码过期"}


def add_avatar_lib(self, avatar_data):
    """上传用户头像"""
    try:
        user = self.current_user #获取当前用户
        user.avatar = avatar_data #给avatar赋值
        user.update_time = datetime.now()  #给修改时间赋值
        self.db.add(user) #把对象添加到session中
        self.db.commit() #提交保存到数据库
    except Exception as e:
        print e
        print '------------'
        print traceback.format_exc()
        print '-------------'
        send_qq_html_email(
            "630551760@qq.com",
            ["630551760@qq.com"],
            "第一课",
            traceback.format_exc().replace("\n", '<br>')
        )
        return {'status': True, 'msg': 'error'}
    return {'status': True, 'msg': "头像上传成功"}


