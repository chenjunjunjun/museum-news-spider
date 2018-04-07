import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver


def read_data():
    data = []  # 博物馆集
    with open('museum1.txt', 'r', encoding='utf-8') as f:
        data = f.read().strip('\ufeff').split('\n')
    return data


def gethtml(url):  # 爬取新闻内容
    page = urllib.request.urlopen(url)
    html = page.read()
    return html


def getres(url):  # 爬取新闻链接
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    response = urllib.request.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find('div', id='content_left').find_all(attrs={"target": "_blank"})  # 爬取所有新闻链接
    res = []
    standard = ['新浪新闻', '搜狐', '网易', '凤凰网', '新华网', '中国新闻网', '腾讯新闻', '澎湃新闻']

    # 挑选出是标准公司发布的新闻的链接
    for link in links:
        flag = 0
        com = link.parent.next_sibling.get_text()[:5]
        for st in standard:
            if com[:len(st)] == st:
                flag = 1
                res.append(link.get('href') + st)
                with open('news_links.txt', 'a', encoding='utf-8') as f:
                    f.write(str([st, link.get('href')])+'\n')
    return res


def getfirst(keywords):  # 根据关键词获取搜索后的链接,即第一页
    driver = webdriver.Firefox(executable_path="geckodriver")
    driver.get("http://news.baidu.com/")  # 打开百度新闻
    search = driver.find_element_by_xpath("//input[@name='word']")  # 找到搜索输入框
    driver.find_element_by_id("newstitle").click()  # 找到新闻标题选项并点击
    search.send_keys(keywords)  # 模拟输入关键词
    driver.find_element_by_id("s_btn_wr").click()  # 提交搜索
    url = driver.current_url  # current_url 方法可以得到当前页面的URL
    driver.quit()
    return url


def getsixpage(url, page_n):
    sixpage = []
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
    response = urllib.request.urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    sixpages = soup.find('p', id='page').find_all('a')
    sixpages = sixpages[:page_n]
    for page in sixpages:
        href = page.get('href')
        href = href[:8] + '=' + href[11:]
        sixpage.append('http://news.baidu.com' + href)
    sixpage.insert(0, url)
    return sixpage


def URLSecondSpiderRun(cfg):
    data = read_data()
    reslink = []  # 新闻链接结果
    oneres = []  # 一家博物馆的新闻
    pagenumber = int(cfg.get('SpiderPage', 'page'))
    for key in data:
        oneres.clear()
        # print(key)
        with open('news_links.txt', 'a', encoding='utf-8') as f:
            f.write(key + '\n')
        first = getfirst(key)  # 获取第一页
        sixpages = getsixpage(first, pagenumber)  # 获取6页
        for page in sixpages:
            oneres.append(getres(page))
        reslink.append(oneres)
