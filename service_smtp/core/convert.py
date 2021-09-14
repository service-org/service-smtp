#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from base64 import b64decode
from base64 import b64encode


def from_name_to_cid(name: t.Text) -> t.Text:
    """ 将名称转换为cid

    @param name: 名称
    @return: t.Text
    """
    return b64encode(name.encode()).decode('utf-8')


def from_cid_to_name(cid: t.Text) -> t.Text:
    """ 将cid转换为名称

    @param cid: 标识
    @return: t.Text
    """
    return b64decode(cid.encode()).decode('utf-8')
