#encoding: utf-8
"""
@Auther: husan
@Date: 2019/9/2 10:49

"""
from src.datatarns.config import DB
import pymysql

def transFail():
    with open('F://清理失败.txt', 'r', encoding='utf-8') as doc:
        line = doc.readline()
        while(line):
            lineArr = line.split(":")
            if lineArr[0] == 't_install_customer':
                transCustomer(lineArr[1])
            elif lineArr[0] == 'ent_buildings':
                transEntBuild(lineArr[1])
            elif lineArr[0] == 't_app_security_user':
                transUser(lineArr[1])
            elif lineArr[0] in ['t_unit_rectify','t_unit_apply_info', 't_sys_user','t_check_task']:
                transOther(lineArr[0], lineArr[1])
            line = doc.readline()

def transCustomer(divisionId):
    conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3], port=DB[4], charset="utf8")
    cur = conn.cursor()
    parentId = getParentDivision(divisionId, conn)
    sql = r"UPDATE t_install_customer SET update_date=now(), division_id_old=division_id, addr_name_old=addr_name, division_id='{}'," \
          r"addr_name=SUBSTRING(addr_name, 1, CHAR_LENGTH(addr_name)-CHAR_LENGTH(SUBSTRING_INDEX(addr_name, '/', -{}))-1) " \
          r"WHERE division_id='{}'".format(parentId[0], parentId[1], divisionId)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def getParentDivision(divisionId, conn):
    cur = conn.cursor()
    sql = r"SELECT parent_id FROM t_sys_division WHERE id='{}'".format(divisionId)
    cur.execute(sql)
    row = cur.fetchone()
    level = 1
    if not row:
        sql = r"SELECT parent_id FROM t_sys_division_bak WHERE id='{}'".format(divisionId)
        cur.execute(sql)
        row = cur.fetchone()
        divisionId = row[0]
        sql = r"SELECT parent_id FROM t_sys_division WHERE id='{}'".format(divisionId)
        cur.execute(sql)
        row = cur.fetchone()
        level = 2
    return (row[0], level)

def transUser(divisionId):
    conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3], port=DB[4], charset="utf8")
    cur = conn.cursor()
    parentId = getParentDivision(divisionId, conn)
    sql = r"UPDATE t_app_security_user SET update_date=now(), division_id='{}' " \
          r"WHERE division_id='{}'".format(parentId[0], divisionId)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def transOther(table, divisionId):
    conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3], port=DB[4], charset="utf8")
    cur = conn.cursor()
    parentId = getParentDivision(divisionId, conn)
    sql = r"UPDATE {} SET update_date=now(), division_id='{}' " \
          r"WHERE division_id='{}'".format(table, parentId[0], divisionId)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

def transEntBuild(divisionId):
    conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3], port=DB[4], charset="utf8")
    cur = conn.cursor()
    m_sql = r"ALTER TABLE ent_buildings ADD COLUMN division_id_old VARCHAR(32) DEFAULT NULL,ADD COLUMN division_name_old VARCHAR(88)  DEFAULT NULL"
    try:
        r = cur.execute(m_sql)
        print(r)
        conn.commit()
    except Exception as e:
        pass
    parentId = getParentDivision(divisionId, conn)
    sql = r"UPDATE ent_buildings SET update_date=now(), division_id_old=division_id, division_name_old=division_name, division_id='{}'," \
          r"division_name=SUBSTRING(division_name, 1, CHAR_LENGTH(division_name)-CHAR_LENGTH(SUBSTRING_INDEX(division_name, '/', -{}))-1) " \
          r"WHERE division_id='{}'".format(parentId[0], parentId[1], divisionId)
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()

transFail()