import requests

url = 'https://www.poi86.com/poi/amap/district/330102/1.html'

r = requests.get(url)

print(r.text)

