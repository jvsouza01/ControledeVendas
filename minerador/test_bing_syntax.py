import urllib.request, urllib.parse, re, base64

def check(q):
    url = f"https://www.bing.com/search?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    algos = re.findall(r'<li class="b_algo".*?</li>', html, re.DOTALL)
    print(f"Query: [{q}] -> algos: {len(algos)}")
    for a in algos[:2]:
        p = re.search(r'<p[^>]*>(.*?)</p>', a)
        if p:
            print("  Snippet:", re.sub(r'<[^>]+>', '', p.group(1))[:120])

check('site:instagram.com "conteudos.pmba"')
check('"instagram.com/conteudos.pmba"')
check('instagram "conteudos.pmba"')
