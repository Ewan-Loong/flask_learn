#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/26 17:05
# @Author  : Ewan
# @File    : om_prod.py
# @Description : 商品库存操作记录表

from sqlalchemy import Column, Integer, String, DATE, DECIMAL, DATETIME, Text, LargeBinary
from sqlalchemy.dialects.mysql import MEDIUMBLOB
from sqlalchemy.sql.functions import current_date

from core.db import Base


class Om_stock_log(Base):
    __tablename__ = 'om_stock_log'

    id = Column("id", Integer, primary_key=True, nullable=False, comment='逻辑主键')
    pid = Column("pid", Integer, nullable=False, comment='商品主键')
    op_type = Column("op_type", Integer, nullable=False, comment='操作类型 1入库2出库3撤销入库4撤销出库')
    op_num = Column("op_num", Integer, nullable=False, comment='操作数量')
    op_uid = Column("op_uid", Integer, nullable=False, comment='操作用户')
    note = Column("note", String(1024), default=None, comment='操作附言')
    c_date = Column("c_date", DATE, default=current_date, nullable=False, comment='创建时间')
