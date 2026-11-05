import urllib.request
import re
import json
import html
import time
import sys
import requests

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

FB_UA = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'

with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\yt_targets.json', 'r', encoding='utf-8') as f:
    video_targets = json.load(f)

with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\existing_handles.json', 'r', encoding='utf-8') as f:
    existing_handles = set(json.load(f))

BLOCKLIST = {
    "p", "reel", "reels", "stories", "explore", "tv", "accounts",
    "login", "developer", "about", "legal", "terms", "privacy", "direct", "share",
    "directory", "press", "help", "aboutus", "support", "tags", "locations", "settings",
    "estrategiaconcursos", "grancursosonline", "alfaconcursos", "direcaoconcursos",
    "qconcursos", "folhadirigida", "focusconcursos", "novaconcursos", "cers",
    "concurseiro", "concursos", "kiwify", "hotmart", "eduzz", "linktree", "beacons", "youtube"
}

def clean_handle(h):
    if not h:
        return None
    h = h.lower().strip().replace('@', '').rstrip('/')
    if '/' in h:
        h = h.split('/')[0]
    if '?' in h:
        h = h.split('?')[0]
    h = h.rstrip('.')
    if h in BLOCKLIST or len(h) < 3 or len(h) > 30:
        return None
    if len(h) > 20 and re.match(r'^[a-f0-9]+$', h):
        return None
    return h

def parse_followers(meta_str):
    if not meta_str:
        return None
    m = re.search(r'([\d\.,]+)\s*(k|m|mil)?\s*seguidores', meta_str, re.IGNORECASE)
    if not m:
        return None
    num_str = m.group(1).strip()
    mult = m.group(2)
    try:
        if mult:
            num_clean = num_str.replace('.', '').replace(',', '.')
            val = float(num_clean)
            mult = mult.lower()
            if mult in ['k', 'mil']:
                val *= 1000
            elif mult == 'm':
                val *= 1000000
            return int(val)
        else:
            if ',' in num_str and len(num_str.split(',')[-1]) == 3:
                num_clean = num_str.replace(',', '')
            elif '.' in num_str and len(num_str.split('.')[-1]) == 3:
                num_clean = num_str.replace('.', '')
            else:
                num_clean = num_str.replace('.', '').replace(',', '')
            return int(num_clean)
    except Exception:
        return None

def check_profile(handle):
    url = f"https://www.instagram.com/{handle}/"
    try:
        r = requests.get(url, headers={'User-Agent': FB_UA, 'Accept-Language': 'pt-BR'}, timeout=6)
        if r.status_code != 200:
            return None
        title_m = re.search(r'<title>(.*?)</title>', r.text)
        title = html.unescape(title_m.group(1)) if title_m else ""
        meta_m = re.search(r'<meta [^>]*content="([^"]*(?:seguidor|follower)[^"]*)"', r.text, re.IGNORECASE)
        meta_str = html.unescape(meta_m.group(1)) if meta_m else ""
        
        followers = parse_followers(meta_str)
        if followers is None:
            return None
        
        name_m = re.search(r'^(.*?)\s*\(@', title)
        nome = name_m.group(1).strip() if name_m else title.split('•')[0].strip()
        if not nome or nome == "Instagram":
            nome = handle.replace('_', ' ').replace('.', ' ').title()
            
        return {
            "handle": handle,
            "nome": nome,
            "followers": followers,
            "meta": meta_str,
            "title": title
        }
    except Exception:
        return None

print(f"Inspecting {len(video_targets)} videos...")

verified_mentors = {}

for vid, niche, query in video_targets:
    v_url = f"https://www.youtube.com/watch?v={vid}"
    try:
        req = urllib.request.Request(v_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=6) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            
            author_m = re.search(r'"author":"([^"]+)"', content)
            author = html.unescape(author_m.group(1)) if author_m else ''
            
            title_m = re.search(r'<title>(.*?)</title>', content)
            v_title = html.unescape(title_m.group(1).replace(' - YouTube', '').strip()) if title_m else ''
            
            # Extract handles
            handles = set()
            for m in re.finditer(r'instagram\.com/([a-zA-Z0-9_\.]{3,30})', content):
                h = clean_handle(m.group(1))
                if h: handles.add(h)
                
            for m in re.finditer(r'(?:insta|instagram|ig|segue lá|segue no insta)[:\s\-]+@?([a-zA-Z0-9_\.]{3,30})', content, re.IGNORECASE):
                h = clean_handle(m.group(1))
                if h: handles.add(h)
                
            for lt in re.finditer(r'linktr\.ee/([a-zA-Z0-9_\.]{3,30})', content):
                h = clean_handle(lt.group(1))
                if h: handles.add(h)
                
            for bc in re.finditer(r'beacons\.ai/([a-zA-Z0-9_\.]{3,30})', content):
                h = clean_handle(bc.group(1))
                if h: handles.add(h)
                
            for h in handles:
                if h in existing_handles or h in verified_mentors:
                    continue
                
                # Check profile
                prof = check_profile(h)
                if prof:
                    f_count = prof['followers']
                    print(f"Checking @{h}: {f_count} followers")
                    if 300 <= f_count <= 25000:
                        print(f"  -> VALID MICRO-MENTOR! @{h} ({f_count} seg) [{niche}]")
                        verified_mentors[h] = {
                            "nome": prof['nome'],
                            "instagram": h,
                            "nicho": niche,
                            "followers": f_count,
                            "meta": prof['meta'],
                            "comoEncontrei": f"Micro-Mentor ({round(f_count/1000, 1) if f_count>=1000 else f_count}k seg) • YouTube/Linktree",
                            "observacoes": f"👥 ~{f_count:,} seguidores | Nicho: {niche}. Encontrado via vídeo '{v_title[:45]}...' ({author}). Bio/Meta: {prof['meta'][:120]}",
                            "prioridade": "alta"
                        }
                    else:
                        print(f"  -> Discarded (followers={f_count})")
    except Exception as e:
        pass

print(f"\nTotal verified micro-mentors found from this batch: {len(verified_mentors)}")
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\batch1_verified.json', 'w', encoding='utf-8') as f:
    json.dump(list(verified_mentors.values()), f, ensure_ascii=False, indent=2)
