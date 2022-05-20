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
        items = MetricMappingCRUD(self.db).get_all_by_equip_type(equipType)
        if items is None:
            return None
        mapping = {}
        for item in items:
            if item.metric_alias not in mapping.keys():
                # fix bug
                if item.metric_alias is not None and item.metric_alias != '':
                    mapping[item.metric_alias] = item.metric_name
        return mapping

    def get_all_mapping_by_equip_type_code(self, equipCode):

        oneRecord = MetricMappingCRUD(self.db).get_one_by_equip_code(equipCode)
        if oneRecord is None:
            return None
        equipTypeCode = oneRecord.equip_type_code
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

    def update_all_mapping(self, equipTypeCode, mappings):
        if mappings is None:
            return
        items = MetricMappingCRUD(self.db).get_all(equipTypeCode)
        if items is None:
            for mapping in mappings:
                if mapping["equipTypeCode"] != equipTypeCode:
                    continue
                mmm = MetricMappingModel(metric_name=mapping["metricName"],
                                         metric_code=mapping["metricCode"],
                                         equip_name=mapping["equipName"],
                                         equip_type='',
                                         equip_type_code=mapping["equipTypeCode"],
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
                    if mapping["equipTypeCode"] != equipTypeCode:
                        continue
                    mmm = MetricMappingModel(
                        metric_name=mapping["metricName"],
                        metric_code=mapping["metricCode"],
                        equip_name=mapping["equipName"],
                        equip_type='',
                        equip_type_code=mapping["equipTypeCode"],
                        equip_code=mapping["equipCode"],
                        metric_alias='',
                        metric_describe=''
                    )
                    self.create_item(mmm)
        items = MetricMappingCRUD(self.db).get_all(equipTypeCode)
        return ServiceResult(items)

    def update_all_metric_alias(self, equipTypeCode, metricName, metric_alias, equipType, metric_describe):
        items = MetricMappingCRUD(self.db).get_record_by_type_and_name(equipTypeCode, metricName)
        for item in items:
            item.metric_alias = metric_alias
            item.metric_describe = metric_describe
            item.equip_type = equipType
            self.update_item(item.metric_code, item)
        items = MetricMappingCRUD(self.db).get_record_by_type_and_name(equipTypeCode, metricName)
        return ServiceResult(items)
