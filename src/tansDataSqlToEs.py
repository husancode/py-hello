import pymysql
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers


conn = pymysql.connect(host='192.168.50.178', user = "root", passwd="123456", db="equipment", port=3306, charset="utf8")
cur = conn.cursor()

sql = r" SELECT customer_name,phone,addr_name,coordinate FROM t_install_customer"
cur.execute(sql)
#获取数据
ret = cur.fetchall();
print(len(ret))
cur.close()
conn.close()

es = Elasticsearch([{'host':'127.0.0.1','port':9200}])
s=time.time()
actions = []
for item in ret:
    if item[3] != None:
        loca = {"lon": float(item[3].split(",")[0]),"lat":float(item[3].split(",")[1])}
        data = {"name": item[0], "phone": item[1], "addr_name": item[2], "location": loca}
        action = {
            "_index": "customer-2",
            "_source": data
        }
        #使用批量写入比单个写入快很多
        actions.append(action)
print(actions)
a = helpers.bulk(es, actions)
e = time.time()
print("trans complete {}:{}".format(a, e-s))