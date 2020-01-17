#!/usr/bin/python
# -*- coding: UTF-8 -*-
from sqlalchemy import Column, Integer, TIMESTAMP, String
from utils.ModelUtils import Base


class Message(Base):
    """"上行"""
    # 表名
    __tablename__ = 'message'
    # 字段，属性
    id = Column(Integer, primary_key=True)
    fromid = Column(String, name="from_id")
    fromname = Column(String, name="from_name")
    frommemberwxid = Column(String, name="from_member_wxid")
    toid = Column(String, name="to_id")
    toname = Column(String, name="to_name")
    content = Column(String)
    createtime = Column(TIMESTAMP, name="create_time")
    state = Column(Integer)
    sendorrecv = Column(Integer, name="send_or_recv")
    msgtype = Column(String, name="msg_type")
