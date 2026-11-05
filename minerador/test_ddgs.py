from duckduckgo_search import DDGS
import json

try:
    with DDGS() as ddgs:
        results = list(ddgs.text('site:instagram.com "mentoria" ("PMBA" OR "PMPE")', max_results=10))
        print("Results count:", len(results))
        for r in results:
            print("Title:", r.get('title'))
            print("Href:", r.get('href'))
            print("Body:", r.get('body'))
            print("-" * 40)
except Exception as e:
    print("DDGS Error:", e)
