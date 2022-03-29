from services.main import AppCRUD
from models.tables import TCluster
from schemas.vrla.cluster_model import ClusterModel
from sqlalchemy import and_


class ClusterCRUD(AppCRUD):
    def create_record(self, item: ClusterModel) -> TCluster:
        reqdao = TCluster(ts=item.ts,  # 主键
                          reqId=item.reqId,
                          x=item.x,
                          y=item.y,
                          z=item.z,
                          color=item.color,
                          size=item.size,
                          shape=item.shape,
                          name=item.name
                          )
        self.db.add(reqdao)
        self.db.commit()
        self.db.refresh(reqdao)
        return reqdao

    def get_records(self, reqId: int, start: int, end: int) -> TCluster:
        records = self.db.query(TCluster).filter(and_(TCluster.reqId == reqId,
                                                      TCluster.ts.between(start, end)
                                                      )).all()
        return records

    def get_records_byIds(self, reqIds: [], start: int, end: int) -> TCluster:
        records = self.db.query(TCluster).filter(and_(TCluster.reqId.in_(reqIds),
                                                      TCluster.ts.between(start, end)
                                                      )).all()
        return records
