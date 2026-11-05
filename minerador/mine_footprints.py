import urllib.request
import urllib.parse
import re
import json
import base64
import html as html_lib
import time
import sys

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

footprints = [
    'site:linktr.ee mentoria "pmba"',
    'site:linktr.ee mentoria "pmpe"',
    'site:linktr.ee mentoria "pmce"',
    'site:linktr.ee mentoria "pmpb"',
    'site:linktr.ee mentoria "pmgo"',
    'site:linktr.ee mentoria "pmmg"',
    'site:linktr.ee mentoria "pmesp"',
    'site:linktr.ee mentoria "pmpr"',
    'site:linktr.ee mentoria "pmsc"',
    'site:linktr.ee mentoria "policia penal"',
    'site:linktr.ee mentoria "gcm"',
    'site:linktr.ee mentoria "guarda municipal"',
    'site:linktr.ee cronograma "policial"',
    'site:linktr.ee cronograma "pmba"',
    'site:linktr.ee cronograma "pmpe"',
    'site:linktr.ee cronograma "pmmg"',
    'site:my.canva.site mentoria "pm"',
    'site:my.canva.site mentoria "policial"',
    'site:my.canva.site mentoria "concurso"',
    'site:beacons.ai mentoria "policial"',
    'site:beacons.ai mentoria "concurso"',
    'site:beacons.ai mentoria "pm"'
]

discovered_links = []

for q in footprints:
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
                title_m = re.search(r'<h2[^>]*>(.*?)</h2>', a)
                title = html_lib.unescape(re.sub(r'<[^>]+>', '', title_m.group(1))) if title_m else ""
                snippet_m = re.search(r'<p[^>]*>(.*?)</p>', a)
                snippet = html_lib.unescape(re.sub(r'<[^>]+>', '', snippet_m.group(1))).strip() if snippet_m else ""
                
                if any(dom in link for dom in ['linktr.ee', 'canva.site', 'beacons.ai', 'instagram.com']):
                    count += 1
                    discovered_links.append({
                        'query': q,
                        'title': title,
                        'link': link,
                        'snippet': snippet
                    })
            print(f"[{q}] -> {count} valid links (Total: {len(discovered_links)})")
    except Exception as e:
        print(f"Error {q}: {e}")
    time.sleep(1.2)

with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\discovered_footprints.json', 'w', encoding='utf-8') as f:
    json.dump(discovered_links, f, ensure_ascii=False, indent=2)
print(f"Saved {len(discovered_links)} discovered footprint links.")
