import urllib.request
import urllib.parse
import re
import json
import base64

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

def decode_bing_u(u_str):
    try:
        padded = u_str + '=' * (4 - len(u_str) % 4)
        return base64.b64decode(padded.replace('-', '+').replace('_', '/')).decode('utf-8', errors='ignore')
    except Exception:
        return ""

def test_bing(query):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            algos = re.findall(r'<li class="b_algo".*?</li>', html, re.DOTALL)
            print(f"Bing found {len(algos)} algo results for query: {query}")
            for a in algos:
                u_m = re.search(r'u=a1([a-zA-Z0-9_\-]+)', a)
                link = decode_bing_u(u_m.group(1)) if u_m else ""
                title_m = re.search(r'<h2[^>]*>(.*?)</h2>', a)
                title = title_m.group(1) if title_m else ""
                title_clean = re.sub(r'<[^>]+>', '', title)
                snippet_m = re.search(r'<p[^>]*>(.*?)</p>', a)
                snippet = re.sub(r'<[^>]+>', '', snippet_m.group(1)).strip() if snippet_m else ""
                print(f"  LINK: {link}")
                print(f"  TITLE: {title_clean}")
                print(f"  SNIPPET: {snippet[:120]}")
                print("---")
    except Exception as e:
        print("Bing error:", e)

test_bing('site:instagram.com "mentoria" ("PMPE" OR "PMBA" OR "PMPB")')
