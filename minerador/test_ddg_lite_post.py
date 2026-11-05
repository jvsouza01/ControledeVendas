import urllib.request
import urllib.parse
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def check_ddg_lite(q):
    url = f"https://lite.duckduckgo.com/lite/"
    data = urllib.parse.urlencode({'q': q}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            print(f"Lite DDG query [{q}] -> html length: {len(html)}")
            # In Lite DDG, results are in table rows
            # Find links and snippets
            links = re.findall(r'class="result-link"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html)
            snippets = re.findall(r'class="result-snippet"[^>]*>(.*?)</td>', html, re.DOTALL)
            print(f"  Links found: {len(links)} | Snippets found: {len(snippets)}")
            for i, (link, title) in enumerate(links[:5]):
                snip = re.sub(r'<[^>]+>', '', snippets[i]).strip() if i < len(snippets) else ""
                print(f"  [{i+1}] {title} | {link}")
                print(f"      {snip[:120]}")
    except Exception as e:
        print("Error:", e)

check_ddg_lite('site:instagram.com "mentoria" PMBA')
check_ddg_lite('site:instagram.com "mentoria" PMPE')
check_ddg_lite('site:instagram.com "mentoria" PMMG')
check_ddg_lite('site:instagram.com "mentoria" "policia penal"')
check_ddg_lite('site:instagram.com "mentoria" "gcm"')
