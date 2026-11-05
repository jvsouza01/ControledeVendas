import sys
import io
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from duckduckgo_search import DDGS

queries = [
    'site:instagram.com "mentoria" PMBA',
    'site:instagram.com "mentoria" PMPE',
    'site:instagram.com "mentoria" PMPB',
    'site:instagram.com "mentoria" PMCE',
    'site:instagram.com "mentoria" PMMG',
    'site:instagram.com "mentoria" PMGO',
    'site:instagram.com "mentoria" PMPR',
    'site:instagram.com "mentoria" PMSC',
    'site:instagram.com "mentoria" PMPA',
    'site:instagram.com "mentoria" "polícia penal"',
    'site:instagram.com "mentoria" "gcm"',
    'site:instagram.com "mentoria" "guarda municipal"',
    'site:instagram.com "cronograma" "pmba"',
    'site:instagram.com "cronograma" "pmpe"',
    'site:linktr.ee mentoria "pmba"',
    'site:linktr.ee mentoria "pmpe"',
    'site:linktr.ee mentoria "policia penal"',
    'site:linktr.ee mentoria "gcm"',
    'site:my.canva.site "mentoria" policial',
    'site:my.canva.site "mentoria" "pm"'
]

with DDGS() as ddgs:
    for q in queries:
        try:
            results = list(ddgs.text(q, max_results=8))
            print(f"=== Query: {q} ({len(results)} results) ===")
            for r in results:
                print("  URL:", r.get('href'))
                print("  Title:", r.get('title'))
                print("  Snippet:", (r.get('body') or '')[:140])
        except Exception as e:
            print(f"Error on {q}: {e}")
