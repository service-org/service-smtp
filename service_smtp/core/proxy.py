#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_core.core.configure import Configure
from service_smtp.constants import SMTP_CONFIG_KEY

from .client import SmtpClient


class SmtpProxy(object):
    """ Smtp代理类 """

    def __init__(self, config: Configure, **options: t.Text) -> None:
        """ 初始化实例

        @param config: 配置对象
        @param options: 其它选项
        """
        self.config = config
        self.options = options

    def __call__(self, alias: t.Text, **options: t.Text) -> SmtpClient:
        """ 代理可调用

        @param alias: 配置别名
        @param options: 其它选项
        @return: Session
        """
        cur_options = self.options
        # 调用时传递的参数配置优先级最高
        cur_options.update(options)
        config = self.config.get(f'{SMTP_CONFIG_KEY}.{alias}.connect_options', default={})
        # 调用时传递的参数配置优先级最高
        config.update(cur_options)
        return SmtpClient(**config)
