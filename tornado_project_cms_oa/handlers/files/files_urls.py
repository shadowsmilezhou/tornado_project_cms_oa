#coding=utf-8
from handlers.files.files_handler import (
    FilesListHandler,FilesUploadHandler,FilesMessageHandler,FilesPageListHandler,
FilesCreateSharingLinks,FilesAuthSharingLinks,FilesSharingListHandler,FilesSaveSharingHandler,

DelFilesHandler,FinalDelFilesHandler,RecoveryFilesHandler,FilesDownLoadHandler,FilesUploadQiniuHandler
,FilesDownLoadQiniuHandler
)

files_urls = [
    (r'/files/files_list/([1-9]{1,3})', FilesListHandler),  #文件列表
    (r'/files/files_up_load', FilesUploadHandler),  #文件上传
    (r'/files/files_up_load_qiniu', FilesUploadQiniuHandler),  #文件上传
    (r'/files/files_message', FilesMessageHandler), #文件详情
    (r'/files/files_page_list/([1-9]{1,3})', FilesPageListHandler), #文件分页
    (r'/files/files_down', FilesDownLoadQiniuHandler), #文件分页

    # 分享链接接口
    (r'/files/files_create_sharing_links', FilesCreateSharingLinks),  # 创建分享链接
    (r'/files/files_auth_sharing_links', FilesAuthSharingLinks),  # 验证分享链接
    (r'/files/files_sharing_list', FilesSharingListHandler),  # 分享链接的文件列表
    (r'/files/files_save_sharing_links', FilesSaveSharingHandler),  # 保存分享链接的文件
    # 回收站接口
    (r'/files/files_delete', DelFilesHandler),  # 删除文件
    (r'/files/files_delete_final', FinalDelFilesHandler),  # 完全删除文件
    (r'/files/files_recovery', RecoveryFilesHandler),  # 恢复文件
]