#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2025/8/21 10:03
# @Author  : Ewan
# @File    : __init__.py
# @Description : 电商订单管理系统

'''
核心模块
1.用户认证系统 user_auth.py
    实现JWT令牌认证机制 -> Token令牌
    包含注册/登录/登出接口
    密码加密存储（bcrypt）
    令牌刷新机制
2.商品管理系统 product_manage.py
    商品CRUD接口
    商品分类标签体系
    库存管理（扣减/回滚）
    图片存储（可选OSS或本地存储）
3.订单处理系统 order_process.py
    购物车功能
    订单创建/支付/取消流程
    集成支付宝沙箱支付
    订单状态机设计（待支付/已支付/已发货/已完成）
'''

from .user_auth import *
from .product_manage import *
from .order_process import *
