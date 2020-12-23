# !.venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: permissions.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
from .string import is_empty
from .string import is_not_empty
from . import error
# from django.http import QueryDict


SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


def param_required(param, param_name):
    assert is_not_empty(param), error.parameter_not_found(param_name)


def readonly(request):
    assert request.method in SAFE_METHODS, error.permission_denied()


def is_authenticated(request):
    from mauth.models import Token

    token_value = request.GET.get('token')
    assert token_value is not None, error.parameter_not_found('token')

    token = Token.objects.filter(token_text=token_value).first()
    assert token is not None, error.parameter_invalid('token')
    assert not token.was_expired(), error.parameter_expired('token')
    token.update_token()

    return token.user


def is_authenticated_or_readonly(request):
    assert (request.method in SAFE_METHODS or is_authenticated(request)), error.permission_denied()


def is_allowed_platform(request):
    platform = request.GET.get('platform')
    if is_empty(platform):
        return False
    platforms = ['phone', 'pad', 'web', 'pc', 'wx']
    assert platform in platforms, error.platform_not_supported()
