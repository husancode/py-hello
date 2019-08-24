#encoding: utf-8
"""
@Auther: husan
@Date: 2019/8/23 10:08
customer数据排查校验
"""

import pymysql
import json
from pandas import DataFrame, Series
import pandas as pd; import numpy as np
from src.datatarns.config import DB
import time
import requests
from src.tool.func_wrap import limit
from geopy.distance import *
from fuzzywuzzy import fuzz

INIT = 0
DOWNLOAD = 1
INVAlID = 2
DEAL = 3

def getCheckData():
    """
    获取待校验数据
    :return:
    """
    conn = pymysql.connect(host=DB[0], user=DB[1], passwd=DB[2], db=DB[3], port=DB[4], charset="utf8")
    cur = conn.cursor()

    sql = r"SELECT * FROM t_install_customer"
    cur.execute(sql)
    records = cur.fetchall()
    cur.close()
    conn.close()
    """
    0:id
    2:customer_name
    4: division_id
    5:addr_name
    6:addr_detail
    17: coordinate
    18: coordinate_level
    """
    frame = DataFrame(records)
    frame = frame[ frame[18].isnull() | (frame[18] > '西湖区&3|3') | (frame[18] == '')]
    records = frame[[0,2,4,5,6,17,18]].sort_values(by=18 , ascending=False)
    level = frame[18]
    level_count = level.value_counts()
    #7
    records['addr_flag'] = INIT
    #8
    records['addr_data'] = ''
    #9
    records['name_flag']= INIT
    #10
    records['name_data'] = ''
    #11
    records['adjust_flag'] = INIT
    #12
    records['adjust_data'] = ''
    #13
    records['match'] = ''
    #14
    records['flag'] = INIT
    fileName = 'customer'+ str(time.time_ns())
    records.to_csv(fileName, sep='\t',index=False, header=None)
    print('download data from db to {}'.format(fileName))
    return fileName

def checkFile(fileName=None):
    if not fileName:
        fileName = getCheckData()
    records = pd.read_csv(fileName, sep='\t', header=None)
    for index, row in records.iterrows():
        row = checkData(row)
        records.iloc[index] = row

    records.to_csv(fileName, sep='\t',index=False, header=None)

def checkData(row):
    """
    flag : 0未处理
    flag: 1 下载数据
    flag:  2 数据不对
    flag:  3 数据初步有效
    flag： 4 数据有效
    :param row:
    :return:
    """
    addr_flag = row[7]
    name_flag = row[9]
    address = row[4]
    if(address != address):
        row[14] = INVAlID
        return
    name = row[1]
    analy_result = list()
    ## flag=0 下载高德位置数据
    if addr_flag == INIT:
        if( address != address):
            addr_flag = INVAlID
        else:
            text = searchPosition(address)
            row[8] = text
            addr_flag = DOWNLOAD
    if name_flag == INIT:
        if (name != name):
            name_flag = INVAlID
        else:
            text = searchPosition(name)
            row[10] = text
            name_flag = DOWNLOAD
    if addr_flag == DOWNLOAD:
        if(address != address):
            addr_flag = INVAlID
        else:
            poisDict = json.loads(row[8])
            if(poisDict['info'] != 'OK'):
                addr_flag = INVAlID
            else:
                poisList = poisDict['pois']
                poisList = checkAddress(poisList)
                match_result = match(poisList, address, name)
                analy_result = analy_result + match_result
                row[13] = match_result[:1]
                row[14] = DEAL
                addr_flag = DEAL
    if name_flag == DOWNLOAD:
        if( name != name):
            name_flag = INVAlID
        else:
            poisDict = json.loads(row[10])
            if (poisDict['info'] != 'OK'):
                name_flag = INVAlID
            else:
                poisList = poisDict['pois']
                poisList = checkAddress(poisList)
                match_result = match(poisList, address, name)
                analy_result = analy_result + match_result[:1]
                name_flag = DEAL
    row[7] = addr_flag
    row[9] = name_flag
    row[11] = DEAL
    row[12] = analy_result
    row[13] = analy_result[:1]
    row[14] = DEAL
    return row


@limit(3000)
def searchPosition(keyword, city='330106'):
    """
    调用高德地图api查找位置坐标
    :param keyword:
    :param city:默认杭州区域
    :return:
    """
    url = r"https://restapi.amap.com/v3/place/text?citylimit=true&key=c358894e83dc95b4b38bb6855d4b2954&page=1&" \
          r"offset=10&city={}&language=zh_cn" \
          r"&keywords={}".format(city, keyword)
    r = requests.get(url)
    print(r.text)
    return r.text

def checkAddress(poisList, dis=200):
    polist = []
    pre = None
    for pois in poisList[:4]:
        location = pois['location']
        if not pre:
            pre = location
            polist.append(pois)
            continue
        d = distance(pre, location)
        if(d > dis):
            polist.append(pois)
        pre = location
    return polist

def distance(p1, p2):
    pair1 = p1.split(",")
    pair2 = p2.split(",")
    if(len(pair1)!=2 or len(pair2) != 2):
        return -1
    return geodesic((pair1[1],pair1[0]), (pair2[1], pair2[0])).m

"""
如何判断2个中文地址的距离相似度
"""

def match(poisList, address, name):
    result = list()
    for pois in poisList:
        pois_name = pois['name']
        pois_address = pois['address']
        if address != address:
            r1 = 0
            r2 = 0
        else:
            r1 = fuzz.ratio(pois_address, address)
            r2 = fuzz.ratio(pois_name, address)
        r3 = fuzz.ratio(pois_name, name)
        r4 = fuzz.ratio(pois_address, name)
        score = max(r1, r2, r3, r4)
        item = {'name':pois_name, 'address': pois_address, 'score':score, 'location':pois['location']}
        result.append(item)
    return list(sorted(result, key= lambda x:x['score'],  reverse=True))[:3]

def match_part(poisList, address, name):
    result = list()
    for pois in poisList:
        pois_name = pois['name']
        pois_address = pois['address']
        if address != address:
            r1 = 0
            r2 = 0
        else:
            r1 = fuzz.partial_token_set_ratio(pois_address, address)
            r2 = fuzz.partial_token_set_ratio(pois_name, address)
        r3 = fuzz.partial_token_set_ratio(pois_name, name)
        r4 = fuzz.partial_token_set_ratio(pois_address, name)
        score = max(r1, r2, r3, r4)
        item = {'name': pois_name, 'address': pois_address, 'score': score, 'location': pois['location']}
        result.append(item)
    return list(sorted(result, key=lambda x: x['score'], reverse=True))[:3]

def showData(fileName, row, col=None):
    records = pd.read_csv(fileName, sep='\t', header=None)
    pd.set_option('max_colwidth', 200)
    if col:
        print(records.loc[row][col])
    else:
        print(records.loc[row])

#checkFile('customer1566614010020670500')






