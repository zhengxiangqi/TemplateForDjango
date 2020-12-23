# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: wxweb.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
import requests
from . import config


def get_access_token(code):
    """
    正确的返回数据如下：
    {
        "access_token":"ACCESS_TOKEN",
        "expires_in":7200,
        "refresh_token":"REFRESH_TOKEN",
        "openid":"OPENID",
        "scope":"SCOPE",
        "unionid": "o6_bmasdasdsad6_2sgVt7hMZOPfL"
    }

    错误的返回数据如下：
    {
        "errcode":40029,
        "errmsg":"invalid code"
    }
    """
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' +\
          'appid=' + config.wxweb['app_id'] +\
          '&secret=' + config.wxweb['app_secret'] +\
          '&code=' + code + \
          '&grant_type=authorization_code'
    result = requests.get(url).json()
    return result


def get_user_info(access_token, openid):
    """
    正确的返回数据如下：
    {
        "openid":"OPENID",
        "nickname":"NICKNAME",
        "sex":1,
        "province":"PROVINCE",
        "city":"CITY",
        "country":"COUNTRY",
        "headimgurl": "http://wx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
        "privilege":[
        "PRIVILEGE1",
        "PRIVILEGE2"
        ],
        "unionid": " o6_bmasdasdsad6_2sgVt7hMZOPfL"
    }

    错误的返回数据如下：
    {
        "errcode":40003,
        "errmsg":"invalid openid"
    }
    """
    url = 'https://api.weixin.qq.com/sns/userinfo?' +\
        'access_token=' + access_token +\
        '&openid=' + openid
    result = requests.get(url).json()
    return result
