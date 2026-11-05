import sys
import urllib.request
import urllib.parse
import re
import base64
import html as html_lib
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

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

queries = [
    'site:instagram.com "mentoria" "pmpe"',
    'site:instagram.com "mentoria" "pmpb"',
    'site:instagram.com "mentoria" "pmce"',
    'site:instagram.com "mentoria" "pmpa"',
    'site:instagram.com "mentoria" "pmgo"',
    'site:instagram.com "mentoria" "pmpr"',
    'site:instagram.com "mentoria" "pmmg"',
    'site:instagram.com "mentoria" "pmsc"',
    'site:instagram.com "mentoria" "polícia penal"',
    'site:instagram.com "mentoria" "gcm"',
    'site:instagram.com "mentoria" "guarda civil municipal"',
    'site:instagram.com "cronograma" "polícia penal"',
    'site:instagram.com "cronograma" "gcm"',
    'site:linktr.ee "mentoria" "pmba"',
    'site:linktr.ee "mentoria" "pmpe"',
    'site:linktr.ee "mentoria" "policia penal"',
    'site:linktr.ee "mentoria" "gcm"',
    'site:my.canva.site "mentoria" "policial"',
    'site:beacons.ai "mentoria" "policial"'
]

for q in queries:
    url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            algos = re.findall(r'<li class="b_algo".*?</li>', content, re.DOTALL)
            print(f"\n=== Query: [{q}] -> {len(algos)} results ===")
            for a in algos[:4]:
                u_m = re.search(r'u=a1([a-zA-Z0-9_\-]+)', a)
                link = decode_bing_u(u_m.group(1)) if u_m else ""
                title_m = re.search(r'<h2[^>]*>(.*?)</h2>', a)
                title = html_lib.unescape(re.sub(r'<[^>]+>', '', title_m.group(1))) if title_m else ""
                snippet_m = re.search(r'<p[^>]*>(.*?)</p>', a)
                snippet = html_lib.unescape(re.sub(r'<[^>]+>', '', snippet_m.group(1))).strip() if snippet_m else ""
                print(f"  Title: {title}")
                print(f"  Link: {link}")
                print(f"  Snippet: {snippet[:150]}")
    except Exception as e:
        print(f"Error on {q}: {e}")
    time.sleep(1)
