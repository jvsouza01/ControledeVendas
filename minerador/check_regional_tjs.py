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

for h in ['concursotjpr', 'concursotjsc', 'concursotjrs', 'concursotjce', 'concursotjba', 'concursotjpe', 'concursotjgo', 'concursotjrn', 'concursotjma', 'concursotjpa']:
    try:
        r = requests.get(f'https://www.instagram.com/{h}/', headers={'User-Agent': FB_UA}, timeout=5)
        meta = re.search(r'<meta [^>]*content="([^"]*(?:seguidor|follower)[^"]*)"', r.text, re.IGNORECASE)
        if meta:
            f = parse_followers(meta.group(1))
            t = re.search(r'<title>(.*?)</title>', r.text)
            title = html.unescape(t.group(1)) if t else ""
            if f and 300 <= f <= 25000:
                print(f"VERIFIED: @{h} ({f} seg) - {title[:40]}")
    except Exception as e:
        pass
