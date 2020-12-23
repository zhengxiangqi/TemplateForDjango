# !.venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: config.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""

# 配置邮箱验证的发件人邮箱账号及密码
mail = {
    'host': 'host',
    'user_name': 'user_name',
    'password': 'password'
}

# 配置阿里云平台信息
alioss = {
    'bucket_name': 'bucket_name',
    'access_key_id': 'access_key_id',
    'access_key_secret': 'access_key_secret',
    'end_point': 'http://oss-cn-shenzhen.aliyuncs.com',
    'domain': 'http://xxx.xxx.xxx',
    'expire_time': 30,
    'upload_dir': ''
}

# 配置短信宝平台信息
cocsms = {
    'host': 'http://api.smsbao.com/sms',
    'user_name': 'user_name',
    'password': 'password',
    'app_name': 'app_name'
}

# 配置微信网页平台信息
wxweb = {
    'app_id': 'app_id',
    'app_secret': 'app_secret'
}

# 配置微信支付信息
wxpay = {
    'app_id': 'app_id',
    'app_secret': 'app_secret',
    'mch_id': 'mch_id',
    'mch_key': 'mch_key',
    'default_body': 'MyProduct'
}
