#encoding: utf-8
"""
@Auther: husan
@Date: 2019/9/2 19:19

"""

from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import json

path = 'E://stat/smoker.dat'
##读取文件每行数据，json转为dict对象
records = [json.loads(json.dumps(eval(line))) for line in open(path)]
frame = DataFrame(records)
pd.set_option('display.max_rows', 100)
tz_count = frame['value'].value_counts()
print(tz_count)
