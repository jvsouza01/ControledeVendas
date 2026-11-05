import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

police_queries = [
    'mentoria pmba',
    'mentoria pmpe',
    'mentoria pmpb',
    'mentoria pmce',
    'mentoria pmmg',
    'mentoria pmesp',
    'mentoria pmgo',
    'mentoria pmpr',
    'mentoria pmsc',
    'mentoria pmpa',
    'mentoria policia penal',
    'mentoria gcm',
    'mentoria guarda municipal',
    'cronograma pmba',
    'cronograma pmpe',
    'cronograma policia penal',
    'cronograma gcm'
]

video_data = {}

for q in police_queries:
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract video blocks or items
            # In ytInitialData, find videoId, title, ownerText
            matches = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})".*?"title":\{"runs":\[\{"text":"([^"]+)"\}\].*?"ownerText":\{"runs":\[\{"text":"([^"]+)"', html)
            print(f"[{q}] -> found {len(matches)} videos")
            for vid, title, owner in matches:
                if vid not in video_data:
                    video_data[vid] = {
                        'title': title,
                        'owner': owner,
                        'query': q
                    }
    except Exception as e:
        print(f"Error on {q}: {e}")

print(f"\nTotal unique videos collected: {len(video_data)}")
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\yt_police_videos.json', 'w', encoding='utf-8') as f:
    json.dump(video_data, f, ensure_ascii=False, indent=2)
