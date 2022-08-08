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
import json
import logging
import time

from models.dao_reqhistory import RequestHistoryCRUD
from services.convert.health_eval_util import HealthEvalUtil
from services.main import AppService
from services.schedule.dynamic_task import DynamicTask
from utils.payload_util import PayloadUtil
from services.convert.cluster_display_util import ClusterDisplayUtil
from services.convert.self_relation_util import SelfRelationUtil
from phmconfig import constants
from utils.time_util import TimeUtil


class BegForService(AppService):

    # equipCode 装备编码
    # metrics 测点名称
    # displayType 模型类型
    # payload  负载， 包含 start end  interval
    def exec(self, equipTypeCode: str, equipCode: str, metrics: str, displayType: str, payload: dict,
             subfrom: int = None, subto: int = None):

        if PayloadUtil.check_relative_time_valid(payload) is False:
            # logging.info("输入的时间不合法,不进行调度")
            return
        # 转换成时间戳
        start_orgin = start = PayloadUtil.get_start_time(payload)
        end_orgin = end = PayloadUtil.get_end_time(payload)

        # 装备编码、测点名称 排序
        devs = equipCode.split(",")
        devs.sort()
        tags = metrics.split(",")
        tags.sort()

        # 查询历史记录
        if displayType in [ClusterDisplayUtil.DISPLAY_2D, ClusterDisplayUtil.DISPLAY_3D,
                           ClusterDisplayUtil.DISPLAY_AGG2D, ClusterDisplayUtil.DISPLAY_AGG3D,
                           SelfRelationUtil.DISPLAY_SELF_RELATION, SelfRelationUtil.DISPLAY_SELF_RELATION_POLYLINE,
                           ClusterDisplayUtil.DISPLAY_SCATTER, ClusterDisplayUtil.DISPLAY_POLYLINE,
                           HealthEvalUtil.DISPLAY_HEALTH_EVAL]:
            hisRecords = RequestHistoryCRUD(self.db).get_records_prefect_match(json.dumps(devs, ensure_ascii=False),
                                                                               json.dumps(tags, ensure_ascii=False),
                                                                               displayType, start, end)

            hisRecords = BegForService.process_special_his_records(hisRecords, displayType, subfrom, subto)
        else:
            return None

        # 若无历史记录，执行调度任务
        if len(hisRecords) <= 0:
            DynamicTask().async_once_task(equipTypeCode, devs, tags, start_orgin, end_orgin,
                                          displayType, subfrom, subto)

    @staticmethod
    def process_special_his_records(hisRecords, displayType, subFrom, subTo):
        found = False
        if displayType in [SelfRelationUtil.DISPLAY_SELF_RELATION]:
            for it in hisRecords:
                params = json.loads(it.params)
                if params["subFrom"] == subFrom and params["subTo"] == subTo:
                    found = True
            if found is False:
                return []
        return hisRecords

    @staticmethod
    def convert_time_stamp_utc(timeStr):
        # 2022-02-13 22:09:59
        timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp * 1000

    @staticmethod
    def enlarge_timeline(timestamp: int):
        time_tuple = time.localtime(timestamp / 1000)
        bj_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
        date = bj_time.split(" ")[0]
        start = BegForService.convert_time_stamp_utc(date + " 00:00:00")
        end = BegForService.convert_time_stamp_utc(date + " 23:59:59")
        return start, end

    @staticmethod
    def getPlayLoadByTimeSegment(timeSegment):
        ts = timeSegment.split("至")
        if len(ts) != 2:
            return None
        if constants.TIME_SEGMENT_SHOW_UTF8 is True:
            from_ = TimeUtil.convert_time_utc_str(BegForService.convert_time_stamp_utc(ts[0]))
            to_ = TimeUtil.convert_time_utc_str(BegForService.convert_time_stamp_utc(ts[1]))
            payload = {"range": {"from": from_, "to": to_}}
        else:
            payload = {"range": {"from": ts[0], "to": ts[1]}}
        return payload
