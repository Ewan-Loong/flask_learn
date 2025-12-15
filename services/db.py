#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/18 10:51
# @Author  : Ewan
# @File    : db.py
# @Description : 数据操作

from flask import Blueprint, request
from sqlalchemy import insert
from core.db import db_session
import models
from core.utils import to_json2

bp = Blueprint('db', __name__, url_prefix='/db', template_folder='/templates')


# @bp.before_request
# def do_before():
#     request.table = request.path.split('/')[-2]
#     print('select table',request.table)


@bp.route('/select/<table_name>', methods=['POST'])
def get_by_id(table_name):
    res = {}

    if request.json:
        id = request.json['id']
        # print(request.path.split('/')[-2].capitalize())
        # capitalize 返回字符串首字母大写
        obj = getattr(models, table_name.capitalize())
        # print(obj.test())

        sql_res = obj.query.filter(obj.id == id).all()

        res['bp'] = to_json2(sql_res)
        # return to_json2(sql_res)
    else:
        res['msg'] = '错误输入'

    return res


@bp.route('/delete/<table_name>', methods=['POST'])
def delete_by_id(table_name):
    assert request.json, '请传入正确的参数'
    id = request.json['id']
    obj = getattr(models, table_name.capitalize())
    u = obj.query.filter(obj.id == id).all()
    if u == 1:
        obj.query.filter(obj.id == id).delect()
        db_session.commit()
        return {'msg': 'ok'}
    else:
        return {'msg': '无法删除不存在的对象'}


@bp.route('/update/<table_name>', methods=['POST'])
def update_by_id(table_name):
    res = {}
    if request.json:
        args = request.json
        obj = getattr(models, table_name.capitalize())
        u = obj.query.filter(obj.id == args['id']).all()
        # u = Student.query.filter(Student.id == args['id']).update(args)
        if u == 1:
            obj.query.filter(obj.id == args['id']).update(args)
            db_session.commit()
            res['msg'] = 'ok'
        else:
            res['msg'] = '无法更新不存在的对象'
    else:
        res['msg'] = '错误输入'

    return res


@bp.route('/insert/<table_name>', methods=['POST'])
def insert_by_none(table_name):
    res = {}
    if request.json:
        args = request.json
        obj = getattr(models, table_name.capitalize())
        # u = Student.session.execute(insert(Student).values(args['values']))
        try:
            ins = db_session.execute(insert(obj).values(args['values']))
            db_session.commit()
            res['msg'] = 'ok'
        except Exception as e:
            db_session.rollback()
            res['msg'] = str(e)
    else:
        res['msg'] = '错误输入'

    return res
