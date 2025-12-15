#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/21 10:09
# @Author  : Ewan
# @File    : product_manage.py
# @Description : 商品管理

from flask import Blueprint, request, abort, url_for
from sqlalchemy import select
from core.db import db_session, select_by_where, insert_by_obj, update_by_obj, delete_by_obj, get_model
from core.api_check import required_token, check_params
from core.utils import to_json2

bp = Blueprint('product_manage', __name__, url_prefix='/ProdManage', template_folder='/templates')


@bp.route('/select_prod', methods=['POST'])
@required_token
# @check_params()
def select_prod():
    data = request.json
    prod = select_by_where('om_prod', data)
    # 查询产品标签
    tag_m = get_model('om_prod_tag')
    tag_rela_m = get_model('om_tag_rela')

    p_tag = db_session.execute(
        select(tag_m, tag_rela_m.pid).join(tag_rela_m, tag_rela_m.tid == tag_m.tid).where(
            tag_m.is_del == 0).where(tag_rela_m.d_date == None)).mappings().all()

    p_tag_flist = []
    for row in p_tag:
        r1 = to_json2(row['om_prod_tag'])[0]
        r2 = {k: v for k, v in row.items() if k != 'om_prod_tag'}
        res = {**r1, **r2}
        # print('res:', res)
        p_tag_flist.append(res)
    # print('p_tag_flist:',p_tag_flist)
    for p in prod:
        tags = []
        for tag in p_tag_flist:
            if tag['pid'] == p['pid']:
                tags.append({'tid': tag['tid'], 'tname': tag['tname']})
        p['tags'] = tags
    return {'msg': '查询成功', 'data': prod}


@bp.route('/create_prod', methods=['POST'])
@required_token
@check_params()
def create_prod():
    data = request.json
    list_data = data['values'] if data.get('values') else [data]
    c = 0
    for i in list_data:
        prod = {k: v for k, v in i.items() if k != 'tags'}
        insert_by_obj('om_prod', prod)

        cur_prod = select_by_where('om_prod', prod)
        delete_by_obj('om_tag_rela', {'pid': cur_prod[0]['pid']})
        tag_add = [{'pid': cur_prod[0]['pid'], 'tid': tid} for tid in i['tags']]
        insert_by_obj('om_tag_rela', tag_add)

        c = c + 1 if cur_prod else c

    #    insert_by_obj('om_prod', list_data)
    #    c = 0
    #    for i in list_data:
    #        prod = select_by_where('om_prod', i)
    #        c = c + 1 if prod else c

    if len(list_data) == c:
        return {'msg': '创建成功'}
    else:
        return {'msg': '创建成功{}个'.format(c)}


@bp.route('/update_prod', methods=['POST'])
@required_token
@check_params()
def update_prod():
    data = request.json
    list_data = data['values'] if data.get('values') else [data]
    update_by_obj('om_prod', list_data)
    c = 0
    for i in list_data:
        prod = {k: v for k, v in i.items() if k != 'tags'}
        update_by_obj('om_prod', prod)
        cur_prod = select_by_where('om_prod', prod)

        delete_by_obj('om_tag_rela', {'pid': prod['pid']})
        tag_add = [{'pid': prod['pid'], 'tid': tid} for tid in i['tags']]
        insert_by_obj('om_tag_rela', tag_add)

        c = c + 1 if cur_prod else c
    if len(list_data) == c:
        return {'msg': '更新成功'}
    else:
        return {'msg': '更新成功{}个'.format(c)}


@bp.route('/delete_prod', methods=['POST'])
@required_token
@check_params('pid', 'uid')
def delete_prod():
    data = request.json
    delete_by_obj('om_prod', {'pid': data['pid'], 'uid': data['uid']})
    delete_by_obj('om_tag_rela', {'pid': data['pid']})
    prod = select_by_where('om_prod', {'pid': data['pid'], 'uid': data['uid']})
    prod_tag = select_by_where('om_tag_rela', {'pid': data['pid']})
    if len(prod) == 0 and len(prod_tag) == 0:
        return {'msg': '删除成功'}
    else:
        return {'msg': '删除失败'}


