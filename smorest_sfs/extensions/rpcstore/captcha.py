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
    app.extensions.captcha
    ~~~~~~~~~~~~~~~~~~~~~~~
    验证码模块
"""

import secrets
import string
from typing import List
from . import AMQPStore


class CaptchaStore(AMQPStore):
    """
    验证码保存以及加载模块

    利用token匹配唯一验证码

    :param token token值
    """

    def __init__(self, token: str):
        self.token = token
        super().__init__(
            f"captcha_{token}",
            exchange="captcha",
            expires=300,
            routing_key=token,
            auto_delete=True,
        )

    def get_captcha(self):
        """获取验证码"""
        self.reload()
        return self.code_lst

    def _generate_captcha(self, length: int):
        """生成验证码"""
        passwd_str = string.digits + string.ascii_letters
        code = "".join([secrets.choice(passwd_str) for i in range(length)])
        self.value = code

    def generate_captcha(self, length: int = 4):
        """保存验证码"""
        self._generate_captcha(length)
        return self.save()

    @property
    def code_lst(self) -> List[str]:
        if self.value is None:
            return []
        return [self.value.upper(), self.value.lower(), self.value]
