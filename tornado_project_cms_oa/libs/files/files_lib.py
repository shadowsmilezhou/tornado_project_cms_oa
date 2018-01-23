#coding=utf-8
from datetime import datetime
from string import printable
import json
from uuid import uuid4
from random import randint, choice
from tornado.concurrent import run_on_executor
from models.files.upload_file_model import Files
from libs.pagination.pagination_libs import Pagination
from libs.qiniu.qiniu_libs import upload_qiniu_file_content, down_qiniu_file

def files_list_lib(self, page):
    """01文件列表"""
    page = int(page)
    items = self.db.query(Files).limit(MAX_PAGE).offset((page - 1) * MAX_PAGE).all()
    if page == 1 and len(items) < MAX_PAGE:
        total = len(items)
    else:
        total = self.db.query(Files).order_by(None).count()
    return Pagination(page, MAX_PAGE, total, items)



def upload_files_lib(self, upload_files):
    """02文件上传到服务器文件夹"""
# [{'body': '222ccc', 'content_type': u'text/plain', 'filename': u'6111.txt'},
# {'body': '111aaaa', 'content_type': u'text/plain', 'filename': u'a.txt'}]
# upload_files['filename']
# upload_files['body']
# upload_files['content_type']
    img_path_list = []
    for upload_file in upload_files:
        file_path = save_file(self, upload_file)
        img_path_list.append(file_path)
    return img_path_list if img_path_list else None


def save_file(self, upload_file):
    """02保存单个文件"""
    files_ext = upload_file['filename'].split('.')[-1]
    files_type = ['jpg', 'bmp', 'png', 'mp4', 'ogg', 'mp3', 'txt']
    if files_ext not in files_type:
        return {'status': False, 'msg': '文件格式不正确','data': ''}
    uuidname = str(uuid4()) + '.%s' % files_ext
    #'sefaegaer.txt'   'sejfiajelgaeirf.jpg'
    file_content = upload_file['body']
    old_file = Files.file_is_existed(file_content)
    if old_file is not None:
        file_path = 'http://192.168.201.135:8000/images/' + old_file.uuid
        return {'status': True, 'msg': '文件保存成功(其实文件在硬盘上)', 'data': file_path}

    url = 'files/' + uuidname
    with open(url, 'wb') as f:
        f.write(file_content)

    file_name = upload_file['filename']
    files = Files()
    files.filename = file_name
    files.uuid = uuidname
    files.content_length = len(file_content)
    files.content_type = upload_file['content_type']
    files.update_time = datetime.now()
    files.file_hash = upload_file['body']
    files.files_users.append(self.current_user)
    self.db.add(files)
    self.db.commit()
    file_path = 'http://192.168.201.135:8000/images/' + files.uuid
    return {'status': True, 'msg': '文件保存成功','data':file_path}


def files_message_lib(self, uuid):
    """03文件详情页"""
    return Files.by_uuid(uuid)


MAX_PAGE = 3

def file_page_lib(self, page):
    """04文件分页列表"""
    # 文件列表
    files = self.current_user.users_files
    print files
    files_page = get_page_list(int(page), files, MAX_PAGE )
    # 回收站文件列表
    files_del = self.current_user.users_files_del
    return files_page, files_del


def get_page_list(current_page, content, MAX_PAGE):
    """04分页算法"""
    #[1,2,3,4,5,6,7,8,9]
    start = (current_page -1) * MAX_PAGE   #2-1 *2   3-1 *2
    end = start + MAX_PAGE    # 2 + 2  4

    split_content = content[start:end]
    total = content.count()
    count = total/MAX_PAGE  #8/2 =4
    if total % MAX_PAGE !=0:
        count += 1

    pre_page = current_page - 1
    next_page = current_page + 1

    if pre_page ==0:
        pre_page =1
    if next_page >count:
        next_page =count

    if count < 5:
        pages = [ p for p in xrange(1, count+1) ]

    elif current_page <=3:
        pages = [ p for p in xrange(1, 6)]

    elif current_page >= count-2:
        pages = [p for p in xrange(count-4, count+1)] #[16.17.18.19.20]

    else:
        pages = [ p for p in xrange(current_page - 2, current_page +3)]  #16 [15,16,17,18,19]

    return {
        'split_content': split_content,
        'count': count,
        'pre_page': pre_page,
        'next_page': next_page,
        'current_page': current_page,
        'pages': pages,
    }



