import time
from threading import Thread
import database
import httpx
import logging
import json
from services.schedule.schedule_service import ScheduleService
from utils.service_result import handle_result
import concurrent.futures


class DynamicTask(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.executor_ = concurrent.futures.ThreadPoolExecutor(max_workers=100)

    def run(self):
        time.sleep(5)  # 等待程序启动
        db = database.SessionLocal()
        so = ScheduleService(db)
        items = handle_result(so.get_items())
        if items is None:
            return None
        for item in items:
            item.firstRun = True
            self.executor_.submit(self.runItem, item)

    def runItem(self, item):
        if item.firstRun is True:
            item.firstRun = False
            time.sleep(item.initDelay)
        if item.enable:
            print(item.dids, item.dtags, item.execUrl)
            with httpx.Client(timeout=None, verify=False) as client:
                params = {"devices": item.dids,
                          "tags": item.dtags,
                          "startts": 0,
                          "endts": 0
                          }
                r = client.post(item.execUrl, json=params)
                logging.info(r)
            time.sleep(item.delay)
            self.executor_.submit(self.runItem, item)

    def stop(self):
        self.executor_.shutdown()
