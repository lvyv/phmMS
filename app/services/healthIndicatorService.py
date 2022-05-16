from models.dao_cellpack import CellPackCRUD
from services.main import AppService
from utils.service_result import ServiceResult
from services.convert.convertor_factory import ConvertorFactory


class HealthIndicatorService(AppService):
    # 获取健康指标从评估数据表中获取
    def health_indicator(self, clz, code, type) -> ServiceResult:
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
