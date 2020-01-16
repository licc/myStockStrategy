#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils import Config

pymysql.install_as_MySQLdb()


class DbUtils:
    """"数据库工具类"""

    _engine = create_engine(Config.mysql_url
                            ,
                            max_overflow=10,  # 超过连接池大小外最多创建的连接
                            pool_size=5,  # 连接池大小
                            pool_timeout=10,  # 池中没有线程最多等待的时间，否则报错
                            pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
                            )

    @staticmethod
    def get_engine():
        return DbUtils._engine

    @staticmethod
    def get_session():
        return sessionmaker(DbUtils._engine)()
