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
from django.db import models
from django.utils import timezone
from rzutils.models import default_natural_key
from rzutils.string import uuidstr
import datetime


class User(models.Model):
    username = models.CharField(unique=True, max_length=200, verbose_name='用户名')
    nickname = models.CharField(blank=True, max_length=200, verbose_name='昵称')
    password = models.CharField(blank=True, max_length=200, serialize=False, verbose_name='MD5密码')
    gender = models.BooleanField(default=True, verbose_name='性别')
    age = models.IntegerField(default=0, verbose_name='年龄')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    education = models.CharField(blank=True, max_length=200, verbose_name='学历')
    level = models.IntegerField(default=0, verbose_name='等级')
    integral = models.IntegerField(default=0, verbose_name='积分')
    gold = models.IntegerField(default=0, verbose_name='金币')
    country = models.CharField(blank=True, max_length=200, verbose_name='国家')
    province = models.CharField(blank=True, max_length=200, verbose_name='省份')
    city = models.CharField(blank=True, max_length=200, verbose_name='城市')
    phone = models.CharField(blank=True, max_length=20, verbose_name='手机')
    summary = models.CharField(blank=True, max_length=200, verbose_name='介绍')
    avatar_url = models.CharField(blank=True, max_length=200, verbose_name='头像')
    mschool = models.CharField(blank=True, max_length=200, verbose_name='学校')
    mgrade = models.CharField(blank=True, max_length=200, verbose_name='年级')
    mclass = models.CharField(blank=True, max_length=200, verbose_name='班级')
    regist_date = models.DateTimeField(verbose_name='注册日期', auto_now=True)
    last_login = models.DateTimeField(verbose_name='最近登录', auto_now=True)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def natural_key(self):
        return default_natural_key(self)

    def __str__(self):
        return self.username


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    token_text = models.CharField(max_length=64)
    exp_date = models.DateTimeField(verbose_name='过期时间')

    class Meta:
        verbose_name = '凭证'
        verbose_name_plural = '凭证'

    def was_expired(self):
        return timezone.now() > self.exp_date

    was_expired.admin_order_field = 'exp_date'
    was_expired.boolean = True
    was_expired.short_description = '是否过期'

    def update_token(self):
        self.exp_date = timezone.now() + datetime.timedelta(days=7)
        self.save()

    @staticmethod
    def create_or_update_token(user):
        token = user.token_set.first()
        if token is None:
            token = Token(user=user, token_text=uuidstr(), exp_date=timezone.now() + datetime.timedelta(days=7))
            token.save()
        else:
            token.token_text = uuidstr()
            token.update_token()
        return token

    def __str__(self):
        return self.user.username + ': ' + self.token_text
