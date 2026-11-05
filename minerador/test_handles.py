import requests
import re
import html
import sys

sys.stdout.reconfigure(encoding='utf-8')

ua = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'

def check_profile(handle):
    url = f"https://www.instagram.com/{handle}/"
    try:
        r = requests.get(url, headers={'User-Agent': ua, 'Accept-Language': 'pt-BR'}, timeout=7)
        if r.status_code != 200:
            print(f"[{handle}] Status: {r.status_code}")
            return None
        title_m = re.search(r'<title>(.*?)</title>', r.text)
        title = html.unescape(title_m.group(1)) if title_m else ""
        meta_m = re.search(r'<meta [^>]*content="([^"]*(?:seguidor|follower)[^"]*)"', r.text, re.IGNORECASE)
        meta_str = html.unescape(meta_m.group(1)) if meta_m else ""
        og_desc = ""
        og_m = re.search(r'<meta property="og:description" content="([^"]*)"', r.text)
        if og_m:
            og_desc = html.unescape(og_m.group(1))
            
        print(f"Profile: @{handle}")
        print(f"  Title: {title}")
        print(f"  Meta: {meta_str}")
        return {
            "handle": handle,
            "title": title,
            "meta": meta_str,
            "og_desc": og_desc
        }
    except Exception as e:
        print(f"[{handle}] Error: {e}")
        return None

check_profile('andrenascimentoconcursos')
check_profile('mentoriatrilhadaaprovacao')
check_profile('focanalei')
