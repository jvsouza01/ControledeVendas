import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
}

def check_insta(handle):
    url = f"https://www.instagram.com/{handle}/"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=6) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            meta_desc = re.search(r'<meta (?:property="og:description"|name="description") content="([^"]+)"', html)
            title = re.search(r'<title>(.*?)</title>', html)
            if meta_desc:
                print(f"@{handle} -> META: {meta_desc.group(1)}")
            else:
                print(f"@{handle} -> Title: {title.group(1) if title else 'No title'}")
    except Exception as e:
        print(f"@{handle} error: {e}")

check_insta('conteudos.pmba')
check_insta('ferreira_34ba')
check_insta('mentoria.barbosa')
check_insta('allanm4rtins')
check_insta('thayna_gcm')
