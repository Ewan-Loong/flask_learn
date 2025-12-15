#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/26 14:40
# @Author  : Ewan
# @File    : test.py


from sqlalchemy import Column, Integer, String, DECIMAL, Table, DATE

from core.db import Base, engine


# 学生基础信息
class Student(Base):
    __tablename__ = 'student'

    id = Column("id", Integer, primary_key=True, comment='学生主键id')
    name = Column("name", String(32), comment='学生名')
    birthday = Column("birthday", DATE, comment='出生日期')
    sex = Column("sex", String(10), comment='性别')
    department = Column("department", String(32), comment='院系')
    speciality = Column("speciality", String(32), comment='专业')
    height = Column("height", DECIMAL(4, 2), comment='身高')
    weight = Column("weight", DECIMAL(4, 2), comment='体重')


# class Address(Base):
#     __tablename__ = 'address'
#
#     id = Column("id", Integer, primary_key=True)
#     user_id = Column("user_id", Integer)
#     address_1 = Column("address_1", String(32))
#     address_2 = Column("address_2", String(32))
#     email = Column("email", String(32))
#     notes = Column("notes", String(32))


# user = Table(
#     "user",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("name", String(32)),
#     Column("fullname", String(32)),
#     Column("age", Integer),
#     Column("sex", String(10)),
#     Column("height", DECIMAL(4, 2)),
#     Column("weight", DECIMAL(4, 2)),
# )
#
# address = Table(
#     "address",
#     Base.metadata,
#     Column("id", Integer, primary_key=True),
#     Column("user_id", Integer),
#     Column("address_1", String(32)),
#     Column("address_2", String(32)),
#     Column("email", String(32)),
#     Column("notes", String(32)),
# )

if __name__ == '__main__':
    # user.drop(checkfirst=True, bind=engine)
    # user.create(bind=engine)
    #
    # address.drop(checkfirst=True, bind=engine)
    # address.create(bind=engine)

    Base.metadata.create_all(bind=engine)
