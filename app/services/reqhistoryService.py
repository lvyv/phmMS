import json

from services.main import AppService
from models.dao_reqhistory import RequestHistoryCRUD
from utils.service_result import ServiceResult

# from utils.app_exceptions import AppException
from utils.time_util import TimeUtil


class ReqHistoryService(AppService):
    def update_item(self, reqid, res) -> ServiceResult:
        req_item = RequestHistoryCRUD(self.db).update_record(reqid, res)
        if not req_item:
            # return ServiceResult(AppException.FooCreateItem())
            pass
        return ServiceResult(req_item)

    def get_time_segment(self, equipCode, metric, displayType):
        devs = equipCode.split(",")
        devs.sort()
        tags = metric.split(",")
        tags.sort()

        record = RequestHistoryCRUD(self.db).get_time_segment(json.dumps(devs, ensure_ascii=False),
                                                              json.dumps(tags, ensure_ascii=False), displayType)
        if len(record) <= 0:
            return ServiceResult(None)
        ret = []
        for item in record:
            if item.startTs <= 0 or item.endTs <= 0:
                continue
            ret.append({
                "equipCode": equipCode,
                "metric": metric,
                "displayType": displayType,
                "timeSegment": ReqHistoryService.convert_time_segment(item.startTs, item.endTs)
            })
        return ServiceResult(ret)

    @staticmethod
    def convert_time_segment(start, end):
        segment = TimeUtil.convert_time_utc_str(start) + "," + TimeUtil.convert_time_utc_str(end)
        return segment

    def get_plugin_all_info(self, displayType):
        record = RequestHistoryCRUD(self.db).get_records_by_displayType(displayType)
        if len(record) <= 0:
            return ServiceResult(None)
        ret = []
        for item in record:
            if item.startTs <= 0 or item.endTs <= 0:
                continue
            ret.append({
                "equipCode": ",".join(it for it in json.loads(item.memo)),
                "metric": ",".join(it for it in json.loads(item.metrics)),
                "displayType": displayType,
                "timeSegment": ReqHistoryService.convert_time_segment(item.startTs, item.endTs)
            })
        return ServiceResult(ret)
