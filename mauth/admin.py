# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: admin.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
from django.contrib import admin
from .models import User
from .models import Token


class UserAdmin(admin.ModelAdmin):
    verbose_name = '用户系统'
    list_filter = ['regist_date']
    list_display = (
        'id', 'username', 'nickname', 'gender', 'age', 'email', 'education', 'level', 'integral', 'country',
        'province', 'city', 'phone', 'summary', 'avatar_url', 'regist_date', 'last_login'
    )
    list_display_links = list_display
    search_fields = ['nickname']


class TokenAdmin(admin.ModelAdmin):
    def user_name(self, obj):
        if obj.user.nickname:
            return obj.user.nickname
        else:
            return obj.user.username
    user_name.admin_order_field = 'user__id'
    user_name.short_description = "所有者"

    verbose_name = '用户凭证'
    list_filter = ['exp_date']
    list_display = (
        'id', 'user_name', 'token_text', 'exp_date', 'was_expired'
    )
    list_display_links = list_display
    search_fields = ['token_text']


admin.site.register(User, UserAdmin)
admin.site.register(Token, TokenAdmin)
