#coding=utf-8

from account_auth_handler import LoginHandler, CaptchaHandler, RegistHandler,MobileCodeHandler

from account_handler import (ProfileHandler,
                             ProfileEditHandler,
                             ProfileModifyEmailHandler,
                             ProfileAuthEmailHandler,
                             ProfileAddAvaterHandler
                             )

accounts_urls = [
    (r'/auth/user_login', LoginHandler),
    (r'/auth/captcha', CaptchaHandler),
    (r'/auth/user_regist', RegistHandler),
    (r'/auth/mobile_code', MobileCodeHandler),
    (r'/account/user_profile', ProfileHandler),
    (r'/account/user_edit', ProfileEditHandler),
    (r'/account/send_user_email', ProfileModifyEmailHandler),
    (r'/account/auth_email_code', ProfileAuthEmailHandler),
    (r'/account/avatar', ProfileAddAvaterHandler),
]

