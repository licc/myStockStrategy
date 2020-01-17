import logging
import threading
import time

from apscheduler.schedulers.background import BackgroundScheduler

from task import MessageTask, PullStockDataTask, StockAnalyzeTask
from utils import Config
from utils.SystemUtils import SystemUtils

if SystemUtils.is_windows():
    from wx.WechatPCAPI import WechatPCAPI

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.ERROR)


def win_run():
    # 监听微信消息
    wx_inst = WechatPCAPI(on_message=MessageTask.on_message, log=logging)
    wx_inst.start_wechat(block=True)

    while not wx_inst.get_myself():
        time.sleep(5)

    print('登陆成功')
    # 监听微信消息
    threading.Thread(target=MessageTask.thread_handle_message).start()
    print("监听消息启动完成")

    wx_inst.send_text(to_user=Config.mychatroom_id, msg=Config.login_msg)
    return wx_inst


if __name__ == '__main__':
    wx_inst = None
    scheduler = BackgroundScheduler()

    if SystemUtils.is_windows():
        print("启动微信...")
        wx_inst = win_run()

    # 周一拉取全量的表数据
    scheduler.add_job(PullStockDataTask.pull_stock_list, 'cron', day_of_week='mon', hour=7, minute=10)

    # 工作日每天获取一次
    scheduler.add_job(PullStockDataTask.pull_stock_data, 'cron', day_of_week='mon-fri', hour=16, minute=10)

    # 每2秒处理一次消息
    scheduler.add_job(MessageTask.process_message, 'interval', seconds=2, max_instances=1, args=[wx_inst])

    # 动态池
    dynamic_scheduler = BackgroundScheduler()
    dynamic_scheduler.start()
    # 第一次加载
    StockAnalyzeTask.refresh_stock_strategy(dynamic_scheduler)
    # 5分钟刷新策略
    scheduler.add_job(StockAnalyzeTask.refresh_stock_strategy, 'interval', seconds=300, args=[dynamic_scheduler])

    scheduler.start()
    print("策略推荐启动完成...")
    if not SystemUtils.is_windows():
        while True:
            time.sleep(1)
