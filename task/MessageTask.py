#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import logging
import time
from datetime import datetime
from queue import Queue

from model.Message import Message
from utils import Config
from utils.MessageUtils import MessageUtils
from utils.SystemUtils import SystemUtils

logging.basicConfig(level=logging.INFO)
queue_recved_message = Queue()


def on_message(message):
    queue_recved_message.put(message)


# 消息处理示例 仅供参考
def thread_handle_message():
    print("开始监听消息了...")
    while True:
        message = queue_recved_message.get()
        try:
            # logging.info(message)
            if 'msg' in message.get('type'):
                # 这里是判断收到的是消息 不是别的响应
                send_or_recv = message.get('data', {}).get('send_or_recv', '')
                state = 0 if send_or_recv[0] == '0' else 1
                content = message.get('data', {}).get('msg', '')
                fromid = message.get('data', {}).get('from_wxid', message.get('data', {}).get('from_chatroom_wxid', ''))
                fromname = message.get('data', {}).get('from_nickname',
                                                       message.get('data', {}).get('from_chatroom_nickname', ''))

                msgobj = Message()
                msgobj.state = state
                msgobj.content = content
                msgobj.msgtype = message.get('type')
                msgobj.frommemberwxid = message.get('data', {}).get('msg', 'from_member_wxid')
                msgobj.creattime = datetime.strptime(message.get('data', {}).get('time', ''), '%Y-%m-%d %H:%M:%S')
                msgobj.sendorrecv = 0 if send_or_recv[0] == '0' else 1

                if send_or_recv[0] == '1':
                    msgobj.fromid = Config.mywx_id
                    msgobj.fromname = Config.mywx_nickname
                    if 'chatroom' in msgobj.msgtype:
                        msgobj.toid = fromid
                        msgobj.toname = fromname

                if send_or_recv[0] == '0':
                    if 'single' in msgobj.msgtype:
                        msgobj.toid = Config.mywx_id
                        msgobj.toname = Config.mywx_nickname
                    if 'chatroom' in msgobj.msgtype:
                        msgobj.fromid = message.get('data', {}).get('from_chatroom_wxid', '')
                        msgobj.fromname = ""
                        msgobj.toid = fromid
                        msgobj.toname = fromname
                MessageUtils.add_message(msgobj)
        except BaseException as e:
            logging.error('error 信息', e.msg)


def process_message(wx_inst):
    # 查询未处理的接收消息
    msglist = MessageUtils.get_messages(0, 1)
    for msg in msglist:
        try:
            # time.sleep(1)
            MessageUtils.update_message_state(msg.id, 1)
            if SystemUtils.is_windows():
                content = json.loads(msg.content)
                if "data" in content.keys() and not len(content['data']) == 0:
                    if content['type'] == "img":
                        aimg = SystemUtils.get_file_absolute(content['data'])
                        logging.info("发送图片：%s aimg:%s" % (content['data'], aimg))
                        wx_inst.send_img(to_user=msg.toid, img_abspath=(r"" + aimg))
                    elif content['type'] == "text":
                        logging.info("发送文字：%s" % content['data'])
                        wx_inst.send_text(to_user=msg.toid, msg=content['data'])
                else:
                    logging.info("发送内容为空：" + msg.content)

        except BaseException as e:
            logging.error('处理 process_message:id:%s content:%s' % (msg.id, msg.content), e.msg)


def main():
    dict = {'data': 'Runoob', 'Age': 7, 'Class': 'First'}
    print(dict['data'])
    content = json.loads('{"data": "33", "type": "img"}')

    print(content['data'])

    print(content.keys())

    if "data" in content.keys():
        print("33333333")


if __name__ == "__main__": main()
