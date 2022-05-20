import json

from models.dao_reqhistory import RequestHistoryCRUD
from services.convert.self_relation_util import SelfRelationUtil
from services.main import AppService
from models.dao_self_relation import SelfRelationCRUD
from utils.payload_util import PayloadUtil
from utils.service_result import ServiceResult
from services.convert.convertor_factory import ConvertorFactory


class SelfRelationService(AppService):
    def create_item(self, pi) -> ServiceResult:
        item = SelfRelationCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    def selfRelation(self, clz, code, metrics, leftTag, rightTag, step, unit, payload) -> ServiceResult:

        start = PayloadUtil.get_start_time(payload)
        end = PayloadUtil.get_end_time(payload)

        devs = code.split(",")
        devs.sort()
        tags = metrics.split(",")
        tags.sort()

        hisRecordId = []
        hisRecords = RequestHistoryCRUD(self.db).get_records(json.dumps(devs, ensure_ascii=False),
                                                             json.dumps(tags, ensure_ascii=False),
                                                             SelfRelationUtil.DISPLAY_SELF_RELATION, start, end)
        for his in hisRecords:
            hisRecordId.append(his.id)
        if len(hisRecordId) == 0:
            items = None
        else:
            items = SelfRelationCRUD(self.db).get_records(hisRecordId)
        if items is None:
            return ServiceResult(None)
        convertor = ConvertorFactory.get_convertor(clz)
        if convertor is None:
            return ServiceResult(None)
        convertItems = convertor.convertSelfRelation(items)
        return ServiceResult(convertItems)
