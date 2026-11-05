import urllib.request, urllib.parse, re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0'}

def check_query(q):
    url = 'https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode('utf-8', errors='ignore')
        # Find all result-link or result__url or uddg
        uddg_links = re.findall(r'href=["\']([^"\']*uddg=[^"\']*)["\']', html)
        print(f"Query: {q} | uddg links: {len(uddg_links)}")
        for l in uddg_links[:10]:
            if 'uddg=' in l:
                actual = urllib.parse.unquote(l.split('uddg=')[1].split('&')[0])
                print("  ->", actual)
    except Exception as e:
        print("Error:", e)

check_query('site:instagram.com "mentoria" PMBA')
check_query('site:instagram.com "mentoria" PMPE')
check_query('site:instagram.com "mentoria" PMPB')
check_query('site:instagram.com "mentoria" "polícia penal"')
check_query('site:instagram.com "mentoria" "gcm"')
