from services.main import AppCRUD
from models.tables import TMetricMapping
from schemas.metricMappingModel import MetricMappingModel
from sqlalchemy import and_, desc


class MetricMappingCRUD(AppCRUD):

    def create_record(self, item: MetricMappingModel) -> TMetricMapping:
        record = TMetricMapping(equip_code=item.equip_code,
                                equip_name=item.equip_name,
                                equip_type=item.equip_type,
                                metric_name=item.metric_name,
                                metric_code=item.metric_code,
                                metric_alias=item.metric_alias,
                                )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_record(self, equip_code: str, metric_name: str) -> TMetricMapping:
        record = self.db.query(TMetricMapping).filter(and_(TMetricMapping.equip_code == equip_code,
                                                           TMetricMapping.metric_name == metric_name)).first()
        if record:
            return record
        return None
