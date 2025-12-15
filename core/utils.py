#!/usr/bin python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/23 15:56
# @Author  : Ewan
# @File    : utils.py
# @Description : 其他工具类
import os
from json import JSONEncoder
from datetime import datetime,date
import uuid
from decimal import Decimal
import time
import threading
import pytz
from flask import current_app


def get_system_timezone():
    """获取当前系统时区"""
    # 尝试获取系统时区
    try:
        return pytz.timezone(time.tzname[time.localtime().tm_isdst])
    except:
        #  fallback: 使用本地时区
        return pytz.utc.localize(datetime.utcnow()).astimezone().tzinfo


def utc_to_local(utc_time):
    """将UTC时间转换为当地时间"""
    if not isinstance(utc_time, datetime):
        raise TypeError("输入必须是datetime对象")

    # 如果UTC时间没有时区信息，手动添加UTC时区
    if utc_time.tzinfo is None:
        utc_time = pytz.utc.localize(utc_time)

    # 获取系统时区
    local_tz = get_system_timezone()

    # 转换为当地时间
    return utc_time.astimezone(local_tz)


def generate_unique_filename(original_name):
    """生成唯一安全的文件名（扩展名不带点）"""
    # 获取扩展名并去除前导点，转为小写
    ext = os.path.splitext(original_name)[1].lower().lstrip('.')

    if ext not in current_app.config.get('ALLOWED_EXTENSIONS'):
        ext = 'txt'  # 默认使用不带点的扩展名

    return f"{uuid.uuid4().hex[:8]}_{int(time.time())}.{ext}"  # 写入时再加点


def is_allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           os.path.splitext(filename)[1].lower().lstrip('.') in current_app.config.get('ALLOWED_EXTENSIONS')


# sql查询结果类型处理 Fixme 可能有遗漏
def sql_type_hand(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime("%Y-%m-%d")
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    elif isinstance(obj, bytes):
        return obj.decode('utf-8')
    else:
        return obj


# 序列化查询结果
def to_json(obj):
    res = {}
    for i in obj.__table__.columns.keys():
        res[i] = obj.__getattribute__(i)
    return res


def to_json2(objs):
    objs = objs if isinstance(objs, list) else [objs]
    res = []
    for item in objs:
        temp = {}
        for key in item.__table__.columns.keys():
            temp[key] = sql_type_hand(getattr(item, key))
        res.append(temp)
    return res
    # return json.dumps(res, cls=DataEncoder, ensure_ascii=False)


# json转码时 处理date datetime类型的数据
class DataEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, uuid.UUID):
            return str(obj)
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')
        else:
            return JSONEncoder.default(self, obj)


# 雪花算法:由Twitter的开源项目Snowflake提出，它生成的ID是一个64位的长整数，可以保证在分布式系统中生成的ID是唯一的。
class Snowflake:
    def __init__(self, datacenter_id, machine_id, epoch=1609459200000):  # Epoch时间，例如2021-01-01 00:00:00 UTC
        self.datacenter_id = datacenter_id  # 数据中心ID
        self.machine_id = machine_id  # 机器ID
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()  # 线程锁保证多线程环境下正确生成ID

    def _time_gen(self):
        return int(time.time() * 1000)

    def _wait_next_millis(self, last_timestamp):
        timestamp = self._time_gen()
        while timestamp <= last_timestamp:
            timestamp = self._time_gen()
        return timestamp

    def next_id(self):
        with self.lock:
            timestamp = self._time_gen()

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & 0xFFF  # 序列号最大为4095，超过则等待下一毫秒
                if self.sequence == 0:  # 如果序列号归零，则需要等待下一毫秒
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            # 构建ID：最高位是负号位，实际上用不到，所以忽略；然后是时间戳、数据中心ID、机器ID和序列号
            # <<位运算 输入1 > 变成0001 > 位运算后变成10000 0000 0000 > 4096
            id = ((timestamp - self.epoch) << 22) | (self.datacenter_id << 17) | (self.machine_id << 12) | self.sequence
            return id


if __name__ == "__main__":
    # sf = Snowflake(datacenter_id=1, machine_id=1)
    # print(sf.next_id())  # 生成一个ID
    # for i in range(10):
    #     print(secrets.token_hex())
    pass
