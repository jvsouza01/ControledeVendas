import requests
import re
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

def inspect_ig(handle):
    url = f"https://www.instagram.com/{handle}/"
    r = requests.get(url, headers=headers, timeout=5)
    print(f"Status for {handle}:", r.status_code)
    # Check title
    title_m = re.search(r'<title>(.*?)</title>', r.text)
    print("Title:", title_m.group(1) if title_m else "None")
    # Check meta tags
    metas = re.findall(r'<meta\s+[^>]*content="([^"]*)"[^>]*>', r.text)
    for m in metas:
        if 'seguidor' in m.lower() or 'follower' in m.lower() or 'post' in m.lower():
            print("Meta snippet:", m)
    # Also check JSON in scripts
    scripts = re.findall(r'<script type="application/ld\+json">({.*?})</script>', r.text, re.DOTALL)
    for s in scripts:
        try:
            data = json.loads(s)
            print("JSON-LD:", data)
        except:
            pass

inspect_ig('sally_concursada')
inspect_ig('antoniodotribunal')
