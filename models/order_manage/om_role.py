#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/12/16 15:13
# @Author  : Ewan
# @File    : om_role.py
# @Description : 用户角色表

from sqlalchemy import Column, Integer, String, DATE, DECIMAL, Boolean, Text
from sqlalchemy.sql.functions import current_date
from core.db import Base, engine


class Om_role(Base):
    __tablename__ = 'om_role'

    rid = Column("rid", Integer, primary_key=True, nullable=False, comment='主键')
    rcode = Column('rcode', String(32), unique=True, nullable=False, comment='角色编码')
    rname = Column("rname", String(32), nullable=False, comment='角色名称')
    description = Column("description", Text, nullable=False, comment='角色描述')
    is_system = Column('is_system', Boolean, default=False, comment='是否系统内置角色')
    c_date = Column("c_date", DATE, default=current_date, nullable=False, comment='创建时间')


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
