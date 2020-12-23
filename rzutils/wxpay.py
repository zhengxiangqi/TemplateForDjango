# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: wxpay.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
import requests
from .string import uuidstr
from .string import md5
from .string import get_original_time_stamp
from .string import parse_xml
from .config import wxpay


UNIFIED_ORDER_URL = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
TRADE_TYPE_MINAPP = "JSAPI"
TRADE_TYPE_WEB = "NATIVE"
TRADE_TYPE_APP = "APP"


def create_unified_order(openid, out_trade_no, notify_url, price=1, body=wxpay['default_body'], trade_type=TRADE_TYPE_MINAPP, spbill_create_ip='0.0.0.0', attach=None):
    """
    微信统一下单，下单完成可获取预支付交易会话标识 prepay_id、二维码链接 code_url（trade_type为NATIVE时）
    """
    nonce_str = uuidstr()
    total_fee = str(price)

    sign = "appid=" + wxpay['app_id'] + '&'
    if attach is not None:
        sign += "attach=" + attach + '&'
    sign += "body=" + body + '&'
    sign += "mch_id=" + wxpay['mch_id'] + '&'
    sign += "nonce_str=" + nonce_str + '&'
    sign += "notify_url=" + notify_url + '&'
    sign += "openid=" + openid + '&'
    sign += "out_trade_no=" + out_trade_no + '&'
    sign += "spbill_create_ip=" + spbill_create_ip + '&'
    sign += "total_fee=" + total_fee + '&'
    sign += "trade_type=" + trade_type + '&'
    sign += 'key=' + wxpay['mch_key']
    sign = md5(sign).upper()

    data = '<xml>'
    data += '<appid>' + wxpay['app_id'] + '</appid>'
    if attach is not None:
        data += '<attach>' + attach + '</attach>'
    data += '<body>' + body + '</body>'
    data += '<mch_id>' + wxpay['mch_id'] + '</mch_id>'
    data += '<nonce_str>' + nonce_str + '</nonce_str>'
    data += '<notify_url>' + notify_url + '</notify_url>'
    data += '<spbill_create_ip>' + spbill_create_ip + '</spbill_create_ip>'
    data += '<total_fee>' + total_fee + '</total_fee>'
    data += '<trade_type>' + trade_type + '</trade_type>'
    data += '<openid>' + openid + '</openid>'
    data += '<out_trade_no>' + out_trade_no + '</out_trade_no>'
    data += '<sign>' + sign + '</sign>'
    data += '</xml>'

    result = requests.post(UNIFIED_ORDER_URL, data=data.encode('utf-8'), json=None)
    result = parse_xml(result.text)
    prepay_id = None
    code_url = None
    if result['return_code'] == 'SUCCESS':
        if result['result_code'] == 'SUCCESS':
            prepay_id = result['prepay_id']
            if trade_type == TRADE_TYPE_WEB:
                code_url = result['code_url']
        else:
            print('\n>>>>>>>>>>>>>>>>>>>> wxpay error 2 >>>>>>>>>>>>>>>>>>>>')
            print(result['err_code'] + ': ' + result['err_code_des'])
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
    else:
        print('\n>>>>>>>>>>>>>>>>>>>> wxpay error 1 >>>>>>>>>>>>>>>>>>>>')
        print(result['return_msg'])
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')

    return prepay_id, code_url


def get_code_url(openid, out_trade_no, notify_url, price=1, body=wxpay['default_body'], spbill_create_ip='0.0.0.0', attach=None):
    """
    适用于网页支付，获取二维码
    """
    trade_type = TRADE_TYPE_WEB
    prepay_id, code_url = create_unified_order(openid, out_trade_no, notify_url, body=body, price=price, trade_type=trade_type, spbill_create_ip=spbill_create_ip, attach=None)
    return code_url


def get_wx_signature(openid, out_trade_no, notify_url, price=1, body=wxpay['default_body'], spbill_create_ip='0.0.0.0', attach=None):
    """
    适用于小程序支付，获取信息后客户端直接就可以发起支付
    """
    trade_type = TRADE_TYPE_MINAPP
    prepay_id, code_url = create_unified_order(openid, out_trade_no, notify_url, body=body, price=price, trade_type=trade_type, spbill_create_ip=spbill_create_ip, attach=None)
    if prepay_id is None:
        return None
    nonce_str = uuidstr()
    package = 'prepay_id=' + prepay_id
    time_stamp = get_original_time_stamp()
    pay_sign = 'appId=' + wxpay['app_id'] + '&' +\
        'nonceStr=' + nonce_str + '&' +\
        'package=' + package + '&' +\
        'signType=MD5&' +\
        'timeStamp=' + time_stamp + '&' +\
        'key=' + wxpay['mch_key']
    pay_sign = md5(pay_sign).upper()

    signature = {
        'timeStamp': time_stamp,
        'nonceStr': nonce_str,
        'package': package,
        'signType': 'MD5',
        'paySign': pay_sign
    }

    return signature
