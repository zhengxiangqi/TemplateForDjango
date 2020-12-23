# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: gpsdistance.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
import math

__earth_radius = 6378.137


def rad(d):
    return d * math.pi / 180.0


def calculate_distance(lat1, lng1, lat2, lng2):
    """
    根据两个位置的经纬度，来计算两地的距离(单位为KM)

    :param lat1: 用户纬度

    :param lng1: 用户经度

    :param lat2: 目标纬度

    :param lng2: 目标经度

    :return: 返回计算出来的两点距离
    """
    radLat1 = rad(lat1)

    radLat2 = rad(lat2)

    difference = radLat1 - radLat2

    mdifference = rad(lng1) - rad(lng2)

    distance = 2 * math.asin(math.sqrt(math.pow(math.sin(difference / 2), 2) + math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(mdifference / 2), 2)))
    distance = distance * __earth_radius
    distance = round(distance * 10000) / 10000
    distance = round(distance, 2)

    return distance


def calculate_area(latitude, longitude, radius):
    """
    获取当前用户一定距离以内的经纬度值

    :param latitude: 纬度

    :param longitude: 经度

    :param radius: 半径范围(单位M)

    :return: 返回计算出来的范围经纬度 {'minLat':最小纬度, 'maxLat':最大纬度, 'minLng':最小经度, 'maxLng':最大经度}
    """
    degree = (24901 * 1609) / 360.0

    mpdLng = abs(degree * math.cos(latitude * (math.pi / 180)))
    dpmLng = 1 / mpdLng
    radiusLng = dpmLng * radius
    # 获取最小经度
    minLng = longitude - radiusLng
    # 获取最大经度
    maxLng = longitude + radiusLng

    dpmLat = 1 / degree
    radiusLat = dpmLat * radius
    # 获取最小纬度
    minLat = latitude - radiusLat
    # 获取最大纬度
    maxLat = latitude + radiusLat

    map = {}
    map['minLat'] = minLat
    map['maxLat'] = maxLat
    map['minLng'] = minLng
    map['maxLng'] = maxLng

    return map


if __name__ == '__main__':
    print(calculate_area(24.46, 118.1, 10000))
