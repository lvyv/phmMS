from services.main import AppCRUD
from models.tables import TMetricMapping
from schemas.metricMappingModel import MetricMappingModel
from sqlalchemy import and_, desc


class MetricMappingCRUD(AppCRUD):
    """
    测点映射CRUD
    """

    def create_record(self, item: MetricMappingModel) -> TMetricMapping:
        """
        创建测点映射记录
        """
        record = TMetricMapping(
            equip_type=item.equip_type,
            metric_name=item.metric_name,
            metric_alias=item.metric_alias,
            metric_describe=item.metric_describe,
            equip_name=item.equip_name,
            equip_code=item.equip_code,
            metric_code=item.metric_code,
            equip_type_code=item.equip_type_code,
            metric_unit=item.metric_unit
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def update_record(self, item) -> TMetricMapping:
        """
        更新测点映射记录
        """
        self.db.add(item)
        self.db.commit()
        return None

    def get_all(self, equip_type_code: str) -> TMetricMapping:
        """
        根据装备类型编码查询记录
        """
        records = self.db.query(TMetricMapping).filter(TMetricMapping.equip_type_code == equip_type_code).all()
        if records:
            return records
        return None

    def get_all_by_equip_type(self, equip_type: str) -> TMetricMapping:
        """
        根据装备类型查询记录
        """
        records = self.db.query(TMetricMapping).filter(TMetricMapping.equip_type == equip_type).all()
        if records:
            return records
        return None

    def get_record_by_type_and_name(self, equip_type_code, metric_name):
        """
        根据转码类型编码和测点名称查询记录
        """
        records = self.db.query(TMetricMapping).filter(and_(TMetricMapping.equip_type_code == equip_type_code,
                                                            TMetricMapping.metric_name == metric_name)).all()
        if records:
            return records
        return None

    def delete_record(self, equip_type_code):
        """
        根据装备类型编码删除记录
        """
        self.db.query(TMetricMapping).filter(TMetricMapping.equip_type_code == equip_type_code).delete()
        self.db.commit()
