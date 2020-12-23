# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: vuforia.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
import httplib
import hashlib
import mimetypes
import hmac
import base64
from email.utils import formatdate
import json

# The hostname of the Cloud Recognition Web API
CLOUD_RECO_API_ENDPOINT = 'cloudreco.vuforia.com'
CLIENT_ACCESS_KEY = 'c68046fbc15fd7d8a69d71965444b2520ebebd34'
CLIENT_SECRET_KEY = 'ec086fd428863b18a65330ec3f0494bfb71d6743'
SERVER_ACCESS_KEY = '8f71612b7144901706f5bff2e24ec405d95165b7'
SERVER_SECRET_KEY = '6ba4884d39684a92ff9e0b3a7a35eaccfbe8beff'
VWS_HOSTNAME = 'vws.vuforia.com'


def compute_md5_hex(data):
    """Return the hex MD5 of the data"""
    h = hashlib.md5()
    h.update(data)
    return h.hexdigest()


def compute_hmac_base64(key, data):
    """Return the Base64 encoded HMAC-SHA1 using the provide key"""
    h = hmac.new(key, None, hashlib.sha1)
    h.update(data)
    return base64.b64encode(h.digest())


def authorization_header_for_request(access_key, secret_key, method, content, content_type, date, request_path):
    """Return the value of the Authorization header for the request parameters"""
    components_to_sign = list()
    components_to_sign.append(method)
    components_to_sign.append(str(compute_md5_hex(content)))
    components_to_sign.append(str(content_type))
    components_to_sign.append(str(date))
    components_to_sign.append(str(request_path))
    string_to_sign = "\n".join(components_to_sign)
    signature = compute_hmac_base64(secret_key, string_to_sign)
    auth_header = "VWS %s:%s" % (access_key, signature)
    return auth_header


def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    lines = []
    for (key, value) in fields:
        lines.append('--' + BOUNDARY)
        lines.append('Content-Disposition: form-data; name="%s"' % key)
        lines.append('')
        lines.append(value)
    for (key, filename, value) in files:
        lines.append('--' + BOUNDARY)
        lines.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        lines.append('Content-Type: %s' % get_content_type(filename))
        lines.append('')
        lines.append(value)
    lines.append('--' + BOUNDARY + '--')
    lines.append('')
    body = CRLF.join(lines)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


def get_content_type(filename):
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'


def send_query(max_num_results, include_target_data, image):
    """
    执行一次图像查询

    :param max_num_results: 支持返回的最大结果数量
    :param include_target_data: 是否返回目标信息
            “top”: only return target_data for top ranked match
            “none”: return no target_data
            “all”: for all matched targets.
    :param image: 图片路径
    :return: 返回查询结果
    """
    http_method = 'POST'
    date = formatdate(None, localtime=False, usegmt=True)

    path = "/v1/query"

    # The body of the request is JSON and contains one attribute, the instance ID of the VuMark
    with open(image, 'rb') as f:
        imagedata = f.read()

    content_type, request_body = encode_multipart_formdata([('include_target_data', include_target_data),
                                                            ('max_num_results', max_num_results)],
                                                           [('image', image, imagedata)])
    content_type_bare = 'multipart/form-data'

    # Sign the request and get the Authorization header
    auth_header = authorization_header_for_request(CLIENT_ACCESS_KEY, CLIENT_SECRET_KEY, http_method, request_body, content_type_bare,
                                                   date, path)

    request_headers = {
        'Accept': 'application/json',
        'Authorization': auth_header,
        'Content-Type': content_type,
        'Date': date
    }

    # Make the request over HTTPS on port 443
    http = httplib.HTTPSConnection(CLOUD_RECO_API_ENDPOINT, 443)
    http.request(http_method, path, request_body, request_headers)

    response = http.getresponse()
    response_body = response.read()
    return response.status, response_body


def get_target_list():
    """
    获取所有目标信息

    :return: 返回查询结果
    """
    http_method = 'GET'
    content_type = 'application/json'
    date = formatdate(None, localtime=False, usegmt=True)
    path = "/targets"
    request_body = ''

    # Sign the request and get the Authorization header
    auth_header = authorization_header_for_request(SERVER_ACCESS_KEY, SERVER_SECRET_KEY, http_method, request_body, content_type,
                                                   date, path)
    request_headers = {
        'Accept': 'application/json',
        'Authorization': auth_header,
        'Content-Type': content_type,
        'Date': date
    }

    # Make the request over HTTPS on port 443
    http = httplib.HTTPSConnection(VWS_HOSTNAME, 443)
    http.request(http_method, path, headers=request_headers)

    response = http.getresponse()
    response_body = response.read()
    return response.status, response_body


