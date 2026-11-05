from duckduckgo_search import DDGS

queries = [
    'site:instagram.com mentoria PMBA',
    'site:instagram.com mentoria PMPE',
    'site:instagram.com mentoria PMPB',
    'site:instagram.com mentoria "polícia penal"',
    'site:instagram.com "mentoria" "gcm"',
    'site:instagram.com "mentoria individual" policial',
    'site:linktr.ee mentoria PMBA',
    'site:my.canva.site mentoria policial'
]

with DDGS() as ddgs:
    for q in queries:
        try:
            results = list(ddgs.text(q, max_results=5))
            print(f"=== Query: {q} ({len(results)} results) ===")
            for r in results:
                print("  URL:", r.get('href'))
                print("  Title:", r.get('title'))
                print("  Snippet:", r.get('body')[:100] if r.get('body') else '')
        except Exception as e:
            print(f"Error on {q}: {e}")
