#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/12/17 10:30
# @Author  : Ewan
# @File    : role_permission.py
# @Description : 用户角色权限

from flask import Blueprint, request
from sqlalchemy import select
from core.db import select_by_where, insert_by_obj, update_by_obj, delete_by_obj, get_model, db_session
from core.api_check import required_token, check_params, check_permission
from core.utils import to_json2

bp = Blueprint('role_permission', __name__, url_prefix='/RolePermission', template_folder='/templates')


@bp.route('/select_role', methods=['GET'])
@required_token
# @check_params()
@check_permission('role:query')
def select_role():
    role = select_by_where('om_role')
    return {'msg': '查询成功', 'data': role}


@bp.route('/create_role', methods=['POST'])
# @required_token
@check_params()
@check_permission('role:add')
def create_role():
    data = request.json
    list_data = data['values'] if data.get('values') else [data]
    for i in list_data:
        exist = select_by_where('om_role', {'rcode': i['rcode']})
        if exist:
            return {'msg': '角色编码 {} 已存在'.format(i['rcode'])}, 400
        insert_by_obj('om_role', i)

    return {'msg': '创建成功'}


@bp.route('/update_role', methods=['POST'])
@required_token
@check_params()
@check_permission('role:update')
def update_role():
    data = request.json
    list_data = data['values'] if data.get('values') else [data]
    c = 0
    for i in list_data:
        exist = select_by_where('om_role', {'rcode': i['rcode']})
        if exist and i['rid'] != exist[0]['rid']:
            return {'msg': '角色编码 {} 已存在'.format(i['rcode'])}, 400
        else:
            update_by_obj('om_role', list_data)
            c = c + 1
    if len(list_data) == c:
        return {'msg': '更新成功'}
    else:
        return {'msg': '更新成功{}个'.format(c)}


@bp.route('/delete_role', methods=['POST'])
@required_token
@check_params('rid', 'rcode')
@check_permission('role:delete')
def delete_role():
    data = request.json
    delete_by_obj('om_role', data)
    role = select_by_where('om_role', data)
    if len(role) == 0:
        return {'msg': '删除成功'}
    else:
        return {'msg': '删除失败'}


@bp.route('/select_permission', methods=['POST'])
@required_token
# @check_params()
@check_permission('role:query')
def select_permission():
    data = request.json
    permission = select_by_where('om_permission', data)
    return {'msg': '查询成功', 'data': permission}


@bp.route('/create_permission', methods=['POST'])
@required_token
@check_params()
def create_permission():
    data = request.json
    list_data = data['values'] if data.get('values') else [data]
    for i in list_data:
        exist = select_by_where('om_permission', {'code': i['code']})
        if exist:
            return {'msg': '权限编码 {} 已存在'.format(i['code'])}, 400
        insert_by_obj('om_permission', i)

    return {'msg': '创建成功'}


@bp.route('/update_permission', methods=['POST'])
@required_token
@check_params()
def update_permission():
    data = request.json
    list_data = data['values'] if data.get('values') else [data]
    c = 0
    for i in list_data:
        exist = select_by_where('om_permission', {'code': i['code']})
        if exist and i['id'] != exist[0]['id']:
            return {'msg': '权限编码 {} 已存在'.format(i['code'])}, 400
        else:
            update_by_obj('om_permission', i)
            c = c + 1
    if len(list_data) == c:
        return {'msg': '更新成功'}
    else:
        return {'msg': '更新成功{}个'.format(c)}


@bp.route('/delete_permission', methods=['POST'])
@required_token
@check_params('id', 'code')
def delete_permission():
    data = request.json
    delete_by_obj('om_permission', data)
    permission = select_by_where('om_permission', data)
    if len(permission) == 0:
        return {'msg': '删除成功'}
    else:
        return {'msg': '删除失败'}


@bp.route('/select_role_permission', methods=['POST'])
@required_token
@check_params('role_id')
@check_permission('role:query')
def select_role_permission():
    data = request.json

    permission = get_model('om_permission')
    role_permission = get_model('om_role_permission')

    sql = db_session.execute(
        select(permission).join(role_permission, role_permission.permission_id == permission.id).where(
            role_permission.role_id == data['role_id'])).mappings().all()

    res = []
    for row in sql:
        res.extend(to_json2(row['om_permission']))

    return {'msg': '查询成功', 'data': res}


@bp.route('/add_role_permission', methods=['POST'])
@required_token
@check_params('role_id', 'permission_id_list')
@check_permission('role:add')
def add_role_permission():
    data = request.json
    permission_id_list = data['permission_id_list']
    for i in permission_id_list:
        obj = {'role_id': data['role_id'], 'permission_id': i}
        exist = select_by_where('om_role_permission', obj)
        if exist:
            return {'msg': '权限 {} 已存在'.format(i)}, 400
        insert_by_obj('om_role_permission', obj)

    return {'msg': '创建成功'}


@bp.route('/delete_role_permission', methods=['POST'])
@required_token
@check_params('role_id', 'permission_id_list')
@check_permission('role:update')
def delete_role_permission():
    data = request.json
    obj = {'role_id': data['role_id'], 'permission_id': data['permission_id_list']}
    delete_by_obj('om_role_permission', obj)
    exist = select_by_where('om_role_permission', obj)
    if len(exist) == 0:
        return {'msg': '删除成功'}
    else:
        return {'msg': '删除失败'}


if __name__ == '__main__':
    pass
