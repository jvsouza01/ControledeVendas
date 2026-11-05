import requests
import re
import urllib.parse

def test_engine(name, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
    }
    try:
        r = requests.get(url, headers=headers, timeout=8)
        print(f"[{name}] Status: {r.status_code}, Length: {len(r.text)}")
        ig_matches = re.findall(r'instagram\.com/([a-zA-Z0-9_\.]{3,30})', r.text)
        print(f"[{name}] IG matches: {set(ig_matches[:10])}")
    except Exception as e:
        print(f"[{name}] Error: {e}")

q = 'site:instagram.com "mentoria individual" "TJSP"'
q_enc = urllib.parse.quote(q)

test_engine("Yahoo", f"https://search.yahoo.com/search?p={q_enc}")
test_engine("Qwant", f"https://www.qwant.com/?q={q_enc}&t=web")
test_engine("Startpage", f"https://www.startpage.com/sp/search?query={q_enc}")
test_engine("Mojeek", f"https://www.mojeek.com/search?q={q_enc}")
