#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_smtp.core.proxy import SmtpProxy
from service_core.cli.subctxs import BaseContext
from service_core.core.configure import Configure


class Smtp(BaseContext):
    """ 用于调试Smtp接口 """

    name: t.Text = 'smtp'

    def __init__(self, config: Configure) -> None:
        """ 初始化实例

        @param config: 配置对象
        """
        super(Smtp, self).__init__(config)
        self.proxy = SmtpProxy(config=config)
