import json
import time

from models.dao_reqhistory import RequestHistoryCRUD
from services.main import AppService
from services.schedule.dynamic_task import DynamicTask
from utils.payload_util import PayloadUtil


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
        start, _ = BegForService.enlarge_timeline(start)
        _, end = BegForService.enlarge_timeline(end)

        # 装备编码、测点名称 排序
        devs = equipCode.split(",")
        devs.sort()
        tags = metrics.split(",")
        tags.sort()

        # 查询历史记录
        if displayType in ["EVAL"]:
            hisRecords = RequestHistoryCRUD(self.db).get_eval_records(json.dumps(devs, ensure_ascii=False),
                                                                      displayType, start, end)
        else:
            hisRecords = RequestHistoryCRUD(self.db).get_records(json.dumps(devs, ensure_ascii=False),
                                                                 json.dumps(tags, ensure_ascii=False),
                                                                 displayType, start, end)
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
