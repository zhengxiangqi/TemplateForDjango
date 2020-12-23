# !.venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: views.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
from django.views import View
from django.utils.decorators import classonlymethod
from django.views.decorators.csrf import csrf_exempt
from rzutils.decorator import assert_handler
from rzutils.decorator import error_handler
from rzutils.response import success


class BaseView(View):
    @classonlymethod
    def as_view_csrf(cls, **initkwargs):
        return csrf_exempt(assert_handler(cls.as_view()))

    def get(self, request, id=None):
        return success(message='http method not allowed')

    def post(self, request, id=None):
        return success(message='http method not allowed')

    def put(self, request, id=None):
        return success(message='http method not allowed')

    def delete(self, request, id=None):
        return success(message='http method not allowed')

    def options(self, request, id=None):
        return success()


class NoneErrorView(View):
    @classonlymethod
    def as_view_csrf(cls, **initkwargs):
        return csrf_exempt(error_handler(cls.as_view()))

    def get(self, request, id=None):
        return success(message='http method not allowed')

    def post(self, request, id=None):
        return success(message='http method not allowed')

    def put(self, request, id=None):
        return success(message='http method not allowed')

    def delete(self, request, id=None):
        return success(message='http method not allowed')

    def options(self, request, id=None):
        return success()
