#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/20 16:54
# @Author  : Ewan
# @File    : hr_staff.py
# @Description : 人员管理
from sqlalchemy import Column, Integer, String, DATE, DECIMAL, DATETIME
from sqlalchemy.sql.functions import current_date

from core.db import Base


class Hr_staff(Base):
    __tablename__ = 'hr_staff'

    staff_no = Column("staff_no", String(32), primary_key=True, comment='职工编号')
    staff_name = Column("staff_name", String(32), nullable=False, comment='职工姓名')
    sex = Column("sex", String(10), nullable=False, comment='性别')
    cert_no = Column("cert_no", String(32), nullable=False, comment='身份证号')
    salary_act = Column("salary_act", String(32), nullable=False, comment='工资账户')

    department_code = Column("department_code", String(32), nullable=False, comment='部门')
    department_name = Column("department_name", String(32), nullable=False, comment='部门')

    position_code = Column("position_code", String(2), nullable=False, default='D0', comment='职位')
    position_name = Column("position_name", String(10), nullable=False, default='员工', comment='职位')
    position_level = Column("position_level", Integer, nullable=False, default=1, comment='职级')

    post_code = Column("post_code", String(10), comment='邮编')
    post_address = Column("post_address", String(512), comment='邮寄地址')
    address = Column("address", String(512), comment='地址')
    mobile_phone = Column("mobile_phone", String(64), nullable=False, comment='手机号码')

    work_date = Column("work_date", DATE, default=current_date(), nullable=False, comment='入职日期')
    leave_date = Column("leave_date", DATE, comment='离职日期')
    status = Column("status", Integer, default=1, nullable=False, comment='1在职 2离职')
