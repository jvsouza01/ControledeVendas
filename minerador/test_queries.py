from duckduckgo_search import DDGS
from googlesearch import search

test_queries = [
    'site:my.canva.site mentoria concurso',
    'site:linktr.ee mentoria concurso',
    'mentoria individual tjsp instagram',
    'mentoria concurso prefeitura instagram',
    'mentoria enfermagem concursos instagram'
]

ddgs = DDGS()
for q in test_queries:
    try:
        res = list(ddgs.text(q, max_results=3))
        print(f"DDG query: '{q}' -> {len(res)} results")
        for r in res[:2]:
            print("  Title:", r.get('title'))
            print("  URL:", r.get('href'))
            print("  Body:", r.get('body')[:120])
    except Exception as e:
        print(f"DDG query '{q}' error:", e)
