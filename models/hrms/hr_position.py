#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/21 16:35
# @Author  : Ewan
# @File    : hr_position.py
# @Description : 职位表

from sqlalchemy import Column, Integer, String, DATE, DECIMAL, DATETIME, Text
from sqlalchemy.sql.functions import current_date

from core.db import Base


class Hr_position(Base):
    __tablename__ = 'hr_position'

    position_code = Column("position_code", String(32), primary_key=True, nullable=False, comment='职位')
    position_name = Column("position_name", String(32), nullable=False, comment='职位')
    describe = Column("describe", Text, comment='描述')

    create_date = Column("create_date", DATE, default=current_date, nullable=False, comment='创建时间')
    close_date = Column("close_date", DATE, comment='关闭时间')
    status = Column("status", Integer, default=1, nullable=False, comment='1活跃 2关闭')
