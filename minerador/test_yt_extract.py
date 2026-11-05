import urllib.request
import re
import json
import sys

# Ensure utf-8 output
sys.stdout.reconfigure(encoding='utf-8')

urls = [
    'https://www.youtube.com/results?search_query="mentoria"+"concurso"+"kiwify"',
    'https://www.youtube.com/results?search_query="mentoria"+"concurso"+"linktree"',
    'https://www.youtube.com/results?search_query="mentoria"+"policia"+"kiwify"',
    'https://www.youtube.com/results?search_query="mentoria"+"tribunal"+"kiwify"',
    'https://www.youtube.com/results?search_query="mentoria"+"carreiras+policiais"+whatsapp',
    'https://www.youtube.com/results?search_query="mentoria"+"inss"+"kiwify"',
    'https://www.youtube.com/results?search_query="mentoria"+"concurso"+"whatsapp"'
]

video_ids = []

for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
            for vid in ids:
                if vid not in video_ids:
                    video_ids.append(vid)
    except Exception as e:
        print("Error fetching search:", e)

print(f"Total video IDs collected: {len(video_ids)}")

# Now for each video ID, fetch watch page and extract description, instagram, kiwify, linktree, whatsapp
leads_found = []
for vid in video_ids[:30]:
    v_url = f"https://www.youtube.com/watch?v={vid}"
    req = urllib.request.Request(v_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            # Extract title
            title_m = re.search(r'<title>(.*?)</title>', html)
            title = title_m.group(1).replace(' - YouTube', '').strip() if title_m else ''
            
            # Extract author / channel
            author_m = re.search(r'"author":"([^"]+)"', html)
            author = author_m.group(1) if author_m else ''
            
            # Extract instagram
            instas = set(re.findall(r'(?:instagram\.com/|@)([a-zA-Z0-9_.]{3,30})', html))
            # Filter obvious common words
            instas = {i for i in instas if i.lower() not in ['youtube', 'google', 'twitter', 'facebook', 'watch', 'channel']}
            
            # Extract links
            kiwifys = set(re.findall(r'https?://(?:pay\.)?kiwify\.com\.br/[a-zA-Z0-9_.-]+', html))
            was = set(re.findall(r'https?://(?:wa\.me|api\.whatsapp\.com)/[a-zA-Z0-9_.-]+', html))
            linktrees = set(re.findall(r'https?://linktr\.ee/[a-zA-Z0-9_.-]+', html))
            hotmarts = set(re.findall(r'https?://(?:go\.)?hotmart\.com/[a-zA-Z0-9_.-]+', html))
            
            if (kiwifys or was or linktrees or hotmarts or instas) and author:
                leads_found.append({
                    'author': author,
                    'title': title,
                    'instas': list(instas)[:2],
                    'kiwifys': list(kiwifys)[:1],
                    'was': list(was)[:1],
                    'linktrees': list(linktrees)[:1],
                    'hotmarts': list(hotmarts)[:1]
                })
    except Exception as e:
        pass

print(f"Extracted {len(leads_found)} candidate leads:")
for l in leads_found[:15]:
    print(f"Channel/Mentor: {l['author']} | Video: {l['title'][:50]}")
    print(f"  Insta: {l['instas']} | Kiwify: {l['kiwifys']} | WA: {l['was']} | Linktree: {l['linktrees']}")
