import json
import time

from models.dao_reqhistory import RequestHistoryCRUD
from services.main import AppService
from services.schedule.dynamic_task import DynamicTask
from utils.payload_util import PayloadUtil
from services.convert.cluster_display_util import ClusterDisplayUtil
from services.convert.self_relation_util import SelfRelationUtil
from phmconfig import constants


class BegForService(AppService):

    # equipCode 装备编码
    # metrics 测点名称
    # displayType 模型类型
    # payload  负载， 包含 start end  interval
    def exec(self, equipCode: str, metrics: str, displayType: str, payload: dict,
             leftTag: int = None, rightTag: int = None, step: int = None, unit: int = None):
        # 转换成时间戳
        start = PayloadUtil.get_start_time(payload)
        end = PayloadUtil.get_end_time(payload)
        # 通过时间戳 获取日期
        if constants.PREFECT_MATCH_HISTORY_QUERY_RECORD is False:
            start, _ = BegForService.enlarge_timeline(start)
            _, end = BegForService.enlarge_timeline(end)

        # 装备编码、测点名称 排序
        devs = equipCode.split(",")
        devs.sort()
        tags = metrics.split(",")
        tags.sort()

        # 查询历史记录
        if displayType in [ClusterDisplayUtil.DISPLAY_2D, ClusterDisplayUtil.DISPLAY_3D,
                           ClusterDisplayUtil.DISPLAY_AGG2D, ClusterDisplayUtil.DISPLAY_AGG3D,
                           SelfRelationUtil.DISPLAY_SELF_RELATION]:
            if constants.PREFECT_MATCH_HISTORY_QUERY_RECORD is False:
                hisRecords = RequestHistoryCRUD(self.db).get_records(json.dumps(devs, ensure_ascii=False),
                                                                     json.dumps(tags, ensure_ascii=False),
                                                                     displayType, start, end)
            else:
                hisRecords = RequestHistoryCRUD(self.db).get_records_prefect_match(json.dumps(devs, ensure_ascii=False),
                                                                                   json.dumps(tags, ensure_ascii=False),
                                                                                   displayType, start, end)
        else:
            if constants.PREFECT_MATCH_HISTORY_QUERY_RECORD is False:
                hisRecords = RequestHistoryCRUD(self.db).get_eval_records(json.dumps(devs, ensure_ascii=False),
                                                                          "EVAL", start, end)
            else:
                hisRecords = RequestHistoryCRUD(self.db).get_eval_records_prefect_match(
                    json.dumps(devs, ensure_ascii=False),
                    "EVAL", start, end)

        # 若无历史记录，执行调度任务
        if len(hisRecords) <= 0:
            DynamicTask().async_once_task(devs, tags, start, end, displayType, leftTag, rightTag, step, unit)

    @staticmethod
    def convert_time_stamp_utc(timeStr):
        # 2022-02-13 22:09:59
        timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp * 1000

    @staticmethod
    def enlarge_timeline(timestamp: int):
        time_tuple = time.localtime(timestamp / 1000)
        bj_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
        date = bj_time.split(" ")[0]
        start = BegForService.convert_time_stamp_utc(date + " 00:00:00")
        end = BegForService.convert_time_stamp_utc(date + " 23:59:59")
        return start, end

    @staticmethod
    def getPlayLoadByTimeSegment(timeSegment):
        ts = timeSegment.split(",")
        if len(ts) != 2:
            return None
        payload = {"range": {"from": ts[0], "to": ts[1]}}
        return payload