def add_image_target_with_data(image_data, target_name, application_metadata=None, active_flag=True):
    """
    添加图像目标

    :param image_data: 图片数据
    :param target_name: 图片名称
    :param application_metadata: 元数据
    :return: 返回添加结果
    """
    http_method = 'POST'
    content_type = 'application/json'
    date = formatdate(None, localtime=False, usegmt=True)
    path = "/targets"

    content = {
        "name": target_name,
        'width': 140.0,
        'image': base64.b64encode(image_data),
        'application_metadata': application_metadata,
        'active_flag': active_flag
    }
    request_body = json.dumps(content)

    # Sign the request and get the Authorization header
    auth_header = authorization_header_for_request(SERVER_ACCESS_KEY, SERVER_SECRET_KEY, http_method, request_body, content_type,
                                                   date, path)
    request_headers = {
        'Accept': 'application/json',
        'Authorization': auth_header,
        'Content-Type': content_type,
        'Date': date
    }

    # Make the request over HTTPS on port 443
    http = httplib.HTTPSConnection(VWS_HOSTNAME, 443)
    http.request(http_method, path, request_body, request_headers)

    response = http.getresponse()
    response_body = response.read()
    return response.status, response_body


def add_image_target(image, target_name, application_metadata=None, active_flag=True):
    """
    添加图像目标

    :param image: 图片路径
    :param target_name: 图片名称
    :param application_metadata: 元数据
    :return: 返回添加结果
    """
    http_method = 'POST'
    content_type = 'application/json'
    date = formatdate(None, localtime=False, usegmt=True)
    path = "/targets"

    with open(image, 'rb') as f:
        imagedata = f.read()

    content = {
        "name": target_name,
        'width': 140.0,
        'image': base64.b64encode(imagedata),
        'application_metadata': application_metadata,
        'active_flag': active_flag
    }
    request_body = json.dumps(content)

    # Sign the request and get the Authorization header
    auth_header = authorization_header_for_request(SERVER_ACCESS_KEY, SERVER_SECRET_KEY, http_method, request_body, content_type,
                                                   date, path)
    request_headers = {
        'Accept': 'application/json',
        'Authorization': auth_header,
        'Content-Type': content_type,
        'Date': date
    }

    # Make the request over HTTPS on port 443
    http = httplib.HTTPSConnection(VWS_HOSTNAME, 443)
    http.request(http_method, path, request_body, request_headers)

    response = http.getresponse()
    response_body = response.read()
    return response.status, response_body


def get_target_info(target_id):
    """
    获取指定目标信息

    :param target_id: 指定目标id
    :return: 返回添加结果
    """
    http_method = 'GET'
    content_type = 'application/json'
    date = formatdate(None, localtime=False, usegmt=True)
    path = "/targets/" + target_id
    request_body = ''

    # Sign the request and get the Authorization header
    auth_header = authorization_header_for_request(SERVER_ACCESS_KEY, SERVER_SECRET_KEY, http_method, request_body, content_type, date, path)
    request_headers = {
        'Accept': 'application/json',
        'Authorization': auth_header,
        'Content-Type': content_type,
        'Date': date
    }

    # Make the request over HTTPS on port 443
    http = httplib.HTTPSConnection(VWS_HOSTNAME, 443)
    http.request(http_method, path, headers=request_headers)

    response = http.getresponse()
    response_body = response.read()
    return response.status, response_body


def update_image_target(target_id, name=None, width=None, image=None, active_flag=None, application_metadata=None):
    """
    修改图像目标信息

    :param target_id: 目标id
    :param name: 目标id
    :param width: 目标id
    :param image: 目标id
    :param active_flag: 目标id
    :param application_metadata: 目标id
    :return: 返回修改结果
    """
    http_method = 'PUT'
    content_type = 'application/json'
    date = formatdate(None, localtime=False, usegmt=True)
    path = "/targets/" + target_id

    content = {}
    if name is not None: content['name'] = name
    if width is not None: content['width'] = width
    if image is not None:
        with open(image, 'rb') as f:
            imagedata = f.read()
        content['image'] = base64.b64encode(imagedata)
    if active_flag is not None: content['active_flag'] = active_flag
    if application_metadata is not None: content['application_metadata'] = application_metadata
    request_body = json.dumps(content)

    # Sign the request and get the Authorization header
    auth_header = authorization_header_for_request(SERVER_ACCESS_KEY, SERVER_SECRET_KEY, http_method, request_body, content_type,
                                                   date, path)
    request_headers = {
        'Accept': 'application/json',
        'Authorization': auth_header,
        'Content-Type': content_type,
        'Date': date
    }

    # Make the request over HTTPS on port 443
    http = httplib.HTTPSConnection(VWS_HOSTNAME, 443)
    http.request(http_method, path, request_body, request_headers)

    response = http.getresponse()
    response_body = response.read()
    return response.status, response_body


