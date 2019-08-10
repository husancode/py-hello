import requests
import re
import time
from html.parser import HTMLParser
from htmlParseFunc import parseUrl
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from hashlib import md5
es = Elasticsearch([{'host':'127.0.0.1','port':9200}])

def cal_md5(data):
    data_str = str(data)
    data_byte = data_str.encode('utf-8')
    m = md5()
    m.update(data_byte)
    return m.hexdigest()

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.links.append(value)
i =1
domain = "https://www.poi86.com"
patern = '^/poi/amap/(\d*).html$';
n = 0
actions = []
start = time.time()
while (i<21):
    url = 'https://www.poi86.com/poi/amap/district/330108/'+str(i)+'.html'
    r = requests.get(url)
    hp = MyHTMLParser()
    hp.feed(r.text)
    hp.close()
    i = i+1

    for link in hp.links:
        if re.match(patern, link):
            n = n+1
            linkUrl = domain+link
            resp = parseUrl(linkUrl)
            id = cal_md5(resp)
            action = {
                "_index": "point",
                "_id":id,
                "_source": resp
            }
            actions.append(action)
            if(n%200 == 0):
                a = helpers.bulk(es, actions)
                actions = []
                print('batch insert es', a)
if(len(actions) > 0):
    helpers.bulk(es, actions)
print('trans complete!time:', time.time()-start)





