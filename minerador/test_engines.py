import urllib.request
import urllib.parse
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

def test_engines():
    q = 'site:instagram.com "mentoria" ("TJSP" OR "TRT")'
    
    # 1. Bing
    url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            print("Bing length:", len(html))
            # check for instagram links
            links = re.findall(r'instagram\.com/([a-zA-Z0-9_\.]+)', html)
            print("Bing ig links:", set(links[:10]))
    except Exception as e:
        print("Bing error:", e)

    # 2. DuckDuckGo
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            print("DDG length:", len(html))
            links = re.findall(r'instagram\.com/([a-zA-Z0-9_\.]+)', html)
            print("DDG ig links:", set(links[:10]))
    except Exception as e:
        print("DDG error:", e)

    # 3. Yahoo
    url = f"https://br.search.yahoo.com/search?p={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html = r.read().decode('utf-8', errors='ignore')
            print("Yahoo length:", len(html))
            links = re.findall(r'instagram\.com/([a-zA-Z0-9_\.]+)', html)
            print("Yahoo ig links:", set(links[:10]))
    except Exception as e:
        print("Yahoo error:", e)

if __name__ == '__main__':
    test_engines()
