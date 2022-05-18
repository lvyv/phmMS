from services.main import AppService
from models.dao_metric_mapping import MetricMappingCRUD
from utils.service_result import ServiceResult
from schemas.metricMappingModel import MetricMappingModel


class MetricMappingService(AppService):
    def create_item(self, pi) -> ServiceResult:
        item = MetricMappingCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    def update_item(self, metricCode, item) -> ServiceResult:
        item = MetricMappingCRUD(self.db).update_record(metricCode, item)
        return ServiceResult(item)

    def get_all_mapping(self, equipType):
        items = MetricMappingCRUD(self.db).get_all(equipType)
        mapping = {}
        for item in items:
            if item.metric_alias not in mapping.keys():
                mapping[item.metric_alias] = item.metric_name
        return mapping

    def update_all_mapping(self, equipType, mappings):
        if mappings is None:
            return
        items = MetricMappingCRUD(self.db).get_all(equipType)
        if items is None:
            for mapping in mappings:
                mmm = MetricMappingModel(metric_name=mapping["metricName"],
                                         metric_code=mapping["metricCode"],
                                         equip_name=mapping["equipName"],
                                         equip_type=equipType,
                                         equip_code=mapping["equipCode"],
                                         metric_alias='',
                                         metric_describe='')
                self.create_item(mmm)
        else:
            for mapping in mappings:
                found = False
                for item in items:
                    if item.metric_code == mapping["metricCode"]:
                        found = True
                        if item.metric_name != mapping["metricName"]:
                            # 更新数据库
                            item.metric_name = mapping["metricName"]
                            item.equip_name = mapping["equipName"]
                            self.update_item(item.metric_code, item)
                        elif item.equip_name != mapping["equipName"]:
                            # 更新数据库
                            item.equip_name = mapping["equipName"]
                            self.update_item(item.metric_code, item)
                if found is False:
                    # 新增记录
                    mmm = MetricMappingModel(
                        metric_name=mapping["metricName"],
                        metric_code=mapping["metricCode"],
                        equip_name=mapping["equipName"],
                        equip_type=equipType,
                        equip_code=mapping["equipCode"],
                        metric_alias='',
                        metric_describe=''
                    )
                    self.create_item(mmm)
