from services.main import AppService
from models.dao_cellpack import CellPackCRUD
from utils.service_result import ServiceResult


class CellPackService(AppService):
    def create_item(self, pi) -> ServiceResult:
        item = CellPackCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    def get_item(self, pi) -> ServiceResult:
        item = CellPackCRUD(self.db).get_record(pi)
        return ServiceResult(item)
