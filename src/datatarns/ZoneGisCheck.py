#清洗zone表坐标数据
import pymysql

def trans(data):
    first = None
    last = None
    for a in data:
        if(first == None):
            first = a
        last = a
    if(first != last):
        data.append(first)
    if(len(data) < 4):
        return []
    else:
        return data

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


conn = pymysql.connect(host='192.168.50.178', user = "root", passwd="123456", db="equipment-20190810", port=3306, charset="utf8")
cur = conn.cursor()
sql = r"select * from zone where amap_polygongeo_u is null"
#sql = r"select * from zone where id=1"

cur.execute(sql)
r = cur.fetchall()
for item in r:
    text = item[1]
    text_new = None
    data_arr = fromText(text)
    if(data_arr[0] == 0):
        print('error data:{}，{}'.format(item[0],item[1]))
    elif(data_arr[0] == 1):
        data_arr_new = trans(data_arr[1])
        if(len(data_arr_new)==0):
            print('length error')
        else:
            text_new = toText(data_arr_new)

    elif(data_arr[0] == 2):
        data_new_arr = []
        for data_item in data_arr[1]:
            data_item = trans(data_item)
            if(len(data_item) > 0):
                data_new_arr.append(data_item)
        text_new = toText(data_new_arr)

    else:
        print('error data:{},{}'.format(item[0]),item[1])

    #print(text_new)
    if(text_new != None):
        sql = r"update zone set amap_polygongeo_u=ST_GeomFromText('{}') where id={}".format(text_new, item[0])
        try:
            r = cur.execute(sql)
            print(r)
        except Exception as e:
            print('Error:', e)
        finally:
            pass
cur.close()
conn.close()
