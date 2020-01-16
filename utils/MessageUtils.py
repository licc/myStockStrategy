#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

from model.Message import Message
from utils.DbUtils import DbUtils


class MessageUtils:
    """"消息工具类"""

    @staticmethod
    def add_message(obj):
        session = DbUtils.get_session()
        session.add(obj)
        session.commit()

    @staticmethod
    def update_message_state(id, state):
        session = DbUtils.get_session()
        session.query(Message).filter_by(id=id).update({"state": state})
        session.close()
        # session.commit()

    @staticmethod
    def get_messages(state, sendorrecv):
        session = DbUtils.get_session()
        list = session.query(Message).filter_by(state=state, sendorrecv=sendorrecv).all()
        return list



def main():
    msglist = MessageUtils.get_messages(0, 1)
    for row in msglist:
        print("   ==%a"%row.id )
        print(row.content)






if __name__ == "__main__": main()
