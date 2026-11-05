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

test_queries = [
    'site:instagram.com "mentoria" "soldado"',
    'site:instagram.com "mentoria" "carreiras policiais"',
    'site:instagram.com "mentoria" "polícia militar"',
    'site:instagram.com "mentoria" "guarda municipal"',
    'site:instagram.com "mentoria" "guarda civil"',
    'site:instagram.com "mentoria" "policia penal"',
    'site:instagram.com "mentoria" "cfo"',
    'site:instagram.com "mentoria" "pmesp"',
    'site:instagram.com "mentoria" "pmmg"',
    'site:instagram.com "mentoria" "pmba"',
    'site:instagram.com "mentoria" "pmce"',
    'site:instagram.com "mentoria" "pmpe"',
    'site:instagram.com "mentoria" "pmpb"',
    'site:instagram.com "mentoria" "pmpa"',
    'site:instagram.com "mentoria" "pmgo"',
    'site:instagram.com "mentoria" "pmpr"',
    'site:instagram.com "mentoria" "pmsc"',
    'site:instagram.com "mentoria" "gcm"',
    'site:instagram.com "cronograma" "pmba"',
    'site:instagram.com "cronograma" "polícia militar"',
    'site:instagram.com "cronograma" "guarda municipal"',
    'site:instagram.com "cronograma" "policia penal"'
]

results_map = {}

for q in test_queries:
    url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            algos = re.findall(r'<li class="b_algo".*?</li>', content, re.DOTALL)
            count = 0
            for a in algos:
                u_m = re.search(r'u=a1([a-zA-Z0-9_\-]+)', a)
                link = decode_bing_u(u_m.group(1)) if u_m else ""
                if 'instagram.com' in link:
                    title_m = re.search(r'<h2[^>]*>(.*?)</h2>', a)
                    title = html_lib.unescape(re.sub(r'<[^>]+>', '', title_m.group(1))) if title_m else ""
                    snippet_m = re.search(r'<p[^>]*>(.*?)</p>', a)
                    snippet = html_lib.unescape(re.sub(r'<[^>]+>', '', snippet_m.group(1))).strip() if snippet_m else ""
                    
                    # Extract handle
                    h_m = re.search(r'instagram\.com/([a-zA-Z0-9_\.]+)', link)
                    if h_m:
                        handle = h_m.group(1).lower()
                        if handle not in ('p', 'reel', 'reels', 'stories', 'explore'):
                            count += 1
                            if handle not in results_map:
                                results_map[handle] = {
                                    'title': title,
                                    'link': link,
                                    'snippet': snippet,
                                    'query': q
                                }
            print(f"[{q}] -> {count} valid IG profiles found (Total unique: {len(results_map)})")
    except Exception as e:
        print(f"Error on {q}: {e}")
    time.sleep(1.2)

print("\n--- Summary of Discovered Handles ---")
for h, data in results_map.items():
    print(f"@{h}: {data['title'][:40]} | Snippet: {data['snippet'][:80]}")
