#!/usr/bin/python
# -*- coding: UTF-8 -*-

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper
Base = declarative_base()


class ModelUtils:
    """"model工具类"""

    @staticmethod
    def get_model(name, engine):
        """根据name创建并return一个新的model类
        name:数据库表名
        engine:create_engine返回的对象，指定要操作的数据库连接，from sqlalchemy import create_engine
        """
        Base.metadata.reflect(engine)
        table = Base.metadata.tables[name]
        t = type(name, (object,), dict())
        mapper(t, table)
        Base.metadata.clear()
        return t
