##恢复revert zone表，t_sys_division, t_install_customer数据
# coding:utf-8

import pymysql
import logging
import re
logging.basicConfig(level=logging.INFO)

conn = pymysql.connect(host='192.168.50.178', user = "root", passwd="123456", db="equipment-20190810", port=3306, charset="utf8")
cur = conn.cursor()

def check():
    i=1
    while(i<825):
        sql = r"SELECT `name`, `division_id` FROM zone WHERE ST_Within(ST_GeomFromText(CONCAT('point(',REPLACE('120.055575,30.199795',',',' '),')')), amap_polygongeo_u) AND id={}".format(i)
        try:
            cur.execute(sql)
        except Exception as e:
            print('excep:', sql)
        i=i+1
def updat():
    sql = r"update zone set amap_polygongeo_u=ST_GeomFromText('POLYGON((120.103816189237 30.286681315105,120.10505560981 30.286752115886,120.104444715712 30.289252115886,120.102903917101 30.289156358507,120.103113606771 30.287993706598,120.103361273872 30.286659884983,120.103816189237 30.286681315105))') where id=513"
    cur.execute(sql)

def revert_customer():
    sql = r"UPDATE t_install_customer SET division_id=division_id_old,addr_name=addr_name_old,division_id_old=NULL,addr_name_old=NULL WHERE division_id_old IS NOT NULL AND addr_name_old IS NOT NULL"
    r = cur.execute(sql)
    logging.info('update customer:{}'.format(r))
    conn.commit()

def revert_division():
    sql = r"DELETE FROM t_sys_division WHERE create_by ='husan'"
    r = cur.execute(sql)
    logging.info('update division data:{}'.format(r))
    conn.commit()

def rever_zone():
    sql = r"update zone set division_id=null"
    r = cur.execute(sql)
    logging.info('clear zone divisionId')
    conn.commit()

def modify_zone():
    pattern = r'^(.*->.*->.*->)(\d{3,8})(.*)$'
    i=0
    sql = r"select id, name from zone"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        m = re.match(pattern, row[1])
        if m:
            i=i+1
            nameNew = m.groups()[0]+m.groups()[2]
            sql = r"update zone set name='{}' where id={}".format(nameNew, row[0])
            cur.execute(sql)
    print(i)
    conn.commit()
#revert_customer()
#revert_division()
#rever_zone()
updat()
cur.close()
conn.close()