#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/23 13:58
# @Author  : Ewan
# @File    : app.py

import importlib
import traceback
from pathlib import Path

from flask import Flask, render_template
from flask.logging import default_handler
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from core.db import init_db
from services import *
from settings.flask_config import config
from settings.flask_logger import file_handler, stream_handler

app = Flask(__name__)
CORS(app)


def create_app(conf="dev"):
    # instance_relative_config :  告诉应用配置文件是相对于 instance folder 的相对路径。
    app.config.from_object(config.get(conf))
    # print(app.config)

    # 确保上传目录存在
    os.makedirs(config.get(conf).UPLOAD_FOLDER, exist_ok=True)

    # 中文返回
    # app.json.ensure_ascii = False

    # 日志记录器调整 重置默认日志输出格式
    # default_handler.setFormatter(api_format)
    app.logger.removeHandler(default_handler)
    app.logger.addHandler(stream_handler)
    app.logger.addHandler(file_handler)

    @app.route('/')
    def get_routes():
        """返回所有已注册的路由"""
        routes = []
        for rule in app.url_map.iter_rules():
            # 排除 Flask 内置的 static 路由
            if rule.endpoint == 'static':
                continue
            routes.append({
                'endpoint': rule.endpoint,
                'methods': sorted(rule.methods),
                'url': rule.rule
            })
        return {"routes": routes}

    # 登陆首页加载
    # @app.route('/hello')
    # def hello():
    #     return render_template('/login.html')

    # 处理所有 /*.html 请求
    # @app.route('/<path:filename>')
    # def serve_html(filename):
    #     # 防止路径穿越
    #     if '..' in filename or filename.startswith('/'):
    #         return "", 404
    #
    #     if filename.endswith('.html'):
    #         try:
    #             return render_template(filename)
    #         except FileNotFoundError:
    #             return "页面未找到", 404
    #     else:
    #         # 如果不是 .html，可以重定向到 index.html 或返回 404
    #         return "无效请求", 404

    @app.before_request
    def log_quest():
        app.logger.info('请求响应')

    # @app.after_request
    # def after_request():
    #     app.logger.info('请求完成')

    # Celery 集成
    # from .celery import app as celery_app
    # from celery.result import AsyncResult
    # @app.route('/task_progress', methods=['POST'])
    # def check_task_progress():
    #     if request.json:
    #         data = request.json
    #         task_id = data['task_id']
    #         result = AsyncResult(task_id, app=celery_app)
    #         return {'state': result.state, 'meta': result.info}  # 返回状态和元数据。

    # 注册蓝图 改用配置
    # app.register_blueprint(bp)

    # 获取蓝图 注册
    route_list = ['services', 'services/order_manage']
    for r in route_list:
        # glob 搜索当前目录下所有*.py文件,返回Path对象 (使用rglob可搜索当前目录及其子目录)
        # stem返回没有扩展名的文件全路径,如 services/hrms/hr_staff.py > hr_staff
        route_files = [f.stem for f in Path(r).glob('*.py') if f.stem != '__init__']

        for route_file in route_files:
            # 动态引入包,并注册bp蓝图对象
            module = importlib.import_module(f"{r.replace('/', '.')}.{route_file}")
            router = getattr(module, "bp", None)
            if router is not None:
                app.register_blueprint(router)

    # 初始化数据库
    init_db()

    # 结束app时断开数据库
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # 通用错误处理
    @app.errorhandler(Exception)
    def error_handling(e):
        app.logger.error(traceback.format_exc())  # 完整错误堆栈
        if isinstance(e, HTTPException):
            return e
        return e.__class__.__name__ + ' ' + str(e), 500

    return app


if __name__ == '__main__':
    create_app()
    # print('路由:', [str(url) for url in app.url_map.iter_rules()])
    app.run(host='0.0.0.0', port=5000)

# 设置环境变量
# set PYTHONPATH=G:\py_workspace\flask_learn;
# 手动启动
# flask --app app:create_app() run -h 0.0.0.0 -p 5000

# 这种方式为动态的添加路由 一般不用 常采用构建蓝图工厂的形式
# def add_route(func):
#     url = os.path.abspath(__file__) + '/' + func.__name__
#     print('正在添加路由:{}'.format(url))
#
#     def inner():
#         create_app().add_url_rule(url, view_func=func, methods=['POST'])
#
#     return inner
