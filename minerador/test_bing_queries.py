import urllib.request
import urllib.parse
import re
import base64

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

def decode_bing_u(u_str):
    try:
        padded = u_str + '=' * (4 - len(u_str) % 4)
        return base64.b64decode(padded.replace('-', '+').replace('_', '/')).decode('utf-8', errors='ignore')
    except Exception:
        return ""

def test_bing_query(q):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            algos = re.findall(r'<li class="b_algo".*?</li>', html, re.DOTALL)
            print(f"Bing query: [{q}] -> {len(algos)} results")
            for a in algos[:5]:
                u_m = re.search(r'u=a1([a-zA-Z0-9_\-]+)', a)
                link = decode_bing_u(u_m.group(1)) if u_m else ""
                title_m = re.search(r'<h2[^>]*>(.*?)</h2>', a)
                title = re.sub(r'<[^>]+>', '', title_m.group(1)) if title_m else ""
                snippet_m = re.search(r'<p[^>]*>(.*?)</p>', a)
                snippet = re.sub(r'<[^>]+>', '', snippet_m.group(1)).strip() if snippet_m else ""
                print(f"  Title: {title}")
                print(f"  Link: {link}")
                print(f"  Snippet: {snippet[:120]}")
                print("---")
    except Exception as e:
        print("Error:", e)

test_bing_query('site:instagram.com "mentoria" "pmba"')
test_bing_query('site:instagram.com/ "mentoria" "pmba"')
test_bing_query('"instagram.com" "mentoria" "pmba"')
test_bing_query('mentoria pmba instagram')
