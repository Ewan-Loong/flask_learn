#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/21 9:32
# @Author  : Ewan
# @File    : __init__.py.py


__doc__ = '实体表结构的额外方法'

import models

from models_extend import base_extend

# 获取添加的模型方法
ex_method = {}
for i in dir(base_extend):
    ms = getattr(base_extend, i)
    if callable(ms):
        ex_method[i] = ms

# 把额外方法添加到模型
for j in dir(models):
    mod = getattr(models, j)
    if hasattr(mod, '__tablename__'):
        # print(mod)
        for k, v in ex_method.items():
            setattr(mod, k, v)
            print("{} 添加额外方法 {}".format(j, k))
