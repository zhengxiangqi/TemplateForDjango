# !.venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: oss2.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
import time
import datetime
import json
import base64
import hmac
from hashlib import sha1 as sha
import oss2
from . import error
from .config import alioss
from .string import uuidstr

__auth = None
__bucket = None


def get_bucket():
    """
    获取阿里云bucket

    :return: 返回阿里云bucket
    """
    global __auth, __bucket
    if __auth is None:
        __auth = oss2.Auth(alioss['access_key_id'], alioss['access_key_secret'])
    if __bucket is None:
        __bucket = oss2.Bucket(__auth, alioss['end_point'], alioss['bucket_name'])
    return __bucket


def get_iso_8601(expire):
    """
    生成阿里云过期时间字段

    :param expire: 过期时间戳

    :return: 返回阿里云过期时间字段
    """
    gmt = datetime.datetime.fromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt


def get_token():
    """
    生成阿里云的签名,并格式化成json格式

    :return: 返回json格式阿里云授权签名,提供给客户端使用
    """
    now = int(time.time())
    expire_syncpoint = now + alioss['expire_time']
    expire = get_iso_8601(expire_syncpoint)

    policy_dict = {}
    policy_dict['expiration'] = expire
    condition_array = []
    array_item = []
    array_item.append('starts-with')
    array_item.append('$key')
    array_item.append(alioss['upload_dir'])
    condition_array.append(array_item)
    policy_dict['conditions'] = condition_array
    policy = json.dumps(policy_dict).strip()
    # policy_encode = base64.encodestring(policy)
    policy_encode = base64.b64encode(bytes(policy, 'utf-8'))
    h = hmac.new(bytes(alioss['access_key_secret'], 'utf-8'), policy_encode, sha)
    sign_result = base64.encodestring(h.digest()).strip()

    token_dict = {}
    token_dict['accessid'] = alioss['access_key_id']
    token_dict['host'] = alioss['end_point']
    token_dict['policy'] = bytes.decode(policy_encode)
    token_dict['signature'] = bytes.decode(sign_result)
    token_dict['expire'] = expire_syncpoint
    token_dict['dir'] = alioss['upload_dir']
    # result = json.dumps(token_dict)
    return token_dict


def upload_file(file_suffix, byte_data):
    """
    使用阿里云上传文件,采用uuid文件名

    :param file_suffix: 文件后缀,例如: png

    :param byte_data: 文件字节数据

    :return: 返回结果
    """
    file_name = uuidstr() + '.' + file_suffix
    result = get_bucket().put_object(key=file_name, data=byte_data)
    assert result.status == 200, error.file_upload_failed
    file_url = alioss['domain'] + '/' + file_name
    return file_url


def upload_file_by_dir(upload_dir, file_suffix, byte_data):
    """
    使用阿里云上传文件,采用uuid文件名

    :param upload_dir: 上传文件路径,例如: img

    :param file_suffix: 文件后缀,例如: png

    :param byte_data: 文件字节数据

    :return: 返回结果
    """
    file_name = uuidstr() + '.' + file_suffix
    result = get_bucket().put_object(key=upload_dir + '/' + file_name, data=byte_data)
    assert result.status == 200, error.file_upload_failed()
    file_url = alioss['domain'] + '/' + upload_dir + '/' + file_name
    return file_url


def delete_file(file_name):
    """
    删除文件

    :param file_name: 包含文件后缀的完整文件名

    :return: 返回是否删除成功
    """
    # result = bucket.delete_object(file_name)
    result = get_bucket().batch_delete_objects([file_name])
    assert result.status == 200, error.file_delete_failed
    return True


def delete_file_by_dir(file_dir, file_name):
    """
    删除文件

    :param file_name: 包含文件后缀的完整文件名

    :return: 返回是否删除成功
    """
    # result = bucket.delete_object(file_name)
    result = get_bucket().batch_delete_objects([file_dir + '/' + file_name])
    assert result.status == 200, error.file_delete_failed
    return True


def delete_file_by_url(url):
    """
    删除文件

    :param url: 文件url

    :return: 返回是否删除成功
    """
    url_split = url.split('/')
    file_name = url_split[len(url_split) - 1]
    return delete_file(file_name)


if __name__ == "__main__":
    token = get_token()
