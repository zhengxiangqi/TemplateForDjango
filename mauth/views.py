# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: views.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
from .models import User
from .models import Token
from django.utils import timezone
from django.http import QueryDict
from django.db.models import Q
from django.core.paginator import Paginator
from rzutils import error
from rzutils.string import md5
from rzutils.string import uuidstr
from rzutils.views import BaseView
from rzutils.permissions import param_required
from rzutils.permissions import is_authenticated
from rzutils.response import success
from rzutils import regex
import datetime


class RegisterApi(BaseView):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        param_required(username, 'username')
        param_required(password, 'password')
        assert regex.check(regex.TYPE_USERNAME, username), error.parameter_invalid('username')
        assert regex.check(regex.TYPE_PASSWORD, password), error.parameter_invalid('password')

        user = User.objects.filter(username=username).first()
        assert user is None, error.object_already_exist('user')

        user = User(username=username, password=md5(password))
        user.save()

        token = Token(user=user, token_text=uuidstr(), exp_date=timezone.now() + datetime.timedelta(days=7))
        token.save()

        return success([user, token], need_serialize=True)


class LoginApi(BaseView):
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        param_required(username, 'username')
        param_required(password, 'password')

        query_set = User.objects.filter(username=username)
        user = query_set.first()
        assert user is not None, error.object_not_found('user')
        user = query_set.filter(password=md5(password)).first()
        assert user is not None, error.parameter_invalid('password')

        token = Token.create_or_update_token(user)

        return success([user, token], need_serialize=True)


class PasswordApi(BaseView):
    def put(self, request):
        user = is_authenticated(request)
        PUT = QueryDict(request.body)

        old_password = PUT.get('old_password')
        new_password = PUT.get('new_password')
        param_required(old_password, 'old_password')
        param_required(new_password, 'new_password')
        assert regex.check(regex.TYPE_PASSWORD, new_password), error.parameter_invalid('new_password')
        assert user.password == md5(old_password), error.parameter_invalid('old_password')

        user.password = md5(new_password)
        user.save()

        return success([user], need_serialize=True)


class UserinfoApi(BaseView):
    def get(self, request):
        user = is_authenticated(request)
        return success([user], need_serialize=True)

    def put(self, request):
        user = is_authenticated(request)
        PUT = QueryDict(request.body)

        user.nickname = PUT.get('nickname') or user.nickname
        user.education = PUT.get('education') or user.education
        user.avatar_url = PUT.get('avatar_url') or user.avatar_url
        user.gender = PUT.get('gender') or user.gender
        user.age = PUT.get('age') or user.age
        user.email = PUT.get('email') or user.email
        user.summary = PUT.get('summary') or user.summary
        user.education = PUT.get('education') or user.education
        user.mschool = PUT.get('mschool') or user.mschool
        user.mgrade = PUT.get('mgrade') or user.mgrade
        user.mclass = PUT.get('mclass') or user.mclass
        user.country = PUT.get('country') or user.country
        user.province = PUT.get('province') or user.province
        user.city = PUT.get('city') or user.city
        user.save()

        return success([user], need_serialize=True)


class SearchApi(BaseView):
    def get(self, request):
        q = request.GET.get('q')
        assert q is not None, error.parameter_not_found('q')

        per_page = request.GET.get('per_page') or 10
        page = request.GET.get('page') or 1
        per_page = int(per_page)
        page = int(page)

        query_set = User.objects.filter(Q(username__icontains=q) | Q(nickname__icontains=q))
        paginator = Paginator(query_set, per_page)
        bind_data = {'cur_page': page, 'per_page': per_page, 'total_page': paginator.num_pages, 'total': paginator.count}

        item_list = []
        for item in paginator.get_page(page).object_list:
            ranking = User.objects.filter(level__gt=item.level).order_by('-level').count()
            same_rank_users = User.objects.order_by('-level').filter(level=item.level)
            for x in range(0, len(same_rank_users)):
                if same_rank_users[x] == item:
                    ranking += x + 1
                    break
            item_list.append(ranking)
        bind_data['ranking_list'] = item_list

        return success(paginator.get_page(page), bind_data=bind_data, need_serialize=True, use_natural_foreign_keys=True)
