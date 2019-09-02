#encoding: utf-8
"""
@Auther: husan
@Date: 2019/9/2 15:06

"""
from src.tool.esTool import ElasticScroll
from pandas import DataFrame, Series
import pandas as pd; import numpy as np

scroll = ElasticScroll([{'host':'192.168.50.178','port':9200}])
query_body = '{"sort":{"createDate":"desc"},"size": 200}'
res = scroll.scroll('sensor-data-smoke', query_body)
with open('E://stat/smoker-test.dat', 'w', encoding='utf-8') as doc:
    while(len(res) > 0):
        for item in res:
            _source = item.get('_source')
            data = {}
            data["id"] = _source["id"]
            data["value"] = _source["value"]
            data["baseId"] = _source["baseId"]
            data["happenTime"] = _source["happenTime"]
            data["smokeId"] = _source["smokeId"]
            print(data, file = doc)
        res = scroll.scroll('sensor-data-smoke', query_body)
