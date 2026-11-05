import requests
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

url = "https://linktr.ee/sally_concursada"
try:
    r = requests.get(url, headers=headers, timeout=5)
    print("Linktree status:", r.status_code)
    # find instagram link or links
    ig_links = re.findall(r'instagram\.com/([a-zA-Z0-9_\.]+)', r.text)
    print("IG links on page:", ig_links)
    # find all links on page
    links = re.findall(r'href="([^"]+)"', r.text)
    print("Links found:", [l for l in links if 'wa.me' in l or 'hotmart' in l or 'kiwify' in l or 'canva' in l][:5])
except Exception as e:
    print("Error:", e)
