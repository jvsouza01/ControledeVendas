import urllib.request
import urllib.parse
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7'
}

def search_yahoo(q):
    url = "https://search.yahoo.com/search?p=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # find links
            links = re.findall(r'href="(https?://[^"]+)"', html)
            # filter instagram, canva, linktree, beacons
            found = set()
            for l in links:
                if 'instagram.com/' in l or 'linktr.ee/' in l or 'my.canva.site' in l or 'beacons.ai/' in l:
                    found.add(l)
            print(f"Yahoo: '{q}' -> found {len(found)} matching links")
            for item in list(found)[:5]:
                print("  ", item)
    except Exception as e:
        print("Yahoo error:", e)

search_yahoo('site:instagram.com "mentoria" PMBA')
search_yahoo('site:linktr.ee mentoria PMBA')
search_yahoo('site:my.canva.site mentoria PM')
