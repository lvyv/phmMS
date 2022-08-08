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
from pydantic import BaseModel


class ReqItemBase(BaseModel):
    """
    所有soh请求：
     - status字段，从pending到settled。
     - result字段，从pending到执行的结果。
     - requestts字段，发起调用的时间戳。
     - settledts字段，回调结果的时间戳。
     - memo字段，保存一些额外信息。
    """
    status: str
    result: str
    requestts: int = 0
    settledts: int = 0
    memo: str = ''
    metrics: str = ''
    displayType: str = ''
    startTs: int
    endTs: int
    params: str


class ReqItemCreate(ReqItemBase):
    """
    创建的时候必须提供模型类型。
    """
    model: str


class ReqItem(ReqItemBase):
    """
    获取记录必须提供关键字id。
    """
    id: int

    class Config:
        orm_mode = True
