from bosonnlp import BosonNLP

import pymysql  # 导入 pymysql


def AnalyzePositive(cfg):
    # nlp = BosonNLP('SeJUopMY.24669.6kCKU4ruI3ss')
    # nlp = BosonNLP('lMdMTyuV.24544.0VHv6klp6Pk6')
    nlp = BosonNLP('sjWBhf9i.24699.rQmsCad9c3Jv')

    # 打开数据库连接
    db = pymysql.connect(host="%s" % cfg.get('db', 'host'),
                         user='%s' % cfg.get('db', 'user'),
                         passwd='%s' % cfg.get('db', 'passwd'),
                         db='%s' % cfg.get('db', 'db'),
                         port=int(cfg.get('db', 'port')),
                         charset='%s' % cfg.get('db', 'charset')
                         )

    # 使用cursor()方法获取操作游标
    cur = db.cursor()

    # 1.查询操作
    # 编写sql 查询语句
    sql1 = "select * from news"
    flag = 0
    content = []
    try:
        cur.execute(sql1)  # 执行sql语句
        results = cur.fetchall()  # 获取查询的所有记录
        # 遍历结果
        for row in results:
            flag = 0
            content.clear()
            content.append(row[0])
            positive = nlp.sentiment(content)
            print(positive)
            if positive[0][0] > positive[0][1]:
                flag = 1
            sql2 = "UPDATE `news` SET `positive` = %s WHERE `news`.`id` = %s" % (
                flag, row[7])
            cur.execute(sql2)
            db.commit()
            print(sql2)
    except Exception as e:
        raise e
    finally:
        db.commit()
        db.close()  # 关闭连接
