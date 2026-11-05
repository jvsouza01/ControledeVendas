import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

# Test 1: Instagram direct
try:
    r = requests.get('https://www.instagram.com/sally_concursada/', headers=headers, timeout=5)
    print("Direct IG status:", r.status_code)
    # Check meta description
    meta = re.search(r'<meta property="og:description" content="([^"]+)"', r.text)
    if meta:
        print("Meta description:", meta.group(1))
    meta2 = re.search(r'<meta name="description" content="([^"]+)"', r.text)
    if meta2:
        print("Meta name desc:", meta2.group(1))
except Exception as e:
    print("IG error:", e)

# Test 2: Picuki
try:
    r = requests.get('https://www.picuki.com/profile/sally_concursada', headers=headers, timeout=5)
    print("Picuki status:", r.status_code)
    m = re.search(r'<span class="followed_by">([^<]+)</span>', r.text)
    if m:
        print("Picuki followers:", m.group(1))
except Exception as e:
    print("Picuki error:", e)
