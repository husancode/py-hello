#encoding: utf-8
"""
@Auther: husan
@Date: 2019/8/22 17

"""
import pymysql
import datetime


def syncData(src, dest, table, tableNew=None, create=False):

    """
     从一个库同步表到另一个库
    :param src: 源数据库
    :param dest: 目标数据库
    :param table: 源表名
    :param tableNew: 目标表名
    :param create:  是否需要创建新表
    :return:
    """
    dbSrc = pymysql.connect(host=src[0], user=src[1], passwd=src[2], db=src[3], port=src[4], charset="utf8")
    curSrc = dbSrc.cursor()
    dbDest = pymysql.connect(host=dest[0], user=dest[1], passwd=dest[2], db=dest[3], port=dest[4], charset="utf8")
    curDest = dbDest.cursor()

    if(create):
        sql = r"SHOW CREATE TABLE {}".format(table)
        curSrc.execute(sql)
        row = curSrc.fetchone()
        createSql= row[1]
        if createSql:
            if tableNew:
                createSql = createSql.replace(table, tableNew)
            print(createSql)
            try:
                curDest.execute(createSql)
                dbDest.commit()
            except Exception as e:
                print('create table error!', e)
                pass
    sql = r"select * from {}".format(table)
    curSrc.execute(sql)
    rows = curSrc.fetchmany(1000)
    if not tableNew:
        tableNew = table
    while(rows):
        insertSql = r"insert into {} values {}".format(tableNew, convert(rows))

        ret = curDest.execute(insertSql)
        print('insert record:{}'.format(ret))
        dbDest.commit()
        rows = curSrc.fetchmany(1000)
    dbSrc.close()
    dbDest.close()

def convert(rows):
    result = ''
    for row in rows:
        result = result +'('
        for item in row:
            if item == None:
                result = result + "Null,"
            elif (type(item) == datetime.datetime):
                result = result + "'"+item.strftime("%Y-%m-%d %H:%M:%S")+"',"
            elif(type(item) == int):
                result = result + ""+str(item) + ","
            else:
                result = result + "'"+item+"',"
        result = result[:-1]+'),'
    result = result[:-1]
    return result


DB = ('192.168.50.178', "root", "123456", "equipment-amap", 3306)
DB2 = ('127.0.0.1','root','123456','equipment',3306)
syncData(DB, DB2, 't_install_customer', tableNew='t_install_customer_new', create=True)





