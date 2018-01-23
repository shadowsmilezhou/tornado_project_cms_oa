#coding=utf-8
from handlers.base.base_handler import BaseHandler
from libs.files.files_lib import (
    files_list_lib,
    upload_files_lib,
    files_message_lib,
    file_page_lib,

create_sharing_links_lib,get_username_lib,get_sharing_files_lib,files_sharing_list_lib,
save_sharing_files_lib,upload_files_qiniu_lib,files_download_qiniu_lib,

del_files_lib,del_final_files_lib,recovery_files_lib,files_download_lib
)

class FilesListHandler(BaseHandler):
    def get(self, page):
        """01文件列表"""
        pagination = files_list_lib(self, page)
        kw = {'pagination': pagination, }
        self.render('files/files_list.html', **kw)


class FilesUploadHandler(BaseHandler):
    """02文件上传到服务器文件夹"""
    def get(self):
        self.render('files/files_upload.html')

    def post(self):
        upload_files =self.request.files.get('importfile', None)
        result = upload_files_lib(self, upload_files)
        if result is None:
            return self.write({'status': 400, 'msg': '有错误了'})
        return self.write({'status': 200, 'msg': '有错误了','data': result})


class FilesMessageHandler(BaseHandler):
    """03文件详情页"""
    def get(self):
        uuid = self.get_argument('uuid', '')
        files = files_message_lib(self, uuid)
        kw = {'files': files}
        self.render('files/files_message.html', **kw)



class FilesPageListHandler(BaseHandler):
    """04文件分页列表"""
    def get(self, page):
        files_page, files_del= file_page_lib(self, page)
        kw = {
            'files': files_page['split_content'],
            'files_page': files_page,
            'files_del': files_del,
        }
        self.render('files/files_page_list.html', **kw)



#-----------------------------分享链接处理器-------------------------------
class FilesCreateSharingLinks(BaseHandler):
    """001创建分享链接"""
    def get(self):
        uuid = self.get_argument('uuid', '')
        fileslinks, password = create_sharing_links_lib(self, uuid)
        kw = {'fileslinks': fileslinks, 'password': password}
        self.render('files/files_create_sharing_links.html', **kw)


class FilesAuthSharingLinks(BaseHandler):
    """002使用密码验证分享链接"""
    def get(self):
        uu = self.get_argument('uuid', '')
        result = get_username_lib(self, uu)
        if result['status'] is False:
            kw = {'username': result['username'], 'uuid1': uu, 'msg': result['msg']}
            return self.render('files/files_auth_sharing_links.html', **kw)
        kw = {'username': result['username'], 'uuid1': uu, 'msg': ''}
        self.render('files/files_auth_sharing_links.html', **kw)

    def post(self):
        uu = self.get_argument('uuid', '')
        password = self.get_argument('password', '')
        result = get_sharing_files_lib(self, uu, password)
        if result['status'] is False:
            return self.write({'status': 400, 'msg': result['msg']})
        return self.write({'status': 200, 'msg': result['msg'], 'links': result['links']})


class FilesSharingListHandler(BaseHandler):
    """003查看分享的文件"""
    def get(self):
        uu = self.get_argument('uuid', '')
        print self.session.set('sharing', 'aa')
        result = files_sharing_list_lib(self, uu)
        if result['status'] is True:
            kw = {'files': result['data'], 'uuid': result['uuid']}
            return self.render('files/files_sharing_list.html', **kw)
        return self.write(result['msg'])


class FilesSaveSharingHandler(BaseHandler):
    """004保存分享的文件"""
    def get(self):
        uu = self.get_argument('uuid', '')
        result = save_sharing_files_lib(self, uu)
        if result['status'] is True:
            return self.redirect('/files/files_page_list/1')
        return self.write(result['msg'])

#-----------------------------分享链接处理器-------------------------------

#-----------------------------回收站接口-----------------------------
class DelFilesHandler(BaseHandler):
    """001删除到回收站"""
    def get(self):
        uuid = self.get_argument('uuid', '')
        del_files_lib(self,uuid)
        return self.redirect('/files/files_page_list/1')


class FinalDelFilesHandler(BaseHandler):
    """002最终删除"""
    def get(self):
        uuid = self.get_argument('uuid', '')
        del_final_files_lib(self, uuid)
        return self.redirect('/files/files_page_list/1')

class RecoveryFilesHandler(BaseHandler):
    """003从回收站恢复"""
    def get(self):
        uuid = self.get_argument('uuid', '')
        recovery_files_lib(self, uuid)
        return self.redirect('/files/files_page_list/1')

#-----------------------------回收站接口结束-----------------------------


import time
class FilesDownLoadHandler1(BaseHandler):
    """01同步下载文件"""
    def get(self):
        uuid = self.get_argument('uuid','')
        if uuid != '':
            filepath = 'files/%s' % uuid
            self.set_header('Content-Type', 'application/octet-stream')
            self.set_header('Content-Disposition', 'attachment; filename=%s' %uuid)
            with open(filepath, 'rb') as f:
                while 1:
                    data = f.read(1024*5)
                    print len(data)
                    if not data:
                        break
                    self.write(data)
                    self.flush()
                    time.sleep(1)
            self.finish()
        else:
            self.write('no uuid')


import tornado.gen
from concurrent.futures import ThreadPoolExecutor
executor1 = ThreadPoolExecutor(50)

class FilesDownLoadHandler(BaseHandler):
    """02异步下载文件"""
    executor = executor1
    @tornado.gen.coroutine
    def get(self):
        uuid = self.get_argument('uuid', '')
        if uuid != '':
            yield files_download_lib(self, uuid)
        else:
            self.write('no uuid')


class FilesUploadQiniuHandler(BaseHandler):
    """03文件上传到七牛服务器"""
    def get(self):
        self.render('files/files_upload.html')

    def post(self):
        upload_files =self.request.files.get('importfile', None)
        result = upload_files_qiniu_lib(self, upload_files)
        if result is None:
            return self.write({'status': 400, 'msg': '有错误了'})
        return self.write({'status': 200, 'msg': '有错误了','data': result})


class FilesDownLoadQiniuHandler(BaseHandler):
    """04从七牛服务器下载文件"""
    def get(self):
        uuid =self.get_argument('uuid', '')
        result = files_download_qiniu_lib(self, uuid)
        if result['status'] is True:
            return self.redirect(result['data'])
        else:
            return self.write(result['msg'])




