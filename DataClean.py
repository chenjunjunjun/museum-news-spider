#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
# @Time    : 17-6-5 下午9:29
# @Author  : 无敌小龙虾
# @File    : DataClean.py
# @Software: PyCharm

import re


class CleanData(object):
    """
    对数据的一些多余项进行清理
    """

    # 对HTML中的中的标签类进行清除
    def HtmlTags(self, content):
        content = re.sub(r'<.*?>', "", content)
        return content

    def other(self, content):
        content = content.strip()
        content = re.sub('\n+', ",", content)
        content = re.sub(' +', " ", content)
        content = re.sub('&quot', "", content)
        content = re.sub('\u200b', "", content)
        content = re.sub('\xa0', "", content)
        content = re.sub(r'(\d{4}-\d{1,2}-\d{1,2})', "", content)
        content = re.sub(r'(\d[\u4e00-\u9fa5]+)', "", content)  # 去 例：4时前
        return content
