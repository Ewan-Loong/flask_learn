#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/26 17:05
# @Author  : Ewan
# @File    : om_prod.py
# @Description : 商品表

from sqlalchemy import Column, Integer, String, DATE, DECIMAL, DATETIME, Text, LargeBinary
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from sqlalchemy.sql.functions import current_date

from core.db import Base


class Om_prod(Base):
    __tablename__ = 'om_prod'

    pid = Column("pid", Integer, primary_key=True, nullable=False, comment='商品主键')
    uid = Column("uid", Integer, nullable=False, comment='用户主键')
    pname = Column("pname", String(32), nullable=False, comment='商品名')
    image = Column("image", MEDIUMBLOB, comment='商品名')
    info = Column("info", String(1024), default=None, comment='描述')
    c_date = Column("c_date", DATE, default=current_date, nullable=False, comment='创建时间')
