import requests
import re
from html.parser import HTMLParser
class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []
    def handle_starttag(self, tag, attrs):
        #print "Encountered the beginning of a %s tag" % tag
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.links.append(value)

url = 'https://www.poi86.com/poi/amap/district/330102/1.html'
domain = "https://www.poi86.com"
r = requests.get(url)
hp = MyHTMLParser()
hp.feed(r.text)
hp.close()
patern = '^/poi/amap/(\d*).html$';
for link in hp.links:
    if re.match(patern, link):
        linkUrl = domain+link
        resp = requests.get(linkUrl)

