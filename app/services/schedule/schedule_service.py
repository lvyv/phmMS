from services.main import AppService
from models.dao_schedule import ScheduleCRUD
from utils.service_result import ServiceResult


class ScheduleService(AppService):
    def create_item(self, pi) -> ServiceResult:
        item = ScheduleCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    def get_items(self) -> ServiceResult:
        item = ScheduleCRUD(self.db).get_records()
        return ServiceResult(item)

    def del_item(self, id) -> ServiceResult:
        item = ScheduleCRUD(self.db).del_record(id)
        return ServiceResult(item)

    def del_items(self) -> ServiceResult:
        item = ScheduleCRUD(self.db).del_records()
        return ServiceResult(item)
