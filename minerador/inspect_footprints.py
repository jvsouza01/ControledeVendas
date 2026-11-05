import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('c:/Users/jao_v/Desktop/ControledeVendas/minerador/discovered_footprints.json', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total footprint items: {len(data)}")
for item in data:
    print(f"[{item['query']}] {item['title'][:40]} -> {item['link']}")