@bp.route('/select_tag', methods=['GET'])
@required_token
def select_tag():
    prod = select_by_where('om_prod_tag', {'is_del': 0})  # 当前有效的产品

    def build_tree(nodes, parent=None):
        L = []
        for item in nodes:
            if item.get('ptid') == (parent if parent is None else parent.get('tid')):
                item['child'] = build_tree(nodes, item)
                L.append(item)
        return L

    # 构造标签树
    tree = build_tree(prod)
    return {'msg': '查询成功', 'data': tree}

    # 方法2 返回top
    # def get_childs(parent):
    #     childs = []
    #     for item in prod:
    #         if item.get('ptid') == parent.get('tid'):
    #             item['child'] = get_childs(item)
    #             childs.append(item)
    #     return childs
    #
    # top = [i for i in prod if i.get('ptid') is None]
    # for i in top:
    #     i['child'] = get_childs(i)
    # return {'msg': '查询成功', 'data': top}


@bp.route('/create_tag', methods=['POST'])
@required_token
@check_params('tname')
def create_tag():
    # 一次新增一个
    data = request.json
    insert_by_obj('om_prod_tag', data)
    prod = select_by_where('om_prod_tag', data)
    if prod:
        return {'msg': '创建成功'}
    else:
        return {'msg': '创建失败'}


@bp.route('/update_tag', methods=['POST'])
@required_token
@check_params('tid')
def update_tag():
    # 一次修改一个
    data = request.json
    update_by_obj('om_prod_tag', data)
    prod = select_by_where('om_prod_tag', data)
    if prod:
        return {'msg': '更新成功'}
    else:
        return {'msg': '更新失败'}


@bp.route('/delete_tag', methods=['POST'])
@required_token
@check_params('tid')
def delete_tag():
    # 逻辑删除标签及其子项
    data = request.json
    nodes = select_by_where('om_prod_tag', {'is_del': 0})

    def delete_node(nodes, node_id):
        # 构建父ID到子ID的映射
        children_map = {}
        for node in nodes:
            if node['ptid'] is not None:
                children_map.setdefault(node['ptid'], []).append(node['tid'])

        # 递归DFS（深度≤5，安全无风险）
        to_remove = []

        def dfs(node_id):
            to_remove.append(node_id)
            if node_id in children_map:
                for child_id in children_map[node_id]:
                    dfs(child_id)

        dfs(node_id)
        return [{'tid': node, 'is_del': 1} for node in to_remove]

    d_list = delete_node(nodes, data['tid'])
    update_by_obj('om_prod_tag', d_list)
    return {'msg': '删除成功'}


@bp.route('/file_test', methods=['POST'])
@required_token
def file_test():
    print('from:', request.form)
    # print('json:', request.get_json(force=True))
    print('file:', request.files)
    print(request.files.to_dict())
    return {'msg': 'ok'}


# @bp.route('/prod_add_tag', methods=['POST'])
# @required_token
# @check_params('pid', 'tid')
# def prod_add_tag():
#     data = request.json
#     in_data = [{'pid': data['pid'], 'tid': tid} for tid in data['tid']]
#     insert_by_obj('om_tag_rela', in_data)
#     add_num = select_by_where('om_tag_rela', data)
#     if len(add_num) == len(data['tid']):
#         return {'msg': '新增产品标签成功'}
#     else:
#         return {'msg': '新增产品标签失败'}
# 
# 
# @bp.route('/prod_del_tag', methods=['POST'])
# @required_token
# @check_params('pid', 'tid')
# def prod_del_tag():
#     data = request.json
#     delete_by_obj('om_tag_rela', data)
#     num = select_by_where('om_tag_rela', data)
#     if num:
#         return {'msg': '删除产品标签成功'}
#     else:
#         return {'msg': '删除产品标签失败'}


@bp.route('/select_stock', methods=['GET'])
@required_token
def select_stock():
    stock = get_model('om_prod_stock')
    prod = get_model('om_prod')
    res = db_session.execute(
        select(prod, stock.quantity).join(stock, prod.pid == stock.pid)).mappings().all()
    res_list = []

    for row in res:
        r1 = to_json2(row['om_prod'])[0]
        r2 = {k: v for k, v in row.items() if k != 'om_prod'}
        res = {**r1, **r2}
        res_list.append(res)

    return {'msg': '查询成功', 'data': res_list}