#-----------------------------分享链接处理器--(可以用另一个用户登录后分享文件)-----------------------------
def create_sharing_links_lib(self, file_uuid):
    """001创建分享链接"""
    #生成redis键
    uu = str(uuid4())
    #生成4位提取密码
    password = ''.join([choice(printable[:62]) for i in xrange(4)])
    #创建字典
    redis_dict = {
        'user': self.current_user.name,
        'file_uuid': file_uuid,
        'password': password
    }
    #序列化字典
    reids_json = json.dumps(redis_dict)
    #保存到redis中
    self.conn.setex('sharing_links:%s' % uu, reids_json, 300)
    return 'http:192.168.201.135:8000/files/files_auth_sharing_links?uuid=%s'%uu, password


def get_username_lib(self,uu):
    """001获取分享者姓名"""
    #查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    #如果没有返回过期
    if redis_json is None:
        return {'status':False, 'msg':'分享已经过期', 'username':''}
    #如果有反序列化，返回用户名
    redis_dict = json.loads(redis_json)
    return {'status':True, 'msg':'', 'username': redis_dict['user']}



def get_sharing_files_lib(self, uu, password):
    """002使用密码验证分享链接"""
    # 查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    # 如果没有返回已经过期
    if redis_json is None:
        return {'status':False, 'msg':'分享已经过期', 'username':''}
    # 如果有反序列化
    redis_dict = json.loads(redis_json)
    #对比用户提交的密码与redis保存的密码
    if password == redis_dict['password']:
        #对比成功，密码保存当前用户的session
        self.session.set('sharing_links_password', password)
        #返回分享链接
        links = '/files/files_sharing_list?uuid=%s' % uu
        return {'status': True, 'msg': '分享11111成功', 'links': links, 'username':''}
    return {'status':False, 'msg': '分享密码输入错误', 'username': redis_dict['user']}


def files_sharing_list_lib(self, uu):
    """003查看分享的文件"""
    if uu == '':
        return {'status': False, 'msg': 'uuid不存在', 'data': ''}
    #获取当前用户的提取密码
    password = self.session.get('sharing_links_password')
    if not password:
        #如果没有密码重新获取链接
        return {'status': False, 'msg': '请重新获取链接', 'data': ''}
    # 查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    # 如果没有返回已经过期，并删除session
    if redis_json is None:
        del self.session['sharing_links_password']
        return {'status': False, 'msg': '分享已经过期', 'data': ''}
    # 如果有反序列化
    redis_dict = json.loads(redis_json)
    # 对比用户session中保存的密码和redis保存的密码
    if password != redis_dict['password']:
        # 如果不相等提示错误
        return {'status': False, 'msg': '您没有获得这个文件的链接', 'data': ''}
    # 返回文件
    files = Files.by_uuid(redis_dict['file_uuid'])
    return {'status': True, 'msg': '分享成功', 'data': [files], 'uuid':uu}


def save_sharing_files_lib(self, uu):
    """004保存分享的文件"""
    if uu == '':
        return {'status': False, 'msg': 'uuid不存在', 'data': ''}
    # 获取当前用户的提取密码
    password = self.session.get('sharing_links_password')
    if not password:
        # 如果没有密码重新获取链接
        return {'status': False, 'msg': '没有权限', 'data': ''}
    # 查询redis
    redis_json = self.conn.get('sharing_links:%s' % uu)
    # 如果没有返回已经过期，并删除session
    if redis_json is None:
        del self.session['sharing_links_password']
        return {'status': False, 'msg': '分享已经过期', 'data': ''}
    # 如果有反序列化
    redis_dict = json.loads(redis_json)
    # 对比用户session中保存的密码和redis保存的密码
    if password != redis_dict['password']:
        # 如果不相等提示错误
        return {'status': False, 'msg': '您没有获得这个文件的链接', 'data': ''}
    # 把文件保存到当前用户
    files = Files.by_uuid(redis_dict['file_uuid'])
    files.files_users.append(self.current_user)
    self.db.add(files)
    self.db.commit()
    return {'status': True, 'msg': '保存成功', 'data': ''}


