#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/26 17:05
# @Author  : Ewan
# @File    : om_prod_tag.py
# @Description : 商品标签定义表

from sqlalchemy import Column, Integer, String, DATE, DECIMAL, DATETIME, Text
from sqlalchemy.sql.functions import current_date

from core.db import Base


class Om_prod_tag(Base):
    __tablename__ = 'om_prod_tag'

    tid = Column("tid", Integer, primary_key=True, nullable=False, comment='标签主键')
    tname = Column("tname", String(32), nullable=False, comment='标签名')
    ptid = Column("ptid", Integer, comment='父标签主键')
    info = Column("info", String(1024), default=None, comment='描述')
    c_date = Column("c_date", DATE, default=current_date, nullable=False, comment='创建时间')
    is_del = Column("is_del", Integer, nullable=False, default=0, comment='逻辑删除')
