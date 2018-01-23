#coding=utf-8
from libs.flash.flash_lib import flash
from libs.db.dbsession import dbSession
from models.article.article_model import (
    Article,
    Comment,
    SecondComment,
    Tag,
    Category,
    UserLikeArticle
)

def article_list_lib(self):
    """01文章列表页"""
    articles = dbSession.query(Article).order_by(Article.createtime.desc()).all()
    comments = dbSession.query(Comment).order_by(Comment.createtime.desc()).all()
    tags = Tag.all()
    categorys = Category.all()
    return articles, comments, tags, categorys


def get_tags_categorys_lib(self):
    """02返回标签和分类"""
    tags = Tag.all()
    categorys = Category.all()
    return tags, categorys


def add_article_lib(self,article_id, title, content, desc, category_id, tags):
    """02添加新文章"""
    if category_id is None or tags is None:
    #if id('') == id(None):
        return {'status': False, 'msg': '请选择分类'}
    if title is None or content is None or desc is None:
        return {'status': False, 'msg': '请输入标题或文章内容'}
    if article_id != '':
        article = Article.by_id(article_id)
        article.tags = []
    else:
        article = Article()
    article.content = content
    article.title = title
    article.desc = desc
    article.category_id = category_id
    for tag_id in tags:
        tag = Tag.by_id(tag_id)
        article.tags.append(tag)
    article.user_id = self.current_user.id
    self.db.add(article)
    self.db.commit()
    if article_id is not None:
        return {'status': True, 'msg': '文档修改成功'}
    return {'status': True, 'msg': '文档添加成功'}


def add_category_tag_lib(self, category_name, tag_name):
    """03添加分类和标签"""
    if category_name is not None:
        category = Category.by_name(category_name)
        if category is not None:
            return {'status': False, 'msg': '分类已经存在'}
        else:
            category = Category()
        category.name = category_name
        self.db.add(category)
        self.db.commit()
        return {'status': True, 'msg': '分类添加成功'}
    if tag_name is not None:
        tag = Tag.by_name(tag_name)
        if tag is not None:
            return {'status': False, 'msg': '标签已经存在'}
        else:
            tag = Tag()
        tag.name = tag_name
        self.db.add(tag)
        self.db.commit()
        return {'status': True, 'msg': '标签添加成功'}
    return {'status': False, 'msg': '请输入标签或分类'}

def del_category_tag_lib(self, c_uuid, t_uuid):
    """04删除标签和分类"""
    if c_uuid is not None:
        category = Category.by_uuid(c_uuid)
        if category is None:
            flash(self, '分类不存在', 'error')
            return {'status': False}
        if category.articles:
            flash(self, '分类下有文章请先删除文章', 'error')
            return {'status': False}
        self.db.delete(category)
        self.db.commit()
        flash(self, '分类删除成功', 'success')
        return {'status': True}
    if t_uuid is not None:
        tag = Tag.by_uuid(t_uuid)
        if tag is None:
            flash(self, '标签不存在', 'error')
            return {'status': False, 'msg': '标签不存在'}
        self.db.delete(tag)
        self.db.commit()
        flash(self, '标签删除成功', 'success')
        return {'status': True}
    flash(self, '请输入标签或分类', 'error')
    return {'status': False}

def article_content_lib(self, article_id):
    if article_id is None:
        return {'status': False, 'msg': '缺少文章ID'}
    article = Article.by_id(article_id)
    if article is None:
        return {'status': False, 'msg': '文章不存在'}
    article.readnum += 1
    self.db.add(article)
    self.db.commit()
    return {'status': True, 'msg': '获取到文章', 'data': article}

def add_comment_lib(self, content, article_id):
    """06添加评论"""
    if article_id is None:
        return {'status': False, 'msg': '缺少文章ID'}
    article = Article.by_id(article_id)
    if article is None:
        return {'status': False, 'msg': '文章不存在'}
    comment = Comment()
    comment.content = content
    comment.article_id = article.id
    comment.user_id = self.current_user.id
    self.db.add(comment)
    self.db.commit()
    return {'status': True, 'msg': '评论提交成功'}


def add_second_comment_lib(self,  content, comment_id):
    """07添加二级评论"""
    if comment_id is None:
        return {'status': False, 'msg': '缺少评论ID'}
    comment = Comment.by_id(comment_id)
    if comment is None:
        return {'status': False, 'msg': '评论不存在'}
    second_comment = SecondComment()
    second_comment.content = content
    second_comment.comment_id = comment.id
    second_comment.user_id = self.current_user.id
    self.db.add(second_comment)
    self.db.commit()
    return {'status': True, 'msg': '二级评论提交成功'}


def add_like_lib(self, article_id):
    """08点赞"""
    if article_id is None:
        return {'status': False, 'msg': '文章ID 不存在'}
    article = Article.by_id(article_id)
    if article is None:
        return {'status': False, 'msg': '文章ID不正确'}
    if self.current_user in article.user_likes:
        """取消点赞功能"""
        article.user_likes.remove(self.current_user)
        self.db.add(article)
        self.db.commit()
        return {'status': True, 'msg': '已经取消点赞了'}
    article.user_likes.append(self.current_user)
    self.db.add(article)
    self.db.commit()
    return {'status': True, 'msg': '点赞成功'}


def search_article_lib(self, category_id, tag_id):
    """09通过分类或标签获取文档"""
    #articles = []
    if tag_id is not None:
        tag = Tag.by_id(tag_id)
        articles = tag.articles
    if category_id is not None:
        category = Category.by_id(category_id)
        articles = category.articles
    comments = dbSession.query(Comment).order_by(Comment.createtime.desc()).all()
    tags = Tag.all()
    categorys = Category.all()
    return articles, comments, tags, categorys

def articles_modify_list_lib(self):
    articles = Article.all()
    return articles


def article_modify_lib(self,article_id):
    if article_id is None:
        return {'status': False, 'msg': '文章ID 不存在'}
    article = Article.by_id(article_id)
    tags, categorys = get_tags_categorys_lib(self)
    return article, categorys, tags


def articles_delete_lib(self, article_id):
    if article_id is None:
        return {'status': False, 'msg': '文章ID 不存在'}
    article = Article.by_id(article_id)
    if article is None:
        return Article.all()
    self.db.delete(article)
    self.db.commit()
    return Article.all()