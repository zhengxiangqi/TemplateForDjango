# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: urls.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
from django.urls import path
from . import views

app_name = 'mauth'

urlpatterns = [
    path('register/', views.RegisterApi.as_view_csrf(), name='register'),
    path('login/', views.LoginApi.as_view_csrf(), name='login'),
    path('password/', views.PasswordApi.as_view_csrf(), name='password'),
    path('userinfo/', views.UserinfoApi.as_view_csrf(), name='userinfo'),
    path('search/', views.SearchApi.as_view_csrf(), name='search'),
]
