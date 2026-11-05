import urllib.request
import urllib.parse
import re
import base64

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

def decode_bing_u(u_str):
    try:
        padding = 4 - (len(u_str) % 4)
        if padding != 4:
            u_str += "=" * padding
        decoded = base64.b64decode(u_str).decode('utf-8', errors='ignore')
        return decoded
    except Exception:
        return ""

q = 'site:instagram.com "mentoria" "tjsp"'
url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
req = urllib.request.Request(url, headers=HEADERS)
with urllib.request.urlopen(req, timeout=10) as r:
    html = r.read().decode('utf-8', errors='ignore')

# Find u=a1...
u_matches = re.findall(r'u=a1([a-zA-Z0-9_\-]+)', html)
print(f"Found {len(u_matches)} bing u=a1 matches")
for u in u_matches[:10]:
    dec = decode_bing_u(u)
    print("Decoded:", dec)

# Also let's see if 'instagram' appears anywhere in html
print("Instagram in html count:", html.count("instagram"))
# Let's see some occurrences
for m in re.finditer(r'instagram', html, re.IGNORECASE):
    idx = m.start()
    print("Occurrence:", html[max(0, idx-50):min(len(html), idx+100)])
    break
