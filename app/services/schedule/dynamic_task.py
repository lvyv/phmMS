import json
import constants
import httpx
import logging
import threading
from services.convert.cluster_display_util import ClusterDisplayUtil
from services.convert.health_eval_util import HealthEvalUtil
from services.convert.self_relation_util import SelfRelationUtil
import concurrent.futures

API_SCHEDULE_PREFIX = constants.PHMMS_URL_PREFIX + "/api/v1/phm/vrla/"
API_SCHEDULE_SOH = constants.PHMMS_URL_PREFIX + "/api/v1/phm/vrla/soh"
API_SCHEDULE_CLUSTER = constants.PHMMS_URL_PREFIX + "/api/v1/phm/vrla/cluster"
API_SCHEDULE_RELATION = constants.PHMMS_URL_PREFIX + "/api/v1/phm/vrla/relation"


class TSchduleTask:
    dids: str
    dtags: str
    startts: int
    endts: int
    equipTypeCode: str
    execUrl: str


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

    @staticmethod
    def __async_task(item):
        logging.info("Schedule Task =>" + item.dids + "<=>" + item.dtags + "<==>" + item.execUrl)
        with httpx.Client(timeout=None, verify=False) as client:
            params = {"devices": item.dids,
                      "tags": item.dtags,
                      "startts": item.startts,
                      "endts": item.endts,
                      "equipTypeCode": item.equipTypeCode
                      }
            r = client.post(item.execUrl, json=params)
            logging.info(r)

    def async_once_task(self, equipTypeCode, devs, tags, start, end, displayType, subfrom: int = None,
                        subto: int = None):

        if displayType in [ClusterDisplayUtil.DISPLAY_2D, ClusterDisplayUtil.DISPLAY_3D,
                           ClusterDisplayUtil.DISPLAY_AGG2D, ClusterDisplayUtil.DISPLAY_AGG3D]:
            item = DynamicTask.make_t_schedule(devs, tags, start, end)
            item.equipTypeCode = equipTypeCode
            item.execUrl = API_SCHEDULE_CLUSTER + "?displayType=" + displayType
            self.__executor.submit(self.__async_task, item)
        elif displayType in [SelfRelationUtil.DISPLAY_SELF_RELATION]:
            # ??????????????????
            if (start <= subfrom <= end and start <= subto <= end) or (subfrom == -1 and subto == -1):
                item = DynamicTask.make_t_schedule(devs, tags, start, end)
                item.equipTypeCode = equipTypeCode
                item.execUrl = API_SCHEDULE_RELATION + "?subFrom=" + str(
                    subfrom) + "&subTo=" + str(subto)
                self.__executor.submit(self.__async_task, item)
        elif displayType in [ClusterDisplayUtil.DISPLAY_POLYLINE, ClusterDisplayUtil.DISPLAY_SCATTER,
                             SelfRelationUtil.DISPLAY_SELF_RELATION_POLYLINE, HealthEvalUtil.DISPLAY_HEALTH_EVAL]:
            item = DynamicTask.make_t_schedule(devs, tags, start, end)
            item.equipTypeCode = equipTypeCode
            item.execUrl = API_SCHEDULE_SOH + "?displayType=" + displayType
            self.__executor.submit(self.__async_task, item)

    @staticmethod
    def make_t_schedule(devs, tags, start, end):
        item = TSchduleTask()
        item.dids = json.dumps(devs, ensure_ascii=False)
        item.dtags = json.dumps(tags, ensure_ascii=False)
        item.startts = start
        item.endts = end
        return item
