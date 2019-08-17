## trans=True,调用高德gps坐标转换接口转换坐标
def trans(data):
    result = []
    first = None
    last = None
    for a in data:
        if(first == None):
            first = a
        if a == last:
            data.remove(a)
        last = a
    if(first != last):
        data.append(first)
    if(len(data) < 4):
        pass
    else:
        result = data
    return result

a =['127.0 30.1', '127.0 30.1','127.01 30.12','127.011 30.12','127.01 30.121','127.01 30.112']
print(a)
c = trans(a)
print(c)
