from services.main import AppCRUD
from models.tables import THealthIndicator
from schemas.vrla.health_indicator_model import HealthIndicatorModel
from sqlalchemy import desc


class HealthIndicatorCRUD(AppCRUD):
    def create_record(self, item: HealthIndicatorModel) -> THealthIndicator:
        reqdao = THealthIndicator(ts=item.ts,  # 主键
                                  did=item.did,
                                  dclz=item.dclz,
                                  soh=item.soh,
                                  state=item.state
                                  )
        self.db.add(reqdao)
        self.db.commit()
        self.db.refresh(reqdao)
        return reqdao

    def get_records(self, dids, limit) -> THealthIndicator:
        items = []
        for did in dids:
            item = self.db.query(THealthIndicator).filter(THealthIndicator.did == did)\
                .order_by(desc(THealthIndicator.ts)).limit(limit).all()
            if item:
                items.append(item)
        if len(items) == 0:
            return None
        return items
