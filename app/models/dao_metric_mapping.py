from services.main import AppCRUD
from models.tables import TMetricMapping
from schemas.metricMappingModel import MetricMappingModel
from sqlalchemy import and_, desc


class MetricMappingCRUD(AppCRUD):

    def create_record(self, item: MetricMappingModel) -> TMetricMapping:
        record = TMetricMapping(
            equip_type=item.equip_type,
            metric_name=item.metric_name,
            metric_alias=item.metric_alias,
            metric_describe=item.metric_describe,
            equip_name=item.equip_name,
            equip_code=item.equip_code,
            metric_code=item.metric_code
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def update_record(self, metric_code: str, item) -> TMetricMapping:
        self.db.add(item)
        self.db.commit()
        return None

    def get_all(self, equip_type: str) -> TMetricMapping:
        records = self.db.query(TMetricMapping).filter(TMetricMapping.equip_type == equip_type).all()
        if records:
            return records
        return None
