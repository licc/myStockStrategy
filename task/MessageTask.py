#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import logging
from datetime import datetime, timedelta
from queue import Queue
import hashlib
import requests

from model.Message import Message
from task import StockAnalyzeTask
from utils import Config
from utils.DbUtils import DbUtils
from utils.MessageUtils import MessageUtils
from utils.ModelUtils import ModelUtils
from utils.SystemUtils import SystemUtils

logging.basicConfig(level=logging.ERROR)
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
                msgobj.frommemberwxid = message.get('data', {}).get('from_member_wxid', '')
                msgobj.createtime = datetime.strptime(message.get('data', {}).get('time', ''), '%Y-%m-%d %H:%M:%S')
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
            logging.error('error 信息', e)


def process_message(wx_inst):
    # 处理下行消息
    __process_mt_message(wx_inst)
    # 处理上行消息
    __process_mo_message(wx_inst)


def __process_mo_message(wx_inst):
    msglist = MessageUtils.get_messages(0, 0, (datetime.now() + timedelta(minutes=-20)))
    for msg in msglist:
        try:
            MessageUtils.update_message_state(msg.id, 1)
            if len(msg.content) > 0 and msg.content[0] == "@":
                strlist = msg.content.split('?')
                if len(strlist) > 1:
                    a_name = strlist[0].strip()
                    a_val = strlist[1].strip()
                    if a_name == "@" + Config.mywx_nickname:
                        if a_val == "1":
                            session = DbUtils.get_session()
                            jbos = session.query(ModelUtils.get_model("strategy_conf", DbUtils.get_engine())) \
                                .filter_by(createid=msg.frommemberwxid).all()
                            session.close()
                            for job in jbos:
                                StockAnalyzeTask.process_job(job)

                        elif a_name == "@" + Config.mywx_nickname:
                            res = tuling(a_val, msg.frommemberwxid)
                            if res["code"] == 200:
                                reply = res["newslist"][0]["reply"]
                                send_d = {"data": reply, "type": "text"}

                                MessageUtils.add_message(
                                    Message(fromid=Config.mywx_id, fromname=Config.mywx_nickname,
                                            toid=msg.fromid, toname=""
                                            , content=json.dumps(send_d),
                                            createtime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                            , state=0, sendorrecv=1, msgtype="msg::chatroom")
                                )
                            else:
                                print(res)

        except BaseException as e:
            logging.error('处理 process_message:id:%s content:%s' % (msg.id, msg.content), e)


# 调用图灵的机器人
def tuling(text, id):
    res = requests.get(
        f"http://api.tianapi.com/txapi/robot/index?key={Config.tulin_apikey}&question={text}&userid={hashlib.md5(id.encode(encoding='UTF-8')).hexdigest()}")
    res_json = res.json()
    return res_json


def __process_mt_message(wx_inst):
    # 查询下行未处理的接收消息
    msglist = MessageUtils.get_messages(0, 1, (datetime.now() + timedelta(minutes=-20)))
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
                        # logging.info("发送文字：%s" % content['data'])
                        wx_inst.send_text(to_user=msg.toid, msg=content['data'])
                else:
                    logging.info("发送内容为空：" + msg.content)

        except BaseException as e:
            logging.error('处理 process_message:id:%s content:%s' % (msg.id, msg.content), e)


def main():
    # __process_mo_message("we23232")
    res = tuling("大盘指数", "dd")
    print(res)
    print(res["code"])
    print(res["newslist"][0]["reply"])


if __name__ == "__main__": main()
