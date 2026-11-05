import urllib.request
import urllib.parse
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

def test_bing(query):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}&setlang=pt-br"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Look for instagram links
            matches = re.findall(r'https?://(?:www\.)?instagram\.com/([a-zA-Z0-9_\.]+)/?', html)
            print(f"Bing matches for '{query}':", set(matches[:15]))
            # Let's inspect text around some matches
            for m in list(set(matches))[:5]:
                idx = html.find(m)
                snippet = html[max(0, idx-100):min(len(html), idx+300)]
                # strip html tags
                clean = re.sub(r'<[^>]+>', ' ', snippet)
                clean = ' '.join(clean.split())
                print(f"  Snippet for {m}: {clean[:150]}")
    except Exception as e:
        print("Error Bing:", e)

test_bing('site:instagram.com "mentoria individual" "TJSP" "seguidores"')
