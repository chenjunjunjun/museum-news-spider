#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Time    : 18-3-24 下午1:33
# @Author  : 无敌小龙虾
# @File    : GetNewsClass.py
# @Software: PyCharm


import re

import requests
from bs4 import BeautifulSoup
from lxml import etree


class GetNews:
    def __init__(self):
        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }

    def GetHtml(self, url):
        try:
            r = requests.get(url, headers=self.headers, timeout=30)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except KeyError as e:
            print(e)
            pass

    @staticmethod
    def ChangeTime(time):
        t = time[0:10]
        t1 = t[0:4]
        t2 = t[5:7]
        t3 = t[8:]
        t = t1 + t2 + t3
        return t

    @staticmethod
    def CleanContent(content):
        content = re.sub("</?\w+[^>]*>", "", str(content))
        content = re.sub("[\n \r]", "", str(content))
        content = re.sub('[\u3000\xa0]', "", content)
        return content

    def GetSinaNews(self, url, flag=1):
        News = []
        bsobj = self.GetHtml(url)
        select = BeautifulSoup(bsobj, "lxml")
        if flag:
            title = select.find('title').get_text()
            time = select.find('span', {"class": "date"}).get_text()
            content = select.find('div', {"class": "article", "id": "article"})
        else:
            title = select.find('title').get_text()
            time = select.find('span', {"id": "navtimeSource"}).get_text()
            content = select.find('div', {"id": "artibody"})
        title = title.strip()
        time = time.strip()
        time = self.ChangeTime(time)
        content = self.CleanContent(content)
        News.append([title, time, content])
        return News

    def GetSohuNews(self, url):
        News = []
        bsobj = self.GetHtml(url)
        select = etree.HTML(bsobj)
        title = select.xpath(
            '//*[@id="article-container"]/div[2]/div[1]/div[1]/h1')
        title = title[0].text
        time = select.xpath('//*[@id="news-time"]')
        time = time[0].text.strip()
        time = self.ChangeTime(time)
        content = select.xpath('//*[@id="mp-editor"]')
        info = content[0].xpath('string(.)').strip()
        info = self.CleanContent(info)
        info = info[:-14]
        News.append([title, time, info])
        return News

    def GetFengNews(self, url, flag=1):
        News = []
        bsobj = self.GetHtml(url)
        if flag:
            select = etree.HTML(bsobj)
            title = select.xpath('//*[@id="artical_topic"]')
            title = title[0].text
            time = select.xpath('//*[@id="artical_sth"]/p/span[1]')
            time = time[0].text.strip()
            content = select.xpath('//*[@id="main_content"]')
            content = content[0].xpath('string(.)').strip()
        else:
            select = BeautifulSoup(bsobj, "lxml")
            title = select.find('h1', {"id": "artical_topic"}).get_text()
            title = title.strip()
            News.append(title)
            time = select.find('div', {"id": "artical_sth"}).get_text()
            time = time.strip()
            content = select.find('div', {"id": "artical_real"}).get_text()

        time = self.ChangeTime(time)
        info = self.CleanContent(content)
        News.append([title, time, info])
        return News

    def GetWangYNews(self, url):
        News = []
        bsobj = self.GetHtml(url)
        select = etree.HTML(bsobj)
        title = select.xpath('//*[@id="epContentLeft"]/h1')
        title = title[0].text
        time = select.xpath('//*[@id="epContentLeft"]/div[1]')
        time = time[0].text.strip()
        time = self.ChangeTime(time)
        content = select.xpath('//*[@id="endText"]')
        info = content[0].xpath('string(.)').strip()
        info = self.CleanContent(info)
        News.append([title, time, info])
        return News

    def GetXinHNews(self, url, flag=1):
        News = []
        bsobj = self.GetHtml(url)
        if flag:
            select = etree.HTML(bsobj)
            title = select.xpath('/html/body/div[2]/div[3]/div/div[1]')
            title = title[0].text.strip()
            time = select.xpath('/html/body/div[2]/div[3]/div/div[2]/span[1]')
            time = time[0].text.strip()
            content = select.xpath('//*[@id="p-detail"]')
            content = content[0].xpath('string(.)').strip()
        else:
            select = BeautifulSoup(bsobj, "lxml")
            title = select.find('h1', {"id": "title"}).get_text()
            title = title.strip()
            time = select.find('span', {"class": "time"}).get_text()
            time = time.strip()
            content = select.find('div', {"class": "article"})
        time = self.ChangeTime(time)
        info = self.CleanContent(content)
        News.append([title, time, info])
        return News

    def GetTencentNews(self, url):
        News = []
        bsobj = self.GetHtml(url)
        select = etree.HTML(bsobj)
        soup = BeautifulSoup(bsobj, 'html.parser')
        title = select.xpath(
            '//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/h1')
        title = title[0].text.strip()
        time = soup.find('span', {'class': 'a_time'})
        time = time.text.strip()
        time = self.ChangeTime(time)
        content = soup.find_all('p', {'class': 'text'})
        info = ""
        for son in content:
            info += str(son.text)
        info = self.CleanContent(info)
        News.append([title, time, info])
        return News

    def GetPengPNews(self, url):
        News = []
        bsobj = self.GetHtml(url)
        soup = BeautifulSoup(bsobj, 'html.parser')
        select = etree.HTML(bsobj)
        title = select.xpath('//h1//text()')
        title = title[0].strip()
        time = soup.find('div', {'class': 'news_about'})
        time = time.find_all('p')[1]
        time = time.text.strip()
        time = self.ChangeTime(time)
        content = soup.find(
            'div', {'class': 'news_txt', 'data-size': 'standard'}).text
        content = self.CleanContent(content)
        News.append([title, time, content])
        return News
