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
import dataselect
from configparser import ConfigParser

if __name__ == '__main__':
    config = ConfigParser()
    config.read('config.ini')
    if config.getboolean('spider', 'spider1'):
        try:
            print('-------FirstURL Spider Start--------')
            URLspider2.URLSecondSpiderRun(config)
            print('-------FirstURL Spider End--------')
        except:
            pass
    if config.getboolean('spider', 'spider2'):
        try:
            print('-------SecondURL Spider Start--------')
            URLspider.URLSpiderRun(config)
            print('-------SecondURL Spider End--------')
        except:
            pass
    if config.getboolean('spider', 'newsspider'):
        try:
            print('-------News Spider Start--------')
            GetNewsData.GetNewsDataRun(config)
            print('-------News Spider End--------')
        except:
            pass

    if config.getboolean('Positive', 'flag'):
        try:
            print('-------News Positive Analysis Start--------')
            positive.AnalyzePositive(config)
            print('-------News Positive Analysis End--------')
        except:
            pass

    if config.getboolean('Confirm', 'flag'):
        try:
            print('-------News Weight Analysis Start--------')
            ConfirmMuseum.AnalyzeWeight(config)
            print('-------News Weight Analysis End--------')
        except:
            pass

    if config.getboolean('cmade', 'flag'):
        try:
            print('-------Custom Made Start--------')
            dataselect.GetInfor(config)
            print('-------Custom Made End--------')
        except:
            pass

    print("Program Ending!")
