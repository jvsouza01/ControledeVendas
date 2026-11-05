import requests
import re
import html
import urllib.parse

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
FB_UA = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'

url = "https://search.yahoo.com/search?p=site%3Ainstagram.com+%22mentoria+individual%22+%22tjsp%22"
r = requests.get(url, headers=headers)
rus = re.findall(r'RU=([^/&]+)', r.text)

print(f"Found {len(rus)} RU links")
for ru in rus:
    dec = urllib.parse.unquote(ru)
    if 'instagram.com' in dec:
        print("  IG Link:", dec)
        # If it's a post, let's fetch it and see what author we get!
        if '/p/' in dec or '/reel/' in dec:
            try:
                res = requests.get(dec, headers={'User-Agent': FB_UA}, timeout=5)
                # Look for author
                # Title often: "Name (@handle) on Instagram: ..." or "<title>... • Instagram photos..."
                t = re.search(r'<title>(.*?)</title>', res.text)
                title_str = t.group(1) if t else ""
                print("    Post Title:", title_str[:100])
                # look for @handle in title
                h_m = re.search(r'\(@([a-zA-Z0-9_\.]+)\)', title_str)
                if h_m:
                    print("    Extracted author handle:", h_m.group(1))
            except Exception as e:
                print("    Error fetching post:", e)
