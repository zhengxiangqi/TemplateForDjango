# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: error.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
from .response import create_resp


def method_not_supported(method):
    return create_resp(code=1000, message='method not supported: ' + method)


def parameter_not_found(parameter):
    return create_resp(code=1001, message='parameter not found: ' + parameter)


def parameter_invalid(parameter):
    return create_resp(code=1002, message='parameter invalid: ' + parameter)


def parameter_expired(parameter):
    return create_resp(code=1003, message='parameter expired: ' + parameter)


def parameter_format_error(parameter):
    return create_resp(code=1004, message='parameter format error: ' + parameter)


def object_not_found(mobject):
    return create_resp(code=4004, message='object not found: ' + mobject)


def object_already_exist(mobject):
    return create_resp(code=4005, message='object already exist: ' + mobject)


def do_something_failed(operation):
    return create_resp(code=4006, message=operation + ' filed')


def platform_not_supported():
    return create_resp(code=3001, message='platform not supported, currently supported: phone、 pad、 web、 pc、 wx')


def operation_denied():
    return create_resp(code=3002, message='operation denied')


def permission_denied():
    return create_resp(code=3003, message='permission denied')


def file_upload_failed():
    return create_resp(code=3004, message='file upload failed')


def file_delete_failed():
    return create_resp(code=3005, message='file delete failed')


def file_type_not_supported():
    return create_resp(code=3006, message='file type not supported')
