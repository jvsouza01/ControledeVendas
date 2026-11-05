import re
import json

path = r'c:\Users\jao_v\Desktop\ControledeVendas\src\data\initialLeads.ts'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

handles = set()
for match in re.finditer(r'["\']instagram["\']:\s*["\']([^"\']+)["\']', text):
    h = match.group(1).strip().lower().lstrip('@')
    handles.add(h)

print(f"Total existing handles: {len(handles)}")
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\existing_handles.json', 'w', encoding='utf-8') as f:
    json.dump(list(handles), f, ensure_ascii=False, indent=2)
print("Saved existing handles to existing_handles.json")
