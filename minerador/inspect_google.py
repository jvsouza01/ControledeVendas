import urllib.request
import urllib.parse
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

def inspect_google(q):
    url = f"https://www.google.com/search?q={urllib.parse.quote(q)}&hl=pt-BR&num=20"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # find all hrefs
            all_hrefs = re.findall(r'href="([^"]+)"', html)
            print(f"Total hrefs: {len(all_hrefs)}")
            for h in set(all_hrefs):
                if 'instagram' in h or 'linktr.ee' in h or 'canva' in h:
                    print("Match:", h)
    except Exception as e:
        print("Error:", e)

inspect_google('site:instagram.com "mentoria" PMBA')
