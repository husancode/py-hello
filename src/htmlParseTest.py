from html.parser import HTMLParser
import requests

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
        self.flag = ""
        self.name = ""
        self.item = ''
        self.result = {}
    def handle_starttag(self, tag, attrs):
        if tag == "h1":
            print(tag)
            self.flag= tag
        elif tag == "span":
            self.flag='span'
    def handle_data(self, data):
        if self.flag == "h1":
            print(data)
            self.name = data
            self.flag = ""
        elif self.flag == 'span':
            if(data == '所属省份:'):
                self.item = 'provice'
            self.flag = ""
url = 'https://www.poi86.com/poi/amap/24327.html'
r = requests.get(url)
hp = MyHTMLParser()
hp.feed(r.text)
hp.close()
print(hp.name)
