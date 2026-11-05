import urllib.request
import re
import json
import time
import sys
import html as html_lib
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\existing_handles.json', 'r', encoding='utf-8') as f:
    existing_handles = set(json.load(f))

# Load already verified to avoid re-checking
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\verified_police_micro.json', 'r', encoding='utf-8') as f:
    already_verified = {x['handle']: x for x in json.load(f)}

BLOCKLIST = {
    "estrategiaconcursos", "grancursosonline", "alfaconcursos", "direcaoconcursos",
    "focusconcursos", "qconcursos", "tecconcursos", "ceisc_", "damasioeducacional",
    "cers", "cersconcursos", "folhadirigida", "pciconcursos", "braboconcursos",
    "nova_concursos", "degraucultural", "centraldeconcursos", "editorajuspodivm",
    "kultivi", "metodoresolve", "garraconcursos", "youtube", "google", "instagram",
    "facebook", "twitter", "whatsapp", "tiktok", "linktree", "kiwify", "hotmart",
    "sympla", "eduzz", "monetizze", "linkedin", "spotify", "telegram",
    "http", "https", "curso", "invites", "instagram.com"
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
googlebot_headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

queries2 = [
    'mentoria pm tocantins',
    'mentoria pm alagoas',
    'mentoria pmal',
    'mentoria pmrn',
    'mentoria pmpi',
    'mentoria pmma',
    'mentoria policia penal sp',
    'mentoria policia penal mg',
    'mentoria policia penal ce',
    'mentoria policia penal go',
    'mentoria gcm sp',
    'mentoria gcm rj',
    'mentoria gcm goiania',
    'mentoria guarda civil municipal',
    'cronograma soldado pmmg',
    'cronograma soldado pmesp',
    'cronograma soldado pmba',
    'cronograma soldado pmce',
    'cronograma soldado pmpb',
    'cronograma cfo pmmg',
    'cronograma cfo pmesp',
    'mentoria bombeiro militar',
    'mentoria cbmmg',
    'mentoria cbmpe',
    'mentoria cbmba'
]

video_data2 = {}
for q in queries2:
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            matches = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})".*?"title":\{"runs":\[\{"text":"([^"]+)"\}\].*?"ownerText":\{"runs":\[\{"text":"([^"]+)"', html)
            for vid, title, owner in matches:
                if vid not in video_data2:
                    video_data2[vid] = {'title': title, 'owner': owner, 'query': q}
    except Exception as e:
        pass

print(f"Collected {len(video_data2)} new videos from batch 2.")

def clean_handle(h):
    if not h:
        return None
    h = h.strip().lower().lstrip('@').rstrip('.,_/')
    h = re.sub(r'[^a-zA-Z0-9_\.]', '', h)
    if len(h) < 3 or len(h) > 30:
        return None
    if h in BLOCKLIST or h in existing_handles or h in already_verified:
        return None
    if any(h.startswith(prefix) for prefix in ['reel', 'p_', 'tag_', 'explore_']):
        return None
    return h

def process_vid(vid, data):
    url = f"https://www.youtube.com/watch?v={vid}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=7) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            ig_urls = re.findall(r'instagram\.com/([a-zA-Z0-9_\.]{3,30})/?', html)
            at_matches = re.findall(r'Instagram:\s*@?([a-zA-Z0-9_\.]{3,30})', html, re.I)
            at_matches2 = re.findall(r'Insta:\s*@?([a-zA-Z0-9_\.]{3,30})', html, re.I)
            candidates = set(ig_urls + at_matches + at_matches2)
            valid = []
            for c in candidates:
                ch = clean_handle(c)
                if ch and ch not in valid:
                    valid.append(ch)
            if valid:
                return {'vid': vid, 'title': data['title'], 'owner': data['owner'], 'query': data['query'], 'handles': valid}
    except:
        pass
    return None

new_candidates = set()
with ThreadPoolExecutor(max_workers=12) as executor:
    futures = {executor.submit(process_vid, vid, data): vid for vid, data in video_data2.items()}
    for f in as_completed(futures):
        res = f.result()
        if res:
            for h in res['handles']:
                new_candidates.add(h)

print(f"Found {len(new_candidates)} fresh candidate handles to verify.")

def parse_follower_count(text):
    if not text:
        return None
    m = re.search(r'([0-9.,]+)\s*([KkMm]|mil|million)?\s*(?:Followers|Seguidores)', text, re.I)
    if not m:
        return None
    num_str = m.group(1).replace(',', '')
    mult = m.group(2)
    try:
        val = float(num_str)
        if mult:
            mult = mult.lower()
            if mult in ('k', 'mil'):
                val *= 1000
            elif mult in ('m', 'million'):
                val *= 1000000
        return int(val)
    except:
        return None

def verify_ig(h):
    url = f"https://www.instagram.com/{h}/"
    req = urllib.request.Request(url, headers=googlebot_headers)
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            meta_desc = re.search(r'<meta (?:property="og:description"|name="description") content="([^"]+)"', content)
            title_m = re.search(r'<title>(.*?)</title>', content)
            raw_desc = html_lib.unescape(meta_desc.group(1)) if meta_desc else ""
            raw_title = html_lib.unescape(title_m.group(1)) if title_m else ""
            followers = parse_follower_count(raw_desc)
            name = ""
            if " - See Instagram" in raw_desc:
                m_name = re.search(r'from (.*?) \(@' + re.escape(h) + r'\)', raw_desc, re.I)
                if m_name:
                    name = m_name.group(1).strip()
            if not name and raw_title:
                name = raw_title.split('(')[0].replace('• Instagram photos and videos', '').replace('- Instagram', '').strip()
            return {
                'handle': h,
                'name': name or f"@{h}",
                'followers': followers,
                'raw_desc': raw_desc,
                'title': raw_title
            }
    except:
        pass
    return None

new_verified = []
for h in sorted(list(new_candidates)):
    res = verify_ig(h)
    if res and res['followers'] is not None:
        f_count = res['followers']
        if 150 <= f_count <= 25000:
            print(f"✅ NEW VERIFIED: @{h} | {f_count} followers | {res['name']}")
            new_verified.append(res)
        else:
            print(f"❌ Size filter (@{h}): {f_count}")
    time.sleep(0.4)

all_verified = list(already_verified.values()) + new_verified
print(f"\nTOTAL ALL VERIFIED MICRO-MENTORS: {len(all_verified)}")

with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\all_verified_police_micro.json', 'w', encoding='utf-8') as f:
    json.dump(all_verified, f, ensure_ascii=False, indent=2)
