import urllib.request
import urllib.parse
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

def search_ddg(query):
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Look for result snippets
            results = []
            # In DDG html, results are in <div class="result ...">
            blocks = re.findall(r'<div class="result results_links.*?</div>\s*</div>\s*</div>', html, re.DOTALL)
            print(f"Query: {query} -> blocks found: {len(blocks)}")
            for b in blocks:
                t_m = re.search(r'<a class="result__snippet[^>]*>(.*?)</a>', b, re.DOTALL)
                title_m = re.search(r'<a class="result__url[^>]*href="([^"]+)"', b)
                snippet = re.sub(r'<[^>]+>', '', t_m.group(1)).strip() if t_m else ""
                raw_url = title_m.group(1) if title_m else ""
                # DDG urls are redirected: //duckduckgo.com/l/?uddg=...
                actual_url = ""
                if 'uddg=' in raw_url:
                    uddg = raw_url.split('uddg=')[1].split('&')[0]
                    actual_url = urllib.parse.unquote(uddg)
                else:
                    actual_url = raw_url
                print(f"URL: {actual_url}")
                print(f"Snippet: {snippet[:120]}")
                print("---")
    except Exception as e:
        print("Error:", e)

search_ddg('site:linktr.ee "mentoria" ("pmba" OR "pmpe" OR "pmce" OR "pmpb")')
