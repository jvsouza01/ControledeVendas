import requests
import re
import html
import json
import sys
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding='utf-8')

FB_UA = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'

with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\existing_handles.json', 'r', encoding='utf-8') as f:
    existing_handles = set(json.load(f))

candidates = [
    # Tribunais
    ("oficialdejusticatjsp", "Tribunais / Jurídica"),
    ("escreventedotj", "Tribunais / Jurídica"),
    ("escreventevunesp", "Tribunais / Jurídica"),
    ("tj.concursos", "Tribunais / Jurídica"),
    ("concursostribunais", "Tribunais / Jurídica"),
    ("analistajudiciario", "Tribunais / Jurídica"),
    ("tecnicojudiciario", "Tribunais / Jurídica"),
    ("concurseirotribunal", "Tribunais / Jurídica"),
    ("analistadotrt", "Tribunais / Jurídica"),
    ("oficialdejustica", "Tribunais / Jurídica"),
    ("tjmg_concurso", "Tribunais / Jurídica"),
    ("tjba_concurso", "Tribunais / Jurídica"),
    ("tjpe_concurso", "Tribunais / Jurídica"),
    ("tjdft_concurso", "Tribunais / Jurídica"),
    ("foconoescrevente", "Tribunais / Jurídica"),
    ("concursotribunais", "Tribunais / Jurídica"),
    
    # Saúde / Enfermagem
    ("enfermagemparaconcurso", "Saúde / Enfermagem"),
    ("enfermeirosconcurseiros", "Saúde / Enfermagem"),
    ("enfermagem.concursos", "Saúde / Enfermagem"),
    ("enfermagemconcursos", "Saúde / Enfermagem"),
    ("mentoriaebserh", "Saúde / Enfermagem"),
    ("ebserhconcurso", "Saúde / Enfermagem"),
    ("professoraenfermagem", "Saúde / Enfermagem"),
    ("prof.enfermagem", "Saúde / Enfermagem"),
    ("resumodeenfermagem", "Saúde / Enfermagem"),
    ("enfermeira.aprovada", "Saúde / Enfermagem"),
    ("enfermagemmentoria", "Saúde / Enfermagem"),
    ("ebserh2024", "Saúde / Enfermagem"),
    ("ebserh2025", "Saúde / Enfermagem"),
    
    # Pedagogia / Magistério
    ("professoraaprovada", "Pedagogia / Educação"),
    ("professoraprovado", "Pedagogia / Educação"),
    ("concursoprofessores", "Pedagogia / Educação"),
    ("pedagogia.concurseira", "Pedagogia / Educação"),
    ("pedagogiaconcurseira", "Pedagogia / Educação"),
    ("pedagogiaparaconcursospublicos", "Pedagogia / Educação"),
    ("pedagogianaveia", "Pedagogia / Educação"),
    ("concurseirapedagoga", "Pedagogia / Educação"),
    ("profconcursada", "Pedagogia / Educação"),
    ("profconcurseira", "Pedagogia / Educação"),
    ("pedagogiadaconcurseira", "Pedagogia / Educação"),
    ("prof.concurseira", "Pedagogia / Educação"),
    ("professorasconcurseiras", "Pedagogia / Educação"),
    ("professoresconcurso", "Pedagogia / Educação"),
    
    # Prefeituras / Adm
    ("concursoprefeitura", "Prefeituras / Adm"),
    ("prefeituraconcurso", "Prefeituras / Adm"),
    ("concursosprefeitura", "Prefeituras / Adm"),
    ("concursoprefeiturasp", "Prefeituras / Adm"),
    ("concursoprefeiturarj", "Prefeituras / Adm"),
    ("assistenteadministrativo", "Prefeituras / Adm"),
    ("concursosmunicipaisbr", "Prefeituras / Adm"),
    ("prefeiturasconcursos", "Prefeituras / Adm"),
    
    # Redação / Discursiva
    ("mentoriadiscursiva", "Redação / Isoladas"),
    ("discursivasparatribunais", "Redação / Isoladas"),
    ("redacaotribunal", "Redação / Isoladas"),
    ("portuguesparaconcursos", "Redação / Isoladas"),
    ("portuguesconcursos", "Redação / Isoladas"),
    ("rlmparaconcursos", "Redação / Isoladas"),
    ("exatasparaconcursos", "Redação / Isoladas"),
    
    # Fiscal / Controle
    ("carreirasfiscaisconcursos", "Fiscal / Controle"),
    ("auditorfiscaliss", "Fiscal / Controle"),
    ("mentoriaauditorfiscal", "Fiscal / Controle"),
    ("auditorfiscalreceita", "Fiscal / Controle"),
    ("sefazfiscal", "Fiscal / Controle"),
    ("concursoauditor", "Fiscal / Controle"),
    ("concursoiss", "Fiscal / Controle")
]

