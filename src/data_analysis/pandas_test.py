"""
@author:husan
@date 2019-08-23 01:08
"""

import json
from pandas import DataFrame, Series
import pandas as pd; import numpy as np
path = 'dataset/example.txt'
##读取文件每行数据，json转为dict对象
records = [json.loads(line) for line in open(path)]
##提取时区字段tz到一个列表
time_zones = [record['tz'] for record in records if 'tz' in record]
print(time_zones[:10])

frame = DataFrame(records)
#print(frame)

tz_count = frame['tz'].value_counts()
print(type(tz_count))
print(tz_count[:10])

clean_tz = frame['tz'].fillna('Missing')
clean_tz[clean_tz == ''] = 'Unknown'
tz_count = clean_tz.value_counts()
print(tz_count)

tz_count[:10].plot(kind='barh', rot=0)