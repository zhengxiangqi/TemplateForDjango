# !.venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: decorator.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
from .response import create_resp


def assert_handler(fun):
    """
    Assert异常装饰器,用来方便的进行断言式接口开发
    """
    def wrapper_fun(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except AssertionError as e:
            return e.args[0]
    return wrapper_fun


def error_handler(fun):
    """
    Assert异常装饰器,用来方便的进行断言式接口开发
    """
    def wrapper_fun(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except AssertionError as e:
            return e.args[0]
        except Exception as e:
            return create_resp(code=8000, data=[], message=str(e))
    return wrapper_fun
