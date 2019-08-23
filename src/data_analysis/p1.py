"""
@author:husan
@date 2019-08-23
json文件处理，统计字段
"""

import json
from src.data_analysis.count import *
path = 'dataset/example.txt'
##读取文件每行数据，json转为dict对象
records = [json.loads(line) for line in open(path)]
##提取时区字段tz到一个列表
time_zones = [record['tz'] for record in records if 'tz' in record]
#print(time_zones[:10])
count = counts(time_zones)
#print(count)
count = counts2(time_zones)
#print(count)
top10_count = top_counts(count, 10)
#print(top10_count)

## 使用python标准库中的 collections.Counter类
from collections import Counter
counts = Counter(time_zones)
print(dict(counts))
print(counts.most_common(10))
## 再次更新，使用列表数据
counts.update(time_zones)
print(counts.most_common(10))
## 支持+ - & | 操作
c2 = Counter({'America/New_York':2})
print(c2 + counts)
print(c2 - counts)
print(c2 | counts)
print(c2 & counts)