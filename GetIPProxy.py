#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Time    : 17-5-25 下午8:48
# @Author  : 无敌小龙虾
# @File    : GetIPProxy.py
# @Software: PyCharm


import requests
import json


class GetIPProxy:

    def __init__(self, types, count, country):
        self.url = 'http://118.24.162.159:8989/?types=%s&count=%s&country=%s'
        self.types = types
        self.count = count
        self.country = country

    def GetIp(self):
        r = requests.get(self.url % (self.types, self.count, self.country))
        return json.loads(r.text)

