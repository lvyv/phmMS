import json

from models.dao_cellpack import CellPackCRUD
from models.dao_cluster_display import ClusterCRUD
from models.dao_self_relation import SelfRelationCRUD
from phmconfig import constants
from services.convert.cluster_display_util import ClusterDisplayUtil
from services.convert.health_eval_util import HealthEvalUtil
from services.convert.self_relation_util import SelfRelationUtil
from services.main import AppService
from models.dao_reqhistory import RequestHistoryCRUD
from services.schedule.beg_for_service import BegForService
from utils.payload_util import PayloadUtil
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
            return ServiceResult([])
        ret = []
        for item in record:
            if item.startTs <= 0 or item.endTs <= 0:
                continue
            # ret.append({
            #     "equipCode": equipCode,
            #     "metric": metric,
            #     "displayType": displayType,
            #     "timeSegment": ReqHistoryService.convert_time_segment(item.startTs, item.endTs)
            # })
            ret.append(ReqHistoryService.convert_time_segment(item.startTs, item.endTs))
        return ServiceResult(ret)

    def delete_time_segment(self, equipCode, metric, timeSegment, displayType):
        devs = equipCode.split(",")
        devs.sort()
        tags = metric.split(",")
        tags.sort()

        payload = BegForService.getPlayLoadByTimeSegment(timeSegment)
        start = PayloadUtil.get_start_time(payload)
        end = PayloadUtil.get_end_time(payload)

        record = RequestHistoryCRUD(self.db).get_records_prefect_match(json.dumps(devs, ensure_ascii=False),
                                                                       json.dumps(tags, ensure_ascii=False),
                                                                       displayType, start, end)

        success = True

        if len(record) > 0:
            for his in record:
                # TODO 删除历史记录
                RequestHistoryCRUD(self.db).delete_record(his.id)
                # TODO 删除数据表
                if displayType in [HealthEvalUtil.DISPLAY_HEALTH_EVAL,
                                   ClusterDisplayUtil.DISPLAY_SCATTER,
                                   ClusterDisplayUtil.DISPLAY_POLYLINE,
                                   SelfRelationUtil.DISPLAY_SELF_RELATION_POLYLINE]:
                    CellPackCRUD(self.db).delete_record(his.id)
                elif displayType in [ClusterDisplayUtil.DISPLAY_2D,
                                     ClusterDisplayUtil.DISPLAY_3D,
                                     ClusterDisplayUtil.DISPLAY_AGG2D,
                                     ClusterDisplayUtil.DISPLAY_AGG3D]:
                    ClusterCRUD(self.db).delete_record(his.id)
                elif displayType in [SelfRelationUtil.DISPLAY_SELF_RELATION]:
                    SelfRelationCRUD(self.db).delete_record(his.id)
                else:
                    success = False
        else:
            success = False

        return ServiceResult(success)

    @staticmethod
    def convert_time_segment(start, end):
        if constants.TIME_SEGMENT_SHOW_UTF8 is True:
            segment = TimeUtil.convert_time_utc_8_str(start) + "至" + TimeUtil.convert_time_utc_8_str(end)
        else:
            segment = TimeUtil.convert_time_utc_str(start) + "至" + TimeUtil.convert_time_utc_str(end)
        return segment

    def get_plugin_all_info(self, displayType):
        record = RequestHistoryCRUD(self.db).get_records_by_displayType(displayType)
        if len(record) <= 0:
            return ServiceResult(None)
        ret = []
        for item in record:
            if item.startTs <= 0 or item.endTs <= 0:
                continue
            # ret.append({
            #     "equipCode": ",".join(it for it in json.loads(item.memo)),
            #     "metric": ",".join(it for it in json.loads(item.metrics)),
            #     "displayType": displayType,
            #     "timeSegment": ReqHistoryService.convert_time_segment(item.startTs, item.endTs)
            # })
            ret.append(ReqHistoryService.convert_time_segment(item.startTs, item.endTs))
        return ServiceResult(ret)

    def get_equip_code(self, displayType):
        record = RequestHistoryCRUD(self.db).get_equip_code(displayType)
        if len(record) <= 0:
            return ServiceResult(None)
        ret = []
        for item in record:
            disguise = ",".join(it for it in json.loads(item.memo))
            ret.append(disguise)
        return ServiceResult(ret)

    def get_equip_metric(self, equipCode, displayType):
        devs = equipCode.split(",")
        devs.sort()

        record = RequestHistoryCRUD(self.db).get_equip_metric(displayType, json.dumps(devs, ensure_ascii=False))
        if len(record) <= 0:
            return ServiceResult(None)
        ret = []
        for item in record:
            disguise = ",".join(it for it in json.loads(item.metrics))
            ret.append(disguise)
        return ServiceResult(ret)

    def get_params(self, equipCode, metric, timeSegment, displayType):
        if displayType not in [SelfRelationUtil.DISPLAY_SELF_RELATION]:
            return ServiceResult([])
        devs = equipCode.split(",")
        devs.sort()
        tags = metric.split(",")
        tags.sort()
        payload = BegForService.getPlayLoadByTimeSegment(timeSegment)
        start = PayloadUtil.get_start_time(payload)
        end = PayloadUtil.get_end_time(payload)
        records = RequestHistoryCRUD(self.db).get_records_prefect_match(json.dumps(devs, ensure_ascii=False),
                                                                        json.dumps(tags, ensure_ascii=False),
                                                                        displayType, start, end)
        ret = []
        for item in records:
            if item.status != constants.REQ_STATUS_SETTLED:
                continue
            param = json.loads(item.params)
            if param["subFrom"] == -1 and param["subTo"] == -1:
                continue
            ret.append(ReqHistoryService.convert_time_segment(param["subFrom"], param["subTo"]))
        return ServiceResult(ret)

    def get_all(self, model):
        records = RequestHistoryCRUD(self.db).get_records_by_model(model)
        return ServiceResult(records)

    def delete_by_id(self, reqId):
        rh = RequestHistoryCRUD(self.db)
        # 获取记录
        record = rh.get_record_by_id(reqId)
        if record is None:
            return ServiceResult(False)
        # 删除记录
        rh.delete_record(reqId)
        # 删除管理数据
        displayType = record.displayType
        if displayType in [HealthEvalUtil.DISPLAY_HEALTH_EVAL,
                           ClusterDisplayUtil.DISPLAY_SCATTER,
                           ClusterDisplayUtil.DISPLAY_POLYLINE,
                           SelfRelationUtil.DISPLAY_SELF_RELATION_POLYLINE]:
            CellPackCRUD(self.db).delete_record(record.id)
        elif displayType in [ClusterDisplayUtil.DISPLAY_2D,
                             ClusterDisplayUtil.DISPLAY_3D,
                             ClusterDisplayUtil.DISPLAY_AGG2D,
                             ClusterDisplayUtil.DISPLAY_AGG3D]:
            ClusterCRUD(self.db).delete_record(record.id)
        elif displayType in [SelfRelationUtil.DISPLAY_SELF_RELATION]:
            SelfRelationCRUD(self.db).delete_record(record.id)

        return ServiceResult(True)
