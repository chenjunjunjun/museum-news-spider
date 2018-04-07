# museum-news-spider
_ _ _

### 项目环境

* Python 3.5+
* MySql

### 项目依赖
 * beautifulsoup4==4.4.1
 * bosonnlp==0.11.0
 * lxml==3.5.0
 * PyMySQL==0.7.11
 * requests==2.18.4
 * Scrapy==1.5.0
 * urllib3==1.22
 * selenium==3.11.0
 * configparser==3.5.0

其中以上依赖可在项目目录下执行`pip install -r requirements.txt`安装，py2与py3并存时，请用`pip3 install -r requirements.txt`
同时需要下载firefox_webdriver，请在[https://github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases)下载相应版本

_ _ _

### 使用说明

1. `MainProgram.py`为主运行程序
2. 本系统在爬去新闻链接部分（即`URLSpider`和`URLSpider2`）采用的数据存储方式为，存储到本地的txt文本格式。
3. 在抓取新闻文本及其详细信息部分（即`GetNewData`），采取的是将数据存入到数据库的方式，数据库的连接方式可在`config.ini`中配置。（声明：在系统中我并没有对数据库部分代码进行重构，所以略显繁重，不过不影响使用。）**另外，在使用这一部分的时候，需要自己事先在本地数据库建表**（偷懒了-_-）,表结构如下
| 列名 | 类型 | 说明|
|--------|--------|--------|
|   id   |  int   |id自增|
|   content   |  text   |内容|
|   title   |  char   |标题|
|   datatime   |  cahr   |新闻时间|
|   link   |  char   |新闻链接|
|   positive   |  bool   |正负面|
|   weight   |  bool   |是否此博物馆新闻|
|   museum   |  char   |博物馆名|

4. 在`URLSpider`中采用了IP代理的方法，但是使用的IP池是免费IP池，稳定性不是很好，所以若网络出现问题，请多试几遍即可
5. 系统有按一定时间范围内爬取新闻的功能，默认关闭，如需要使用，可在`config.ini`中的**timelimit**开启，*** limit ***以年为单位
6. 新闻内容的正负面分析采用的是第三方平台[bosonnlp](http://www.bosonnlp.com)提供的服务，此功能默认关闭，如需开此，可在`config.ini`中`Positive`设置。但由于使用的是免费服务，一天只有500条的分析量，如需一次性分析500条以上，则需自己更改密钥（在`positive.py`中内置了三个密钥，但只启动一个，如若必要，可自己手动注释更改）
7. 增加了新闻筛选功能（即初步确定此新闻是否是相对应博物馆新闻），默认关闭，基本操作与**6**中说明一致
8. 在`config.ini`中设置了URL爬取页面数`SpiderPage`，默认为6，若需爬取更多URL，可适当自行更改为更大数字
