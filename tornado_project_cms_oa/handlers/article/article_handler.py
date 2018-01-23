#coding=utf-8
import json

from handlers.base.base_handler import BaseHandler
from libs.article.aritcle_libs import (
    article_list_lib,
    get_tags_categorys_lib,articles_delete_lib,
    add_article_lib,articles_modify_list_lib,article_modify_lib,
    add_category_tag_lib,del_category_tag_lib,search_article_lib,
    article_content_lib, add_comment_lib, add_second_comment_lib,add_like_lib
)

class ArticleListHandler(BaseHandler):
    """01文章列表页"""
    def get(self):
        articles, comments, tags, categorys = article_list_lib(self)
        kw = {
            'articles': articles,
            'newarticles': articles[:3],
            'newcomments': comments[:3],
            'tags': tags,
            'categorys': categorys,
        }
        return self.render('article/article_list.html', **kw)

class AddArticleHandler(BaseHandler):
    """02添加新文章"""
    def get(self):
        tags, categorys = get_tags_categorys_lib(self)
        kw = {'tags': tags, 'categorys': categorys}
        return self.render('article/add_article.html', **kw)

    def post(self):
        title = self.get_argument('title', None)
        content = self.get_argument('article', None)
        desc = self.get_argument('desc', None)
        category = self.get_argument('category', None)
        article_id = self.get_argument('article_id', '')

        tags = json.loads(self.get_argument('tags', None))

        print article_id
        print title, content, desc, category, tags
        result = add_article_lib(self, article_id,title, content, desc, category, tags)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class AddCategoryTagHandler(BaseHandler):
    """03添加分类和标签"""
    def get(self):
        tags, categorys = get_tags_categorys_lib(self)
        kw = {'tags': tags, 'categorys': categorys}
        return self.render('article/article_add_category_tag.html', **kw)

    def post(self):
        category_name = self.get_argument('category_name', None)
        tag_name = self.get_argument('tag_name', None)
        result = add_category_tag_lib(self, category_name, tag_name)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})

class DelCategoryTagHandler(BaseHandler):
    """04删除标签和分类"""
    def get(self):
        c_uuid = self.get_argument('c_uuid', None)
        t_uuid = self.get_argument('t_uuid', None)
        result = del_category_tag_lib(self, c_uuid, t_uuid)
        if result['status'] is True:
            return self.redirect('/article/add_category_tag')
        return self.redirect('/article/add_category_tag')

class ArticleContentHandler(BaseHandler):
    """05文档详情页"""
    def get(self):
        article_id = self.get_argument('id', None)
        result = article_content_lib(self, article_id)
        if result['status'] is True:
            article = result['data']
            comments = article.comments
            kw = {'article': article, 'comments': comments}
            return self.render('article/article.html', **kw)
        return result['msg']

class AddCommentHandler(BaseHandler):
    """06添加评论"""
    def post(self):
        content = self.get_argument('content', None)
        article_id = self.get_argument('id', None)
        result = add_comment_lib(self, content, article_id)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class AddSecondCommentHandler(BaseHandler):
    """07添加二级评论"""
    def post(self):
        content = self.get_argument('content', None)
        comment_id = self.get_argument('id', None)
        result = add_second_comment_lib(self, content, comment_id)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class AddLikeHandler(BaseHandler):
    """08点赞"""
    def post(self):
        article_id = self.get_argument('article_id', None)
        result = add_like_lib(self, article_id)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class SearchByCategoryTagHandler(BaseHandler):
    """09通过分类或标签获取文档"""
    def get(self):
        category_id = self.get_argument('category_id', None)
        tag_id = self.get_argument('tag_id', None)
        articles, comments, tags, categorys = search_article_lib(self, category_id,tag_id)
        kw = {
            'articles': articles,
            'newarticles': articles[:3],
            'newcomments': comments[:3],
            'tags': tags,
            'categorys': categorys,
        }
        return self.render('article/article_list.html', **kw)

class AritlceModifyListHandler(BaseHandler):
    def get(self):
        articles = articles_modify_list_lib(self)
        kw = {'articles': articles}
        self.render('article/article_modify_manage.html', **kw)


class ArticleModifyHandler(BaseHandler):
    def get(self):
        article_id = self.get_argument('id', '')
        print article_id,'------------'
        article, categorys, tags = article_modify_lib(self, article_id)
        kw = {'article': article, 'categorys': categorys, 'tags': tags}
        self.render('article/article_modify.html', **kw)


class ArticleDeleteHandler(BaseHandler):
    def get(self):
        article_id = self.get_argument('id', '')
        articles = articles_delete_lib(self, article_id)
        kw = {'articles': articles}
        self.render('article/article_modify_manage.html', **kw)




