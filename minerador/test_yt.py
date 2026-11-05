import urllib.request
import re
import json

urls = [
    'https://www.youtube.com/results?search_query="mentoria"+"concurso"+"kiwify"',
    'https://www.youtube.com/results?search_query="mentoria"+"concurso"+"linktr.ee"',
    'https://www.youtube.com/results?search_query="mentoria"+"policia"+"kiwify"',
    'https://www.youtube.com/results?search_query="mentoria"+"tribunais"+"kiwify"'
]

for url in urls:
    print("Fetching:", url)
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract video titles and channel names
            # In ytInitialData
            matches = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}\].*?"ownerText":\{"runs":\[\{"text":"([^"]+)"', html)
            print(f"Found {len(matches)} results")
            for title, channel in matches[:5]:
                print(f"  [{channel}] -> {title}")
    except Exception as e:
        print("Error:", e)
