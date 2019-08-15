#经纬度坐标转换
import pymysql
import requests
import json

##坐标首位相连，如果点数小于4个（需要有大于3个不同位置的点），数据无效，返回空数组
## trans=True,调用高德gps坐标转换接口转换坐标
def trans(data, trans=False):
    result = []
    first = None
    last = None
    for a in data:
        if(first == None):
            first = a
        last = a
    if(first != last):
        data.append(first)
    if(len(data) < 4):
        pass
    else:
        result = data
    if trans:
        location = ";".join(map(lambda x: x.replace(' ',','),result))
        url = r"https://restapi.amap.com/v3/assistant/coordinate/convert?key=c358894e83dc95b4b38bb6855d4b2954&locations={}&coordsys=gps".format(location)
        resText = requests.get(url)
        res = json.loads(resText.text)
        if 'locations' in res:
            location = res['locations']
            result = list(map(lambda x: x.replace(',',' '),location.split(";")))
    return result

## 根据数组返回坐标mysql插入文本，多个数组MULTIPOLYGON，单个数组返回POLYGON
def toText(data):
    if(type(data) == list):
        if(type(data[0]) == list):
            result = 'MULTIPOLYGON('
            for a in data:
                item = ",".join(a)
                result = result+'(('+item+')),'
            result = result[:-1]+')'
            return result
        else:
            return 'POLYGON(('+",".join(data)+'))'

## 根据文本解析成坐标数组，多个区域返回（2，arr），单个区域返回(1,arr),无效数据返回(0,[])
def fromText(text):
    _start_str = text[:7]
    if('POLYGON' == _start_str):
        _text_arr = text[9:len(text) - 2].split(",")
        return (1,_text_arr)
    elif ('MULTIPO' == _start_str):
        _text_arr = []
        _text = text[13:len(text) - 1]
        _mult_text_arr = _text.split(")),")
        for item in _mult_text_arr:
            item = item.replace("((", "").replace("))", "")
            item_arr = item.split(",")
            _text_arr.append(item_arr)
        return (2,_text_arr)
    else:
        return (0,[])




