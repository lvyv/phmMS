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

    def get_records(self, reqId: int, start: int, end: int) -> TSelfRelation:
        records = self.db.query(TSelfRelation).filter(and_(TSelfRelation.reqId == reqId,
                                                           TSelfRelation.ts.between(start, end)
                                                           )).all()
        return records

    def get_records_byIds(self, reqIds: [], start: int, end: int) -> TSelfRelation:
        records = self.db.query(TSelfRelation).filter(and_(TSelfRelation.reqId.in_(reqIds),
                                                           TSelfRelation.ts.between(start, end)
                                                           )).all()
        return records
