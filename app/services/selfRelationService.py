import json

from phmconfig import constants
from models.dao_cellpack import CellPackCRUD
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

    def create_batch(self, reqid, batch) -> ServiceResult:
        items = SelfRelationCRUD(self.db).create_batch(reqid, batch)
        return ServiceResult(items)

    def selfRelation(self, clz, code, metrics, payload, subFrom, subTo) -> ServiceResult:

        start = PayloadUtil.get_start_time(payload)
        end = PayloadUtil.get_end_time(payload)

        devs = code.split(",")
        devs.sort()
        tags = metrics.split(",")
        tags.sort()
        hisRecordId = []
        hisRecords = RequestHistoryCRUD(self.db).get_records_prefect_match(json.dumps(devs, ensure_ascii=False),
                                                                           json.dumps(tags, ensure_ascii=False),
                                                                           SelfRelationUtil.DISPLAY_SELF_RELATION,
                                                                           start, end)
        if hisRecords is None:
            return ServiceResult("自相关模型未查找到记录...")
        for his in hisRecords:
            params = json.loads(his.params)
            if params["subFrom"] == subFrom and params["subTo"] == subTo:
                hisRecordId.append(his.id)
        if len(hisRecordId) == 0:
            items = None
        else:
            items = SelfRelationCRUD(self.db).get_records(hisRecordId)
        if items is None or len(items) == 0:
            return ServiceResult("自相关模型正在调度中，请稍等...")
        convertor = ConvertorFactory.get_convertor(clz)
        if convertor is None:
            return ServiceResult("equipType只支持battery")
        convertItems = convertor.convertSelfRelationMulti(items)
        return ServiceResult(convertItems)
