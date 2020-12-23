# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: cocsms.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
import requests
import hashlib
from . import error
from .config import cocsms


COCSMS_ERROR_MESSAGE = {
    '0': '验证码发送成功',
    '30': '密码错误',
    '40': '账号不存在',
    '41': '余额不足',
    '42': '帐号过期',
    '43': 'IP地址限制',
    '50': '内容含有敏感词',
    '51': '手机号码不正确',
}


def send(phone, code):
    """
    发送短信验证码

    :param phone: 手机号码

    :param code: 验证码

    :return: 返回发送结果,0为成功,其余均为失败
    """
    password = hashlib.md5(cocsms['password']).hexdigest()
    content = '【%s】您的验证码是%s, 10分钟内有效. 若非本人操作请忽略此消息' % (cocsms['app_name'], str(code))
    result = requests.get(cocsms['host'] + '?u=' + cocsms['user_name'] + '&p=' + password + '&m=' + str(phone) + '&c=' + content)
    status_code = result.content
    assert str(status_code) != '51', error.parameter_format_error('phone')
    assert str(status_code) == '0', error.do_something_failed('send verify code')
    return True


if __name__ == '__main__':
    result = send('18559666045', 3034)
    print(result)
