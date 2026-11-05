import urllib.request
import urllib.parse
import re
import html as html_lib
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

def inspect_yahoo_page(q):
    url = f"https://br.search.yahoo.com/search?p={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            content = r.read().decode('utf-8', errors='ignore')
            # Each result is in an <li class="">
            blocks = re.findall(r'<div class="compTitle[^"]*">.*?<div class="compText[^"]*">.*?</div>', content, re.DOTALL)
            print(f"Query: [{q}] -> {len(blocks)} blocks found")
            for b in blocks:
                t_m = re.search(r'<h3[^>]*>(.*?)</h3>', b, re.DOTALL)
                title = html_lib.unescape(re.sub(r'<[^>]+>', '', t_m.group(1))).strip() if t_m else ""
                s_m = re.search(r'<div class="compText[^"]*">(.*?)</div>', b, re.DOTALL)
                snippet = html_lib.unescape(re.sub(r'<[^>]+>', '', s_m.group(1))).strip() if s_m else ""
                u_m = re.search(r'href="([^"]+)"', b)
                raw_u = u_m.group(1) if u_m else ""
                actual_u = ""
                if 'RU=' in raw_u:
                    ru = re.search(r'RU=([^/&]+)', raw_u)
                    if ru:
                        actual_u = urllib.parse.unquote(ru.group(1))
                else:
                    actual_u = raw_u
                print(f"  Title: {title}")
                print(f"  URL: {actual_u}")
                print(f"  Snippet: {snippet[:120]}")
                print("---")
    except Exception as e:
        print("Error:", e)

inspect_yahoo_page('site:instagram.com "mentoria" "PMSC"')
