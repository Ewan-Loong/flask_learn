#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/18 17:04
# @Author  : Ewan
# @File    : teacher.py
# @Description : 老师表

from sqlalchemy import Column, ForeignKey, Integer, String, Table, DECIMAL, DATE

from core.db import Base, engine


# 老师基础信息
class Teacher(Base):
    __tablename__ = 'teacher'

    id = Column("id", Integer, primary_key=True, comment='教师主键id')
    name = Column("name", String(32), comment='教师名')
    university = Column("university", String(32), comment='毕业院系')
    speciality = Column("speciality", String(32), comment='专业')
    department = Column("department", String(32), comment='院系')
    birthday = Column("birthday", DATE, comment='出生日期')
    sex = Column("sex", String(10), comment='性别')
    height = Column("height", DECIMAL(4, 2), comment='身高')
    weight = Column("weight", DECIMAL(4, 2), comment='体重')


# teacher = Table(
#     "teacher",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String(32)),
#     Column("fullname", String(32)),
#     Column("nickname", String(32)),
# )

if __name__ == '__main__':
    # teacher.drop(checkfirst=True, bind=engine)
    # teacher.create(bind=engine)

    Base.metadata.create_all(bind=engine)
