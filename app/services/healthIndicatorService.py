from models.dao_cellpack import CellPackCRUD
from services.main import AppService
from models.dao_health_indicator import HealthIndicatorCRUD
from utils.service_result import ServiceResult
from services.convert.convertor_factory import ConvertorFactory


class HealthIndicatorService(AppService):
    def create_item(self, pi) -> ServiceResult:
        item = HealthIndicatorCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    def get_item(self, pi) -> ServiceResult:
        item = HealthIndicatorCRUD(self.db).get_record(pi)
        return ServiceResult(item)

    def health_indicator(self, clz, code, type) -> ServiceResult:
        codes = code.split(",")
        if type == '0' or 0:
            limit = 1
        else:
            limit = 50
        items = HealthIndicatorCRUD(self.db).get_records(codes, limit)
        if items is None:
            return ServiceResult(None)
        convertor = ConvertorFactory.get_convertor(clz)
        if convertor is None:
            return ServiceResult(None)
        convertItems = convertor.convertHealthIndicator(items)
        return ServiceResult(convertItems)

    # 获取健康指标从评估数据表中获取
    def health_indicator2(self, clz, code, type) -> ServiceResult:
        devs = code.split(",")
        if type == '0' or 0:
            limit = 1
        else:
            limit = 50
        items = CellPackCRUD(self.db).get_records_by_limit(devs, limit)
        if items is None:
            return ServiceResult(None)
        convertor = ConvertorFactory.get_convertor(clz)
        if convertor is None:
            return ServiceResult(None)
        convertItems = convertor.convertHealthIndicator(items)
        return ServiceResult(convertItems)
