import pymysql
conn = pymysql.connect(host='192.168.50.178', user = "root", passwd="123456", db="test", port=3306, charset="utf8")
cur = conn.cursor()
#查询数据
#r = cur.execute("SET SESSION group_concat_max_len=102400")
#print("r", r)
sql = r"SELECT GROUP_CONCAT(REPLACE(REPLACE(ST_ASTEXT(`position`),'POINT(',''),')','')) FROM test.sys_point WHERE  MBRWITHIN(`position`, (SELECT `area` FROM test.sys_area WHERE `name`='灵隐街道'))"
cur.execute(sql)
#获取数据
ret = cur.fetchone();
print(ret)
print(ret[0])
print(len(ret[0]))

li = ('af9876a89310456d8845ab20a94fb744','af9876a89310456d8845ab20a94fb744','00092419497e4f4dadd6130a912c8c5f')
sql3 = "SELECT * FROM  equipment.`t_sensor_alarm_user` u  WHERE u.`id` IN {}".format(li)
print(sql3)
cur.execute(sql3)
ret3 = cur.fetchall()
print(ret3)
print(len(ret3))

cur.close()
conn.close()
