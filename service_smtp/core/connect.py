#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations


import traceback
import typing as t

from smtplib import SMTP
from smtplib import SMTP_SSL
from email.header import Header
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.base import MIMEBase

class Connection(object):
    """ Smtp通用连接类 """
    def __init__(
            self,
            *args: t.Any,
            username: t.Text,
            password: t.Text,
            debug: t.Optional[bool] = None,
            warp_ssl: t.Optional[bool] = None,
            **kwargs: t.Any
    ) -> None:
        """ 初始化实例

        @param args: 位置参数
        @param: username: 认证账户
        @param: password: 认证密码
        @param: debug: 是否启用调试?
        @param warp_ssl: 使用ssl?
        @param kwargs: 命名参数
        """
        self.debug = debug or False
        self.username = username
        self.password = password
        self.warp_ssl = warp_ssl or False
        self.server = SMTP_SSL(*args, **kwargs) if self.warp_ssl else SMTP(*args, **kwargs)

    def release(self) -> None:
        """ 注销本此链接 """
        self.server.__exit__()

    def send_mail(
            self,
            subject: t.Text,
            message: MIMEBase,
            me: t.Optional[t.Union[t.Text, t.List[t.Text, t.Text]]] = None,
            to: t.Optional[t.Union[t.Text, t.List[t.Text, t.Text]]] = None,
            cc: t.Optional[t.Union[t.Text, t.List[t.Text, t.Text]]] = None
    ) -> t.Tuple[bool, t.Text]:
        """ 发送通用邮件

        @param subject: 邮件主题
        @param message: 邮件内容
        @param me: 发送人,支持多人
        @param to: 接收人,支持多人
        @param cc: 抄送人,支持多人
        @return: t.Tuple[bool, t.Text]
        """
        send_result, send_errors = True, ''
        try:
            if isinstance(me, list):
                me = [formataddr(_) for _ in me]
            else:
                me = [] if me is None else [me]
            if isinstance(to, list):
                to = [formataddr(_) for _ in to]
            else:
                to = [] if to is None else [to]
            if isinstance(cc, list):
                cc = [formataddr(_) for _ in cc]
            else:
                cc = [] if cc is None else [cc]
            message['to'] = Header(','.join(to), 'utf-8')
            message['cc'] = Header(','.join(cc), 'utf-8')
            message['Subject'] = Header(subject, 'utf-8')
            self.debug and self.server.set_debuglevel(1)
            message['From'] = Header(','.join(me), 'utf-8')
            self.server.login(self.username, self.password)
            self.server.sendmail(me[0], to, message.as_string())
        except:
            send_result = False
            send_errors = traceback.format_exc()
        finally:
            return send_result, send_errors

    def send_text_mail(
            self,
            subject: t.Text,
            message: t.Text,
            me: t.Optional[t.Union[t.Text, t.List[t.Text, t.Text]]] = None,
            to: t.Optional[t.Union[t.Text, t.List[t.Text, t.Text]]] = None,
            cc: t.Optional[t.Union[t.Text, t.List[t.Text, t.Text]]] = None
    ) -> t.Tuple[bool, t.Text]:
        """

        @param subject: 邮件主题
        @param message: 邮件内容
        @param me: 发送人,支持多人
        @param to: 接收人,支持多人
        @param cc: 抄送人,支持多人
        @return: t.Tuple[bool, t.Text]
        """
        message = MIMEText(message, _subtype='plain', _charset='utf-8')
        return self.send_mail(subject=subject, message=message, me=me, to=to, cc=cc)


