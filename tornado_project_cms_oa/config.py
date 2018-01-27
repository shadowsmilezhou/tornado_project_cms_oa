#coding=utf-8
from libs.flash.flash_lib import get_flashed_messages
from libs.permission.permission_auth.permission_interface_libs import menu_permission

settings = dict(
        template_path = 'templates',
        static_path = 'static',
        debug = True,
        cookie_secret = 'aaaa',
        login_url = '/auth/user_login',
        xsrf_cookies = True,
        ui_methods= {
            "menu_permission": menu_permission,
            "get_flashed_messages": get_flashed_messages,
            # "tasks_id":tasks_id_messages,
        },
        # pycket的配置信息
        pycket = {
             'engine': 'redis',  # 设置存储器类型
             'storage': {
                 'host': 'localhost',
                 'port': 6379,
                 'db_sessions': 5,
                 'db_notifications': 11,
                 'max_connections': 2 ** 31,
             },
             'cookies': {
                 'expires_days': 30,  # 设置过期时间
                 #'max_age': 5000,
             },
         },
)