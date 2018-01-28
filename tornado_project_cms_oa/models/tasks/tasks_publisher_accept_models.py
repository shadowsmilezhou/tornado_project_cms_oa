# -*- coding:utf-8 -*-
from uuid import uuid4
from datetime import datetime
from string import printable

from pbkdf2 import PBKDF2

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (create_engine, Column, Integer, String,
                        Text, Boolean, Date, DateTime, ForeignKey)

from libs.db.dbsession import Base
from libs.db.dbsession import dbSession




class UserToTasks(Base):
    """用户任务多对多关系表"""
    __tablename__="tasks_to_users"
    u_id = Column(Integer,ForeignKey("user.id"), primary_key=True )
    t_id = Column(Integer,ForeignKey("tasks.id"), primary_key=True)


class Tasks(Base):
    '''
    任务表
    '''
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text)

    category_id = Column(Integer, ForeignKey('tasks_category.id'))
    num_task = Column(Integer,default=0)
    createtime = Column(DateTime, index=True, default=datetime.now)
    # category_content = Column(String(10),unique=True)

    users = relationship("User", secondary=UserToTasks.__table__)
    # category = relationship('CategoryTasks', backref='tasks')

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def by_id(cls, id):
        return dbSession.query(cls).filter_by(id=id).first()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter_by(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(content=name).first()

    @classmethod
    def by_category(cls, category):
        return dbSession.query(cls).filter_by(category_content=category).all()





class CategoryTasks(Base):
    """分类表"""
    __tablename__ = 'tasks_category'
    id = Column(Integer, primary_key=True)
    uuid = Column(String(36), unique=True,  default=lambda:str(uuid4()))
    name = Column(String(50), unique=True, )
    createtime = Column(DateTime, index=True, default=datetime.now)

    # 建立orm查询关系,分类表与任务表的一对多关系
    tasks = relationship('Tasks', backref='category')

    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def by_id(cls, id):
        return dbSession.query(cls).filter_by(id=id).first()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter_by(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter_by(name=name).first()