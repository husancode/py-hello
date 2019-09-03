#encoding: utf-8
"""
@Auther: husan
@Date: 2019/9/2 19:19

"""

from pandas import DataFrame, Series
import pandas as pd; import numpy as np
import matplotlib.pyplot as plt
import json

path = 'E://stat/smoker.dat'
day_file = 'smoker-day.stat'
month_file = 'smoker-month.stat'
hour_file = 'smoker-hour.stat'
hour1_file = 'smoker-hour1.stat'
##读取文件每行数据，json转为dict对象
records = [json.loads(json.dumps(eval(line))) for line in open(path)]
df = DataFrame(records)
# tz_count = df['value'].value_counts()
# print(tz_count)
#
# baseId_count = frame['baseId'].value_counts()
# print(baseId_count)
# print(df.loc[:10, ['id','happenTime']])

def dayCount():
    df1 = df.copy()
    df1['happenTime'] = df1.apply(lambda x: x.happenTime[0:10], axis=1)
    day_alarm_count = df1.groupby(['happenTime']).id.count()
    day_base_count = df1.groupby(['happenTime']).baseId.nunique()
    day_count = pd.merge(day_alarm_count, day_base_count, on='happenTime')
    return day_count
def monthCount():
    df1 = df.copy()
    df1['happenTime'] = df1.apply(lambda x: x.happenTime[0:7], axis=1)
    month_alarm_count = df1.groupby(['happenTime']).id.count()
    month_base_count = df1.groupby(['happenTime']).baseId.nunique()
    month_count = pd.merge(month_alarm_count, month_base_count, on='happenTime')
    return month_count

def hourCount():
    df1 = df.copy()
    df1['happenTime'] = df1.apply(lambda x: x.happenTime[0:13], axis=1)
    hour_alarm_count = df1.groupby(['happenTime']).id.count()
    hour_base_count = df1.groupby(['happenTime']).baseId.nunique()
    hour_count = pd.merge(hour_alarm_count, hour_base_count, on='happenTime')
    return hour_count

def hourCount1():
    df1 = df.copy()
    df1 = df1[(df1['happenTime'] >= '2019-01-01') & (df1['happenTime'] <= '2019-08-31')]
    df1['happenTime'] = df1.apply(lambda x: x.happenTime[11:13], axis=1)
    print(df1['happenTime'])
    hour_alarm_count = df1.groupby(['happenTime']).id.count()
    hour_base_count = df1.groupby(['happenTime']).baseId.nunique()
    hour_count = pd.merge(hour_alarm_count, hour_base_count, on='happenTime')
    return hour_count


#dayCount().to_csv('smoker-day.stat', sep='\t',index=True, header=True)
#monthCount().to_csv('smoker-month.stat', sep='\t',index=True, header=True)
#hourCount().to_csv(hour_file, sep='\t', index=True, header=True)

def showMonthStat():
    df1 = pd.read_csv(month_file, sep='\t', header=0)
    #6月数据不完整剔除
    df1.rename(columns={'happenTime': 'alarmTime', 'id': 'alarmCount', 'baseId': 'deviceCount'}, inplace=True)
    df1.plot(x='alarmTime', y=['alarmCount', 'deviceCount'] , title="month_stat")
    plt.legend()
    plt.grid()  # 生成网格
    plt.tight_layout()
    plt.show()

def showDayStat(start, end):
    df1 = pd.read_csv(day_file, sep='\t', header=0)
    df1 = df1[(df1['happenTime'] >= start) & (df1['happenTime'] <= end)]
    df1['happenTime'] = df1.apply(lambda x: x.happenTime[5:], axis=1)
    df1.rename(columns={'happenTime': 'alarmTime', 'id': 'alarmCount', 'baseId': 'deviceCount'}, inplace=True)
    df1.plot(x='alarmTime', y=['alarmCount', 'deviceCount'], title="day_stat",figsize=(20,10))
    plt.legend()
    plt.tight_layout()
    plt.show()

def showDayStatByMonth():
    df1 = pd.read_csv(day_file, sep='\t', header=0)
    ax = None
    for a in range(8):
        month = a +1
        start = r"2019-0{}-01".format(month)
        end = r"2019-0{}-31".format(month)
        df2 = df1[(df1['happenTime'] >= start) & (df1['happenTime'] <= end)]
        df2['happenTime'] = df2.apply(lambda x: x.happenTime[8:], axis=1)
        title = 'alarm0'+str(month)
        df2.rename(columns={'happenTime': 'alarmTime', 'id': title, 'baseId': 'device-07'}, inplace=True)
        ax = df2.plot(x='alarmTime', y=[title], title="day_stat", figsize=(20, 15), ax=ax, yticks=[50,100,200,300,500,1000,4000])
    plt.legend()
    plt.grid()  # 生成网格
    plt.tight_layout()
    plt.show()


