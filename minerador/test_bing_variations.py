import sys
import urllib.request
import urllib.parse
import re
import base64
import html as html_lib

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

variations = [
    'site:instagram.com mentoria pmpe',
    'site:instagram.com mentoria pmce',
    'site:instagram.com mentoria pmgo',
    'site:instagram.com mentoria pmmg',
    'site:instagram.com mentoria pmpr',
    'site:instagram.com mentoria "policia penal"',
    'site:instagram.com mentoria "gcm"',
    'site:instagram.com mentoria "concurso policial"',
    'site:instagram.com "mentoria policial"',
    'site:instagram.com "mentoria" "concurso"',
    'site:instagram.com "mentoria para concurso"',
    'site:instagram.com/ "mentoria" pmpe',
    'site:instagram.com/ "mentoria" pmmg',
    'site:instagram.com/ "mentoria" gcm',
    'site:instagram.com/ "mentoria" policia',
    'site:instagram.com/ "cronograma" pmba',
    'site:instagram.com/ "cronograma" pmpe'
]

for q in variations:
    url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            algos = re.findall(r'<li class="b_algo".*?</li>', content, re.DOTALL)
            ig_results = []
            for a in algos:
                u_m = re.search(r'u=a1([a-zA-Z0-9_\-]+)', a)
                link = decode_bing_u(u_m.group(1)) if u_m else ""
                if 'instagram.com' in link:
                    title_m = re.search(r'<h2[^>]*>(.*?)</h2>', a)
                    title = html_lib.unescape(re.sub(r'<[^>]+>', '', title_m.group(1))) if title_m else ""
                    snippet_m = re.search(r'<p[^>]*>(.*?)</p>', a)
                    snippet = html_lib.unescape(re.sub(r'<[^>]+>', '', snippet_m.group(1))).strip() if snippet_m else ""
                    ig_results.append((title, link, snippet))
            print(f"[{q}] -> IG matches: {len(ig_results)}")
            for t, l, s in ig_results[:3]:
                print(f"   {t} | {l}")
                print(f"   Snippet: {s[:100]}")
    except Exception as e:
        print(f"Error {q}: {e}")
