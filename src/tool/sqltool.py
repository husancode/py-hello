#encoding: utf-8
"""
@Auther: husan
@Date: 2019/8/22 17

"""
import pymysql
import datetime

def syncData(src, dest, table, tableNew=None, create=False, clearIfExist = False):

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
    print('table {} sync  start!'.format(table))
    if not tableNew:
        tableNew = table
    if(create):

        sql = r"SHOW CREATE TABLE {}".format(table)
        curSrc.execute(sql)
        row = curSrc.fetchone()
        createSql= row[1]

        if createSql:
            if tableNew:
                createSql = createSql.replace(table, tableNew)
            dropSql = r"drop table {}".format(tableNew)
            try:
                curDest.execute(dropSql)
                dbDest.commit()
            except Exception as e:
                print('drop table error!', e)
                pass
            try:
                curDest.execute(createSql)
                dbDest.commit()
            except Exception as e:
                print('create table error!', e)
                pass
    columns = descTable(src, table)

    sql = buildSelectSql(table, columns)
    print(sql)
    curSrc.execute(sql)
    rows = curSrc.fetchmany(1000)

    if (clearIfExist):
        deleteSql = r"delete from {}".format(tableNew)
        curDest.execute(deleteSql)
    while(rows):
        insertSql = buildInsertSql(tableNew, columns, rows)
        ret = curDest.execute(insertSql)
        print('insert record:{}'.format(ret))
        dbDest.commit()
        rows = curSrc.fetchmany(1000)
    dbSrc.close()
    dbDest.close()
    print('table {} sync complete'.format(table))

def convert(rows, columns):
    result = ''
    for row in rows:
        result = result +'('
        i = 0
        for item in row:
            if item == None:
                result = result + "Null,"
            elif (type(item) == datetime.datetime):
                result = result + "'"+item.strftime("%Y-%m-%d %H:%M:%S")+"',"
            elif(type(item) == int):
                result = result + ""+str(item) + ","
            elif(columns[i][1] == 'geometry' or columns[i][1] == 'point'):
                result = result + "ST_GeomFromText('"+item+"'),"
            elif(type(item) == bytes):
                result = result + "'" + str(item, encoding = "utf-8") + "',"
            elif(type(item) == str):
                result = result + "'"+pymysql.escape_string(item)+"',"
            else:
                result = result + "'"+str(item)+"',"
            i = i + 1
        result = result[:-1]+'),'
    result = result[:-1]
    return result

def getTables(src, ignore=None):
    """
    返回数据库所有的表（不包含视图）
    :param ignore:排除某些表
    :return:
    """
    conn = pymysql.connect(host=src[0], user=src[1], passwd=src[2], db=src[3], port=src[4], charset="utf8")
    showTables = r"show tables"
    cur = conn.cursor()
    cur.execute(showTables)
    tables = cur.fetchall()
    cur.close()
    conn.close()
    result = []
    for table in tables:
        if(not table[0].startswith('v_')):
            result.append(table[0])
    if(ignore):
        return list(set(result).difference(ignore))
    else:
        return result

def descTable(src, table):
    """
        返回表的字段
        :param ignore:排除某些表
        :return:
        """
    conn = pymysql.connect(host=src[0], user=src[1], passwd=src[2], db=src[3], port=src[4], charset="utf8")
    showColumns = r"DESC {}".format(table)
    cur = conn.cursor()
    cur.execute(showColumns)
    columns = cur.fetchall()


    cur.close()
    conn.close()
    return columns

def buildSelectSql(table, columns):
    sql = r"select "
    i = 0
    for column in columns:
        clu = "`"+column[0]+"`"
        if (column[1] == 'geometry' or column[1] == 'point'):
            clu = 'ST_ASTEXT(' + clu + ')'
        sql = sql + clu + ','
        i = i + 1
    sql = sql[0:len(sql) - 1]
    sql = sql + ' from ' + table
    return sql

def buildInsertSql(table, columns, rows):
    insertSql = r"insert into " + table + "("
    for column in columns:
        clu = "`"+column[0]+"`"
        insertSql = insertSql + clu + ","
    insertSql = insertSql[0: len(insertSql) - 1]
    insertSql = insertSql + ")values {}".format(convert(rows, columns))
    print(insertSql)
    return insertSql

def syncDB(src, dest):
    """
    同步2个数据库数据
    :param src:
    :param dest:
    :return:
    """
    import time
    start = time.time()
    ignore = set(['t_operation_log'])
    tables = getTables(src, ignore)
    for table in tables:
        syncData(src, dest, table, create=True)
    print('complete:{}'.format(time.time()- start))

def compareCustomer(src, dest, divisionId):
    sql = r"SELECT id FROM t_install_customer WHERE division_id IN(SELECT id FROM t_sys_division WHERE parent_ids LIKE '%{}%')".format(divisionId)
    dbSrc = pymysql.connect(host=src[0], user=src[1], passwd=src[2], db=src[3], port=src[4], charset="utf8")
    curSrc = dbSrc.cursor()
    dbDest = pymysql.connect(host=dest[0], user=dest[1], passwd=dest[2], db=dest[3], port=dest[4], charset="utf8")
    curDest = dbDest.cursor()
    curSrc.execute(sql)
    rows = curSrc.fetchall()
    curDest.execute(sql)
    rows_2 = curDest.fetchall()
    curSrc.close()
    dbSrc.close()
    curDest.close()
    dbDest.close()
    set_1 = set([row[0] for row in rows])
    set_2 = set([row[0] for row in rows_2])
    print(set_1.difference(set_2))
    print(set_2.difference(set_1))

DB = ('192.168.50.178', "root", "123456", "equipment-amap", 3306)
DB2 = ('127.0.0.1', "root", "123456", "equipment", 3306)
syncDB(DB, DB2)

#compareCustomer(DB, DB_O, '2f9cdb6ec1ef43de9b910c2395d3dc48')




