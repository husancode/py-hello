from elasticsearch import Elasticsearch
es = Elasticsearch([{'host':'127.0.0.1','port':9200}])
es.index(index="point",id=1,body={"province":"浙江省","city":"杭州市","district":"上城区","address":"中河中路9号","phone":"0571-87046999","flag":["餐饮服务","中餐厅","火锅店"],"location":[120.172183,30.237726],"name":"食神锅奉行(鼓楼店)","comment":""})
