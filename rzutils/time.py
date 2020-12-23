# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: time.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
import time
import datetime

ISOTIMEFORMAT = '%Y-%m-%d %X'


def date_now():
    """
    获取当前时间的日期格式

    :return: 返回当前时间,例如: '2016-04-01 15:28:09'
    """
    return time.strftime(ISOTIMEFORMAT, time.localtime())


def get_today():
    """
    获取当前时间的日期格式

    :return: 返回当前时间,例如: '2016-04-01 15:28:09'
    """
    return datetime.date.strftime(datetime.datetime.today(), ISOTIMEFORMAT)


def get_delta_day(weeks=0, days=0, hours=0, minutes=0, seconds=0):
    """
    获取当前时间的指定差额日期的日期格式，例如几个月前、几天前、几小时前、几分钟前、几秒前

    :return: 返回当前时间,例如: '2016-04-01 15:28:09'
    """
    today = datetime.datetime.today()
    deltaDay = today - datetime.timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
    return datetime.date.strftime(deltaDay, ISOTIMEFORMAT)


def get_original_time():
    """
    获取原始的(1900年1月1日零点零分零秒)时间的日期格式

    :return: 返回当前时间,例如: '2016-04-01 15:28:09'
    """
    return datetime.time().strftime(ISOTIMEFORMAT)


def get_original_time_stamp():
    """
    获取原始的(1900年1月1日零点零分零秒)时间的时间戳

    :return: 返回时间戳,例如: '1490840662'
    """
    return int(time.time())
