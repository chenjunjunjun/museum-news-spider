from datetime import datetime
import pymysql


def GetMySqlData(getsql, cfg):
    db = pymysql.connect(host="%s" % cfg.get('db', 'host'),
                         user='%s' % cfg.get('db', 'user'),
                         passwd='%s' % cfg.get('db', 'passwd'),
                         db='%s' % cfg.get('db', 'db'),
                         port=int(cfg.get('db', 'port')),
                         charset='%s' % cfg.get('db', 'charset')
                         )
    cursor = db.cursor()
    # getsql = 'SELECT content,museum,id from news'
    try:
        cursor.execute(getsql)
        data = cursor.fetchall()
        return data
    except:
        db.rollback()
    finally:
        db.close()


def SelectForTime(strtime):
    news_time = datetime.strptime(strtime, '%Y%m%d')
    news_timestamp = datetime.timestamp(news_time)  # 判断时间戳
    # print(news_timestamp)
    return news_timestamp


def GetInfor(cfg):
    mname = cfg.get('cmade', 'name')
    mtime1 = SelectForTime(cfg.get('cmade', 'start'))
    mtime2 = SelectForTime(cfg.get('cmade', 'end'))
    getsql = 'select * from news where museum="%s" ' % mname
    data = GetMySqlData(getsql, cfg)
    newdata = list()
    for item in data:
        if mtime1 <= SelectForTime(item[2]) <= mtime2:
            newdata.append(item)
    print("正面新闻：")
    for column in newdata:
        if column[4] == 1:
            print(column[0])
    print("负面新闻：")
    for column in newdata:
        if column[4] == 0:
            print(column[0])
