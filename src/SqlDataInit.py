import pymysql
conn = pymysql.connect(host='192.168.50.178', user = "root", passwd="123456", db="equipment", port=3306, charset="utf8")
cur = conn.cursor()
sql = r" SELECT ref.`station_id`,ref.`division_id`,a.name,a.`lnglats`,s.area_id FROM ess_station_area_ref  ref  LEFT JOIN t_amap_division a ON ref.`division_id` = a.`division_id` LEFT JOIN ess_station s ON ref.`station_id`=s.id"
cur.execute(sql)
#获取数据
ret = cur.fetchall()
print(ret)
for item in ret:
    area = item[3]
    areaArr = area.split(",")
    first = None
    last = None
    for aArea in areaArr:
        if first == None:
            first = aArea
        last = aArea
    if(first != last):
        area = area +','+first
    area = 'POLYGON(('+area+'))'
    sql2 = r"INSERT INTO `ess_station_area` (`id`,`area_name`,`parent_id`,`area`,`create_time`,`update_time`) VALUES('{}','{}','{}',ST_GeomFromText('{}'),now(),null)".format(item[1],item[2],item[4],area)
    print(sql2)
    cur.execute(sql2)
cur.close()
conn.close()