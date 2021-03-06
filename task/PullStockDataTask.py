#!/usr/bin/python
# -*- coding: UTF-8 -*-
import asyncio
import datetime as datetime
import json
import logging

import tushare as ts

from model.Message import Message
from utils import Config
from utils.DbUtils import DbUtils
from utils.MessageUtils import MessageUtils
from utils.ModelUtils import ModelUtils

logging.basicConfig(level=logging.INFO)


def pull_stock_list():
    """拉取所有票据列表保存到配置表"""
    count = 0
    try:

        df = ts.get_stock_basics()
        df.drop(['area', "pe", "outstanding", "totals", "totalAssets",
                 "fixedAssets", "reserved", "undp", "perundp", "rev", "profit",
                 "reservedPerShare", "esp", "bvps", "pb", "timeToMarket",
                 "liquidAssets", "gpr", "npr", "holders"], axis=1, inplace=True)
        # df.drop_duplicates(subset=['code'], keep="first", inplace=True)
        """清空表数据"""
        session = DbUtils.get_session()
        session.execute('truncate table tick_conf ')
        session.commit()
        session.close()

        df.insert(2, 'create_time', datetime.datetime.now())
        df.to_sql('tick_conf', DbUtils.get_engine(), if_exists='append')
        count = df.shape[0]

    except BaseException as e:
        logging.error('数据保存失败-总条数:%s' % (count), e)
    else:
        logging.info('数据保存成功-总条数:%s' % (count))


def pull_stock_data():
    """拉取票据信息"""
    # 交易日历
    sdate = (datetime.datetime.now() + datetime.timedelta(days=-0))
    edate = datetime.datetime.now()

    pull_stock_cal(sdate.strftime('%Y%m%d'), edate.strftime('%Y%m%d'))
    session = DbUtils.get_session()
    rows = session.query(ModelUtils.get_model("tick_conf", DbUtils.get_engine())).all()
    session.close()
    for row in rows:
        get_stock_data(row.code, sdate.strftime('%Y-%m-%d'), edate.strftime('%Y-%m-%d'))

    else:
        send_d = {"data": "当日数据拉取成功！！！", "type": "text"}
        MessageUtils.add_message(
            Message(fromid=Config.mywx_id, fromname=Config.mywx_nickname,
                    toid=Config.mychatroom_id, toname=""
                    , content=json.dumps(send_d), createtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    , state=0, sendorrecv=1, msgtype="msg::chatroom")
        )


def pull_stock_cal(sdate, edate):
    try:
        pro = ts.pro_api(token="cb077c8126fe4be0fb59e986f6a60146b5b40b65bb1a2d040675b7b8")
        df = pro.query('trade_cal', start_date=sdate, end_date=edate)
        print(df)
        df.to_sql('trade_cal', DbUtils.get_engine(), if_exists='append')
    except BaseException as e:
        logging.error('数据保存失败: startDate:%s endDate:%s ' % (sdate, edate), e)


def get_stock_data(stockNo, startDate, endDate):
    """获取指定code时间的票据信息"""
    try:
        df = ts.get_hist_data(stockNo, start=startDate, end=endDate)
        if not df.empty:
            df.insert(0, 'code', stockNo)
            df.to_sql('tick_data', DbUtils.get_engine(), if_exists='append')
    except BaseException as e:
        logging.error('数据保存失败:stockNo:%s startDate:%s endDate:%s ' % (stockNo, startDate, endDate), e)


def main():
    # pull_stock_cal("20200117", "20200117")
    # get_stock_data("600187","20200116", "20200116")
    # get_stock_data("20200116","20200116", "20200116")

    pull_stock_data()


if __name__ == "__main__": main()
