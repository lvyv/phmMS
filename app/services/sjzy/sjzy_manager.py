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
from datetime import datetime

from phmconfig import constants
from services.http.dataCenterService import DataCenterService
from services.metricMappingService import MetricMappingService
import logging


class SjzyManager:
    LastTime = 0

    # 根据装备名称，同步测点数据
    def dataSync(self,  equipTypeCode, equipType, db):

        # 每隔5分钟，同步测点
        now_time = int(datetime.now().timestamp())
        if self.LastTime == 0 or now_time - self.LastTime > constants.EQUIP_METRIC_SYNC_GAP:
            self.LastTime = now_time
            logging.info("sync equip metric ...")
        else:
            return None
        # 通过测点
        so = MetricMappingService(db)
        metrics = DataCenterService.download_zb_metric_by_type_code(equipTypeCode)
        # 同步电池测点映射数据
        so.update_all_mapping(equipTypeCode, metrics, equipType)
