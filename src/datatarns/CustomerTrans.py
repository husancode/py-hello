#清洗t_install_customer表坐标数据
import pymysql
import logging
logging.basicConfig(level=logging.INFO)

conn = pymysql.connect(host='192.168.50.178', user = "root", passwd="123456", db="equipment-20190810", port=3306, charset="utf8")
cur = conn.cursor()
m_sql = r"ALTER TABLE t_install_customer ADD COLUMN division_id_old VARCHAR(32) DEFAULT NULL,ADD COLUMN addr_name_old VARCHAR(88)  DEFAULT NULL"
try:
    r = cur.execute(m_sql)
    print(r)
    conn.commit()
except Exception as e:
    pass

ssql = r"SELECT `id`,`division_id`,`coordinate`,`customer_name`,`addr_name`,`addr_detail` FROM t_install_customer WHERE coordinate IS NOT NULL"

cur.execute(ssql)

zoneCur = conn.cursor()
r = None
notInXihuList = []
notInJiedaoList = []
notInShequList = []
jiedaoCmpList =[]
shequCmpList=[]
tranList = []
while(True):
    r = cur.fetchmany(1000)
    if not r:
        break
    for row in r:
        zoneSql = r"SELECT `name`, `division_id` FROM zone WHERE ST_Within(ST_GeomFromText(CONCAT('point(',REPLACE('{}',',',' '),')')), amap_polygongeo_u) ORDER BY LENGTH(`name`) ASC".format(row[2])
        zoneCur.execute(zoneSql)
        zoneList = zoneCur.fetchall()
        if(len(zoneList) == 0):
            notInXihuList.append(row)
        elif(len(zoneList) == 1):
            notInJiedaoList.append(row)
        elif(len(zoneList) == 2):
            notInShequList.append(row)
        elif(len(zoneList) == 3):
            addrArr = row[4].split("/")
            zoneNameArr = zoneList[len(zoneList)-1][0].split("->")
            if(addrArr[0] != zoneNameArr[1]):
                jiedaoCmpList.append(row)
            elif(addrArr[1] != zoneNameArr[2]):
                shequCmpList.append(row)
        else:
            addrArr = row[4].split("/")
            zone = zoneList[len(zoneList) - 1]
            zoneNameArr = zone[0].split("->")
            # if (addrArr[0] != zoneNameArr[1]):
            #     jiedaoCmpList.append(row)
            # elif (addrArr[1] != zoneNameArr[2]):
            #     shequCmpList.append(row)
            #     print(row)
            #     print(zoneList)
            if(row[1] != zone[1]):
                upSql = r"UPDATE t_install_customer SET division_id_old=division_id,addr_name_old=addr_name,division_id='{}',addr_name='{}' WHERE id='{}'".format(zone[1],zone[0][5:].replace('->','/'),row[0])
                tranList.append(row)
                zoneCur.execute(upSql)
conn.commit()
cur.close()
zoneCur.close()
conn.close()

with open('F://不在西湖区范围客户列表.txt','w',encoding='utf-8') as doc:
    print(notInXihuList,file=doc)

with open('F://不在西湖区街道范围客户列表.txt','w',encoding='utf-8') as doc:
    print(notInJiedaoList,file=doc)

with open('F://不在西湖区社区范围客户列表.txt','w',encoding='utf-8') as doc:
    print(notInShequList,file=doc)

with open('F://街道不一致客户列表.txt','w',encoding='utf-8') as doc:
    print(jiedaoCmpList,file=doc)

with open('F://社区不一致客户列表.txt','w',encoding='utf-8') as doc:
    print(shequCmpList,file=doc)

with open('F://转移区域客户列表.txt','w',encoding='utf-8') as doc:
    print(tranList,file=doc)
