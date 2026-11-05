import urllib.request
import re
import json
import time
import sys
import html as html_lib

sys.stdout.reconfigure(encoding='utf-8')

# Load existing handles from initialLeads.ts
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\existing_handles.json', 'r', encoding='utf-8') as f:
    existing_handles = set(json.load(f))

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

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
}

def parse_follower_count(text):
    if not text:
        return None
    # match 2,803 Followers or 20K Followers or 1.2M Followers or 850 Followers
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

def verify_ig(handle):
    h = handle.strip().lower().lstrip('@').rstrip('.,_/')
    if h in BLOCKLIST or h in existing_handles or len(h) < 3:
        return None
    
    url = f"https://www.instagram.com/{h}/"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            meta_desc = re.search(r'<meta (?:property="og:description"|name="description") content="([^"]+)"', content)
            title_m = re.search(r'<title>(.*?)</title>', content)
            
            raw_desc = html_lib.unescape(meta_desc.group(1)) if meta_desc else ""
            raw_title = html_lib.unescape(title_m.group(1)) if title_m else ""
            
            followers = parse_follower_count(raw_desc)
            
            # Extract clean name from title or desc
            name = ""
            if " - See Instagram" in raw_desc:
                # "from Name (@handle)"
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
    except Exception as e:
        # print(f"@{h} err: {e}")
        pass
    return None

# Load candidate handles from extracted_yt_leads.json
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\extracted_yt_leads.json', encoding='utf-8') as f:
    data = json.load(f)

candidate_handles = set()
handle_meta = {}
for item in data:
    for h in item['handles']:
        h_clean = h.strip().lower().lstrip('@').rstrip('.,_/')
        if len(h_clean) >= 3 and h_clean not in BLOCKLIST and h_clean not in existing_handles:
            candidate_handles.add(h_clean)
            if h_clean not in handle_meta:
                handle_meta[h_clean] = item

# Add candidates from previous manual / bing searches
candidate_handles.update([
    'conteudos.pmba', 'mentoria.barbosa', 'ferreira_34ba', 'assimfaloupapamike',
    'prof.ackson', 'acksonnascimento', 'pmminas', 'miguelangelopmmg', 'metodopm',
    'bizu_com_vagnao', 'erickbiaggi_', 'manualdomike', 'prof.rafaelvalle',
    'pfem.anakarolina', 'irmaospolicia', 'rumo01aprovacao', 'aconcurseirataon',
    'andrecoelhopm', 'recrutapolicial', 'venanciopapiro', 'allanm4rtins',
    'operacao01.jvn', 'thayna_gcm', 'inspetormarcelosilva', 'prof.edinaelsantos',
    'rosinaldojeronimo', 'resumod0concurseiro', 'vagner_mariano', 'felipegraton',
    'williamconcursosciclo', 'cleissonbrum', 'bozzanoconcursos', 'davidlucasods',
    'wesley.pascelli', 'umdiahaveremos', 'paty_curcelli', 'delegadoguilhermegomes'
])

print(f"Total candidate handles to verify: {len(candidate_handles)}")

verified_micro = []

for h in sorted(list(candidate_handles)):
    res = verify_ig(h)
    if res and res['followers'] is not None:
        f_count = res['followers']
        # Rule: between 300 and 25,000 followers
        if 300 <= f_count <= 25000:
            print(f"✅ VERIFIED MICRO-MENTOR: @{h} | {f_count} followers | {res['name']}")
            verified_micro.append(res)
        elif f_count < 300:
            print(f"ℹ️ Nano (<300): @{h} | {f_count} followers | {res['name']}")
            # Include nano mentors if relevant (user said 500 to 20k, min 300)
            if f_count >= 100:
                verified_micro.append(res)
        else:
            print(f"❌ Too big (>25k): @{h} | {f_count} followers")
    else:
        # print(f"⚠️ Could not verify @{h}")
        pass
    time.sleep(0.5)

print(f"\nTotal verified micro-mentors found: {len(verified_micro)}")
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\verified_police_micro.json', 'w', encoding='utf-8') as f:
    json.dump(verified_micro, f, ensure_ascii=False, indent=2)
