#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/21 15:53
# @Author  : Ewan
# @File    : hr_depart.py
# @Description : 部门表
from sqlalchemy import Column, Integer, String, DATE, DECIMAL, DATETIME, Text
from sqlalchemy.sql.functions import current_date

from core.db import Base


class Hr_depart(Base):
    __tablename__ = 'hr_depart'

    department_code = Column("department_code", String(32), primary_key=True, nullable=False, comment='部门')
    department_name = Column("department_name", String(32), nullable=False, comment='部门')
    describe = Column("describe", Text, comment='部门描述')

    manager_staff_no = Column("manager_staff_no", String(32), nullable=False, comment='部门管理者')
    manager_staff_name = Column("manager_staff_name", String(32), nullable=False, comment='部门管理者')

    create_date = Column("create_date", DATE, default=current_date, nullable=False, comment='创建时间')
    close_date = Column("close_date", DATE, comment='关闭时间')
    status = Column("status", Integer, default=1, nullable=False, comment='1活跃 2关闭')
