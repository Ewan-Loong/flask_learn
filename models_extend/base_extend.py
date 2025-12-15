#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/23 9:34
# @Author  : Ewan
# @File    : base_extend.py
# @Description : 基本拓展 全模型可以添加的方法

# FIXME 待完善 目前添加的方法不知道如何调用self,方法给到的self实际是名为self的参数变量


from functools import wraps


class mod_extend:
    # 接受装饰的表
    def __init__(self, table=None):
        self.table = table

    # 接受调用的方法
    def __call__(self, callback):
        if isinstance(callback, classmethod):
            callback.__func__.__anotation__ = self
        else:
            callback.__anotation__ = self

        @wraps(callback)
        def wrap(*args, **kwargs):
            print(f"inner {self.table}")
            return callback(*args, **kwargs)

        return wrap
