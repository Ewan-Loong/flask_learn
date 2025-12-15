#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/26 16:58
# @Author  : Ewan
# @File    : om_user.py
# @Description : om用户表
from sqlalchemy import Column, Integer, String, DATE, DECIMAL, DATETIME, Text
from sqlalchemy.sql.functions import current_date

from core.db import Base


class Om_user(Base):
    __tablename__ = 'om_user'

    uid = Column("uid", Integer, primary_key=True, nullable=False, comment='主键')
    name = Column("name", String(32), primary_key=True, nullable=False, comment='姓名')
    birthdt = Column("birthdt", DATE, nullable=False, comment='出生日期')
    passwd = Column("passwd", String(64), nullable=False, comment='密码')
    on_line = Column("on_line", Integer, default=-1, nullable=False, comment='1在线 -1不在线')
