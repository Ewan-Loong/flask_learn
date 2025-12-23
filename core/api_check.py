#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/21 15:35
# @Author  : Ewan
# @File    : api_Token.py
# @Description : Token令牌工具
import functools
from datetime import timedelta, datetime
import time
import pytz
from flask import request, current_app
from itsdangerous import TimedSerializer, SignatureExpired, BadSignature
from sqlalchemy import select
from core.db import get_model, db_session
from core.utils import is_allowed_file, to_json2


# 生成密钥 并补充过期时间
def generate_token(data):
    # , expires_in=EXPIRES_IN):
    secret_key = getattr(current_app.config, "SECRET_KEY", 'DEFAULT_SECRET_KEY')
    s = TimedSerializer(secret_key)
    # expire = (datetime.now() + EXPIRES_IN).timestamp()
    # data.update({"exp": expires_in.seconds})
    return s.dumps(data)


# 校验Token / Token更新
def verify_token(t):
    secret_key = getattr(current_app.config, "SECRET_KEY", 'DEFAULT_SECRET_KEY')
    expires_in = getattr(current_app.config, "PERMANENT_SESSION_LIFETIME", timedelta(minutes=60))  # 过期时间默认60min
    resp = {'msg': "Token处理成功", 'data': {}}
    s = TimedSerializer(secret_key)
    try:
        data, exp = s.loads(t, return_timestamp=True)
        resp['data'] = data
        now = datetime.now(pytz.timezone('UTC')).replace(microsecond=0)
        seconds = (now - exp).total_seconds()  # 剩余时间秒数
        # print(seconds, expires_in.total_seconds())
        if seconds > expires_in.total_seconds():
            raise SignatureExpired('Token过期')
        if seconds < expires_in.total_seconds() / 2:  # 剩余有效时间小于过期时间的1/2重新生成
            resp['Token'] = generate_token(data)
            resp['msg'] = "Token更新成功"
    except Exception as e:
        raise e
    return resp


# 定义装饰器验证Token
def required_token(func):
    # flask的装饰器一定需要带上 @functools.wraps(func) 以保证最外层的函数名不变 且装饰器需要放置再最外层
    @functools.wraps(func)
    def required_inner(*arg, **kwargs):
        try:
            res = verify_token(request.headers['Token'])
            # print('Token校验通过')
        except SignatureExpired:
            return {'msg': "Token过期"}, 401
        except BadSignature:
            return {'msg': "Token校验失败"}, 401
        except Exception as e:
            return {'msg': str(e)}, 400
        return func(*arg, **kwargs)

    return required_inner


# 定义装饰器验证请求参数非空完整性 注意带参装饰器需要带括号@check_params()
def check_params(*required_params):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 获取不同请求的参数
            if request.method == 'POST':
                # get_json - JSON数据获取,force=True确保返回字典或列表,空会返回{}或[]
                # form.to_dict - 表单数据获取,注意:该方法不包含文件等非表单字段的数据
                args_list = request.get_json(force=True) if request.is_json else request.form.to_dict()
            else:  # 如果是GET请求，则获取URL参数
                args_list = request.args.to_dict()
            if not required_params:
                if not args_list:
                    return {'msg': 'Parameter cannot be empty'}, 400
            else:
                missing = [item for item in required_params if item not in args_list.keys() or args_list[item] == '']
                if missing:
                    return {'msg': 'Missing parameter: {}'.format(','.join(missing))}, 400
            return func(*args, **kwargs)

        return wrapper

    return decorator


# 定义角色权限校验器
def check_permission(*permission_list):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 获取当前请求的用户 token中包含用户id
            uid = request.headers['Token'].split('.')[0]
            # TODO 可以配置上redis缓存机制 提高校验速度

            # 数据库获取用户角色权限信息
            user = get_model('om_user')
            permission = get_model('om_permission')
            role_permission = get_model('om_role_permission')

            sql = db_session.execute(
                select(permission)
                .join(role_permission, role_permission.permission_id == permission.id)
                .join(user, user.rid == role_permission.role_id)
                .where(user.uid == uid)
            ).mappings().all()
            # 权限验证并返回
            user_per = []
            for row in sql:
                user_per.extend(to_json2(row['om_permission']))

            user_per_list = set(i['code'] for i in user_per)
            # 通配符权限
            permission_build = set([i.split(':')[0] + ':*' for i in permission_list])
            if not (set(permission_list).issubset(user_per_list) or set(permission_build).issubset(user_per_list)):
                miss = [i for i in permission_list if i not in user_per_list]
                return {'msg': '用户缺少权限{}'.format(miss)}, 403
            else:
                current_app.logger.info('用户({})调用API权限验证通过'.format(uid))
            return func(*args, **kwargs)

        return wrapper

    return decorator


# 验证文件上传时 文件是否符合服务器要求-文件名 文件类型 文件大小
def check_files(func):
    @functools.wraps(func)
    def decorator(*arg, **kwargs):
        if 'file' not in request.files:
            return {'msg': 'No file part found'}, 400

        file = request.files['file']
        if file.filename == '':
            return {'msg': 'No selected file'}, 400

        if not is_allowed_file(file.filename):
            return {"msg": "Type not supported"}, 400

        if len(file.read()) > current_app.config.get('MAX_FILE_SIZE'):
            return {"msg": "Size exceeds limit (16MB)"}, 400
        file.seek(0)

        return func(*arg, **kwargs)

    return decorator


if __name__ == '__main__':
    # 生成令牌
    Token = generate_token({'user': 'A01'})
    print("生成令牌:", Token)
    time.sleep(1)
    # 验证令牌
    res = verify_token(Token)
    print("验证令牌:", res)

    # # 示例用法
    # # 创建一个UTC时间（带时区信息）
    # utc_now = pytz.utc.localize(datetime.utcnow())
    # print(f"UTC时间: {utc_now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
    #
    # # 转换为当地时间
    # local_time = utc_to_local(utc_now)
    # print(f"当地时间: {local_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
    # print(f"系统时区: {local_time.tzinfo.zone}")
    pass
