import json

import constants
from models.dao_reqhistory import RequestHistoryCRUD
from services.main import AppService
from models.dao_cellpack import CellPackCRUD
from utils.service_result import ServiceResult
from utils.payload_util import PayloadUtil
from services.convert.convertor_factory import ConvertorFactory


class CellPackService(AppService):
    def create_item(self, pi) -> ServiceResult:
        item = CellPackCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    def health_eval(self, clz, code, metrics, payload, allMetrics) -> ServiceResult:
        start = PayloadUtil.get_start_time(payload)
        end = PayloadUtil.get_end_time(payload)

        if constants.MODEL_SCHEDULE_PREFECT_MATCH is True:
            devs = code.split(",")
            devs.sort()
            # TODO fix metrics -> allMetrics
            tags = allMetrics.split(",")
            tags.sort()
            hisRecordId = []
            hisRecords = RequestHistoryCRUD(self.db).get_records(json.dumps(devs, ensure_ascii=False),
                                                                 json.dumps(tags, ensure_ascii=False),
                                                                 "EVAL", start, end)
            for his in hisRecords:
                hisRecordId.append(his.id)
            if len(hisRecordId) == 0:
                items = None
            else:
                items = CellPackCRUD(self.db).get_records_by_reqIds(hisRecordId)
        else:
            items = CellPackCRUD(self.db).get_records(code, start, end)
        if items is None:
            return ServiceResult(None)
        convertor = ConvertorFactory.get_convertor(clz)
        if convertor is None:
            return ServiceResult(None)
        convertItems = convertor.convert(items, metrics)
        return ServiceResult(convertItems)
