from html.parser import HTMLParser
import requests

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.result = {}
        self.flag = ""
        self.field = []
    def handle_starttag(self, tag, attrs):
        self.flag = tag
    def handle_data(self, data):
        if self.flag == "h1":
            self.result['name'] = data
            self.flag = ''
        elif data == '所属省份:':
            self.field = ["province", None]
        elif data == '所属城市:':
            self.field = ["city", None]
        elif data == '所属区县:':
            self.field = ["district", None]
        elif data == '详细地址:':
            self.field = ['address']
        elif data == '电话号码:':
            self.field = ['phone']
        elif data == '所属分类:':
            self.field = ['flag']
        elif data == '图吧坐标:':
            self.field = ['location']
        elif len(self.field) > 0:
            p = self.field.pop()
            if p != None:
                self.result[p] = data.strip()

def parseUrl(url):
    r = requests.get(url)
    hp = MyHTMLParser()
    hp.feed(r.text)
    hp.close()
    flag = hp.result['flag'].split(";")
    hp.result['flag'] = flag
    location = hp.result['location'].split(",")
    if len(location) ==2:
        location =[float(location[0]),float(location[1])]
        hp.result['location'] = location
    return hp.result
