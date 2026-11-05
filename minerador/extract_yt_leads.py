import urllib.request
import re
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

# Load existing handles from initialLeads.ts
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\existing_handles.json', 'r', encoding='utf-8') as f:
    existing_handles = set(json.load(f))

# Load video data
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\yt_police_videos.json', 'r', encoding='utf-8') as f:
    video_dict = json.load(f)

BLOCKLIST = {
    "estrategiaconcursos", "grancursosonline", "alfaconcursos", "direcaoconcursos",
    "focusconcursos", "qconcursos", "tecconcursos", "ceisc_", "damasioeducacional",
    "cers", "cersconcursos", "folhadirigida", "pciconcursos", "braboconcursos",
    "nova_concursos", "degraucultural", "centraldeconcursos", "editorajuspodivm",
    "kultivi", "metodoresolve", "garraconcursos", "youtube", "google", "instagram",
    "facebook", "twitter", "whatsapp", "tiktok", "linktree", "kiwify", "hotmart",
    "sympla", "eduzz", "monetizze", "linkedin", "spotify", "telegram"
}

def clean_handle(h):
    if not h:
        return None
    h = h.strip().lower().lstrip('@').rstrip('.,_/')
    h = re.sub(r'[^a-zA-Z0-9_\.]', '', h)
    if len(h) < 3 or len(h) > 30:
        return None
    if h in BLOCKLIST or h in existing_handles:
        return None
    if any(h.startswith(prefix) for prefix in ['reel', 'p_', 'tag_', 'explore_']):
        return None
    return h

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def process_video(vid, data):
    url = f"https://www.youtube.com/watch?v={vid}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=7) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Channel subscriber count if present
            sub_m = re.search(r'([0-9,\.]+\s*(?:mil|k|mi|subscribers|inscritos))', html, re.I)
            subs = sub_m.group(1) if sub_m else "N/D"
            
            # Instagram links or mentions
            # Pattern 1: instagram.com/handle
            ig_urls = re.findall(r'instagram\.com/([a-zA-Z0-9_\.]{3,30})/?', html)
            # Pattern 2: @handle in description
            at_matches = re.findall(r'Instagram:\s*@?([a-zA-Z0-9_\.]{3,30})', html, re.I)
            at_matches2 = re.findall(r'Insta:\s*@?([a-zA-Z0-9_\.]{3,30})', html, re.I)
            
            candidates = set(ig_urls + at_matches + at_matches2)
            valid_handles = []
            for c in candidates:
                ch = clean_handle(c)
                if ch and ch not in valid_handles:
                    valid_handles.append(ch)
            
            # Also extract linktree, canva, kiwify, beacons, wa.me
            lt = re.findall(r'https?://(?:www\.)?linktr\.ee/[a-zA-Z0-9_\.\-]+', html)
            canva = re.findall(r'https?://[a-zA-Z0-9_\.\-]+\.my\.canva\.site/[a-zA-Z0-9_\.\-]+', html)
            beacons = re.findall(r'https?://(?:www\.)?beacons\.ai/[a-zA-Z0-9_\.\-]+', html)
            kiwify = re.findall(r'https?://(?:pay\.)?kiwify\.com\.br/[a-zA-Z0-9_\.\-]+', html)
            wa = re.findall(r'https?://(?:wa\.me|api\.whatsapp\.com)/[0-9a-zA-Z_\.\-]+', html)
            
            if valid_handles:
                return {
                    'vid': vid,
                    'title': data['title'],
                    'owner': data['owner'],
                    'query': data['query'],
                    'handles': valid_handles,
                    'subs': subs,
                    'linktree': list(set(lt))[:1],
                    'canva': list(set(canva))[:1],
                    'beacons': list(set(beacons))[:1],
                    'kiwify': list(set(kiwify))[:1],
                    'whatsapp': list(set(wa))[:1]
                }
    except Exception as e:
        pass
    return None

results = []
print(f"Processing {len(video_dict)} videos with ThreadPoolExecutor...")

with ThreadPoolExecutor(max_workers=12) as executor:
    futures = {executor.submit(process_video, vid, data): vid for vid, data in video_dict.items()}
    for f in as_completed(futures):
        res = f.result()
        if res:
            results.append(res)
            print(f"Found: {res['owner']} -> @{res['handles'][0]} | Query: {res['query']}")

print(f"\nTotal extracted leads with valid Instagram: {len(results)}")
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\extracted_yt_leads.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("Saved to extracted_yt_leads.json")
