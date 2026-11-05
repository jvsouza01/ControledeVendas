import urllib.request, re, json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('c:/Users/jao_v/Desktop/ControledeVendas/minerador/yt_police_videos.json', 'r', encoding='utf-8') as f:
    vids = list(json.load(f).keys())

for vid in vids[10:25]:
    url = f'https://www.youtube.com/watch?v={vid}'
    try:
        html = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=5).read().decode('utf-8', errors='ignore')
        # check for escaped instagram
        ig_escaped = re.findall(r'instagram\.com[\\/]+([a-zA-Z0-9_\.]{3,30})', html)
        print(f"Vid {vid} -> ig_escaped: {ig_escaped}")
    except Exception as e:
        print("err:", e)
