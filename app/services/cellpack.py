from services.main import AppService
from models.dao_cellpack import CellPackCRUD
from utils.service_result import ServiceResult
from utils.payload_util import PayloadUtil
from services.convert.cellpack_convertor import CellPackConvertor


class CellPackService(AppService):
    def create_item(self, pi) -> ServiceResult:
        item = CellPackCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    def get_item(self, pi) -> ServiceResult:
        item = CellPackCRUD(self.db).get_record(pi)
        return ServiceResult(item)

    def health_eval(self, type, code, metrics, payload) -> ServiceResult:
        start = PayloadUtil.get_start_time(payload)
        end = PayloadUtil.get_end_time(payload)
        items = CellPackCRUD(self.db).get_records(code, start, end)
        if items is None:
            return ServiceResult(None)
        convertItems = CellPackConvertor.convert(items, metrics)
        return ServiceResult(convertItems)

