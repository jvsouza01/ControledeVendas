import urllib.request, urllib.parse

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote('site:instagram.com mentoria PMBA')
req = urllib.request.Request(url, headers=headers)
try:
    resp = urllib.request.urlopen(req, timeout=10)
    html = resp.read().decode('utf-8', errors='ignore')
    print("Length:", len(html))
    print(html[:1000])
except Exception as e:
    print("Error:", e)
