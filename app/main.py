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
entrypoint of the app
=========================

三层架构应用程序的主入口.
"""
from mqtt.mqttclient import MqttClient
from services.schedule.dynamic_task import DynamicTask
from utils.app_exceptions import AppExceptionCase
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import schedule_model_router, reqhistory_router, cellpack_router, config_router
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from utils.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)
from utils.app_exceptions import app_exception_handler
import threading
import models.tables as tb
import logging
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 支持跨域
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount('/static', StaticFiles(directory='../swagger_ui_dep/static'), name='static')
logging.info(f'Worker Thread: {threading.current_thread().ident:6}     tables {tb.TABLES}.')

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


app.include_router(reqhistory_router.router)
app.include_router(schedule_model_router.router)
app.include_router(cellpack_router.router)
app.include_router(config_router.router)


def startMqtt():
    MqttClient().start()


logging.info(f'dynamic task start up.')
DynamicTask().start()
logging.info(f'mqtt client start up.')
threading.Thread(target=startMqtt()).start()
