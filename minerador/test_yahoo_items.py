import requests
import re
import html

FB_UA = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'

def check_item(url):
    r = requests.get(url, headers={'User-Agent': FB_UA, 'Accept-Language': 'pt-BR'}, timeout=7)
    title = re.search(r'<title>(.*?)</title>', r.text)
    meta = re.search(r'<meta property="og:description" content="([^"]*)"', r.text)
    print(f"\nURL: {url}")
    print("Title:", html.unescape(title.group(1)) if title else "None")
    print("Meta:", html.unescape(meta.group(1)) if meta else "None")

check_item('https://www.instagram.com/matsueda.concursos/')
check_item('https://www.instagram.com/naprocuradoria/')
check_item('https://www.instagram.com/p/C7QkfqDuhgm/')
