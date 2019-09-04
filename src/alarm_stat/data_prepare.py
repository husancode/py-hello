#encoding: utf-8
"""
@Auther: husan
@Date: 2019/9/2 15:06

"""
from src.tool.esTool import ElasticScroll
from pandas import DataFrame, Series
import pandas as pd; import numpy as np

def prepareEs():
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

def prepareMysql():
    import pymysql
    from datetime import datetime
    from datetime import timedelta
    conn = pymysql.connect(host='36.26.64.1', user='equipment', passwd='equiPment888rUnyUan', db='equipment', port=22222, charset="utf8")
    cur = conn.cursor()
    with open('E://stat/alarm.dat', 'w', encoding='utf-8') as doc:
        sql = r"SELECT * FROM t_sensor_alarm_msg WHERE alarm_date>='2019-01-01 00:00:00' ORDER BY alarm_date DESC"
        cur.execute(sql)
        rows = cur.fetchmany(1000)
        while(rows):
            for row in rows:
                alarmDate = row[6] + timedelta(hours=-8)
                data = {'id':row[1], 'baseId':row[2], 'dealStatus':row[4], 'alarmDate':alarmDate.strftime(('%Y-%m-%dT%H:%M:%S')), 'misreport':row[9], 'level':row[11]}
                print(data, file= doc)
            rows = cur.fetchmany(1000)
    cur.close()
    conn.close()

prepareMysql()

