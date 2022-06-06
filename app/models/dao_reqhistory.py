import time

from sqlalchemy import and_, desc, or_

from services.main import AppCRUD
from models.tables import TReqHistory
from schemas.reqhistory_model import ReqItemCreate
from phmconfig import constants as ct


class RequestHistoryCRUD(AppCRUD):
    """
    电池模型请求数据访问。
    """

    def create_record(self, item: ReqItemCreate) -> TReqHistory:
        record = TReqHistory(model=item.model,
                             status=item.status,
                             result=item.result,
                             requestts=item.requestts,
                             memo=item.memo,
                             metrics=item.metrics,
                             displayType=item.displayType,
                             startTs=item.startTs,
                             endTs=item.endTs)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def update_record(self, reqid, result) -> TReqHistory:
        record = self.db.query(TReqHistory).filter(TReqHistory.id == reqid).first()
        record.status = ct.REQ_STATUS_SETTLED
        record.result = result
        record.settledts = int(time.time() * 1000)
        self.db.commit()
        return record

    def get_record_last(self, equipCode: str, metrics: str, displayType: str) -> TReqHistory:
        record = self.db.query(TReqHistory).filter(and_(TReqHistory.memo == equipCode,
                                                        TReqHistory.metrics == metrics,
                                                        TReqHistory.status == ct.REQ_STATUS_SETTLED,
                                                        TReqHistory.displayType == displayType)) \
            .order_by(desc(TReqHistory.id)).first()
        if record:
            return record
        return None

    def get_records(self, equipCode: str, metrics: str, displayType: str, start: int, end: int) -> TReqHistory:
        records = self.db.query(TReqHistory).filter(and_(TReqHistory.memo == equipCode,
                                                         TReqHistory.metrics == metrics,
                                                         TReqHistory.status == ct.REQ_STATUS_SETTLED,
                                                         TReqHistory.displayType == displayType,
                                                         or_(TReqHistory.startTs.between(start, end),
                                                             TReqHistory.endTs.between(start, end),
                                                             and_(TReqHistory.startTs >= start,
                                                                  TReqHistory.endTs <= end),
                                                             and_(TReqHistory.startTs <= start,
                                                                  TReqHistory.endTs >= end)
                                                             )
                                                         )).all()
        return records

    def get_records_prefect_match(self, equipCode: str, metrics: str,
                                  displayType: str, start: int, end: int) -> TReqHistory:
        records = self.db.query(TReqHistory).filter(and_(TReqHistory.memo == equipCode,
                                                         TReqHistory.metrics == metrics,
                                                         TReqHistory.status == ct.REQ_STATUS_SETTLED,
                                                         TReqHistory.displayType == displayType,
                                                         and_(TReqHistory.startTs == start,
                                                              TReqHistory.endTs == end))).all()
        return records

    # 获取时间片段
    def get_time_segment(self, equipCode: str, metrics: str, displayType: str):
        records = self.db.query(TReqHistory).filter(and_(TReqHistory.memo == equipCode,
                                                         TReqHistory.status == ct.REQ_STATUS_SETTLED,
                                                         TReqHistory.metrics == metrics,
                                                         TReqHistory.displayType == displayType)).all()
        return records

    def get_records_by_displayType(self, displayType):
        records = self.db.query(TReqHistory).filter(and_(TReqHistory.displayType == displayType,
                                                         TReqHistory.status == ct.REQ_STATUS_SETTLED)).all()
        return records
