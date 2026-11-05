import urllib.request
import urllib.parse
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

def test_engine(name, url):
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read().decode('utf-8', errors='ignore')
            ig = re.findall(r'instagram\.com/([a-zA-Z0-9_\.]+)', data)
            valid = [x for x in set(ig) if x not in ('p', 'reel', 'reels', 'explore', 'about', 'legal')]
            print(f"[{name}] length: {len(data)} | Valid IG: {len(valid)} -> {valid[:5]}")
    except Exception as e:
        print(f"[{name}] error: {e}")

q = 'mentoria PMBA instagram'
test_engine('Mojeek', f"https://www.mojeek.com/search?q={urllib.parse.quote(q)}")
test_engine('Qwant', f"https://www.qwant.com/?q={urllib.parse.quote(q)}&t=web")
test_engine('Brave', f"https://search.brave.com/search?q={urllib.parse.quote('site:instagram.com mentoria PMBA')}")
