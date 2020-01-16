#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json
import logging
from datetime import datetime

from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import text

from model.Message import Message
from utils import Config
from utils.HtmlUtils import HtmlUtils
from utils.DbUtils import DbUtils
from utils.MessageUtils import MessageUtils
from utils.ModelUtils import ModelUtils

logging.basicConfig(level=logging.INFO)


def refresh_stock_strategy(scheduler):
    """刷新job信息"""
    print("刷新job")
    currjobs = scheduler.get_jobs()
    session = DbUtils.get_session()

    jbos = session.query(ModelUtils.get_model("strategy_conf", DbUtils.get_engine())).all()
    session.close()

    for job in currjobs:
        job.remove()

    for job in jbos:
        scheduler.add_job(process_job, CronTrigger.from_crontab(job.cron), name=job.name, args=[job])


def process_job(job):
    """处理单个任务"""
    session = DbUtils.get_session()
    try:
        cursor = session.execute(job.strategy_sql)
        snos = cursor.fetchall()

        code_list = [item for sublist in snos for item in sublist]

        if len(code_list) != 0:
            # 根据策略数据查询详情数据
            cursor = session.execute(
                text(
                    "select  t.*,t2.name from tick_data t LEFT JOIN tick_conf t2 on t.code=t2.code where t.code in :code_list ORDER BY t.code,t.date asc"),
                params={"code_list": code_list})

            result = cursor.fetchall()
            session.close()

            data = {}
            for row in result:
                sno = row[2]
                # 以编号为字典
                if sno not in data.keys():
                    data[sno] = {}
                    data[sno]['name'] = row[16]
                s_d_data = data[sno]

                # 编号字典内部的 日期
                if "category" not in s_d_data.keys():
                    s_d_data['category'] = []
                s_d_data['category'].append(row[1])

                # 日K数据
                if "day" not in s_d_data.keys():
                    s_d_data['day'] = []

                # 开盘(open)，收盘(close)，最低(lowest)，最高(highest)
                s_d_data['day'].append([row[3], row[5], row[6], row[4]])

                if "ma5" not in s_d_data.keys():
                    s_d_data['ma5'] = []
                s_d_data['ma5'].append(row[10])

                if "ma10" not in s_d_data.keys():
                    s_d_data['ma10'] = []
                s_d_data['ma10'].append(row[11])

                if "ma20" not in s_d_data.keys():
                    s_d_data['ma20'] = []
                s_d_data['ma20'].append(row[12])

            data["name"] = job.name
            img_path = HtmlUtils.generate_img(
                HtmlUtils.generate_html("./static/template", 'ktemp.html', data))

            send_d = {"name": job.name, "data": img_path, "type": "img", "snos": ','.join(data.keys())}
            MessageUtils.add_message(
                Message(fromid=Config.mywx_id, fromname=Config.mywx_nickname,
                        toid=(job.toid if not job.toid is None and len(job.toid) > 0 else Config.mychatroom_id),
                        toname=""
                        , content=json.dumps(send_d), creattime=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        , state=0, sendorrecv=1, msgtype="msg::chatroom")
            )

    except BaseException as e:
        logging.error('处理单个任务失败:name:' + job.name, e)
    finally:
        session.close()


def main():
    print(CronTrigger.from_crontab("40 4 * * 1-5"))


if __name__ == "__main__": main()
