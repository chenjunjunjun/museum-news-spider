#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Time    : 18-3-17 下午1:29
# @Author  : 无敌小龙虾
# @File    : URLspider.py
# @Software: PyCharm


import requests
from bs4 import BeautifulSoup
from DataClean import CleanData
import time
from GetIPProxy import GetIPProxy
import random

clean = CleanData()
IP = GetIPProxy(0, 4, '国内')


# 获取url 页面
def GetHtml(url):
    try:
        headers = {
            'Host':
                'news.sogou.com',
            'Connection':
                'keep-alive',
            'Cache-Control':
                'max-age=0',
            'Upgrade-Insecure-Requests':
                '1',
            'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept':
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding':
                'gzip, deflate',
            'Accept-Language':
                'zh-CN,zh;q=0.8',
            'Cookie':
                'IPLOC=CN1100; '
                'SUV=006D988C79C3934A593829E035D65477; '
                'usid=L7jFdrUcprFe17as; SUID=519C04CA2313940A000000005AA9F275; '
                'ld=kkllllllll2z$KJClllllV$IDXUlllllhkvtUyllll9lllllRZlll5@@@@@@@@@@; '
                'LSTMV=193%2C84; LCLKINT=6598; SNUID=D821B974BEB8DA0147AFB9BBBE0C983C; '
                'sct=31; newsCity=%u5317%u4EAC',
        }
        proxies = IpControl()
        r = requests.get(url, proxies=proxies, headers=headers, timeout=30)
        if r.status_code == 502:
            r = requests.get(url, headers=headers, timeout=30)
        if r.status_code == 404:
            headers = {
                'Host':
                    'news.sogou.com',
                'Connection':
                    'keep-alive',
                'Cache-Control':
                    'max-age=0',
                'Upgrade-Insecure-Requests':
                    '1',
                'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                    '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
                'Accept':
                    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':
                    'gzip, deflate',
                'Accept-Language':
                    'zh-CN,zh;q=0.8',
                'Cookie':
                    'IPLOC=CN1100;'
                    'newsCity=%u5317%u4EAC;'
                    'sct=2;SMYUV=1495192621108969;'
                    'SNUID=E01A834D8682E1554887FEB487E935AF;'
                    'SUID=669C04CA6C39980A000000005AB0B47E;'
                    'SUV=1495192621108581;'
            }
            r = requests.get(url, proxies=proxies, headers=headers, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        pass


def IpControl():
    ip_list = IP.GetIp()
    ip = random.choice(ip_list)
    proxies = {
        "http": "http://%s:%s" % (ip[0], ip[1]),
        "https": "http://%s:%s" % (ip[0], ip[1])
    }
    return proxies


# 在页面内爬取新闻链接
def GetNewsUrl(url, p_list, museum_name, page_n):
    news_url_list = []
    back_url = []
    for i in range(page_n+1):
        news_url = url + "&page=" + str(i)
        try:
            content = GetHtml(news_url)
            soup = BeautifulSoup(content, 'html.parser')
            father = soup.find_all('div', {'class': 'vrwrap'})
            time.sleep(2)
            for son in father:
                try:
                    news_from = son.find('p', {'class': 'news-from'}).text
                    news_from = clean.other(news_from)
                    if news_from in p_list:
                        granson = son.find('h3')
                        nurl = granson.find('a').attrs['href']
                        if nurl not in back_url:
                            back_url.append(nurl)
                            news_url_list.append([news_from, nurl])
                    else:
                        continue
                except:
                    pass
        except:
            SaveLog([museum_name, news_url])
            print('fail to request')
            pass
        continue
    return news_url_list


def CycleMulist(m_list, p_list, url, page_n):
    for museum in m_list:
        try:
            museum_url = url + museum
            news_url = GetNewsUrl(museum_url, p_list, museum, page_n=page_n)
            SaveData(museum, news_url)
        except:
            pass
        continue


# 上载博物馆以及门户网站名单
def LoadData():
    m_path = 'museum.txt'
    p_path = 'portals.txt'
    m_list = OpenFile(m_path)
    p_list = OpenFile(p_path)
    return m_list, p_list


def OpenFile(path):
    ilt = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            line = f.readline()
            while line:
                line = clean.other(line)
                ilt.append(line)
                line = f.readline()
            f.close()
            return ilt
    except:
        print("fail to open file." + path)


def SaveData(name, data):
    save_path = 'news_links.txt'
    try:
        with open(save_path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            for da in data:
                f.write(str(da) + '\n')
            print('success to save!')
        f.close()

    except KeyError as e:
        print(e)


def SaveLog(log):
    save_path = '../spiderlogfile/log.txt'  # 存储日志
    with open(save_path, 'a', encoding='utf-8') as f:
        f.write(str(log) + '\n')
    f.close()



def URLSpiderRun(cfg):
    start_time = time.time()
    page_number = int(cfg.get('SpiderPage', 'page'))
    start_url = 'http://news.sogou.com/news?query='
    museum_list, portal_list = LoadData()
    CycleMulist(museum_list, portal_list, start_url, page_n=page_number)
    end_time = time.time()
    print(end_time - start_time)
