#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

"""
=========================
data access layer
=========================

data access层，负责处理模型调用的历史记录。
"""

# Author: Awen <26896225@qq.com>
# License: MIT

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
                                                        TReqHistory.displayType == displayType)) \
            .order_by(desc(TReqHistory.id)).first()
        if record:
            return record
        return None

    def get_records(self, equipCode: str, metrics: str, displayType: str, start: int, end: int) -> TReqHistory:
        records = self.db.query(TReqHistory).filter(and_(TReqHistory.memo == equipCode,
                                                         TReqHistory.metrics == metrics,
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


