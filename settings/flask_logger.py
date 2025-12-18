#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/28 9:29
# @Author  : Ewan
# @File    : flask_logger.py
# @Description : 自定义log 通过 app.logger.addHandler(mail_handler) 添加

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import has_request_context, request

# 日志格式化类型
file_format = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url_rule
            # record.remote_addr = request.remote_addr

            if request.method == 'GET':
                record.args = request.args.to_dict()
            elif request.method == 'POST':
                if request.content_type == 'application/json':
                    record.args = request.json
                elif 'multipart/form-data' in request.content_type:
                    record.args = request.form.to_dict()
                    if request.files:
                        # record.args.update({k: v.filename for k, v in request.files.to_dict().items()})
                        record.args.update(request.files.to_dict())
            elif request.method=='OPTIONS':
                # 预检方法无参数
                record.msg = 'OPTIONS without params'
            else:
                # FIXME method只处理了GET/POST , Content-Type只考虑了键值对/JSON/表单数据
                record.msg = 'Params cannot be parsed'
        else:
            record.url = None
            # record.remote_addr = None

        return super().format(record)


# '[%(asctime)s] %(levelname)s %(url)s | %(args)s | %(message)s'
# '[%(asctime)s] %(levelname)s %(remote_addr)s Req %(url)s : %(args)s Msg:%(message)s'
api_format = RequestFormatter(
    '[%(asctime)s] %(levelname)s %(url)s args:%(args)s : %(message)s'
)

# 文件日志处理器 10M 备份数3
file_handler = RotatingFileHandler('logs/flask_api.log', encoding='utf-8', maxBytes=1024 * 1024 * 10, backupCount=3)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(api_format)

# Stream日志处理器 
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(api_format)

# 根日期记录器 日志名/日志等级 这里直接使用flaks的logger
# root_logger = logging.getLogger('root_logger')
# root_logger.setLevel(logging.DEBUG)
# root_logger.addHandler(file_handler)
