from services.main import AppService
from models.dao_cellpack import CellPackCRUD
from utils.service_result import ServiceResult
from utils.payload_util import PayloadUtil
from services.convert.convertor_factory import ConvertorFactory


class CellPackService(AppService):
    def create_item(self, pi) -> ServiceResult:
        item = CellPackCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    def health_eval(self, clz, code, metrics, payload) -> ServiceResult:
        start = PayloadUtil.get_start_time(payload)
        end = PayloadUtil.get_end_time(payload)
        items = CellPackCRUD(self.db).get_records(code, start, end)
        if items is None:
            return ServiceResult(None)
        convertor = ConvertorFactory.get_convertor(clz)
        if convertor is None:
            return ServiceResult(None)
        convertItems = convertor.convert(items, metrics)
        return ServiceResult(convertItems)
