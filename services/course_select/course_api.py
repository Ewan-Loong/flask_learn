#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/22 15:56
# @Author  : Ewan
# @File    : course_api.py
# @Description : 课程相关的后端
import datetime
import json

from flask import Blueprint, render_template, abort, request
from sqlalchemy import insert

from core.db import db_session
from models.course_select.course import *
from models.course_select.student import *

bp = Blueprint('course', __name__, url_prefix='/cs', template_folder='/templates')


@bp.route('/apply_course', methods=['POST'])
def apply_course():
    res = {}
    if request.json:
        data = request.json

        ca = CourseApply.query.filter(CourseApply.cid == data['cid'], CourseApply.sid == data['sid'],
                                      CourseApply.status.in_([1, 3])).one_or_none()

        if not ca:
            c = Course.query.filter(Course.id == data['cid']).one_or_none()
            s = Student.query.filter(Student.id == data['sid']).one_or_none()
            if c and s:
                # 插入登录记录
                c_apply = dict(cid=c.id, cname=c.cname, sid=s.id, sname=s.name, tid=c.tid, tname=c.tname,
                               apply_time=datetime.datetime.now(), status=1)
                db_session.execute(insert(CourseApply).values(c_apply))
                db_session.commit()
                res['mes'] = '申请成功'
            else:
                res['mes'] = '课程/学生不存在'
        else:
            res['mes'] = '请勿重复申请'
    else:
        res['msg'] = '错误输入'

    return res


@bp.route('/cancel_course', methods=['POST'])
def cancel_course():
    res = {}
    if request.json:
        data = request.json

        ca = CourseApply.query.filter(CourseApply.id == data['id'], CourseApply.sid == data['sid'], ).one_or_none()
        if ca and not ca.agree_time:
            if not ca.cancel_time:
                body = dict(cancel_time=datetime.datetime.now(), status=2)
                CourseApply.query.filter(CourseApply.id == data['id']).update(body)
                db_session.commit()
                res['mes'] = '取消申请成功'
            else:
                res['mes'] = '不能取消已经取消的课程申请'
        else:
            res['mes'] = '申请记录不存在 / 已被教师同意不允许取消'
    else:
        res['msg'] = '错误输入'

    return res


@bp.route('/agree_course', methods=['POST'])
def agree_course():
    res = {}
    if request.json:
        data = request.json

        ca = CourseApply.query.filter(CourseApply.id == data['id'], CourseApply.tid == data['tid'], ).one_or_none()

        if ca and ca.status == 1:
            body = dict(agree_time=datetime.datetime.now(), status=3)
            CourseApply.query.filter(CourseApply.id == data['id']).update(body)
            Course.query.filter(Course.id == ca.cid).update({Course.select_count: Course.select_count + 1})

            c_select = dict(cid=ca.cid, cname=ca.cname, sid=ca.sid, sname=ca.sname, tid=ca.tid, tname=ca.tname,
                            apply_time=ca.apply_time, agree_time=body["agree_time"])
            db_session.execute(insert(CourseSelect).values(c_select))

            db_session.commit()
            res['mes'] = '同意课程申请'
        else:
            res['mes'] = '该申请不存在 / 无法操作非申请状态的申请'
    else:
        res['msg'] = '错误输入'

    return res


@bp.route('/disagree_course', methods=['POST'])
def disagree_course():
    res = {}
    if request.json:
        data = request.json

        ca = CourseApply.query.filter(CourseApply.id == data['id'], CourseApply.tid == data['tid'], ).one_or_none()

        if ca and ca.status == 1:
            body = dict(disagree_time=datetime.datetime.now(), status=4)
            CourseApply.query.filter(CourseApply.id == data['id']).update(body)
            db_session.commit()
            res['mes'] = '不同意课程申请'
        else:
            res['mes'] = '该申请不存在 / 无法操作非申请状态的申请'
    else:
        res['msg'] = '错误输入'

    return res
