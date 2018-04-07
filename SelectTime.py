#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Time    : 18-4-3 下午4:25
# @Author  : 无敌小龙虾
# @File    : SelectTime.py
# @Software: PyCharm


from datetime import datetime


def SelectForTime(strtime, limit):
    news_time = datetime.strptime(strtime, '%Y%m%d')
    # b = datetime.date(a)   # 将2018-20-10 00:00:00 转为2018-20-10 datetime.date类型
    today_time = datetime.today()  # 今日时间
    news_timestamp = datetime.timestamp(news_time)  # 判断时间戳
    today_timestamp = datetime.timestamp(today_time)  # 今日时间戳
    judge_time = today_timestamp - 365 * limit * 24 * 60 * 60  # 判断基准时间戳
    if judge_time < news_timestamp:
        return 1
    else:
        return 0
