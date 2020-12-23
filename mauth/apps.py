# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: apps.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
from django.apps import AppConfig


class MauthConfig(AppConfig):
    name = 'mauth'
    verbose_name = '用户系统'
