#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/26 17:05
# @Author  : Ewan
# @File    : om_tag_rela.py
# @Description : 商品标签关系表

from sqlalchemy import Column, Integer, String, DATE, DECIMAL, DATETIME, Text
from sqlalchemy.sql.functions import current_date

from core.db import Base


class Om_tag_rela(Base):
    __tablename__ = 'om_tag_rela'

    pid = Column("pid", Integer, primary_key=True, nullable=False, comment='商品主键')
    tid = Column("tid", Integer, primary_key=True, nullable=False, comment='标签主键')
    c_date = Column("c_date", DATE, default=current_date, nullable=False, comment='创建时间')
    d_date = Column("d_date", DATE, comment='删除时间')
