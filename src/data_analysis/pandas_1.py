
"""
@author:husan
@date 2019-08-23 22:36
"""

import pandas as pd
import numpy as np


def show1():
    dates = pd.date_range('20170101', periods=7, freq='D')
    df = pd.DataFrame(np.random.randn(7,4), index=dates, columns=list('ABCD'))
    print(df)
    print("--------------" * 10)
    print("统计信息：")
    print(df.describe())
    print("------" * 10)
    print("行列转换：")
    print(df.T)
    print("------" * 10)
    print("根据行或列的索引进行排序：axis=0 行索引， axis=1列索引：")
    print(df.sort_index(axis=0, ascending=False))
    print("------" * 10)
    print("根据某列的值进行排序：")
    print(df.sort_values(by='B'))


def show2():
    df2 = pd.DataFrame({ 'A' : 1.,
                         'B' : pd.Timestamp('20170102'),
                         'C' : pd.Series(1,index=list(range(4)),dtype='float32'),
                         'D' : np.array([3] * 4,dtype='int32'),
                         'E' : pd.Categorical(["test","train","test","train"]),
                         'F' : 'foo' })
    print(df2)

def show3():
    dates = pd.date_range('20170101', periods=7, freq='D')
    df = pd.DataFrame(np.random.randn(7,4), index=dates, columns=list('ABCD'))
    print(df)
    print('---'*10, '选取某列:')
    print(df['A'])
    print('----'*10,"切片行:")
    print(df[1:3])
    print('----'*10,"切片行:")
    print(df['2017-01-04':'2017-01-04'])
show3()






