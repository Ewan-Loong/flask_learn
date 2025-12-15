#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/21 10:09
# @Author  : Ewan
# @File    : user_auth.py
# @Description : 用户认证

from flask import Blueprint, request

from core.db import select_by_where, insert_by_obj, update_by_obj, delete_by_obj
from core.api_check import required_token, generate_token, verify_token, check_params
from bcrypt import gensalt, hashpw, checkpw

bp = Blueprint('user_auth', __name__, url_prefix='/UserAuth', template_folder='/templates')


@bp.route('/login', methods=['POST'])
@check_params('name', 'passwd')
def login():
    res = {'msg': '登录成功'}
    data = request.json
    user = select_by_where('om_user', {'name': data['name']})
    if not user:
        res['msg'] = '未查找到该用户'
    if user:
        if checkpw(data['passwd'].encode(), user[0]['passwd'].encode()):
            if user[0]['on_line'] == -1:
                user[0]['on_line'] = 1
                update_by_obj('om_user', user)
            res['token'] = generate_token(user[0]['uid'])
            res['user'] = user[0]
        else:
            res['msg'] = '用户名或密码错误'
    return res


@bp.route('/logout', methods=['POST'])
@required_token
@check_params('name', 'uid')
def logout():
    data = request.json
    user = select_by_where('om_user', data)
    user[0]['on_line'] = -1
    update_by_obj('om_user', user)
    return {'msg': '登出成功'}


@bp.route('/refresh_token')
@required_token
def refresh_token():
    # TOKEN检查刷新
    new_token = verify_token(request.headers['Token'])
    return {'code': 0, 'msg': '更新成功', 'token': new_token.get('Token')}


@bp.route('/select_user', methods=['POST'])
@required_token
# @check_params()
def select_user():
    data = request.json
    user = select_by_where('om_user', data)
    for i in user:
        i['passwd'] = '******'
    return {'msg': '查询成功', 'data': user}


@bp.route('/create_user', methods=['POST'])
# @required_token
@check_params()
def create_user():
    data = request.json
    list_data = data['values'] if data.get('values') else [data]
    salt = gensalt(14)  # 密码加密盐
    for i in list_data:
        # 密码加密并转化为字符串
        i['passwd'] = hashpw(i['passwd'].encode(), salt).decode('utf-8')
    insert_by_obj('om_user', list_data)
    c = 0
    for i in list_data:
        user = select_by_where('om_user', i)
        c = c + 1 if user else c
    if len(list_data) == c:
        return {'msg': '创建成功'}
    else:
        return {'msg': '创建成功{}个'.format(c)}


@bp.route('/update_user', methods=['POST'])
@required_token
@check_params()
def update_user():
    data = request.json
    list_data = data['values'] if data.get('values') else [data]
    salt = gensalt(14)  # 密码加密盐
    # 密码加密并转化为字符串
    for i in list_data:
        psd = i.get('passwd')
        if psd and psd != '******':
            i['passwd'] = hashpw(i['passwd'].encode(), salt).decode('utf-8')
        else :
            i.pop('passwd')
    update_by_obj('om_user', list_data)
    c = 0
    for i in list_data:
        user = select_by_where('om_user', i)
        c = c + 1 if user else c
    if len(list_data) == c:
        return {'msg': '更新成功'}
    else:
        return {'msg': '更新成功{}个'.format(c)}


@bp.route('/delete_user', methods=['POST'])
@required_token
@check_params('uid', 'name')
def delete_user():
    data = request.json
    data.pop('passwd')
    delete_by_obj('om_user', data)
    user = select_by_where('om_user', data)
    if len(user) == 0:
        return {'msg': '删除成功'}
    else:
        return {'msg': '删除失败'}

# @bp.errorhandler(500)
# def auth_not_found(error):
#     return {'msg': '输入参数错误'}, 500
