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
    app.modules
    ~~~~~~~~~~~~~~~~~~~~~

    项目的核心模块，主要处理HTTP请求与返回，定义
    基本的方法以及序列化类，而核心业务则放在services
    模块。
"""
from importlib import import_module
from typing import NoReturn
from flask import Flask
from smorest_sfs.extensions import api


def preload_module(module: str):
    if hasattr(module, "preload_modules"):
        for submodule in module.preload_modules:
            import_module(f".modules.{module}.{submodule}", "smorest_sfs")


def init_app(app: Flask):
    """
    初始化模块
    """

    module_names = app.config["ENABLED_MODULES"]
    base_prefix = (
        app.config["MODULE_BASE_PREFIX"] if "MODULE_BASE_PREFIX" in app.config else ""
    )

    for module_name in module_names:
        preload_module(module_name)
        module = import_module(f".modules.{module_name}", "smorest_sfs")
        api.register_blueprint(module.blp, base_prefix=base_prefix)