#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/20 17:23
# @Author  : Ewan
# @File    : hr_staff.py
# @Description : api
import logging

from flask import Blueprint, request
from sqlalchemy import insert
from sqlalchemy.sql.functions import current_date
from core.db import db_session
from core.utils import to_json2
from models.hrms import Hr_staff
from pypinyin import lazy_pinyin, Style

bp = Blueprint('hr_staff', __name__, url_prefix='/hr', template_folder='/templates')


@bp.route('/create_staff', methods=['POST'])
def create_staff():
    assert request.json['values'], "员工信息不能为空"

    values = request.json['values']
    no = Hr_staff.query.count()
    for item in values:
        item["staff_no"] = ''.join(lazy_pinyin(item["staff_name"])) + f'{no:0>3}'
        no = no + 1
    try:
        u = db_session.execute(insert(Hr_staff).values(values))
        db_session.commit()
        return {"msg": 'ok'}
    except Exception as e:
        db_session.rollback()
        raise e


@bp.route('/update_staff', methods=['POST'])
def update_staff():
    assert request.json, "更新信息不能为空"

    args = request.json
    u = Hr_staff.query.filter(Hr_staff.staff_no == args['staff_no']).update(args)
    db_session.commit()

    return {'msg': 'ok'} if u == 1 else {'msg': '更新失败'}


@bp.route('/select_staff', methods=['POST'])
def select_staff():
    assert request.json['staff_no'], "查询员工号不能为空"

    staff_no = request.json['staff_no']
    sql_res = Hr_staff.query.filter(Hr_staff.staff_no == staff_no).all()
    return {'res': to_json2(sql_res)}


@bp.route('/leave_staff', methods=['POST'])
def leave_staff():
    assert request.json['staff_no'], "删除员工号不能为空"

    args = request.json
    # u = Hr_staff.query.filter(Hr_staff.staff_no == args['staff_no']).delete()
    u = Hr_staff.query.filter(Hr_staff.staff_no == args['staff_no'], Hr_staff.status == 1).one()
    if u:
        u.leave_date = current_date()
        u.status = 2
        db_session.commit()
        return {'msg': 'ok'}
    else:
        return {'msg': '删除失败'}
