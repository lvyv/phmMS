from services.main import AppService
from models.dao_metric_mapping import MetricMappingCRUD
from utils.service_result import ServiceResult


class MetricMappingService(AppService):
    def create_item(self, pi) -> ServiceResult:
        item = MetricMappingCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    # 通过装备类型，测点名称，查询测点别名
    def get_item(self, equipType, metricName) -> ServiceResult:
        item = MetricMappingCRUD(self.db).get_record(equipType, metricName)
        return ServiceResult(item)

    def get_all_mapping(self, equipType):
        items = MetricMappingCRUD(self.db).get_all(equipType)
        mapping = {}
        for item in items:
            if item.metric_alias not in mapping.keys():
                mapping[item.metric_alias] = item.metric_name
        return mapping
