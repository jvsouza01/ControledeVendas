import requests
import re
import html
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

FB_UA = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'

candidates = [
    ("focanompu", "Tribunais / Jurídica"),
    ("concursotrt2", "Tribunais / Jurídica"),
    ("concursotrt15", "Tribunais / Jurídica"),
    ("concursotrt3", "Tribunais / Jurídica"),
    ("focanadpu", "Tribunais / Jurídica"),
    ("concursodpu", "Tribunais / Jurídica"),
    ("concursompe", "Tribunais / Jurídica"),
    ("enfermagemilustrada", "Saúde / Enfermagem"),
    ("enfermagem.resumos", "Saúde / Enfermagem"),
    ("pedagogiaconcurseira", "Pedagogia / Educação"),
    ("mentoriaparatribunais", "Tribunais / Jurídica"),
    ("tribunais_concursos", "Tribunais / Jurídica"),
    ("trtconcursos", "Tribunais / Jurídica"),
    ("prof.felipepereira", "Tribunais / Jurídica"),
    ("professormatheus", "Tribunais / Jurídica")
]

def parse_followers(meta_str):
    if not meta_str: return None
    m = re.search(r'([\d\.,]+)\s*(k|m|mil)?\s*seguidores', meta_str, re.IGNORECASE)
    if not m: return None
    num_str = m.group(1).strip()
    mult = m.group(2)
    try:
        if mult:
            val = float(num_str.replace('.', '').replace(',', '.'))
            if mult.lower() in ['k', 'mil']: val *= 1000
            elif mult.lower() == 'm': val *= 1000000
            return int(val)
        else:
            if ',' in num_str and len(num_str.split(',')[-1]) == 3: num_clean = num_str.replace(',', '')
            elif '.' in num_str and len(num_str.split('.')[-1]) == 3: num_clean = num_str.replace('.', '')
            else: num_clean = num_str.replace('.', '').replace(',', '')
            return int(num_clean)
    except: return None

for h, niche in candidates:
    url = f"https://www.instagram.com/{h}/"
    try:
        r = requests.get(url, headers={'User-Agent': FB_UA, 'Accept-Language': 'pt-BR'}, timeout=5)
        if r.status_code == 200:
            title_m = re.search(r'<title>(.*?)</title>', r.text)
            title = html.unescape(title_m.group(1)) if title_m else ""
            meta_m = re.search(r'<meta [^>]*content="([^"]*(?:seguidor|follower)[^"]*)"', r.text, re.IGNORECASE)
            meta_str = html.unescape(meta_m.group(1)) if meta_m else ""
            f = parse_followers(meta_str)
            if f and 300 <= f <= 25000:
                name_m = re.search(r'^(.*?)\s*\(@', title)
                nome = name_m.group(1).strip() if name_m else title.split('•')[0].strip()
                if not nome or nome == "Instagram": nome = h.replace('_', ' ').title()
                print(f"FOUND: @{h} ({f} seg) [{niche}] - {nome}")
    except: pass
