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
from phmconfig.dataConvertUtil import DataConvertUtil
from services.main import AppCRUD
from models.tables import TCluster
from schemas.vrla.cluster_model import ClusterModel
from sqlalchemy import and_


class ClusterCRUD(AppCRUD):
    """
    聚类CRUD
    """
    def create_record(self, item: ClusterModel) -> TCluster:
        """
        创建一条记录
        """
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
        """
        批量创建记录
        """
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
        """
        根据请求ID列表查询记录
        """
        records = self.db.query(TCluster).filter(TCluster.reqId.in_(reqIds)).all()
        return records

    def delete_record(self, reqid):
        """
        通过请求ID删除记录
        """
        self.db.query(TCluster).filter(TCluster.reqId == reqid).delete()
        self.db.commit()
