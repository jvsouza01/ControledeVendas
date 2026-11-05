import requests
import re

user_agents = {
    'facebook': 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
    'googlebot': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'whatsapp': 'WhatsApp/2.21.12.21 N',
    'twitter': 'Twitterbot/1.0',
    'telegram': 'TelegramBot (like TwitterBot)'
}

for name, ua in user_agents.items():
    try:
        r = requests.get('https://www.instagram.com/sally_concursada/', headers={'User-Agent': ua, 'Accept-Language': 'pt-BR,pt;q=0.9'}, timeout=5)
        print(f"UA {name} -> Status: {r.status_code}, Length: {len(r.text)}")
        title = re.search(r'<title>(.*?)</title>', r.text)
        print(f"  Title: {title.group(1) if title else 'None'}")
        meta = re.search(r'<meta [^>]*content="([^"]*(?:seguidor|follower)[^"]*)"', r.text, re.IGNORECASE)
        if meta:
            print(f"  Meta: {meta.group(1)}")
    except Exception as e:
        print(f"Error {name}:", e)
