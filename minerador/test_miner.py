import requests
import re
import urllib.parse
import html
import time
import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
}

FB_UA = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'

# Load existing handles
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\existing_handles.json', 'r', encoding='utf-8') as f:
    existing_handles = set(json.load(f))

BLOCKLIST = {
    "p", "reel", "reels", "stories", "explore", "tv", "accounts",
    "login", "developer", "about", "legal", "terms", "privacy", "direct", "share",
    "directory", "press", "help", "aboutus", "support", "tags", "locations", "settings",
    "estrategiaconcursos", "grancursosonline", "alfaconcursos", "direcaoconcursos",
    "qconcursos", "folhadirigida", "focusconcursos", "novaconcursos", "cers",
    "concurseiro", "concursos", "kiwify", "hotmart", "eduzz", "linktree", "beacons"
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
    # avoid hashes / random hex
    if len(h) > 20 and re.match(r'^[a-f0-9]+$', h):
        return None
    return h

def search_yahoo_handles(query, max_pages=2):
    found = set()
    for page in range(max_pages):
        b = page * 10 + 1
        url = f"https://search.yahoo.com/search?p={urllib.parse.quote(query)}&b={b}"
        try:
            r = requests.get(url, headers=HEADERS, timeout=8)
            # Find RU=
            rus = re.findall(r'RU=([^/&]+)', r.text)
            for ru in rus:
                dec = urllib.parse.unquote(ru)
                # match profile
                m_prof = re.search(r'instagram\.com/([a-zA-Z0-9_\.]{3,30})/?(?:\?|$)', dec)
                if m_prof:
                    h = clean_handle(m_prof.group(1))
                    if h:
                        found.add((h, dec))
                # match linktree
                m_lt = re.search(r'linktr\.ee/([a-zA-Z0-9_\.]{3,30})', dec)
                if m_lt:
                    h = clean_handle(m_lt.group(1))
                    if h:
                        found.add((h, dec))
            time.sleep(0.5)
        except Exception as e:
            print(f"Error Yahoo '{query}': {e}")
    return found

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
        r = requests.get(url, headers={'User-Agent': FB_UA, 'Accept-Language': 'pt-BR'}, timeout=7)
        if r.status_code != 200:
            return None
        title_m = re.search(r'<title>(.*?)</title>', r.text)
        title = html.unescape(title_m.group(1)) if title_m else ""
        meta_m = re.search(r'<meta [^>]*content="([^"]*(?:seguidor|follower)[^"]*)"', r.text, re.IGNORECASE)
        meta_str = html.unescape(meta_m.group(1)) if meta_m else ""
        
        followers = parse_followers(meta_str)
        if followers is None:
            return None
        
        # Name extraction
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

if __name__ == '__main__':
    print("Testing Yahoo Miner...")
    q = 'site:instagram.com "mentoria individual" "tjsp"'
    handles = search_yahoo_handles(q, max_pages=1)
    print("Found handles:", handles)
    for h, origin in handles:
        prof = check_profile(h)
        if prof:
            print(f"Verified @{h}: {prof['nome']} - {prof['followers']} followers")
