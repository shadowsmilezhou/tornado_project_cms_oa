#coding=utf-8
from handlers.base.base_handler import BaseHandler
from libs.account.account_auth_libs import (create_captcha_img,
                                            get_mobile_code_lib,
                                            auth_captche,login, regist)

class CaptchaHandler(BaseHandler):
    """01生成验证码"""
    def get(self):
        pre_code = self.get_argument('pre_code', '')
        code = self.get_argument('code', '')
        img = create_captcha_img(self, pre_code, code)
        self.set_header("Content-Type", "image/jpg")
        self.write(img)


class LoginHandler(BaseHandler):
    """02登录函数"""
    def get(self):
        self.render("account/auth_login.html")

    def post(self):
        name = self.get_argument('name', '')
        password = self.get_argument('password', '')
        code = self.get_argument('code', '')
        captcha_code = self.get_argument('captcha', '')

        result = auth_captche(self, captcha_code, code)
        #{'status': False, 'msg': '请输入图形验证码'}
        if result['status'] is False:
            return self.write({'status': 400, 'msg': result['msg']})
        result = login(self, name, password)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class MobileCodeHandler(BaseHandler):
    """03发送手机短信"""
    def post(self):
        mobile = self.get_argument('mobile', '')
        code = self.get_argument('code', '')
        captcha = self.get_argument('captcha', '')
        print mobile, code, captcha
        result = get_mobile_code_lib(self,  mobile, code, captcha)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})



class RegistHandler(BaseHandler):
    """04注册函数"""
    def get(self):
        self.render("account/auth_regist.html", message="注册")

    def post(self):
        mobile = self.get_argument('mobile', '')
        mobile_captcha = self.get_argument('mobile_captcha', '')
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')
        captcha = self.get_argument('captcha', '')
        result = regist(self, name, mobile, mobile_captcha,
                        password1, password2, captcha, code)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})
