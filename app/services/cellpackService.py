import json

from phmconfig import constants
from models.dao_reqhistory import RequestHistoryCRUD
from services.convert.health_eval_util import HealthEvalUtil
from services.main import AppService
from models.dao_cellpack import CellPackCRUD
from utils.service_result import ServiceResult
from utils.payload_util import PayloadUtil
from services.convert.convertor_factory import ConvertorFactory


class CellPackService(AppService):
    def create_item(self, pi) -> ServiceResult:
        item = CellPackCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    def create_batch(self, reqid,  items) -> ServiceResult:

        # TODO 通过 reqid 查询到 equipTypeCode
        rhi = RequestHistoryCRUD(self.db).get_record_by_id(reqid)
        if rhi is None:
            clz = "N/A"
        else:
            clz = rhi.model

        items = CellPackCRUD(self.db).create_batch(reqid, items, clz)
        return ServiceResult(items)

    def health_eval(self, clz, code, metrics, payload, allMetrics) -> ServiceResult:
        """
        从数据库中查询健康评估数据
        :param clz: 装备类型编码
        :param code:  设备
        :param metrics: 测点
        :param payload:  时间段
        :param allMetrics:  全部测点
        :return:
        """
        start = PayloadUtil.get_start_time(payload)
        end = PayloadUtil.get_end_time(payload)

        devs = code.split(",")
        devs.sort()
        # TODO fix metrics -> allMetrics
        tags = allMetrics.split(",")
        tags.sort()

        hisRecordId = []

        # 查询历史记录
        hisRecords = RequestHistoryCRUD(self.db).get_records_prefect_match(json.dumps(devs, ensure_ascii=False),
                                                                           json.dumps(tags, ensure_ascii=False),
                                                                           HealthEvalUtil.DISPLAY_HEALTH_EVAL,
                                                                           start, end)
        for his in hisRecords:
            hisRecordId.append(his.id)
        if len(hisRecordId) == 0:
            items = None
        else:
            items = CellPackCRUD(self.db).get_records_by_reqIds(hisRecordId)

        if items is None or len(items) == 0:
            return ServiceResult("评估模型正在调度中，请稍等...")
        convertor = ConvertorFactory.get_convertor(clz)
        if convertor is None:
            return ServiceResult("equipType只支持battery")
        # 数据转换
        convertItems = convertor.convert(items, metrics)
        return ServiceResult(convertItems)
