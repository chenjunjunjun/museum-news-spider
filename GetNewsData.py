#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Time    : 18-3-24 下午3:16
# @Author  : 无敌小龙虾
# @File    : GetNewsData.py
# @Software: PyCharm

import re
import time
import pymysql
from GetNewsClass import GetNews
from SelectTime import SelectForTime

run_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def GetData(path, openflag, limit, cfg):
    museum_name = ''
    news_list = LoadData(path)
    get = GetNews()
    data = []
    for news in news_list:
        if len(news) == 1:
            museum_name = news
        if len(news) != 1:
            try:
                if news[0] in ['新浪新闻中心', '新浪新闻']:
                    data = get.GetSinaNews(news[1])
                elif news[0] in ['搜狐网', '搜狐']:
                    data = get.GetSohuNews(news[1])
                elif news[0] in ['网易新闻', '网易']:
                    data = get.GetWangYNews(news[1])
                elif news[0] in ['凤凰资讯频道', '凤凰网']:
                    data = get.GetFengNews(news[1])
                elif news[0] == '腾讯新闻':
                    data = get.GetTencentNews(news[1])
                elif news[0] == '新华网':
                    data = get.GetXinHNews(news[1])
                elif news[0] == '澎湃新闻':
                    data = get.GetPengPNews(news[1])
                else:
                    pass
                if openflag:
                    if SelectForTime(data[0][1], limit):
                        SaveToMySql(museum_name, news[1], data, cfg)
                        print("success to save")
                else:
                    SaveToMySql(museum_name, news[1], data, cfg)
                    print("success to save")
            except:
                try:
                    if news[0] in ['新浪新闻中心', '新浪新闻']:
                        data = get.GetSinaNews(news[1], flag=0)
                        if openflag:
                            if SelectForTime(data[0][1], limit):
                                SaveToMySql(museum_name, news[1], data, cfg)
                                print("success to save second model")
                        else:
                            SaveToMySql(museum_name, news[1], data, cfg)
                            print("success to save second model")
                    elif news[0] in ['凤凰网', '凤凰资讯频道']:
                        data = get.GetFengNews(news[1], flag=0)
                        if openflag:
                            if SelectForTime(data[0][1], limit):
                                SaveToMySql(museum_name, news[1], data, cfg)
                                print("success to save second model")
                        else:
                            SaveToMySql(museum_name, news[1], data, cfg)
                            print("success to save second model")
                    elif news[0] == '新华网':
                        data = get.GetXinHNews(news[1], flag=0)
                        if openflag:
                            if SelectForTime(data[0][1], limit):
                                SaveToMySql(museum_name, news[1], data, cfg)
                                print("success to save second model")
                        else:
                            SaveToMySql(museum_name, news[1], data, cfg)
                            print("success to save second model")
                    else:
                        print(news[1])
                        SaveLog(news[1])
                except:
                    print(news[1])
                    SaveLog(news[1])
                    pass
                pass


def SaveToMySql(name, url, data, cfg):
    db = pymysql.connect(host="%s" % cfg.get('db', 'host'),
                         user='%s' % cfg.get('db', 'user'),
                         passwd='%s' % cfg.get('db', 'passwd'),
                         db='%s' % cfg.get('db', 'db'),
                         port=int(cfg.get('db', 'port')),
                         charset='%s' % cfg.get('db', 'charset')
                         )
    cursor = db.cursor()
    sql = 'INSERT INTO test(title,datetime,content,museum,link) VALUES (%s,%s,%s, %s, %s)'
    try:
        cursor.execute(sql, (data[0][0], data[0][1], data[0][2], name, url))
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()


def SaveLog(log):
    save_path = '../logfile/%s.txt' % run_time  # 存储日志
    with open(save_path, 'a', encoding='utf-8') as f:
        f.write(str(log) + '\n')
    f.close()


def LoadData(path):
    ilt_list = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            line = f.readline().strip()
            while line:
                ilt_list.append(line)
                line = f.readline().strip()
        f.close()
        end_list = []
        for i in ilt_list:
            i = re.sub(r"\[", '', i)
            i = re.sub(r'\]', '', i)
            i = re.sub('\'', '', i)
            i = i.split(',')
            end_list.append(i)
        return end_list
    except KeyError as eee:
        SaveLog(eee)
        print(eee)


def GetNewsDataRun(cfg):
    data_path = 'news_links.txt'
    GetData(data_path, openflag=cfg.get('timelimit', 'flag'), limit=float(cfg.get('timelimit', 'limit')), cfg=cfg)
