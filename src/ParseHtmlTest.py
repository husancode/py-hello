from html.parser import HTMLParser
import requests

r = requests.get('https://www.poi86.com/poi/amap/district/330102/1.html')
print(r.text)
