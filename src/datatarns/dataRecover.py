## 从客户id数据恢复

import pymysql
import logging
logging.basicConfig(level=logging.INFO)

conn = pymysql.connect(host='192.168.50.178', user = "root", passwd="123456", db="equipment-20190810", port=3306, charset="utf8")
cur = conn.cursor()

field = ['division_id']

sql = r"desc t_sys_division"
cur.execute(sql)
rows = cur.fetchall()
print(rows)

