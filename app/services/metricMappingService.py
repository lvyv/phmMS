from services.main import AppService
from models.dao_metric_mapping import MetricMappingCRUD
from utils.service_result import ServiceResult


class MetricMappingService(AppService):
    def create_item(self, pi) -> ServiceResult:
        item = MetricMappingCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    # 通过装备编码，测点名称，查询测点别名
    def get_item(self, equipCode, metricName) -> ServiceResult:
        item = MetricMappingCRUD(self.db).get_record(equipCode, metricName)
        return ServiceResult(item)
