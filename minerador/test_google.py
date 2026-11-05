import urllib.request
import urllib.parse
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

def test_google(q):
    url = f"https://www.google.com/search?q={urllib.parse.quote(q)}&hl=pt-BR&num=20"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            print(f"Google: '{q}' -> HTML length: {len(html)}")
            # look for /url?q=
            urls = re.findall(r'/url\?q=([^&]+)', html)
            print("Direct url?q= matches:", len(urls))
            for u in urls[:10]:
                print(" ", urllib.parse.unquote(u))
            # Also look for href="https://www.instagram.com/..."
            ig_matches = re.findall(r'href="(https://www\.instagram\.com/[^"]+)"', html)
            print("Direct href instagram matches:", len(ig_matches))
            for ig in ig_matches[:5]:
                print("  IG:", ig)
    except Exception as e:
        print("Google error:", e)

test_google('site:instagram.com "mentoria" PMBA')
