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

from smorest_sfs.modules.storages.models import Storages
from smorest_sfs.modules.users.models import User
from smorest_sfs.modules.roles.models import Role

ADMIN_AVATOR = {
    "name": "AdminAvator.jpg",
    "storetype": "avator",
    "saved": True,
    "filetype": "image/jpeg",
    "path": "default/AdminAvator.jpg",
}
USER_AVATOR = {
    "name": "DefaultAvator.jpg",
    "storetype": "avator",
    "saved": True,
    "filetype": "image/jpeg",
    "path": "default/DefaultAvator.jpg",
}


def create_user(user: User, is_admin: bool = False) -> User:
    """
    创建用户

    :param              user: User                  用户ORM
    :param              is_admin: bool              是否admin

    创建头像信息,创建用户基本信息
    """
    user.roles = Role.get_by_user_default(is_admin)
    avator = Storages(**ADMIN_AVATOR) if is_admin else Storages(**USER_AVATOR)
    user.userinfo.avator = avator
    return user.save()
