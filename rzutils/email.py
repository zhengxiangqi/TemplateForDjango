# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: emailtool.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
from . import config
import smtplib
from email.mime.text import MIMEText
import hashlib
import time

__mailto_list = ['1075953039@qq.com']


def send(to_list, sub, content):
    content = '<a href="' + content + '">' + content + '</a>'
    msg = MIMEText(content, _subtype='html', _charset='gb2312')
    msg['Subject'] = sub + '(操作码:' + hashlib.md5(str(time.time())).hexdigest() + ')'
    msg['From'] = config.mail['user_name']
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(config.mail['host'])
        server.login(config.mail['user_name'], config.mail['password'])
        server.sendmail(config.mail['user_name'], to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False


if __name__ == '__main__':
    if send(__mailto_list, "hello", "hello world！"):
        print("发送成功")
    else:
        print("发送失败")
