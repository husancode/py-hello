## t_amap_basics 和 t_amap_division 坐标字段修改类型

#经纬度坐标转换
import pymysql
import requests
import json
import lnglatTrans

conn = pymysql.connect(host='127.0.0.1', user = "root", passwd="123456", db="equipment", port=3306, charset="utf8")
cur = conn.cursor()

sqlAddColumn = r"ALTER TABLE t_amap_basics ADD COLUMN lnglat_new GEOMETRY DEFAULT NULL"
cur.execute(sqlAddColumn)

sqlAddColumn = r"ALTER TABLE t_amap_division ADD COLUMN lnglat_new GEOMETRY DEFAULT NULL"
cur.execute(sqlAddColumn)

sql = r"SELECT id,lnglats FROM t_amap_basics"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    lnglat = row[1].split(",")
    lnglat = lnglatTrans.trans(lnglat)
    lnglatStr = lnglatTrans.toText(lnglat)
    print(lnglatStr)
    sql = r"update t_amap_basics set lnglat_new=ST_GeomFromText('{}') where id='{}'".format(lnglatStr, row[0])
    cur.execute(sql)

sql = r"SELECT id,lnglats FROM t_amap_division"
cur.execute(sql)
rows = cur.fetchall()
for row in rows:
    lnglatStr = None
    if(row[1].startswith('POLYGON')):
        lnglatStr = row[1]
    else:
        lnglat = row[1].split(",")
        lnglat = lnglatTrans.trans(lnglat)
        lnglatStr = lnglatTrans.toText(lnglat)
    print(lnglatStr)
    sql = r"update t_amap_division set lnglat_new=ST_GeomFromText('{}') where id='{}'".format(lnglatStr, row[0])
    cur.execute(sql)

sqlAddColumn = r"alter table t_amap_basics change lnglats lnglats_bak text"
cur.execute(sqlAddColumn)

sqlAddColumn = r"alter table t_amap_basics change lnglat_new lnglats GEOMETRY"
cur.execute(sqlAddColumn)

sqlAddColumn = r"alter table t_amap_division change lnglats lnglats_bak text"
cur.execute(sqlAddColumn)

sqlAddColumn = r"alter table t_amap_division change lnglat_new lnglats GEOMETRY"
cur.execute(sqlAddColumn)



