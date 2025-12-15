#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/22 10:16
# @Author  : Ewan
# @File    : course.py
# @Description : 课程相关表

from sqlalchemy import Column, Integer, String, DATE, DECIMAL, DATETIME

from core.db import Base


# 课程基础信息
class Course(Base):
    __tablename__ = 'course'

    id = Column("id", Integer, primary_key=True, comment='课程主键id')
    cname = Column("cname", String(32), comment='课程名')
    tid = Column("tid", Integer, comment='教师主键id')
    tname = Column("tname", String(32), comment='教师名')

    open_date = Column("open_date", DATE, comment='开课时间')
    close_date = Column("close_date", DATE, comment='结课时间')
    credit = Column("credit", DECIMAL(4, 2), comment='课程学费')
    total_count = Column("total_count", Integer, comment='课程最多人数')
    select_count = Column("select_count", Integer, comment='当前选课人数')


# 选课申请记录表
class CourseApply(Base):
    __tablename__ = 'course_apply'

    id = Column("id", Integer, primary_key=True, comment='主键id')
    cid = Column("cid", Integer, comment='课程主键id')
    cname = Column("cname", String(32), comment='课程名')

    sid = Column("sid", Integer, comment='学生主键id')
    sname = Column("sname", String(32), comment='学生名')
    apply_time = Column("apply_time", DATETIME, comment='申请选课时间')
    cancel_time = Column("cancel_time", DATETIME, comment='取消申请时间')

    tid = Column("tid", Integer, comment='老师主键id')
    tname = Column("tname", String(32), comment='老师名')
    agree_time = Column("agree_time", DATETIME, comment='申请同意时间')
    disagree_time = Column("disagree_time", DATETIME, comment='申请不同意时间')

    status = Column("status", Integer, comment='选课申请状态 1 申请中 2 取消申请 3 同意 4 不同意')


# 选课事实表 存储当前选课成功的记录 【其实从记录表也能获取到选课成功的信息】
class CourseSelect(Base):
    __tablename__ = 'course_select'

    id = Column("id", Integer, primary_key=True, comment='逻辑主键')
    cid = Column("cid", Integer, comment='课程主键id')
    cname = Column("cname", String(32), comment='课程名')

    tid = Column("tid", Integer, comment='老师主键id')
    tname = Column("tname", String(32), comment='老师名')
    agree_time = Column("agree_time", DATETIME, comment='申请同意时间')

    sid = Column("sid", Integer, comment='学生主键id')
    sname = Column("sname", String(32), comment='学生名')
    apply_time = Column("apply_time", DATETIME, comment='申请时间')
