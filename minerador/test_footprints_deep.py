import urllib.request
import re
import json
import time
import sys
import html as html_lib

sys.stdout.reconfigure(encoding='utf-8')

googlebot_headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
browser_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

linktrees = [
    'https://linktr.ee/mentoriatatica',
    'https://linktr.ee/paidoconcurso',
    'https://linktr.ee/andrezacaetanomentoria',
    'https://linktr.ee/mentoriacarreiraspoliciais',
    'https://linktr.ee/wagalvarenga',
    'https://linktr.ee/geovanemoraes2'
]

def check_linktree(url):
    try:
        req = urllib.request.Request(url, headers=browser_headers)
        with urllib.request.urlopen(req, timeout=6) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            ig_m = re.findall(r'instagram\.com/([a-zA-Z0-9_\.]{3,30})', html)
            title_m = re.search(r'<title>(.*?)</title>', html)
            title = title_m.group(1).replace('| Linktree', '').strip() if title_m else ""
            print(f"Linktree {url} -> Title: {title} | IG: {set(ig_m)}")
            return {'url': url, 'title': title, 'ig': list(set(ig_m))}
    except Exception as e:
        print(f"Linktree {url} err: {e}")
    return None

for lt in linktrees:
    check_linktree(lt)
    time.sleep(0.5)

reels = [
    'https://www.instagram.com/reel/Dd77WEoOATo/',
    'https://www.instagram.com/p/Dd5Ud6dNNHy/',
    'https://www.instagram.com/p/Dd6iKUYt0Zp/',
    'https://www.instagram.com/reel/Dc1nx9CK4WZ/',
    'https://www.instagram.com/reel/De19kIlRwc2/',
    'https://www.instagram.com/reel/DesFhAfhIgb/',
    'https://www.instagram.com/p/DY4jUq2JBzW/',
    'https://www.instagram.com/reel/DcgSydox5qJ/',
    'https://www.instagram.com/reel/DezSPrlvWGU/',
    'https://www.instagram.com/p/DesGnIMlG5j/'
]

def check_post(url):
    try:
        req = urllib.request.Request(url, headers=googlebot_headers)
        with urllib.request.urlopen(req, timeout=6) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            meta_desc = re.search(r'<meta (?:property="og:description"|name="description") content="([^"]+)"', html)
            title_m = re.search(r'<title>(.*?)</title>', html)
            raw_desc = html_lib.unescape(meta_desc.group(1)) if meta_desc else ""
            raw_title = html_lib.unescape(title_m.group(1)) if title_m else ""
            
            # Find handle in title: "Name on Instagram: ..." or "@handle" or "from Name (@handle)"
            h_m = re.search(r'@([a-zA-Z0-9_\.]{3,30})', raw_title + " " + raw_desc)
            handle = h_m.group(1) if h_m else ""
            print(f"Post {url}:")
            print(f"  Title: {raw_title[:80]}")
            print(f"  Desc: {raw_desc[:100]}")
            print(f"  Handle: @{handle}")
    except Exception as e:
        print(f"Post {url} err: {e}")

for r in reels:
    check_post(r)
    time.sleep(0.5)
