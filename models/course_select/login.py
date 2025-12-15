#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/22 10:08
# @Author  : Ewan
# @File    : bp.py
# @Description : 登陆记录表
from sqlalchemy import Column, Integer, String, DATE, DECIMAL, DATETIME

from core.db import Base


# 登录记录表
class LoginRecord(Base):
    __tablename__ = 'login_record'
    # 逻辑主键 sqlalchemy ORM 不允许定义一个没有主键的表
    id = Column("id", Integer, primary_key=True, comment='逻辑主键id')

    in_id = Column("in_id", Integer, comment='登录人主键id')
    name = Column("name", String(32), comment='登录人名')
    type = Column("type", String(16), comment='登录人类型')
    in_time = Column("in_time", DATETIME, comment='登录时间')