@bp.route('/select_stock_log', methods=['GET'])
@required_token
@check_params('pid')
def select_stock_log():
    pid = request.args.get('pid')
    stock_log = get_model('om_stock_log')
    prod = get_model('om_prod')
    res = db_session.execute(
        select(stock_log, prod.pname).join(prod, prod.pid == stock_log.pid).where(prod.pid == pid)).mappings().all()
    res_list = []
    for row in res:
        r1 = to_json2(row['om_stock_log'])[0]
        r2 = {k: v for k, v in row.items() if k != 'om_stock_log'}
        res = {**r1, **r2}
        res_list.append(res)

    return {'msg': '查询成功', 'data': res_list}


@bp.route('/stock_in', methods=['POST'])
@required_token
@check_params('pid', 'op_uid', 'op_num', 'note')
def stock_in():
    # 商品入库
    data = request.json
    if data['op_num'] < 0:
        return {'msg': '入库数量不合法'}, 500
    op_prod = {'pid': data['pid']}
    prod = select_by_where('om_prod_stock', op_prod)
    if not prod:  # 如果该产品没有库存信息
        op_prod['quantity'] = data['op_num']
        insert_by_obj('om_prod_stock', op_prod)
    else:
        op_prod['quantity'] = prod[0]['quantity'] + data['op_num']
        update_by_obj('om_prod_stock', op_prod)

    # 补充操作信息到商品出入库流水表
    log = {'pid': data['pid'], 'op_type': 1, 'op_num': data['op_num'], 'op_uid': data['op_uid'], 'note': data['note']}
    insert_by_obj('om_stock_log', log)

    return {'msg': '商品成功入库{}件'.format(data['op_num'])}


@bp.route('/stock_out', methods=['POST'])
@required_token
@check_params('pid', 'op_uid', 'op_num', 'note')
def stock_out():
    # 商品出库
    data = request.json
    if data['op_num'] < 0:
        return {'msg': '出库数量不合法'}, 500
    op_prod = {'pid': data['pid']}
    prod = select_by_where('om_prod_stock', op_prod)
    if not prod:  # 如果该产品没有库存信息
        return {'msg': '商品库存信息不存在,请先入库后再出库'}, 500
    else:
        if prod[0]['quantity'] < data['op_num']:
            return {'msg': '出库数量不能大于当前库存'}, 500
        else:
            prod[0]['quantity'] -= data['op_num']
            update_by_obj('om_prod_stock', prod)
    # 补充操作信息到商品出入库流水表
    log = {'pid': data['pid'], 'op_type': 2, 'op_num': data['op_num'], 'op_uid': data['op_uid'], 'note': data['note']}
    insert_by_obj('om_stock_log', log)
    return {'msg': '商品成功出库{}件'.format(data['op_num'])}


@bp.route('/stock_cancel', methods=['POST'])
@required_token
@check_params('id', 'uid')
def stock_cancel():
    # 出入库操作撤销
    data = request.json
    op_log = select_by_where('om_stock_log', {'id': data['id']})
    if not op_log:  # 如果没有该日志
        return {'msg': '操作信息不存在,撤销操作失败'}, 500
    else:
        if op_log[0]['op_type'] == 1:
            prod = select_by_where('om_prod_stock', {'pid': op_log[0]['pid']})
            prod[0]['quantity'] -= op_log[0]['op_num']
            # 补充操作信息到商品出入库流水表
            log = {'pid': op_log[0]['pid'], 'op_type': 3, 'op_num': op_log[0]['op_num'], 'op_uid': data['uid'],
                   'note': '商品入库撤销'}
        elif op_log[0]['op_type'] == 2:
            prod = select_by_where('om_prod_stock', {'pid': op_log[0]['pid']})
            prod[0]['quantity'] += op_log[0]['op_num']
            # 补充操作信息到商品出入库流水表
            log = {'pid': op_log[0]['pid'], 'op_type': 4, 'op_num': op_log[0]['op_num'], 'op_uid': data['uid'],
                   'note': '商品出库撤销'}
        else:
            return {'msg': '该记录不支持撤销'}, 500
        update_by_obj('om_prod_stock', prod)
        insert_by_obj('om_stock_log', log)
    return {'msg': '撤销成功'}
