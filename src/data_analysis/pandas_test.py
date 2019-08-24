"""
@author:husan
@date 2019-08-23 01:08
"""

import json
from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import matplotlib.pyplot as plt

path = 'dataset/example.txt'
##读取文件每行数据，json转为dict对象
records = [json.loads(line) for line in open(path)]

def printColumn():
    ##提取时区字段tz到一个列表：列表生成式
    time_zones = [record['tz'] for record in records if 'tz' in record]
    print(time_zones[:10])


frame = DataFrame(records)

def statTz():
    tz_count = frame['tz'].value_counts()
    print(type(tz_count))
    print(tz_count[:10])

def statTzAndShow():
    clean_tz = frame['tz'].fillna('Missing')
    clean_tz[clean_tz == ''] = 'Unknown'
    tz_count = clean_tz.value_counts()
    tz_count[:10].plot(kind='barh', rot=1)
    plt.show()
def statBrowser():
    """
    按浏览器客户端统计数量
    :return:
    """
    clients = Series([ x.split()[0] for x in frame['a'].dropna()])
    print(clients.value_counts())

def statSystem():
    """
    统计系统
    :return:
    """
    cframe = frame[frame.a.notnull()]
    operat = np.where(cframe['a'].str.contains('Windows'),'Windows','Other')
    by_tz_os = cframe.groupby(['tz', operat])
    agg_counts = by_tz_os.size().unstack().fillna(0)
    print(agg_counts[:3])
    indexer = agg_counts.sum(1).argsort()
    count_subset = agg_counts.take(indexer)[-10:]
    count_subset.plot(kind='barh', stacked=True)
    plt.show()

#printColumn()
statTz()
#statBrowser()

statSystem()