#-----------------------------分享链接处理器结束-------------------------------

#-----------------------------回收站接口-----------------------------
def del_files_lib(self, uuid):
    """001删除到回收站"""
    files = Files.by_uuid(uuid)
    files.files_users.remove(self.current_user)
    files.files_users_del.append(self.current_user)
    self.db.add(files)
    self.db.commit()


def del_final_files_lib(self, uuid):
    """002彻底删除"""
    files = Files.by_uuid(uuid)
    files.files_users_del.remove(self.current_user)
    self.db.add(files)
    self.db.commit()


def recovery_files_lib(self,uuid):
    """003从回收站恢复"""
    files = Files.by_uuid(uuid)
    files.files_users_del.remove(self.current_user)
    files.files_users.append(self.current_user)
    self.db.add(files)
    self.db.commit()
#-----------------------------回收站接口结束-----------------------------

import time
@run_on_executor
def files_download_lib(self, uuid):
    """02异步下载文件"""
    filepath = 'files/%s' % uuid
    self.set_header('Content-Type', 'application/octet-stream')
    self.set_header('Content-Disposition', 'attachment; filename=%s' % uuid)
    with open(filepath, 'rb') as f:
        while 1:
            data = f.read(1024 * 5)
            print len(data)
            if not data:
                break
            self.write(data) #IO
            self.flush()
            time.sleep(1)
    self.finish()


def upload_files_qiniu_lib(self, upload_files):
    """03文件上传到七牛服务器"""
    img_path_list = []
    for upload_file in upload_files:
        file_path = save_qiniu_file(self, upload_file)
        img_path_list.append(file_path)
    return img_path_list if img_path_list else None


def save_qiniu_file(self, upload_file):
    """03保存单个文件到七牛"""
    files_ext = upload_file['filename'].split('.')[-1]
    files_type = ['jpg', 'bmp', 'png', 'mp4', 'ogg', 'mp3', 'txt']
    if files_ext not in files_type:
        return {'status': False, 'msg': '文件格式不正确', 'data': ''}

    file_content = upload_file['body']
    old_file = Files.file_is_existed(file_content)
    if old_file is not None:
        file_path = 'http://oq54v29ct.bkt.clouddn.com/' + old_file.uuid
        return {'status': True, 'msg': '文件保存成功(其实文件在硬盘上)', 'data': file_path}

    #上传到七牛
    ret, info = upload_qiniu_file_content(file_content)
    print ret
    print info
    if info.status_code != 200:
        return {'status': False, 'msg': '文件上传到七牛失败', 'data': ''}

    file_name = upload_file['filename']
    files = Files()
    files.filename = file_name
    files.uuid = ret #保存的七牛返回的文件名
    files.content_length = len(file_content)
    files.content_type = upload_file['content_type']
    files.update_time = datetime.now()
    files.file_hash = upload_file['body']
    files.files_users.append(self.current_user)
    self.db.add(files)
    self.db.commit()
    file_path = 'http://oq54v29ct.bkt.clouddn.com/' + files.uuid
    return {'status': True, 'msg': '文件上传到七牛成功', 'data': file_path}


def files_download_qiniu_lib(self, uuid):
    """04从七牛服务器下载文件"""
    if uuid == '':
        return {'status':False, 'msg': '没有文件ID'}
    old_file = Files.by_uuid(uuid)
    if old_file is None:
        return {'status': False, 'msg': '文件不存在'}
    qiniu_url = 'http://oq54v29ct.bkt.clouddn.com/%s' % uuid
    url = down_qiniu_file(qiniu_url)
    print url
    return {'status': True, 'data': url}
















