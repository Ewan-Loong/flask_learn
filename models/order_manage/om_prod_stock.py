#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/26 17:05
# @Author  : Ewan
# @File    : om_prod_stock.py
# @Description : 商品库存表

from sqlalchemy import Column, Integer, String, DATE, DECIMAL, DATETIME, Text
from sqlalchemy.sql.functions import current_date

from core.db import Base


class Om_prod_stock(Base):
    __tablename__ = 'om_prod_stock'

    pid = Column("pid", Integer, primary_key=True, nullable=False, comment='商品主键')
    quantity = Column("quantity", Integer, nullable=False, default=0, comment='库存数量')
    c_date = Column("c_date", DATE, default=current_date, nullable=False, comment='创建时间')
