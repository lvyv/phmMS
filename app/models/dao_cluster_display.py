from services.main import AppCRUD
from models.tables import TCluster2D
from schemas.vrla.cluster_model import Cluster2DModel
from sqlalchemy import and_


class Cluster2DCRUD(AppCRUD):
    def create_record(self, item: Cluster2DModel) -> TCluster2D:
        reqdao = TCluster2D(ts=item.ts,  # 主键
                            reqId=item.reqId,
                            x=item.x,
                            y=item.y,
                            color=item.color,
                            size=item.size,
                            shape=item.shape,
                            name=item.name
                            )
        self.db.add(reqdao)
        self.db.commit()
        self.db.refresh(reqdao)
        return reqdao

    def get_records(self, reqId: int, start: int, end: int) -> TCluster2D:
        records = self.db.query(TCluster2D).filter(and_(TCluster2D.reqId == reqId,
                                                        TCluster2D.ts.between(start, end)
                                                        )).all()
        return records
