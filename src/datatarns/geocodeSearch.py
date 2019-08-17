import requests
import pymysql

def search(address,city="330106"):
    url = r"https://restapi.amap.com/v3/place/text?s=rsv3&children=&key=8325164e247e15eea68b59e89200988b&" \
        r"page=1&offset=10&city={}&language=zh_cn&platform=JS&logversion=2.0&sdkversion=1.3&appname=" \
        r"https://lbs.amap.com/console/show/picker&csid=8B1D9ABE-6437-40D9-9D9D-AC988EF97B95&keywords={}".format(city, address)
    res = requests.get(url)
    print(res.text)
    return res.text

def connInit():
    conn = pymysql.connect(host='192.168.50.178', user="root", passwd="123456", db="equipment-20190810", port=3306,
                           charset="utf8")
    return conn

def tableScan():
    showTables = r"show tables"

