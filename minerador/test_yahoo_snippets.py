import requests
import re
import urllib.parse
import html

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def test_yahoo(query):
    url = f"https://search.yahoo.com/search?p={urllib.parse.quote(query)}"
    r = requests.get(url, headers=headers, timeout=8)
    
    # In Yahoo, results are in <div class="dd algo ...">
    algos = re.findall(r'<div class="[^"]*algo[^"]*".*?</li>', r.text, re.DOTALL)
    print(f"\nQuery: {query} -> Algos: {len(algos)}")
    for a in algos:
        # title
        title_m = re.search(r'<h3[^>]*>(.*?)</h3>', a)
        title = html.unescape(re.sub(r'<[^>]+>', '', title_m.group(1))) if title_m else ""
        
        # snippet
        comp_m = re.search(r'<div class="compText[^"]*">(.*?)</div>', a)
        comp = html.unescape(re.sub(r'<[^>]+>', '', comp_m.group(1))) if comp_m else ""
        
        # ru link
        ru_m = re.search(r'RU=([^/&]+)', a)
        link = urllib.parse.unquote(ru_m.group(1)) if ru_m else ""
        
        print(f"  Title: {title}")
        print(f"  Link: {link}")
        print(f"  Snippet: {comp[:120]}")

test_yahoo('site:instagram.com "mentoria individual" "tjsp"')
test_yahoo('site:instagram.com "mentoria" ("ebserh" OR "enfermagem para concursos")')
