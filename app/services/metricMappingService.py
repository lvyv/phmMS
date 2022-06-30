from services.main import AppService
from models.dao_metric_mapping import MetricMappingCRUD
from utils.service_result import ServiceResult
from schemas.metricMappingModel import MetricMappingModel


class MetricMappingService(AppService):
    def create_item(self, pi) -> ServiceResult:
        item = MetricMappingCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    def update_item(self, item) -> ServiceResult:
        item = MetricMappingCRUD(self.db).update_record(item)
        return ServiceResult(item)

    def get_all_mapping_by_equip_type_code(self, equipTypeCode):
        items = MetricMappingCRUD(self.db).get_all(equipTypeCode)
        if items is None:
            return None
        mapping = {}
        for item in items:
            if item.metric_alias not in mapping.keys():
                # fix bug
                if item.metric_alias is not None and item.metric_alias != '':
                    mapping[item.metric_alias] = item.metric_name
        return mapping

    def get_items_by_equip_type_code(self, equipTypeCode):
        return ServiceResult(MetricMappingCRUD(self.db).get_all(equipTypeCode))

    def update_all_mapping(self, equipTypeCode, mappings, equipType):
        if mappings is None:
            return

        items = MetricMappingCRUD(self.db).get_all(equipTypeCode)

        if items is None:
            for mapping in mappings:
                if mapping["equipTypeCode"] != equipTypeCode:
                    continue
                mmm = MetricMappingModel(metric_name=mapping["metricName"],
                                         metric_code='',
                                         equip_name='',
                                         equip_type=equipType,
                                         equip_type_code=mapping["equipTypeCode"],
                                         equip_code='',
                                         metric_alias=mapping["metricAlias"] if "metricAlias" in mapping.keys() else '',
                                         metric_unit=mapping["metricUnit"],
                                         metric_describe='')
                self.create_item(mmm)
        else:
            for mapping in mappings:
                found = False
                for item in items:
                    if item.metric_name == mapping["metricName"]:
                        found = True
                        if item.metric_unit != mapping["metricUnit"] or item.equip_type != equipType:
                            item.equip_type = equipType
                            item.metric_unit = mapping["metricUnit"]
                            if "metricAlias" in mapping.keys():
                                item.metric_alias = mapping["metricAlias"]
                            self.update_item(item)
                if found is False:
                    # 新增记录
                    if mapping["equipTypeCode"] != equipTypeCode:
                        continue
                    mmm = MetricMappingModel(
                        metric_name=mapping["metricName"],
                        metric_code='',
                        equip_name='',
                        equip_type=equipType,
                        equip_type_code=mapping["equipTypeCode"],
                        equip_code='',
                        metric_alias=mapping["metricAlias"] if "metricAlias" in mapping.keys() else '',
                        metric_unit=mapping["metricUnit"],
                        metric_describe=''
                    )
                    self.create_item(mmm)
        items = MetricMappingCRUD(self.db).get_all(equipTypeCode)
        return ServiceResult(items)

    def update_all_metric_alias(self, equipTypeCode, metricName, metric_alias, metric_describe):
        items = MetricMappingCRUD(self.db).get_record_by_type_and_name(equipTypeCode, metricName)
        if items is None:
            return ServiceResult("测点名称在数据库中不存在")
        for item in items:
            item.metric_alias = metric_alias
            item.metric_describe = metric_describe
            self.update_item(item)
        items = MetricMappingCRUD(self.db).get_record_by_type_and_name(equipTypeCode, metricName)
        return ServiceResult(items)

    def delete_by_equip_type_code(self, equip_type_code):
        MetricMappingCRUD(self.db).delete_record(equip_type_code)
