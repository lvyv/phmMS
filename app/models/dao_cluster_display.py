from phmconfig.dataConvertUtil import DataConvertUtil
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

    def create_batch(self, reqid, displayType, items) -> TCluster:
        batch = []
        for did in items.keys():
            item = DataConvertUtil.cluster(reqid, displayType, did, items)
            reqdao = TCluster(ts=item["ts"],  # 主键
                              reqId=reqid,
                              x=item["x"],
                              y=item["y"],
                              z=item["z"],
                              color=item["color"],
                              size=item["size"],
                              shape=item["shape"],
                              name=item["name"]
                              )
            batch.append(reqdao)
        self.db.add_all(batch)
        self.db.commit()
        return reqdao

    def get_records(self, reqIds: []) -> TCluster:
        records = self.db.query(TCluster).filter(TCluster.reqId.in_(reqIds)).all()
        return records

    def delete_record(self, reqid):
        self.db.query(TCluster).filter(TCluster.reqId == reqid).delete()
        self.db.commit()
