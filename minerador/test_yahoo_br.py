import urllib.request
import urllib.parse
import re
import html as html_lib

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

queries = [
    'site:instagram.com "mentoria" "PMPE"',
    'site:instagram.com "mentoria" "PMPB"',
    'site:instagram.com "mentoria" "PMCE"',
    'site:instagram.com "mentoria" "PMBA"',
    'site:instagram.com "mentoria" "PMPA"',
    'site:instagram.com "mentoria" "PMGO"',
    'site:instagram.com "mentoria" "PMPR"',
    'site:instagram.com "mentoria" "PMMG"',
    'site:instagram.com "mentoria" "PMSC"',
    'site:instagram.com "mentoria" "polícia penal"',
    'site:instagram.com "mentoria" "gcm"',
    'site:instagram.com "mentoria" "guarda municipal"',
    'site:linktr.ee "mentoria" "pmpe"',
    'site:linktr.ee "mentoria" "pmba"',
    'site:linktr.ee "mentoria" "gcm"',
    'site:linktr.ee "mentoria" "policia penal"',
    'site:my.canva.site "mentoria" "policial"',
    'site:beacons.ai "mentoria" "policial"'
]

for q in queries:
    url = f"https://br.search.yahoo.com/search?p={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            content = r.read().decode('utf-8', errors='ignore')
            # Extract links
            links = re.findall(r'href="([^"]+)"', content)
            matched = set()
            for l in links:
                # Yahoo redirects like RU=...
                if 'RU=' in l:
                    m = re.search(r'RU=([^/&]+)', l)
                    if m:
                        dec = urllib.parse.unquote(m.group(1))
                        matched.add(dec)
                elif any(dom in l for dom in ['instagram.com', 'linktr.ee', 'canva.site', 'beacons.ai']):
                    matched.add(l)
            # filter
            valid = [x for x in matched if any(d in x for d in ['instagram.com', 'linktr.ee', 'canva.site', 'beacons.ai'])]
            print(f"[{q}] -> {len(valid)} matches: {valid[:3]}")
    except Exception as e:
        print(f"Error {q}: {e}")