def delete_target(target_id):
    """
    删除指定目标

    :param target_id: 指定目标id
    :return: 返回删除结果
    """
    http_method = 'DELETE'
    content_type = 'application/json'
    date = formatdate(None, localtime=False, usegmt=True)
    path = "/targets/" + target_id
    request_body = ''

    # Sign the request and get the Authorization header
    auth_header = authorization_header_for_request(SERVER_ACCESS_KEY, SERVER_SECRET_KEY, http_method, request_body, content_type, date, path)
    request_headers = {
        'Accept': 'application/json',
        'Authorization': auth_header,
        'Content-Type': content_type,
        'Date': date
    }

    # Make the request over HTTPS on port 443
    http = httplib.HTTPSConnection(VWS_HOSTNAME, 443)
    http.request(http_method, path, headers=request_headers)

    response = http.getresponse()
    response_body = response.read()
    return response.status, response_body


def check_for_duplicate(target_id):
    """
    查询是否存在类似的target

    :param target_id: 指定目标id
    :return: 返回查询结果
    """
    http_method = 'GET'
    content_type = 'application/json'
    date = formatdate(None, localtime=False, usegmt=True)
    path = "/duplicates/" + target_id
    request_body = ''

    # Sign the request and get the Authorization header
    auth_header = authorization_header_for_request(SERVER_ACCESS_KEY, SERVER_SECRET_KEY, http_method, request_body, content_type, date, path)
    request_headers = {
        'Accept': 'application/json',
        'Authorization': auth_header,
        'Content-Type': content_type,
        'Date': date
    }

    # Make the request over HTTPS on port 443
    http = httplib.HTTPSConnection(VWS_HOSTNAME, 443)
    http.request(http_method, path, headers=request_headers)

    response = http.getresponse()
    response_body = response.read()
    return response.status, response_body


if __name__ == '__main__':
    # 识别指定图片，若存在多个匹配的情况，最新的target排在前面且有详情，其余被匹配到的target以target_id的形式同样存在列表中
    status, query_response = send_query(max_num_results='10',
                                        include_target_data='top',
                                        image='./targets/hardshoot_512.png')
    print('send_query: ', status, query_response)

    # 获取target列表，返回的为target_id的列表，没有详细信息，详细信息只能通过id一个个获取
    status, query_response = get_target_list()
    print('get_target_list: ', status, query_response)

    # 添加target，可设置target初始状态为激活或未激活，未激活状态的target将不参与相似匹配，添加后target处于处理阶段，然后是成功或失败阶段
    status, query_response = add_image_target(image='./targets/hardshoot_512.png',
                                              target_name='test_target_05',
                                              application_metadata=base64.b64encode('{"title":"这是一个游戏图标","img_url":"http://scanme.oss-cn-shenzhen.aliyuncs.com/smcup.png"}'),
                                              active_flag=True)
    query_response = json.loads(query_response)
    print('add_image_target: ', status, query_response)
    target_id = query_response['target_id']

    # 根据target_id检测该target对应的图片是否存在相似的target，在处理阶段的target同样会被拿来对比，一般情况为在处理中的拿来与其他target进行对比
    status, query_response = check_for_duplicate(target_id)
    query_response = json.loads(query_response)
    print('check_for_duplicate: ', status, query_response)

    # 根据target_id获取target的详细信息，若target在处理阶段，则获取信息无效
    status, query_response = get_target_info(target_id)
    print('get_target_info: ', status, query_response)

    # 根据target_id修改target信息，若target在处理阶段，则删除无效
    status, query_response = update_image_target(target_id,
                                                 name=None, width=None, image=None, active_flag=True,
                                                 application_metadata=None)
    print('update_image_target: ', status, query_response)

    # 根据target_id删除target，若target在处理阶段，则删除无效
    status, query_response = delete_target(target_id)
    print('delete_target: ', status, query_response)
