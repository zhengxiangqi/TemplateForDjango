# !.venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: string.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
import hashlib
import uuid
import time
import xml.etree.ElementTree as ET


def is_empty(value):
    """
    判断值是否为空

    :param value: 值或对象

    :return: 若值为空则返回True,否则返回False
    """
    if value == '' or value is None:
        return True
    if isinstance(value, bytes):
        if len(value) == 0:
            return True
    return False


def is_not_empty(value):
    """
    判断值是否为非空

    :param value: 值或对象

    :return: 若值为非空则返回True,否则返回False
    """
    if isinstance(value, bytes):
        if len(value) == 0:
            return False
    if value != '' and value is not None:
        return True
    return False


def none_to_empty(dict):
    """
    将数据库获取到的数据中的null转换成空字符串，便于接口使用

    :param dict: 数据字典

    :return: 返回处理好的数据字典
    """
    for k in dict:
        if dict[k] is None:
            dict[k] = ''
        elif dict[k] == 'None':
            dict[k] = ''
    return dict


def uuidstr():
    """
    生成uuid字符串

    :return: 返回32位uuid字符串(小写)
    """
    return uuid.uuid1().hex


def md5(value):
    """
    对指定字符串生成md5字符串

    :param value: 用来md5格式化的字符串

    :return: 返回md5字符串
    """
    value = str(value).encode(encoding='utf-8')
    md5value = hashlib.md5(value).hexdigest()
    return md5value


def get_original_time_stamp():
    """
    获取原始的(1900年1月1日零点零分零秒)时间的时间戳

    :return: 返回时间戳,例如: '1490840662'
    """
    return str(int(time.time()))


def parse_xml(xmlstring):
    """xml生成为dict：，
    将tree中个节点添加到list中，将list转换为字典dict_init
    叠加生成多层字典dict_new"""
    root = ET.fromstring(xmlstring)
    dict_new = {}
    for child in root:
        dict_new[child.tag] = child.text
    return dict_new


def get_param_name(param):
    for itemx, itemy in locals().items():
        if param == itemy and itemx != 'item':
            return itemx