def showDayDeviceStatByMonth():
    df1 = pd.read_csv(day_file, sep='\t', header=0)
    ax = None
    for a in range(8):
        month = a +1
        start = r"2019-0{}-01".format(month)
        end = r"2019-0{}-31".format(month)
        df2 = df1[(df1['happenTime'] >= start) & (df1['happenTime'] <= end)]
        df2['happenTime'] = df2.apply(lambda x: x.happenTime[8:], axis=1)
        title = 'device0'+str(month)
        df2.rename(columns={'happenTime': 'alarmTime', 'baseId': title}, inplace=True)
        ax = df2.plot(x='alarmTime', y=[title], title="day_stat", figsize=(15, 10), ax=ax, yticks=[10,20,50,100,150,200,250,300])
    plt.legend()
    plt.tight_layout()
    plt.grid()  # 生成网格
    plt.show()

def showHourStat(start, end):
    df1 = pd.read_csv(hour_file, sep='\t', header=0)
    print(df1.describe())
    df1 = df1[(df1['happenTime'] >= start) & (df1['happenTime'] < end)]
    df1['happenTime'] = df1.apply(lambda x: x.happenTime[8:], axis=1)
    df1.rename(columns={'happenTime': 'alarmTime', 'id': 'alarmCount', 'baseId': 'deviceCount'}, inplace=True)
    df1.plot(x='alarmTime', y=['alarmCount', 'deviceCount'], title="hour_stat", figsize=(15, 10))
    plt.legend()
    plt.tight_layout()
    plt.show()


def showHourTotalStat():
    df1 = pd.read_csv(hour1_file, sep='\t', header=0)
    df1.rename(columns={'happenTime': 'alarmTime', 'id': 'alarmCount', 'baseId': 'deviceCount'}, inplace=True)
    df1.plot(x='alarmTime', y=['alarmCount', 'deviceCount'], title="hour_stat", figsize=(15, 10),
             xticks=[00,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23])
    plt.legend()
    plt.tight_layout()
    plt.grid()  # 生成网格
    plt.show()

def showDayRatio(start, end):
    df1 = pd.read_csv(day_file, sep='\t', header=0)
    df1 = df1[(df1['happenTime'] >= start) & (df1['happenTime'] <= end)]
    df1['happenTime'] = df1.apply(lambda x: x.happenTime[5:], axis=1)
    df1['ratio'] = df1['id']/df1['baseId']
    df1.rename(columns={'happenTime': 'alarmTime'}, inplace=True)
    df1.plot(x='alarmTime', y=['ratio'], title="day_stat_ratio", figsize=(20, 10))
    plt.legend()
    plt.tight_layout()
    plt.grid()  # 生成网格
    plt.show()


def showDeviceStat(start, end):
    df1 = df.copy()
    df1 = df1[(df1['happenTime'] >= start) & (df1['happenTime'] < end)]
    device_count = df1.groupby(['baseId']).id.count()
    device_count = device_count.sort_values(ascending=False)
    print(device_count[:25])
    return
    device_count[:25].plot(kind='barh', stacked=True, title="device-7th")
    plt.legend()
    plt.tight_layout()
    plt.grid()  # 生成网格
    plt.show()

def showDevice(baseId,start, end):
    df1 = df.copy()
    df1 = df1[(df1['baseId']==baseId) & (df1['happenTime'] >= start) & (df1['happenTime'] < end)]
    df1.plot(x='happenTime', y=['value'], title=baseId, figsize=(20, 10))
    plt.legend()
    plt.tight_layout()
    plt.grid()  # 生成网格
    plt.show()

def showDeviceByHourStat(baseId, start, end):
    df1 = df.copy()
    df1 = df1[(df1['baseId']==baseId) & (df1['happenTime'] >= start) & (df1['happenTime'] < end)]
    if df1.empty:
        print('no alarm data')
        return
    df1['happenTime'] = df1.apply(lambda x: x.happenTime[0:13], axis=1)
    hour_alarm_count = df1.groupby(['happenTime']).id.count()
    print(hour_alarm_count)
    hour_alarm_count.plot(x='happenTime', y=['id'], title=baseId, figsize=(20, 10))
    plt.legend()
    plt.tight_layout()
    plt.grid()  # 生成网格
    plt.show()

def showValue():
    df1 = df.copy()
    df1 = df1[(df1['value'] != 0.0)]
    df1 = df1['value'].sort_values(ascending=False)
    print(df1.describe())
    print(df1[30:])
    print(df1[:30])

def statByHourAndDevice():
    df1 = df.copy()
    df1['happenTime'] = df1.apply(lambda x: x.happenTime[0:13], axis=1)
    dd = df1.groupby(['happenTime','baseId'])
    df1 = dd.size().sort_values(ascending=False)
    print(df1.describe())
    df1.to_csv('smoker-hour-device.stat', sep='\t', index=True, header=True)
    df1[:30].plot(kind='barh', stacked=True, title="device-hour-max")
    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.show()

#showDeviceStat('2019-08-01','2019-09-01')
#showDeviceByHourStat('0eadde314a54479c976951aaaefe4ea1','2019-01-01','2019-09-01')
statByHourAndDevice()

#showValue()
#按月报警统计

#按日报警统计

#按设备报警统计

#单独设备详情


