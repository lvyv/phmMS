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
import logging
from datetime import datetime
from phmconfig import constants


class TimeGrapUtil:
    last_time = 0

    def canClick(self):
        now_time = int(datetime.now().timestamp())
        if self.last_time == 0 or now_time - self.last_time > constants.CLICK_GRAP:
            self.last_time = now_time
            # logging.info("time grap is arrived, can click...")
            return True
        return False
