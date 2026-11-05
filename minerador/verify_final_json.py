import json

path = r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\lote_micro_policial.json'
with open(path, 'r', encoding='utf-8') as f:
    leads = json.load(f)

print(f"Total leads in file: {len(leads)}")
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\existing_handles.json', 'r', encoding='utf-8') as f:
    existing = set(json.load(f))

duplicates = [l['instagram'] for l in leads if l['instagram'] in existing]
print(f"Duplicates with initialLeads: {len(duplicates)}")

for i, l in enumerate(leads[:6]):
    print(f"[{i+1}] {l['nome']} (@{l['instagram']})")
    print(f"    Encontrei: {l['comoEncontrei']}")
    print(f"    Obs: {l['observacoes'][:100]}...")
