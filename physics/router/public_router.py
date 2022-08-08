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
from fastapi import APIRouter
from typing import Optional

from services.configManagerService import ConfigManagerService

router = APIRouter(
    prefix="/api/v1/public",
    tags=["公共配置"],
    responses={404: {"description": "Not found"}},
)


@router.post("/conf/params")
async def modify_primary_conf_params(msHost: Optional[str] = None, mdHost: Optional[str] = None,
                                     dbHost: Optional[str] = None, dbUser: Optional[str] = None,
                                     dbPw: Optional[str] = None, dbName: Optional[str] = None,
                                     grafanaHost: Optional[str] = None, sjzyHost: Optional[str] = None,
                                     schema: Optional[bool] = None, sample: Optional[int] = None,
                                     multiSelf: Optional[bool] = None, clickGap: Optional[int] = None):
    """
    更新MD服务配置
    :param msHost:
    :param mdHost:
    :param dbHost:
    :param dbUser:
    :param dbPw:
    :param dbName:
    :param grafanaHost:
    :param sjzyHost:
    :param schema:
    :param sample:
    :param multiSelf:
    :param clickGap:
    :return:
    """
    return ConfigManagerService.update(msHost, mdHost, dbHost, dbUser, dbPw, dbName,
                                       grafanaHost, sjzyHost, schema, sample, multiSelf, clickGap)


# 查询 MD服务配置
@router.get("/conf/getParams")
async def query_primary_conf_params():
    return ConfigManagerService.query()
