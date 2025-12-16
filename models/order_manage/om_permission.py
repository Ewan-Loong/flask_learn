#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/12/16 15:45
# @Author  : Ewan
# @File    : om_permission.py
# @Description : 权限定义表


from sqlalchemy import Column, Integer, String, DATE, DECIMAL, Boolean, Text
from sqlalchemy.sql.functions import current_date
from core.db import Base, engine


class Om_permission(Base):
    __tablename__ = 'om_permission'

    id = Column("id", Integer, primary_key=True, nullable=False, comment='主键')
    code = Column('code', String(32), unique=True, nullable=False, comment='权限编码')
    name = Column("name", String(32), nullable=False, comment='权限名称')
    description = Column("description", Text, comment='权限描述')
    category = Column('category', String(50), comment='权限类别')
    scope = Column('scope', String(50), comment='管控资源类型（API/菜单/按钮）')
    c_date = Column("c_date", DATE, default=current_date, nullable=False, comment='创建时间')


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
