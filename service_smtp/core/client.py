#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from smtplib import SMTP
from smtplib import SMTP_SSL
from logging import getLogger
from email.header import Header
from email.utils import parseaddr
from email.utils import formataddr
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

logger = getLogger(__name__)


class SmtpClient(object):
    """ Smtp通用连接类 """

    def __init__(
            self,
            *args: t.Any,
            username: t.Text,
            password: t.Text,
            debug: t.Optional[bool] = None,
            wrap_ssl: t.Optional[bool] = None,
            **kwargs: t.Any
    ) -> None:
        """ 初始化实例

        @param args: 位置参数
        @param: username: 认证账户
        @param: password: 认证密码
        @param: debug: 启用调试?
        @param wrap_ssl: 启用ssl?
        @param kwargs: 命名参数
        """
        self._args = args
        self._kwargs = kwargs
        self.debug = debug or False
        self.username = username
        self.password = password
        self.wrap_ssl = wrap_ssl or False

    def connect(self) -> t.Union[SMTP_SSL, SMTP]:
        """ 创建一个连接

        @return: t.Union[SMTP_SSL, SMTP]
        """
        smtp_class = SMTP_SSL if self.wrap_ssl else SMTP
        return smtp_class(*self._args, **self._kwargs)

    @staticmethod
    def fmt_mails(mails: t.List[t.Text]) -> t.List[t.Text]:
        """ 格式化邮件名

        @param mails: 地址列表
        @return: t.List[t.Text]
        """
        result = []
        for mail in mails:
            pair = parseaddr(mail)
            addr = Header(pair[0], 'utf-8').encode(), pair[1]
            result.append(formataddr(addr, charset='utf-8'))
        return result

    def send_mail(
            self,
            subject: t.Text,
            message: MIMEBase,
            me: t.Optional[t.Union[t.Text, t.List[t.Text]]] = None,
            to: t.Optional[t.Union[t.Text, t.List[t.Text]]] = None,
            cc: t.Optional[t.Union[t.Text, t.List[t.Text]]] = None
    ) -> None:
        """ 发送通用邮件

        @param subject: 邮件主题
        @param message: 邮件内容
        @param me: 发送人
        @param to: 接收人
        @param cc: 抄送人
        @return: None
        """
        client = self.connect()
        subject = Header(subject, 'utf-8')
        subject = subject.encode()
        if not isinstance(me, list):
            me = [] if me is None else [me]
        me = self.fmt_mails(me) if me else me
        if not isinstance(to, list):
            to = [] if to is None else [to]
        to = self.fmt_mails(to) if to else to
        if not isinstance(cc, list):
            cc = [] if cc is None else [cc]
        cc = self.fmt_mails(cc) if cc else cc
        message['to'] = ','.join(to)
        message['cc'] = ','.join(cc)
        message['Subject'] = subject
        message['From'] = ','.join(me)
        self.debug and client.set_debuglevel(1)
        client.login(self.username, self.password)
        me = me[0] if len(me) == 1 else self.username
        message = message.as_string()
        client.sendmail(me, to + cc, message)
        client.quit()

    def send_text_mail(
            self,
            subject: t.Text,
            message: t.Text,
            me: t.Optional[t.Union[t.Text, t.List[t.Text]]] = None,
            to: t.Optional[t.Union[t.Text, t.List[t.Text]]] = None,
            cc: t.Optional[t.Union[t.Text, t.List[t.Text]]] = None
    ) -> None:
        """ 发送文本邮件

        @param subject: 邮件主题
        @param message: 邮件内容
        @param me: 发送人
        @param to: 接收人
        @param cc: 抄送人
        @return: None
        """
        message = MIMEText(message, _subtype='plain', _charset='utf-8')
        self.send_mail(subject=subject, message=message, me=me, to=to, cc=cc)

    def send_html_mail(
            self,
            subject: t.Text,
            message: t.Text,
            files: t.Optional[t.List[t.Tuple[t.Text, bytes]]] = None,
            imags: t.Optional[t.List[t.Tuple[t.Text, bytes]]] = None,
            me: t.Optional[t.Union[t.Text, t.List[t.Text]]] = None,
            to: t.Optional[t.Union[t.Text, t.List[t.Text]]] = None,
            cc: t.Optional[t.Union[t.Text, t.List[t.Text]]] = None,
    ) -> None:
        """ 发送网页邮件

        @param subject: 邮件主题
        @param message: 邮件内容
        @param me: 发送人
        @param to: 接收人
        @param cc: 抄送人
        @param files: 附件中的文件
        @param imags: 附件中的图片
        @return: t.Tuple[bool, t.Optional[t.Text]]
        """
        multipart = MIMEMultipart()
        multipart.attach(MIMEText(message, _subtype='html', _charset='utf-8'))
        for (file_name, file_bytes) in files or []:
            f = MIMEText(file_bytes, _subtype='base64', _charset='utf-8')
            f['Content-Type'] = 'application/octet-stream'
            f.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', file_name))
            multipart.attach(f)
        for (imag_name, imag_bytes) in imags or []:
            i = MIMEImage(imag_bytes, _subtype='png')
            i.add_header('Content-ID', imag_name)
            multipart.attach(i)
        self.send_mail(subject=subject, message=multipart, me=me, to=to, cc=cc)
