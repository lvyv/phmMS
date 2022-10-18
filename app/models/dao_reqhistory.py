#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 The CASICloud Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
# pylint: disable=invalid-name
# pylint: disable=missing-docstring
import time

from sqlalchemy import and_, desc, or_, distinct, asc

from services.main import AppCRUD
from models.tables import TReqHistory
from schemas.reqhistory_model import ReqItemCreate
from phmconfig import constants as ct


class RequestHistoryCRUD(AppCRUD):
    """
    历史请求数据访问CRUD。
    """

    def create_record(self, item: ReqItemCreate) -> TReqHistory:
        """
        创建一条历史记录
        """
        record = TReqHistory(model=item.model,
                             status=item.status,
                             result=item.result,
                             requestts=item.requestts,
                             memo=item.memo,
                             metrics=item.metrics,
                             displayType=item.displayType,
                             startTs=item.startTs,
                             endTs=item.endTs,
                             params=item.params
                             )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def update_record(self, reqid, result) -> TReqHistory:
        """
        删除一条记录
        """
        record = self.db.query(TReqHistory).filter(TReqHistory.id == reqid).first()
        record.status = ct.REQ_STATUS_SETTLED
        record.result = result
        record.settledts = int(time.time() * 1000)
        self.db.commit()
        return record

    def get_record_last(self, equipCode: str, metrics: str, displayType: str) -> TReqHistory:
        """
        查询最后一条记录
        """
        record = self.db.query(TReqHistory).filter(and_(TReqHistory.memo == equipCode,
                                                        TReqHistory.metrics == metrics,
                                                        TReqHistory.status == ct.REQ_STATUS_SETTLED,
                                                        TReqHistory.displayType == displayType)) \
            .order_by(desc(TReqHistory.id)).first()
        if record:
            return record
        return None

    def get_records(self, equipCode: str, metrics: str, displayType: str, start: int, end: int) -> TReqHistory:
        """
        模糊匹配查询满足条件记录
        """
        records = self.db.query(TReqHistory).filter(and_(TReqHistory.memo == equipCode,
                                                         TReqHistory.metrics == metrics,
                                                         # TReqHistory.status == ct.REQ_STATUS_SETTLED,
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
        """
        精确匹配查询满足条件记录
        """
        records = self.db.query(TReqHistory).filter(and_(TReqHistory.memo == equipCode,
                                                         TReqHistory.metrics == metrics,
                                                         # TReqHistory.status == ct.REQ_STATUS_SETTLED,
                                                         TReqHistory.displayType == displayType,
                                                         and_(TReqHistory.startTs == start,
                                                              TReqHistory.endTs == end))).all()
        return records

    # 获取时间片段
    def get_time_segment(self, equipCode: str, metrics: str, displayType: str, scheduleState: bool):
        """
        查询满足条件记录
        """
        if scheduleState is True:
            records = self.db.query(TReqHistory).filter(and_(TReqHistory.memo == equipCode,
                                                             TReqHistory.metrics == metrics,
                                                             TReqHistory.displayType == displayType)) \
                .order_by(desc(TReqHistory.startTs), desc(TReqHistory.endTs)).all()
        else:
            records = self.db.query(TReqHistory).filter(and_(TReqHistory.memo == equipCode,
                                                             TReqHistory.status == ct.REQ_STATUS_SETTLED,
                                                             TReqHistory.metrics == metrics,
                                                             TReqHistory.displayType == displayType)) \
                .order_by(desc(TReqHistory.startTs), desc(TReqHistory.endTs)).all()
        return records

    def get_records_by_displayType(self, displayType):
        """
        根据类型查询记录
        """
        records = self.db.query(TReqHistory).filter(and_(TReqHistory.displayType == displayType,
                                                         TReqHistory.status == ct.REQ_STATUS_SETTLED)).all()
        return records

    def get_equip_code(self, displayType):
        """
        根据类型查询记录
        """
        records = self.db.query(TReqHistory).filter(TReqHistory.displayType == displayType) \
            .distinct(TReqHistory.memo).all()
        return records

    def get_equip_metric(self, displayType, equipCode):
        """
        根据类型、装备编码查询记录
        """
        records = self.db.query(TReqHistory).filter(and_(TReqHistory.displayType == displayType,
                                                         TReqHistory.memo == equipCode)) \
            .distinct(TReqHistory.metrics).all()
        return records

    def delete_record(self, reqid):
        """
        根据请求ID删除记录
        """
        self.db.query(TReqHistory).filter(TReqHistory.id == reqid).delete()
        self.db.commit()

    def get_record_by_id(self, reqId):
        """
        根据类型查询记录
        """
        return self.db.query(TReqHistory).filter(TReqHistory.id == reqId).first()

    def get_records_by_model(self, model: str) -> TReqHistory:
        """
        根据equipType查询记录
        """
        records = self.db.query(TReqHistory).filter(TReqHistory.model == model).order_by(asc(TReqHistory.id)).all()
        return records
