from bosonnlp import BosonNLP
import pymysql


def ConfirmMuseum(text, museum, textid):
    # nlp = BosonNLP('SeJUopMY.24669.6kCKU4ruI3ss')
    # nlp = BosonNLP('lMdMTyuV.24544.0VHv6klp6Pk6')
    nlp = BosonNLP('sjWBhf9i.24699.rQmsCad9c3Jv')
    try:
        flag = 0
        text = text[0:1000]
        result = nlp.ner(text)[0]
        words = result['word']
        entities = result['entity']
        for entitie in entities:
            if entitie[2] == 'org_name':
                org_name = ''.join(words[entitie[0]:entitie[1]])
                if museum in org_name:
                    flag = 1
                    break
            elif entitie[2] == 'location':
                location = ''.join(words[entitie[0]: entitie[1]])
                if museum in location:
                    flag = 1
                    break
        if flag:
            print('Confirm!')
            return 1
        else:
            print('Not!')
            return 0
    except KeyError as e:
        print('exit in %s' % textid)
        print(e)


def AnalyzeWeight(cfg):
    db = pymysql.connect(host="%s" % cfg.get('db', 'host'),
                         user='%s' % cfg.get('db', 'user'),
                         passwd='%s' % cfg.get('db', 'passwd'),
                         db='%s' % cfg.get('db', 'db'),
                         port=int(cfg.get('db', 'port')),
                         charset='%s' % cfg.get('db', 'charset')
                         )
    cursor = db.cursor()
    getsql = 'SELECT content,museum,id from news'
    try:
        cursor.execute(getsql)
        data = cursor.fetchall()
        for son in data:
            flag = ConfirmMuseum(son[0], son[1], son[2])
            putsql = 'UPDATE news SET weight = %s where id= %s' % (flag, son[2])
            cursor.execute(putsql)
            db.commit()
    except KeyError:
        db.rollback()
    finally:
        db.close()
