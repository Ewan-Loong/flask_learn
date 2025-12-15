#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/22 14:53
# @Author  : Ewan
# @File    : bp.py
# @Description : 登录退出接口
import datetime
import json

from flask import Blueprint, request
from sqlalchemy import insert

from core.db import db_session
from models import course_select
from models.course_select import LoginRecord

bp = Blueprint('login', __name__, url_prefix='/cs', template_folder='/templates')


@bp.route('/login', methods=['POST'])
def login_by_id():
    res = {}
    if request.json:
        data = request.json
        obj = getattr(course_select, data['type'].capitalize())
        # print(obj)
        sql_res = obj.query.filter(obj.id == data['id']).one_or_none()
        if sql_res:
            # 插入登录记录
            login_record = dict(in_id=data['id'], name=sql_res.name, type=data['type'],
                                in_time=datetime.datetime.now())
            db_session.execute(insert(LoginRecord).values(login_record))
            db_session.commit()
            res['mes'] = '登录成功'
        else:
            res['mes'] = '{}:{}不存在'.format(data['type'].capitalize(), data['id'])
    else:
        res['msg'] = '错误输入'

    return res
