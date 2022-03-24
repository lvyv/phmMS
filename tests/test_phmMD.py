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
phmMD unit test module
=========================

模型微服务测试主入口.
"""

# Author: Awen <26896225@qq.com>
# License: MIT

import unittest
import uvicorn
from physics import __version__
from phmconfig import basiccfg as bcf
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s: %(asctime)s %(filename)s %(message)s',
                    datefmt='%a %d %b %Y %H:%M:%S')


def test_version():
    assert __version__ == "0.1.0"


class TestMain(unittest.TestCase):
    """
    Tests for `健康模型构件` entrypoint.
    本测试案例启动整个健康模型构件（可以在数据资源集成分系统的算法开发软件中部署的模型协同工作）
    访问运行本案例的URL：
    https://IP:29081/docs，执行POST /subprocess，发送start/stop命令启停视频识别流水线。
    注意
    """
    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_Main(self):
        """Test physics.main:app"""
        logging.info(f'********************  CASICLOUD AI METER services  ********************')
        logging.info(f'phmMD is starting...')
        logging.info(f'phmMD micro service starting at {bcf.PHMMD_HOST}: {bcf.PHMMD_PORT}')
        uvicorn.run('physics.main:app',  # noqa 标准用法
                host=bcf.PHMMD_HOST,
                port=bcf.PHMMD_PORT,
                ssl_keyfile=bcf.PHMMD_KEY,
                ssl_certfile=bcf.PHMMD_CER,
                log_level='warning',
                workers=1
                )


if __name__ == "__main__":
    unittest.main()
