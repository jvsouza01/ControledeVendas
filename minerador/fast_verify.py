import json
import re
import requests
import html
import sys

sys.stdout.reconfigure(encoding='utf-8')

FB_UA = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'

with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\existing_handles.json', 'r', encoding='utf-8') as f:
    existing_handles = set(json.load(f))

# Let's collect candidates from all our scripts and tests
candidates = [
    # Already verified
    ("antoniodotribunal", "Tribunais / Jurídica", "Antonio do Tribunal", 3702, "Servidor TJSP, mentoria individual e cronograma focado na Vunesp"),
    ("matsueda.concursos", "Tribunais / Jurídica", "Lucas Matsueda", 14000, "Mentor de concursos públicos e tribunais, cronograma estratégico"),
    ("naprocuradoria", "Tribunais / Jurídica", "Nathalia Mariano", 15000, "Mentoria e acompanhamento individual para Procuradorias e Tribunais"),
    ("andrenascimentoconcursos", "Tribunais / Concursos", "André Nascimento", 7979, "Mentor de concursos públicos e tribunais, cronogramas e planejamento"),
    ("mentoriatrilhadaaprovacao", "Carreiras Administrativas / Concursos", "Trilha da Aprovação", 808, "Mentoria de estudos e acompanhamento personalizado para concursos"),
    ("mentedeconcurseiro_oficial", "Concursos / Geral", "Mente de Concurseiro", 5411, "Planejamento de estudos, cronogramas e mentoria para concursos públicos"),
    ("proffernandabarbosa", "Saúde / Enfermagem", "Fernanda Barbosa", 1347, "Professora e mentora de enfermagem para concursos e EBSERH"),
]

# Additional candidate handles to test right now
test_pool = [
    ("profadrianamenezes", "Concursos"), # wait, check if in existing_handles
    ("profguilhermeneves", "Exatas / RLM"),
    ("prof.elvinomagalhaes", "Tribunais"),
    ("elvino.magalhaes", "Tribunais"),
    ("coachconcursos", "Concursos"),
    ("mentoriaconcurso", "Concursos"),
    ("mentoriaparaconcursos", "Concursos"),
    ("cronosconcursos", "Concursos"),
    ("daniritter", "Saúde"),
    ("professorafl", "Pedagogia"),
    ("pedagogiaparaconcursos", "Pedagogia"),
    ("professoresconcursados", "Pedagogia"),
    ("mentoriaredacao", "Redação"),
    ("redacaonota1000concursos", "Redação"),
    ("profjhonatan", "Tribunais"),
    ("proftiagolobo", "Tribunais"),
    ("profrodrigosilva", "Tribunais"),
    ("profmarcosantonio", "Tribunais"),
    ("focanotrt", "Tribunais"),
    ("mentoriatrt", "Tribunais"),
    ("mentoriatjsp", "Tribunais"),
    ("profalexandre", "Fiscal"),
    ("auditorfiscalconcursos", "Fiscal"),
    ("mentoriafiscal", "Fiscal"),
    ("metododeaprovacao", "Concursos"),
    ("aprovadoemconcursos", "Concursos"),
    ("gabaritandoconcursos", "Concursos"),
    ("pedagogiaconcursos", "Pedagogia"),
    ("professoresconcursos", "Pedagogia"),
    ("enfermagemparaconcursos", "Saúde / Enfermagem"),
    ("enfconcursos", "Saúde / Enfermagem"),
    ("residenciaenfermagem", "Saúde / Enfermagem"),
    ("mentoriaebserh", "Saúde / Enfermagem"),
    ("ebserhconcursos", "Saúde / Enfermagem"),
    ("redacaoparaconcursos", "Redação"),
    ("discursivasconcursos", "Redação"),
    ("professordecioterror", "Português / Redação"),
    ("professoraadrianafigueiredo", "Português"),
    ("ricardobaronovsky", "Tribunais"),
    ("thalliusmoraes", "Tribunais"),
    ("brunoklippel", "Tribunais"),
    ("profbrunoklippel", "Tribunais")
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

results = []
seen = set()

# Add initial verified
for handle, nicho, nome, f_count, obs in candidates:
    if handle in existing_handles:
        continue
    seen.add(handle)
    results.append({
        "nome": nome,
        "instagram": handle,
        "nicho": nicho,
        "comoEncontrei": f"Micro-Mentor ({round(f_count/1000, 1) if f_count>=1000 else f_count}k seg) • Bio/Linktree",
        "observacoes": f"👥 ~{f_count:,} seguidores | {obs}",
        "prioridade": "alta"
    })

print(f"Starting verification of {len(test_pool)} candidates...")

for handle, niche in test_pool:
    h = handle.lower().strip()
    if h in seen or h in existing_handles:
        continue
    
    url = f"https://www.instagram.com/{h}/"
    try:
        r = requests.get(url, headers={'User-Agent': FB_UA, 'Accept-Language': 'pt-BR'}, timeout=6)
        if r.status_code != 200:
            continue
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
                
            print(f"VERIFIED: @{h} ({followers} seg) - {nome}")
            seen.add(h)
            results.append({
                "nome": nome,
                "instagram": h,
                "nicho": niche,
                "comoEncontrei": f"Micro-Mentor ({round(followers/1000, 1) if followers>=1000 else followers}k seg) • Instagram/Bio",
                "observacoes": f"👥 ~{followers:,} seguidores | Nicho: {niche}. Meta/Bio: {meta_str[:120]}",
                "prioridade": "alta"
            })
    except Exception as e:
        pass

print(f"\nTotal verified micro-mentors in results: {len(results)}")
