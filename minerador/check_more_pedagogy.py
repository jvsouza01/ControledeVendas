import requests
import re
import html
import sys

sys.stdout.reconfigure(encoding='utf-8')
FB_UA = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'

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

handles = [
    ("pedagogiaparaoquadro", "Pedagogia / Educação"),
    ("concursopedagogico", "Pedagogia / Educação"),
    ("resumosdepedagogia", "Pedagogia / Educação"),
    ("resumospedagogicos", "Pedagogia / Educação"),
    ("concursospedagogia", "Pedagogia / Educação"),
    ("pedagogiaresumos", "Pedagogia / Educação"),
    ("foconopedagogo", "Pedagogia / Educação"),
    ("pedagogiadescomplicada", "Pedagogia / Educação"),
    ("pedagogiaparaconcursando", "Pedagogia / Educação"),
    ("concurseirapedagoga_", "Pedagogia / Educação"),
    ("professoresconcurseiros", "Pedagogia / Educação"),
    ("pedagogiadivertida", "Pedagogia / Educação"),
    ("pedagogiaparainiciantes", "Pedagogia / Educação"),
    ("foconaenfermagemconcursos", "Saúde / Enfermagem"),
    ("resumosenf", "Saúde / Enfermagem"),
    ("enfermagem_concursos_ebserh", "Saúde / Enfermagem"),
    ("concurseiraenfermeira", "Saúde / Enfermagem"),
    ("ebserh_resumos", "Saúde / Enfermagem"),
    ("mentoriaebserh2024", "Saúde / Enfermagem")
]

for h, niche in handles:
    try:
        r = requests.get(f'https://www.instagram.com/{h}/', headers={'User-Agent': FB_UA}, timeout=4)
        meta = re.search(r'<meta [^>]*content="([^"]*(?:seguidor|follower)[^"]*)"', r.text, re.IGNORECASE)
        if meta:
            f = parse_followers(meta.group(1))
            t = re.search(r'<title>(.*?)</title>', r.text)
            title = html.unescape(t.group(1)) if t else ""
            if f and 300 <= f <= 25000:
                print(f"VERIFIED: @{h} ({f} seg) [{niche}] - {title[:40]}")
    except Exception as e:
        pass
