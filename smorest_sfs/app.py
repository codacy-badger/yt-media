#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2019 RedLotus <ssfdust@gmail.com>
# Author: RedLotus <ssfdust@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
    app.app
    ~~~~~~~~~~~~~~~~~~~~~~

    实例模块

    包含flask和celery实例
"""

from .factory import create_app

# from .extensions.celery import celery_ext

ENABLED_MODULES = ["auth", "users"]

app = create_app(ENABLED_MODULES)

#  celery = celery_ext.get_celery_app()
