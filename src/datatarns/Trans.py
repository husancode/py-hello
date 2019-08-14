#清洗t_install_customer表坐标数据
import pymysql

import threading, multiprocessing

def loop():
    x = 0
    while True:
        x = x ^ 1

for i in range(multiprocessing.cpu_count()):
    t = threading.Thread(target=loop)
    t.start()

conn = pymysql.connect(host='192.168.50.178', user = "root", passwd="123456", db="equipment-20190810", port=3306, charset="utf8")
cur = conn.cursor()
m_sql = r"SELECT `customer_name`, addr_name_old,addr_name,division_id_old,division_id FROM t_install_customer WHERE division_id_old IS NOT NULL"
cur.execute(m_sql)
r = cur.fetchall()
#
# with open('F://转移区域客户列表.txt','w',encoding='utf-8') as doc:
#     print(r,file=doc)
