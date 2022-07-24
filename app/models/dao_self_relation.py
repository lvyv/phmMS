import time

from services.main import AppCRUD
from models.tables import TSelfRelation
from schemas.vrla.self_relation_model import SelfRelationModel
from sqlalchemy import and_


class SelfRelationCRUD(AppCRUD):
    """
    自相关CRUD操作类
    """

    def create_record(self, item: SelfRelationModel) -> TSelfRelation:
        """
        添加一条自相关记录
        """
        reqdao = TSelfRelation(ts=item.ts,
                               reqId=item.reqId,
                               lag=item.lag,
                               value=item.value,
                               own_key=item.own_key
                               )
        self.db.add(reqdao)
        self.db.commit()
        self.db.refresh(reqdao)
        return reqdao

    def create_batch(self, reqid, items) -> TSelfRelation:
        """
        批量添加自相关记录
        """
        batch = []
        for did in items.keys():
            eqitem = items[did]
            for index, item in enumerate(eqitem["lag"]):
                reqdao = TSelfRelation(ts=int(time.time() * 1000),
                                       reqId=reqid,
                                       lag=item,
                                       value=eqitem["value"][index],
                                       own_key=did
                                       )
                batch.append(reqdao)
        self.db.add_all(batch)
        self.db.commit()
        return reqdao

    def get_records(self, reqIds: []) -> TSelfRelation:
        """
        通过请求ID列表获取记录列表
        """
        records = self.db.query(TSelfRelation).filter(TSelfRelation.reqId.in_(reqIds)).all()
        return records

    def delete_record(self, reqid):
        """
        通过请求ID删除记录
        """
        self.db.query(TSelfRelation).filter(TSelfRelation.reqId == reqid).delete()
        self.db.commit()
