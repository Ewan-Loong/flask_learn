#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/26 14:03
# @Author  : Ewan
# @File    : db.py


from sqlalchemy import create_engine, Table, select, insert, update, delete
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

from core.utils import to_json2
from settings import flask_config

engine = create_engine(flask_config.DB_URI,
                       pool_pre_ping=True,  # 自动检测连接有效性
                       pool_recycle=3600  # 每小时重建连接
                       )
# 反射数据库表模型:这样可以不手动建模型,直接使用 Base.classes[table] 获取模型;但不能反射非主键表
Base = automap_base()
Base.prepare(engine, reflect=True)
# print('已反射可使用模型:', Base.classes.keys())

# Base = declarative_base()
# Base.query = db_session.query_property()

# 自动刷新和提交 False,使用 db_session.commit() 提交, 使用db_session.close() 关闭
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))


def init_db():
    # 初始化数据库
    # 首次启动时,需在该位置导入所需模型,然后则会自动在数据库建表
    # 后续则使用 Base.classes[table] 获取模型
    # import models.order_manage
    Base.metadata.create_all(bind=engine)
    Base.prepare(engine, reflect=True)


def get_model(table_name):
    '''根据字符串名称返回模型类'''
    return Base.classes[table_name]


def build_subquery(table_name, fields_filter):
    '''根据字典对象生成子查询'''
    model = Base.classes[table_name]
    sql = select(model)
    for col, val in fields_filter.items():
        if isinstance(val, list):
            sql = sql.where(model.__table__.c[col].in_(val))
        else:
            sql = sql.where(model.__table__.c[col] == val)
    return sql.subquery()


# 定义基础增删查改
def select_by_where(table, by_filter=None):
    '''
    :param table: 表名字符串
    :param by_filter: 字典对象,{字段名:值/值列表,字段名:值/值列表...}
    :return: 字典列表
    '''
    # res = db_session.execute().fetchall() execute方法返回的是Row objects不易获取字段属性
    model = Base.classes[table]
    sql = select(model)
    if by_filter is not None:
        for col, val in by_filter.items():
            if isinstance(val, list):
                sql = sql.where(model.__table__.c[col].in_(val))
            else:
                sql = sql.where(model.__table__.c[col] == val)
    sql = sql.with_for_update(read=True)  # 加锁
    rows = db_session.scalars(sql).all()  # 返回: model类的obj list
    res = to_json2(rows)  # 格式化成 [{字段:值},...]
    return res


def insert_by_obj(table, objs):
    if not isinstance(objs, list):
        objs = [objs]
    try:
        model = Base.classes[table]
        if engine.name == 'mysql':
            db_session.execute(insert(model), objs)  # 注意mysql后端不支持returning
            res = objs
        else:
            rows = db_session.scalars(insert(model).returning(model), objs).all()
            res = to_json2(rows)  # 格式化成 [{字段:值},...]
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
    return res


def update_by_obj(table, objs):
    if not isinstance(objs, list):
        objs = [objs]
    try:
        model = Base.classes[table]
        # 这里update的内容是除了主键以外传入的所有参数,等价于使用update set where
        if engine.name == 'mysql':
            rows = db_session.execute(update(model), objs)  # 注意mysql后端不支持returning
            res = objs
        else:
            rows = db_session.scalars(update(model).returning(model), objs).all()
            res = to_json2(rows)  # 格式化成 [{字段:值},...]
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
    return res


def delete_by_obj(table, by_filter):
    try:
        model = Base.classes[table]
        sql = delete(model)
        if by_filter is not None:
            for col, val in by_filter.items():
                if isinstance(val, list):
                    sql = sql.where(model.__table__.c[col].in_(val))
                else:
                    sql = sql.where(model.__table__.c[col] == val)
        db_session.execute(sql)  # delete 没有返回
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
    return by_filter

# 以下内容暂未搞懂
# click.command 定义一个名为 init-db 命令行,类似于用代码编写脚本

# @click.command('init-db')
# @with_appcontext
# def init_db_command():
#     """清除现有数据并创建新表。"""
#     init_db()
#     click.echo('Initialized the database.')

# 把close_db 和 init_db_command 注册到app
# app.cli.add_command() 添加一个新的 可以与 flask 一起工作的命令；直接使用 flask init-db

# def init_app(app):
#     app.cli.add_command(init_db_command)
