import urllib.request
import re
import json
import time
import sys
import html as html_lib

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\existing_handles.json', 'r', encoding='utf-8') as f:
    existing_handles = set(json.load(f))

with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\verified_police_micro.json', 'r', encoding='utf-8') as f:
    already_verified = {x['handle']: x for x in json.load(f)}

googlebot_headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

new_batch = [
    ("marcosleandro856", "Marcos Leandro | Mentoria Musashi", "Linktree/WhatsApp", "Mentoria Musashi para carreiras policiais"),
    ("robson.ferreira_oficial", "Prof. Robson Ferreira", "Instagram/Reels", "Mentoria para Carreiras Policiais e PMPE"),
    ("verto.mentoria", "Verto Mentoria", "Instagram/Reels", "Mentoria especializada em PMPE e concursos policiais"),
    ("tenentebmsamuel", "Tenente Samuel", "Instagram/Reels", "Oficial e mentor para PMPE e CBMPE"),
    ("junior.aguia41", "Prof. Maurício Junior | Águia 41", "Instagram/Reels", "Mentoria Águia 41 para PMPE e Carreiras Policiais"),
    ("vitorbarbozamsp", "Vitor Barboza | MSP", "Instagram/Reels", "Mentoria Carreiras Policiais e PMGO"),
    ("prof.gilbertosoares", "Prof. Gilberto Soares", "Instagram/Reels", "Mentoria para CFO e Soldado PMSC"),
    ("objetivo01mentoria", "Objetivo 01 Mentoria", "Instagram/Reels", "Mentoria Concursos Policiais PMSC"),
    ("qgmentoria", "QG Mentoria", "Instagram/Reels", "Mentoria tática para PMSC e carreiras policiais"),
    ("mentoriaemconcursos", "Fernando Descovi | Mentoria", "Instagram/Reels", "Mentoria em Concursos Policiais PMSC"),
    ("operacaopernambuco", "Rafael Rocha | Operação PE", "Instagram Outbound", "Mentoria e planejamento para PMPE"),
    ("mentoriatatica", "Mentoria Tática", "Linktree Outbound", "Mentoria Carreira Policial"),
    ("wagalvarenga", "Wagner Alvarenga", "Linktree Outbound", "Mentoria Soldado e Oficial PMMG"),
    ("andrezacaetanomentoria", "Andreza Caetano", "Linktree Outbound", "Mentoria para carreiras policiais"),
    ("paidoconcurso", "Pai do Concurso", "Linktree Outbound", "Mentoria e cronogramas para Polícia Penal e PPGO"),
    ("mentoriacarreiraspoliciais", "Daniel Leal | Mentoria Policial", "Linktree Outbound", "Mentoria Carreiras Policiais")
]

def parse_follower_count(text):
    if not text:
        return None
    m = re.search(r'([0-9.,]+)\s*([KkMm]|mil|million)?\s*(?:Followers|Seguidores)', text, re.I)
    if not m:
        return None
    num_str = m.group(1).replace(',', '')
    mult = m.group(2)
    try:
        val = float(num_str)
        if mult:
            mult = mult.lower()
            if mult in ('k', 'mil'):
                val *= 1000
            elif mult in ('m', 'million'):
                val *= 1000000
        return int(val)
    except:
        return None

fresh_verified = []

for h, name, source, obs in new_batch:
    h = h.lower()
    if h in existing_handles:
        print(f"Skipping @{h} (in initialLeads)")
        continue
    if h in already_verified:
        print(f"Skipping @{h} (already verified)")
        continue
    
    url = f"https://www.instagram.com/{h}/"
    req = urllib.request.Request(url, headers=googlebot_headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            meta_desc = re.search(r'<meta (?:property="og:description"|name="description") content="([^"]+)"', content)
            raw_desc = html_lib.unescape(meta_desc.group(1)) if meta_desc else ""
            f_count = parse_follower_count(raw_desc)
            if f_count is not None:
                if 100 <= f_count <= 25000:
                    print(f"✅ VERIFIED MICRO: @{h} | {f_count} followers | {name}")
                    fresh_verified.append({
                        'handle': h,
                        'name': name,
                        'followers': f_count,
                        'comoEncontrei': f"Micro-Mentor ({f_count:,} seg) • {source}".replace(',', '.'),
                        'observacoes': f"👥 ~{f_count:,} seguidores | {obs}. Meta: {raw_desc[:100]}".replace(',', '.'),
                        'prioridade': 'alta'
                    })
                else:
                    print(f"❌ Size check failed @{h}: {f_count}")
            else:
                title_m = re.search(r'<title>(.*?)</title>', content)
                t = title_m.group(1) if title_m else ""
                print(f"⚠️ No count @{h}: {t}")
    except Exception as e:
        print(f"Err @{h}: {e}")
    time.sleep(0.4)

print(f"\nFresh verified: {len(fresh_verified)}")
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\fresh_verified.json', 'w', encoding='utf-8') as f:
    json.dump(fresh_verified, f, ensure_ascii=False, indent=2)
