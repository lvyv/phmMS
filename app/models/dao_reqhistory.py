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

from sqlalchemy import and_, desc

from services.main import AppCRUD
from models.tables import TReqHistory
from schemas.reqhistory_model import ReqItemCreate
from phmconfig import constants as ct


class RequestHistoryCRUD(AppCRUD):
    """
    电池模型请求数据访问。
    """

    def create_record(self, item: ReqItemCreate) -> TReqHistory:
        reqdao = TReqHistory(model=item.model,
                             status=item.status,
                             result=item.result,
                             requestts=item.requestts,
                             memo=item.memo,
                             metrics=item.metrics,
                             displayType=item.displayType,
                             startTs=item.startTs,
                             endTs=item.endTs)
        self.db.add(reqdao)
        self.db.commit()
        self.db.refresh(reqdao)
        return reqdao

    def update_record(self, reqid, result) -> TReqHistory:
        reqdao = self.db.query(TReqHistory).filter(TReqHistory.id == reqid).first()
        reqdao.status = ct.REQ_STATUS_SETTLED
        reqdao.result = result
        reqdao.settledts = int(time.time() * 1000)
        self.db.commit()
        return reqdao

    def get_record(self, reqid: int) -> TReqHistory:
        reqdao = self.db.query(TReqHistory).filter(TReqHistory.id == reqid).first()
        if reqdao:
            return reqdao
        return None

    def get_record_by_condition(self, equipCode: str, metrics: str, displayType: str) -> TReqHistory:
        # TODO fix 查询数据失败
        reqdao = self.db.query(TReqHistory).filter(and_(TReqHistory.memo == equipCode,
                                                        TReqHistory.metrics == metrics,
                                                        TReqHistory.displayType == displayType)) \
            .order_by(desc(TReqHistory.id)).first()
        if reqdao:
            return reqdao
        return None

    def get_records_by_condition(self, equipCode: str, metrics: str, displayType: str) -> TReqHistory:
        records = self.db.query(TReqHistory).filter(and_(TReqHistory.memo == equipCode,
                                                         TReqHistory.metrics == metrics,
                                                         TReqHistory.displayType == displayType)) \
            .all()
        return records
