from elasticsearch import Elasticsearch
from hashlib import md5
es = Elasticsearch([{'host':'127.0.0.1','port':9200}])
data = {"province":"浙江省","city":"杭州市","district":"上城区","address":"中河中路9号","phone":"0571-87046999","flag":["餐饮服务","中餐厅","火锅店"],"location":[120.171028,30.247218],"name":"食神锅奉行(鼓楼店)","comment":""}
data_str = str(data)
data_byte = data_str.encode('utf-8')
m = md5()
m.update(data_byte)
result = m.hexdigest()
print(result)

#es.index(index="point",id=1,body= data)
