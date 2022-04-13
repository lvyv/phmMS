from services.main import AppCRUD
from models.tables import TSelfRelation
from schemas.vrla.self_relation_model import SelfRelationModel
from sqlalchemy import and_


class SelfRelationCRUD(AppCRUD):
    def create_record(self, item: SelfRelationModel) -> TSelfRelation:
        reqdao = TSelfRelation(ts=item.ts,
                               reqId=item.reqId,
                               lag=item.lag,
                               value=item.value
                               )
        self.db.add(reqdao)
        self.db.commit()
        self.db.refresh(reqdao)
        return reqdao

    def get_records(self, reqIds: []) -> TSelfRelation:
        records = self.db.query(TSelfRelation).filter(TSelfRelation.reqId.in_(reqIds)).all()
        return records
