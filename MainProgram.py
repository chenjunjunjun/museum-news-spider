#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Time    : 18-3-31 下午4:52
# @Author  : 无敌小龙虾
# @File    : MainProgram.py
# @Software: PyCharm


import ConfirmMuseum
import GetNewsData
import URLspider
import URLspider2
import positive
from configparser import ConfigParser

if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini')
    try:
        print('-------FirstURL Spider Start--------')
        URLspider2.URLSecondSpiderRun(config)
        print('-------FirstURL Spider End--------')
    except KeyError:
        pass

    try:
        print('-------SecondURL Spider Start--------')
        URLspider.URLSpiderRun(config)
        print('-------SecondURL Spider End--------')
    except KeyError:
        pass

    try:
        print('-------News Spider Start--------')
        GetNewsData.GetNewsDataRun(config)
        print('-------News Spider End--------')
    except KeyError:
        pass

    if config.get('Positive', 'flag'):
        try:
            print('-------News Positive Analysis Start--------')
            positive.AnalyzePositive(config)
            print('-------News Positive Analysis End--------')
        except KeyError:
            pass

    if config.get('Confirm', 'flag'):
        try:
            print('-------News Weight Analysis Start--------')
            ConfirmMuseum.AnalyzeWeight(config)
            print('-------News Weight Analysis End--------')
        except KeyError:
            pass
