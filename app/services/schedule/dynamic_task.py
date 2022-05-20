import json
import time

import constants
import database
import httpx
import logging
import threading

from models.tables import TSchedule
from services.convert.cluster_display_util import ClusterDisplayUtil
from services.convert.self_relation_util import SelfRelationUtil
from services.schedule.schedule_service import ScheduleService
from utils.service_result import handle_result
import concurrent.futures

API_SCHEDULE_PREFIX = constants.PHMMS_URL_PREFIX + "/api/v1/phm/vrla/"
API_SCHEDULE_SOH = constants.PHMMS_URL_PREFIX + "/api/v1/phm/vrla/soh"
API_SCHEDULE_CLUSTER = constants.PHMMS_URL_PREFIX + "/api/v1/phm/vrla/cluster"
API_SCHEDULE_RELATION = constants.PHMMS_URL_PREFIX + "/api/v1/phm/vrla/relation"


class DynamicTask(object):
    _instance_lock = threading.Lock()
    init_first = False

    def __init__(self):
        if DynamicTask.init_first is False:
            DynamicTask.init_first = True
            self.__executor = concurrent.futures.ThreadPoolExecutor(max_workers=100)
            self.__isStop = False
            self.__items = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with DynamicTask._instance_lock:
                if not hasattr(cls, '_instance'):
                    DynamicTask._instance = super().__new__(cls)
        return DynamicTask._instance

    def start(self):
        self.__executor.submit(self.__exec)

    def stop(self):
        self.__isStop = True
        self.__executor.shutdown()

    def push(self, data):
        if data is None:
            return
        if self.__items is None:
            data.firstRun = True
            self.__items = [data]
        else:
            for item in self.__items:
                if item.id == data.id:
                    self.__items.remove(item)
                    break
            data.firstRun = True
            self.__items.append(data)
        pass

    def pop(self, data):
        if data is None:
            return
        for item in self.__items:
            if item.id == data.id:
                self.__items.remove(item)
                break
        pass

    def popAll(self, dataS):
        if dataS is None:
            return
        for data in dataS:
            self.pop(data)

    def __loadData(self):
        db = database.SessionLocal()
        so = ScheduleService(db)
        self.__items = handle_result(so.get_items())
        if self.__items is None:
            return
        for item in self.__items:
            item.firstRun = True

    @staticmethod
    def __updateData(item):
        db = database.SessionLocal()
        so = ScheduleService(db)
        so.update_item(item)
        pass

    def __exec(self):
        time.sleep(5)  # 等待程序启动
        self.__loadData()
        while self.__isStop is False:
            time.sleep(1)
            if self.__items is None:
                continue
            currentTime = int(round(time.time())) * 1000
            for item in self.__items:
                if item.firstRun is True:
                    if currentTime > item.initDelay * 1000 + item.startTime:
                        item.firstRun = False
                        item.startts = item.startTime
                        item.endts = currentTime
                        item.startTime = currentTime
                        item.execUrl = API_SCHEDULE_PREFIX + item.execUrl
                        self.__executor.submit(self.__async_task, item)
                else:
                    if currentTime > item.delay * 1000 + item.startTime:
                        item.startts = item.startTime
                        item.endts = currentTime
                        item.startTime = currentTime
                        self.__executor.submit(self.__async_task, item)

    @staticmethod
    def __async_task(item):
        if item.enable:
            logging.info("Schedule Task =>" + item.dids + "<=>" + item.dtags + "<==>" + item.execUrl)
            with httpx.Client(timeout=None, verify=False) as client:
                params = {"devices": item.dids,
                          "tags": item.dtags,
                          "startts": item.startts,
                          "endts": item.endts
                          }
                r = client.post(item.execUrl, json=params)
                logging.info(r)
            try:
                DynamicTask.__updateData(item)
            except Exception as e:
                print(e)
            finally:
                pass

    def async_once_task(self, devs, tags, start, end, displayType, leftTag: int = None,
                        rightTag: int = None, step: int = None, unit: int = None):

        item = TSchedule()
        item.enable = True
        item.dids = json.dumps(devs, ensure_ascii=False)
        item.dtags = json.dumps(tags, ensure_ascii=False)
        item.startts = start
        item.endts = end

        if displayType in [ClusterDisplayUtil.DISPLAY_2D, ClusterDisplayUtil.DISPLAY_3D,
                           ClusterDisplayUtil.DISPLAY_AGG2D, ClusterDisplayUtil.DISPLAY_AGG3D]:
            item.execUrl = API_SCHEDULE_CLUSTER + "?displayType=" + displayType
        elif displayType in [SelfRelationUtil.DISPLAY_SELF_RELATION]:
            item.execUrl = API_SCHEDULE_RELATION + "?leftTag=" + str(
                leftTag) + "&rightTag=" + str(rightTag) + "&step=" + str(step) + "&unit=" + str(unit)
        else:
            item.execUrl = API_SCHEDULE_SOH

        self.__executor.submit(self.__async_task, item)
