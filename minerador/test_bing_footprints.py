import urllib.request
import urllib.parse
import re
import base64
import html

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

def decode_bing_u(u_str):
    try:
        u_str = u_str.replace('-', '+').replace('_', '/')
        padding = 4 - (len(u_str) % 4)
        if padding != 4:
            u_str += "=" * padding
        decoded = base64.b64decode(u_str).decode('utf-8', errors='ignore')
        return decoded
    except Exception:
        return ""

def test_bing_query(query):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}&setlang=pt-br"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            html_text = r.read().decode('utf-8', errors='ignore')
        algos = re.findall(r'<li class="b_algo".*?</li>', html_text, re.DOTALL)
        print(f"\nQuery: '{query}' -> Found {len(algos)} algo items")
        for a in algos[:8]:
            u_m = re.search(r'u=a1([a-zA-Z0-9_\-]+)', a)
            link = decode_bing_u(u_m.group(1)) if u_m else ""
            title_m = re.search(r'<h2[^>]*>(.*?)</h2>', a)
            title = html.unescape(re.sub(r'<[^>]+>', '', title_m.group(1))) if title_m else ""
            snippet_m = re.search(r'<p[^>]*>(.*?)</p>', a)
            snippet = html.unescape(re.sub(r'<[^>]+>', '', snippet_m.group(1))) if snippet_m else ""
            print(f"  Title: {title}")
            print(f"  Link: {link}")
            print(f"  Snippet: {snippet[:120]}")
    except Exception as e:
        print("Error:", e)

test_bing_query('"linktr.ee" "mentoria" "tjsp"')
test_bing_query('"linktr.ee" "mentoria" "ebserh"')
test_bing_query('"my.canva.site" "mentoria" "concurso"')
