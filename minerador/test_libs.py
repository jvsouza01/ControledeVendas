from duckduckgo_search import DDGS
from googlesearch import search
import json

print("Testing googlesearch-python...")
try:
    results = list(search('site:instagram.com "mentoria individual" "TJSP"', num_results=5, advanced=True))
    print(f"Google found {len(results)} results:")
    for r in results:
        print("Title:", r.title)
        print("URL:", r.url)
        print("Desc:", r.description)
except Exception as e:
    print("Google error:", e)

print("\nTesting duckduckgo_search...")
try:
    ddgs = DDGS()
    ddg_res = list(ddgs.text('site:instagram.com "mentoria individual" "TJSP"', max_results=5))
    print(f"DDG found {len(ddg_res)} results:")
    for r in ddg_res:
        print("Title:", r.get('title'))
        print("URL:", r.get('href'))
        print("Body:", r.get('body'))
except Exception as e:
    print("DDG error:", e)
