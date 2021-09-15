# 运行环境

|system |python | 
|:------|:------|      
|cross platform |3.9.16|

# 组件安装

```shell
pip install -U service-smtp 
```

# 服务配置

> config.yaml

```yaml
CONTEXT:
  - service_smtp.cli.subctxs.smtp:Smtp
SMTP:
  test:
    connect_options:
      wrap_ssl: true
      host: test.com
      port: 465
      username: me@test.com
      password: user_passwd
```

# 入门案例

```yaml
├── config.yaml
├── facade.py
└── project
    ├── __init__.py
    └── service.py
```

> service.py

```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from PIL import Image
from io import BytesIO
from io import StringIO
from PIL import ImageDraw
from logging import getLogger
from service_smtp.core.dependencies import Smtp
from service_smtp.core.client import SmtpClient
from service_smtp.core.convert import from_name_to_cid
from service_croniter.core.entrypoints import croniter
from service_core.core.service import Service as BaseService

logger = getLogger(__name__)


class Service(BaseService):
    """ 微服务类 """

    # 微服务名称
    name = 'demo'
    # 微服务简介
    desc = 'demo'

    # SMTP协议
    smtp: SmtpClient = Smtp(alias='test')

    @croniter.cron('* * * * * */1')
    def test_send_text_mail(self) -> None:
        """ 测试发送文本邮件

        @return: None
        """
        succ, errs = self.smtp.send_text_mail(
            subject='subject - test_send_text_mail',
            message='message - test_send_text_mail',
            me='me@test.com',
            to=['to@test.com'],
            cc=['cc@test.com']
        )
        logger.debug(f'yeah~ yeah~ yeah~, text mail succ={succ} errs={errs}')

    @croniter.cron('* * * * * */1')
    def test_send_html_mail(self) -> None:
        """ 测试发送网页邮件

        @return: None
        """
        succ, errs = self.smtp.send_html_mail(
            subject='subject - test_send_html_mail',
            message='<h1>message - test_send_html_mail</h1>',
            me='发件人<me@test.com>',
            to=['收件人<to@test.com>'],
            cc=['抄送人<cc@test.com>']
        )
        logger.debug(f'yeah~ yeah~ yeah~, html mail succ={succ} errs={errs}')

    @croniter.cron('* * * * * */1')
    def test_send_file_mail(self) -> None:
        """ 测试发送附件邮件

        @return: None
        """
        file_name = '附件.text'
        string_io = StringIO('内容')
        succ, errs = self.smtp.send_html_mail(
            subject='subject - test_send_file_mail',
            message='<h1>message - test_send_file_mail</h1>',
            me='发件人<me@test.com>',
            to=['收件人<to@test.com>'],
            cc=['抄送人<cc@test.com>'],
            files=[(file_name, string_io.read().encode())]
        )
        logger.debug(f'yeah~ yeah~ yeah~, file mail succ={succ} errs={errs}')

    @croniter.cron('* * * * * */1')
    def test_send_imag_mail(self) -> None:
        """ 测试发送图片邮件

        @return: None
        """
        image = Image.new('RGB', (300, 50))
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), 'message - test_send_imag_mail')
        bytes_io = BytesIO()
        image.save(bytes_io, 'PNG')
        image_name = from_name_to_cid('图片.png')
        succ, errs = self.smtp.send_html_mail(
            subject='subject - test_send_imag_mail',
            message=f'<img src="cid:{image_name}">',
            me='发件人<me@test.com>',
            to=['收件人<to@test.com>'],
            cc=['抄送人<cc@test.com>'],
            imags=[(image_name, bytes_io.getvalue())]
        )
        logger.debug(f'yeah~ yeah~ yeah~, imag mail succ={succ} errs={errs}')
```

> facade.py

```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from project import Service

service = Service()
```

# 运行服务

> core start facade --debug

# 接口调试

> core shell --shell `shell`

```shell
* eventlet 0.31.1
    - platform: macOS 10.15.7
      error  : changelist must be an iterable of select.kevent objects
      issue  : https://github.com/eventlet/eventlet/issues/670#issuecomment-735488189
    - platform: macOS 10.15.7
      error  : monkey_patch causes issues with dns .local #694
      issue  : https://github.com/eventlet/eventlet/issues/694#issuecomment-806100692

2021-09-14 16:46:06,432 - 9204 - DEBUG - load subcmd service_core.cli.subcmds.start:Start succ
2021-09-14 16:46:06,433 - 9204 - DEBUG - load subcmd service_core.cli.subcmds.config:Config succ
2021-09-14 16:46:06,433 - 9204 - DEBUG - load subcmd service_core.cli.subcmds.shell:Shell succ
2021-09-14 16:46:06,433 - 9204 - DEBUG - load subcmd service_core.cli.subcmds.debug:Debug succ
2021-09-14 16:46:06,468 - 9204 - DEBUG - load subctx service_smtp.cli.subctxs.smtp:Smtp succ
2021-09-14 16:46:06,468 - 9204 - DEBUG - load subctx service_core.cli.subctxs.config:Config succ
CPython - 3.9.6 (tags/v3.9.6:db3ff76, Jun 28 2021, 15:26:21) [MSC v.1929 64 bit (AMD64)]
>>> s.smtp.proxy('test').send_text_mail(subject='subject - test_send_text_mail', message='message - test_send_text_mail', me='me@test.com', to=['to@test.com'], cc=['cc@test.com'])
(True, None)
```

# 运行调试

> core debug --port `port`
