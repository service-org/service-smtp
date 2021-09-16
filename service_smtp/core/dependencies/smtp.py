#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_smtp.core.client import SmtpClient
from service_smtp.constants import SMTP_CONFIG_KEY
from service_core.core.context import WorkerContext
from service_core.core.service.dependency import Dependency


class Smtp(Dependency):
    """ Smtp依赖类 """

    def __init__(self, alias: t.Text, connect_options: t.Optional[t.Dict[t.Text, t.Any]] = None, **kwargs: t.Any):
        """ 初始化实例

        @param alias: 配置别名
        @param connect_options: 连接配置
        @param kwargs: 其它配置
        """
        self.alias = alias
        self.session_map = {}
        self.connect_options = connect_options or {}
        super(Smtp, self).__init__(**kwargs)

    def setup(self) -> None:
        """ 生命周期 - 载入阶段

        @return: None
        """
        connect_options = self.container.config.get(f'{SMTP_CONFIG_KEY}.{self.alias}.connect_options', default={})
        # 防止YAML中声明值为None
        self.connect_options = (connect_options or {}) | self.connect_options
        self.connect_options.setdefault('timeout', 5)

    def get_instance(self, context: WorkerContext) -> t.Any:
        """ 获取注入对象
        @param context: 上下文对象
        @return: t.Any
        """
        # 主要用于优雅关闭每条连接
        call_id = context.worker_request_id
        self.session_map[call_id] = SmtpClient(**self.connect_options)
        return self.session_map[call_id]

    def worker_finish(self, context: WorkerContext) -> None:
        """ 工作协程 - 完毕回调
        @param context: 上下文对象
        @return: None
        """
        # 主要用于优雅关闭每条连接
        call_id = context.worker_request_id
        session = self.session_map.pop(call_id, None)
        session and session.release()
