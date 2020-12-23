# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: models.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
import json
from django.core import serializers


def default_natural_key(obj):
    return json.loads(serializers.serialize('json', [obj]))