def parse_followers(meta_str):
    if not meta_str:
        return None
    m = re.search(r'([\d\.,]+)\s*(k|m|mil)?\s*seguidores', meta_str, re.IGNORECASE)
    if not m:
        return None
    num_str = m.group(1).strip()
    mult = m.group(2)
    try:
        if mult:
            num_clean = num_str.replace('.', '').replace(',', '.')
            val = float(num_clean)
            mult = mult.lower()
            if mult in ['k', 'mil']:
                val *= 1000
            elif mult == 'm':
                val *= 1000000
            return int(val)
        else:
            if ',' in num_str and len(num_str.split(',')[-1]) == 3:
                num_clean = num_str.replace(',', '')
            elif '.' in num_str and len(num_str.split('.')[-1]) == 3:
                num_clean = num_str.replace('.', '')
            else:
                num_clean = num_str.replace('.', '').replace(',', '')
            return int(num_clean)
    except Exception:
        return None

def check(item):
    handle, niche = item
    h = handle.lower().strip()
    if h in existing_handles:
        return None
    url = f"https://www.instagram.com/{h}/"
    try:
        r = requests.get(url, headers={'User-Agent': FB_UA, 'Accept-Language': 'pt-BR'}, timeout=5)
        if r.status_code != 200:
            return None
        title_m = re.search(r'<title>(.*?)</title>', r.text)
        title = html.unescape(title_m.group(1)) if title_m else ""
        meta_m = re.search(r'<meta [^>]*content="([^"]*(?:seguidor|follower)[^"]*)"', r.text, re.IGNORECASE)
        meta_str = html.unescape(meta_m.group(1)) if meta_m else ""
        
        followers = parse_followers(meta_str)
        if followers is not None and 300 <= followers <= 25000:
            name_m = re.search(r'^(.*?)\s*\(@', title)
            nome = name_m.group(1).strip() if name_m else title.split('•')[0].strip()
            if not nome or nome == "Instagram":
                nome = h.replace('_', ' ').replace('.', ' ').title()
            print(f"MATCH: @{h} ({followers} seg) [{niche}] - {nome}")
            return {
                "nome": nome,
                "instagram": h,
                "nicho": niche,
                "followers": followers,
                "meta": meta_str,
                "comoEncontrei": f"Micro-Mentor ({round(followers/1000, 1) if followers>=1000 else followers}k seg) • Instagram Verificado",
                "observacoes": f"👥 ~{followers:,} seguidores | Nicho: {niche}. Bio/Meta: {meta_str[:120]}",
                "prioridade": "alta"
            }
    except Exception:
        pass
    return None

matches = []
with ThreadPoolExecutor(max_workers=7) as executor:
    for res in executor.map(check, candidates):
        if res:
            matches.append(res)

print(f"\nFound {len(matches)} new verified micro-mentors in this batch!")
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\new_matches_3.json', 'w', encoding='utf-8') as f:
    json.dump(matches, f, ensure_ascii=False, indent=2)
