# !venv/bin/python3
# -*- coding: utf-8 -*-
# Licensed under MIT License
# Copyright © 2018 zhengxiangqi All rights reserved

"""
@Filename: iplocation.py
@Project: *
@Author: zhengxiangqi
@Date: 9/14/18
"""
import json
import urllib.request as urllib2


class location_freegeoip():
    """
    build the mapping of the ip address and its location.
    the geo info is from <freegeoip.net>
    """

    def __init__(self, ip):
        '''
        Constructor of location_freegeoip class
        '''
        self.ip = ip
        self.api_format = 'json'
        self.api_url = 'http://freegeoip.net/%s/%s' % (self.api_format, self.ip)
        self.datadict = {}

    def get_geoinfo(self):
        """
        get the geo info from the remote API.
        return a dict about the location.
        """
        urlobj = urllib2.urlopen(self.api_url)
        data = urlobj.read()
        self.datadict = json.loads(data, encoding='utf-8')
        return self.datadict

    def get_country_code(self):
        return self.datadict['country_code']

    def get_country_name(self):
        return self.datadict['country_name']

    def get_region_code(self):
        return self.datadict['region_code']

    def get_region_name(self):
        return self.datadict['region_name']

    def get_city(self):
        return self.datadict['city']

    def get_zip_code(self):
        return self.datadict['zip_code']

    def get_time_zone(self):
        return self.datadict['time_zone']

    def get_latitude(self):
        return self.datadict['latitude']

    def get_longitude(self):
        return self.datadict['longitude']

    def get_metro_code(self):
        return self.datadict['metro_code']


class location_taobao():
    '''
    build the mapping of the ip address and its location
    the geo info is from Taobao
    e.g. http://ip.taobao.com/service/getIpInfo.php?ip=112.111.184.63
    The getIpInfo API from Taobao returns a JSON object.
    '''

    def __init__(self, ip):
        self.ip = ip
        self.api_url = 'http://ip.taobao.com/service/getIpInfo.php?ip=%s' % self.ip
        self.datadict = {}

    def get_geoinfo(self):
        """
        get the geo info from the remote API.
        return a dict about the location.
        """
        urlobj = urllib2.urlopen(self.api_url)
        data = urlobj.read()
        self.datadict = json.loads(data, encoding='utf-8')['data']
        return self.datadict

    def get_country(self):
        return self.datadict['country']

    def get_country_id(self):
        return self.datadict['country_id']

    def get_area(self):
        return self.datadict['area']

    def get_area_id(self):
        return self.datadict['area_id']

    def get_region(self):
        return self.datadict['region']

    def get_region_id(self):
        return self.datadict['region_id']

    def get_city(self):
        return self.datadict['city']

    def get_city_id(self):
        return self.datadict['city_id']

    def get_county(self):
        return self.datadict['county']

    def get_county_id(self):
        return self.datadict['county_id']

    def get_isp(self):
        return self.datadict['isp']

    def get_isp_id(self):
        return self.datadict['isp_id']

    def get_ip(self):
        return self.datadict['ip']


if __name__ == '__main__':
    ip = '110.84.0.129'
    iploc = location_freegeoip(ip)
    iploc.get_geoinfo()
