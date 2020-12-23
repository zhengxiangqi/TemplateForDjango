# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: regex.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
import re

TYPE_EMAIL = 0
TYPE_PHONE_GLOBAL = 1
TYPE_PHONE_CN = 2
TYPE_USERNAME = 3
TYPE_PASSWORD = 3
TYPE_NUMBER = 4
TYPE_CHAR = 5

PATTERN_EMAIL = '^(\w)+(\.\w+)*@(\w)+((\.\w{2,3}){1,3})$'
PATTERN_PHONE_GLOBAL = '^(([0\+]\d{2,3}-)?(0\d{2,3})-)?(\d{7,8})(-(\d{3,}))?$'
PATTERN_PHONE_CN = '^(13[0-9]|14[0-9]|15[0-9]|17[0-9]|18[0-9])\d{8}$'
PATTERN_USERNAME = '^[a-zA-Z\d\.\-\_]+$'
PATTERN_NUMBER = '^[\d]+$'
PATTERN_CHAR = '^[a-zA-Z]+$'
PATTERN = [PATTERN_EMAIL, PATTERN_PHONE_GLOBAL, PATTERN_PHONE_CN, PATTERN_USERNAME, PATTERN_NUMBER, PATTERN_CHAR]


def check(re_type, string):
    """
    正则表达式验证

    :param re_type: 验证类型,目前支持:TYPE_EMAIL/TYPE_PHONE_GLOBAL/TYPE_PHONE_CN

    :param string: 验证字段

    :return: 若验证通过,则返回对象,否则返回None
    """
    string = str(string)
    result = re.match(PATTERN[re_type], string)
    return result
