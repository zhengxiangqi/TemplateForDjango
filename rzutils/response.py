# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: response.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
import json
from django.http import HttpResponse
from django.core import serializers


def create_resp(code, data=[], message='', bind_data={}, content_type="application/json"):
    resp = {'code': code, 'data': data, 'message': message}
    resp = dict(resp, **bind_data)
    if content_type != "application/json":
        http_resp = HttpResponse(data, content_type=content_type)
    else:
        http_resp = HttpResponse(json.dumps(resp), content_type=content_type)
    http_resp['Access-Control-Allow-Origin'] = '*'
    http_resp['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
    http_resp['Access-Control-Allow-Headers'] = "Referer,Accept,Origin,User-Agent,Content-Type"
    return http_resp


def success(data=[], message='success', need_serialize=False, bind_data={}, use_natural_foreign_keys=False, use_natural_primary_keys=False, content_type="application/json"):
    if need_serialize:
        data = serializers.serialize('json', data, use_natural_foreign_keys=use_natural_foreign_keys, use_natural_primary_keys=use_natural_primary_keys)
        data = json.loads(data)

    return create_resp(2000, data, message, bind_data, content_type)
