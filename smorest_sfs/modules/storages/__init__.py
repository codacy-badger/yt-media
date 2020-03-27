#!/usr/bin/env python3
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
    app.modules.storages
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    文件系统模块

    用以管理系统的文件系统，负责文件的跟踪、
    上传与下载。
"""

from flask_smorest import Blueprint
from app.extensions import api

blp = Blueprint("Storages", __name__, url_prefix="/storages", description="文件管理模块")


def init_app(app):
    """初始化模块

    :param              app: Flask                  Flask实例
    """
    from . import resources, models  # pylint: disable=unused-import

    base_prefix = (
        app.config["MODULE_BASE_PREFIX"] if "MODULE_BASE_PREFIX" in app.config else ""
    )

    api.register_blueprint(blp, base_prefix=base_prefix)
