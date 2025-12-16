#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/12/16 16:16
# @Author  : Ewan
# @File    : om_role_permission.py
# @Description : 角色权限配置表

from sqlalchemy import Column, Integer, String, DATE, DECIMAL, Boolean, Text
from sqlalchemy.sql.functions import current_date
from core.db import Base, engine


class Om_role_permission(Base):
    __tablename__ = 'om_role_permission'

    role_id = Column("role_id", Integer, primary_key=True, nullable=False, comment='角色主键')
    permission_id = Column("permission_id", Integer, primary_key=True, nullable=False, comment='权限主键')
    c_date = Column("c_date", DATE, default=current_date, nullable=False, comment='创建时间')


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
