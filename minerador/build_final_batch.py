import json
import re

# 1. Load initialLeads handles to guarantee zero duplication
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\existing_handles.json', 'r', encoding='utf-8') as f:
    existing_handles = set(json.load(f))

# 2. Load batch 1 (verified_police_micro.json)
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\verified_police_micro.json', 'r', encoding='utf-8') as f:
    batch1 = json.load(f)

# 3. Load batch 2 (fresh_verified.json)
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\fresh_verified.json', 'r', encoding='utf-8') as f:
    batch2 = json.load(f)

# 4. Load catalog additions (verified_catalog_batch.json)
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\verified_catalog_batch.json', 'r', encoding='utf-8') as f:
    batch3 = json.load(f)

# Rich metadata mapping for each handle
police_metadata = {
    "allanm4rtins": {
        "nome": "Allan Martins | Carreiras Policiais",
        "foco": "PMPB, PMPE e Carreiras Policiais",
        "comoEncontrei": "Micro-Mentor (17k seg) • YouTube/Linktree",
        "bio": "Mentor independente focado em Soldado PMPB e PMPE. Vende cronogramas e mentoria com metas semanais."
    },
    "augusttolca": {
        "nome": "Sd Augusto | Mentoria R.O.T.A.",
        "foco": "PMESP e PMMG",
        "comoEncontrei": "Micro-Mentor (4.3k seg) • YouTube/WhatsApp",
        "bio": "Policial Militar atuante que oferece mentoria estratégica R.O.T.A. com acompanhamento individual de metas."
    },
    "canal.maykonsalvador": {
        "nome": "Maykon Salvador | MS Concursos",
        "foco": "GCM e Carreiras Policiais",
        "comoEncontrei": "Micro-Mentor (6.1k seg) • YouTube/Kiwify",
        "bio": "Especialista em concursos de Guardas Civis Municipais (GCMs) e polícias locais. Vende cronogramas na Kiwify."
    },
    "conteudos.pmba": {
        "nome": "Conteúdos PMBA | Mentoria",
        "foco": "PMBA e Bombeiros BA",
        "comoEncontrei": "Micro-Mentor (2.8k seg) • Instagram/WhatsApp",
        "bio": "Perfil tático regional com cronogramas e mentoria de questões e lei seca para Soldado PMBA."
    },
    "cppconcursos": {
        "nome": "CPP Concursos | Carreiras Policiais",
        "foco": "Polícia Militar e Penal",
        "comoEncontrei": "Micro-Mentor (18k seg) • YouTube/Hotmart",
        "bio": "Preparatório e mentoria direcionada para editais policiais e bombeiros militares."
    },
    "davidlucasods": {
        "nome": "David Lucas Santos | Mentoria PMSC",
        "foco": "PMSC e PMPR",
        "comoEncontrei": "Micro-Mentor (345 seg) • YouTube/Instagram",
        "bio": "Mentor individual para concursos policiais do Sul (PMSC/PMPR), focando em planejamento de estudos."
    },
    "delegadoguilhermegomes": {
        "nome": "Delegado Guilherme Gomes | Mentoria",
        "foco": "Polícia Civil e Carreiras Policiais",
        "comoEncontrei": "Micro-Mentor (3.2k seg) • Linktree/Instagram",
        "bio": "Delegado de Polícia Civil e mentor. Acompanha alunos em turmas reduzidas com ciclos de estudo e discursivas."
    },
    "ferreira_34ba": {
        "nome": "Ferreira Mentoria | PM e PCBA",
        "foco": "PMBA e PCBA",
        "comoEncontrei": "Micro-Mentor (20k seg) • Instagram/Linktree",
        "bio": "Soldado da PMBA com mentoria individual e curso de questões específico para o concurso da PM Bahia."
    },
    "gkconcursosyt": {
        "nome": "GK Concursos | GCM e Policial",
        "foco": "GCM e Guardas Municipais",
        "comoEncontrei": "Micro-Mentor (3.7k seg) • YouTube/Linktree",
        "bio": "Canal e mentoria focada em concursos de Guardas Municipais e Prefeituras em todo o Brasil."
    },
    "inspetormarcelosilva": {
        "nome": "Inspetor Marcelo Silva | GCM Brasil",
        "foco": "Guarda Civil Municipal (GCM)",
        "comoEncontrei": "Micro-Mentor (5.6k seg) • YouTube/WhatsApp",
        "bio": "Inspetor de Guarda Municipal com mentoria e legislação aplicada para concursos de GCM municipais."
    },
    "maismilitar": {
        "nome": "Mais Militar | Preparatório",
        "foco": "PMPR, PMSC e Militares",
        "comoEncontrei": "Micro-Mentor (14k seg) • YouTube/Hotmart",
        "bio": "Mentoria e planejamento estratégico para concursos policiais militares do Paraná e Santa Catarina."
    },
    "mentoria.barbosa": {
        "nome": "Mentoria Barbosa | PMBA",
        "foco": "PMBA e Soldado",
        "comoEncontrei": "Micro-Mentor (154 seg) • Instagram/Direct",
        "bio": "Mentor individual de nicho fechado para Soldado da Polícia Militar da Bahia (PMBA)."
    },
    "netocapaverde": {
        "nome": "Capaverde | Mentor Policial Militar",
        "foco": "Polícia Militar e Carreiras de Segurança",
        "comoEncontrei": "Micro-Mentor (11k seg) • YouTube/Linktree",
        "bio": "Mentor tático independente que ensina rotina e organização de ciclo de estudos para concursos policiais."
    },
    "objetivopolicial47": {
        "nome": "Objetivo Policial | Carreiras Policiais",
        "foco": "PMBA, PMPE e Carreiras Policiais",
        "comoEncontrei": "Micro-Mentor (15k seg) • YouTube/WhatsApp",
        "bio": "Mentoria e simulados focados em editais de polícias militares do Nordeste."
    },
    "operacao01.jvn": {
        "nome": "João Víctor Nóbrega | Operação 01",
        "foco": "Polícia Penal, PC e PM",
        "comoEncontrei": "Micro-Mentor (11k seg) • YouTube/Kiwify",
        "bio": "Mentor independente para carreiras policiais e Polícia Penal (PPCE/PPRN). Vende acompanhamento na Kiwify."
    },
    "paty_curcelli": {
        "nome": "Patricia Curcelli | Preparação e TAF",
        "foco": "PMESP, PMMG e Policiais",
        "comoEncontrei": "Micro-Mentor (23k seg) • Instagram/Linktree",
        "bio": "Especialista em preparação física (TAF) e orientação de rotina para concurseiros da PMESP e policiais."
    },
    "portalconcursos": {
        "nome": "Portal Concursos | GCM e PM",
        "foco": "GCM e Polícia Militar",
        "comoEncontrei": "Micro-Mentor (6.4k seg) • YouTube/Hotmart",
        "bio": "Mentoria regional e simulados focados em Guardas Civis Municipais e Soldado da PM."
    },
    "prof.edinaelsantos": {
        "nome": "Edinael Santos | Concursos Policiais e GCM",
        "foco": "GCM e Polícia Científica",
        "comoEncontrei": "Micro-Mentor (16k seg) • YouTube/WhatsApp",
        "bio": "Professor e mentor especialista em legislação e preparação para GCMs e órgãos policiais estaduais."
    },
    "projeto8020": {
        "nome": "Projeto 80/20 | Mentoria Policial",
        "foco": "PMPR e PMSC",
        "comoEncontrei": "Micro-Mentor (760 seg) • YouTube/Linktree",
        "bio": "Mentoria focada no princípio de Pareto (80/20) para aprovação rápida em polícias militares."
    },
    "resumeai.raphael": {
        "nome": "Raphael Nonato | Resume Aí",
        "foco": "PMPE e PMPB",
        "comoEncontrei": "Micro-Mentor (1.6k seg) • YouTube/Kiwify",
        "bio": "Mentor e professor de História/Geografia regional com cronogramas direcionados para PMPE e PMPB."
    },
    "resumod0concurseiro": {
        "nome": "Bruno Cordeiro | Resumo do Concurseiro",
        "foco": "Polícia Penal, PM e GCM",
        "comoEncontrei": "Micro-Mentor (23k seg) • YouTube/Linktree",
        "bio": "Mentor independente que comercializa resumos e cronogramas práticos para carreiras policiais e GCM."
    },
    "teotonioneto.of": {
        "nome": "Teotônio Neto | Mentoria Policial",
        "foco": "PM e Carreiras Policiais",
        "comoEncontrei": "Micro-Mentor (15k seg) • YouTube/WhatsApp",
        "bio": "Mentor independente com turmas pequenas para concursos policiais e orientação individual."
    },
    "thiag_valentim": {
        "nome": "Thiago Valentim | Mentor Concursos",
        "foco": "PM e Carreiras Policiais",
        "comoEncontrei": "Micro-Mentor (1.3k seg) • YouTube/Instagram",
        "bio": "Aprovado em concursos policiais que auxilia concurseiros na montagem do plano de estudos individual."
    },
    "vagner_mariano": {
        "nome": "Vagner Mariano | Tribo Concursos",
        "foco": "Polícia Penal e Carreiras Policiais",
        "comoEncontrei": "Micro-Mentor (1.5k seg) • YouTube/WhatsApp",
        "bio": "Mentor e fundador da Tribo Concursos, focado em editais de Polícia Penal e polícias militares."
    },
    "venanciopapiro": {
        "nome": "Venancio Papiro | Concursos Policiais",
        "foco": "PMPE e Carreiras Policiais",
        "comoEncontrei": "Micro-Mentor (9.4k seg) • YouTube/Instagram",
        "bio": "Policial militar e mentor com cronogramas e acompanhamento de rotina para concurseiros da PMPE."
    },
    "wesley.pascelli": {
        "nome": "Wesley Pascelli | Carioca na PMESP",
        "foco": "Soldado PMESP",
        "comoEncontrei": "Micro-Mentor (7.4k seg) • YouTube/Linktree",
        "bio": "Soldado PMESP com mentoria 'Carioca na PMESP' ensinando o passo a passo para aprovação na Vunesp."
    },
    "william.concursos": {
        "nome": "William Edney | Concursos Públicos",
        "foco": "PMMG e PMESP",
        "comoEncontrei": "Micro-Mentor (1.7k seg) • YouTube/Linktree",
        "bio": "Mentor de ciclo de estudos e planejamento individual para concursos militares de MG e SP."
    },
    "robson.ferreira_oficial": {
        "nome": "Prof. Robson Ferreira | Mentoria Policial",
        "foco": "PMPE, PCPE e Carreiras Policiais",
        "comoEncontrei": "Micro-Mentor (21k seg) • Instagram/Reels",
        "bio": "Professor e mentor policial com acompanhamento focado em reta final e editais de Pernambuco."
    },
    "verto.mentoria": {
        "nome": "Verto Mentoria | Concursos Policiais",
        "foco": "PMPE e Polícias Militares",
        "comoEncontrei": "Micro-Mentor (1.7k seg) • Instagram/Linktree",
        "bio": "Mentoria especializada em PMPE com planejamento verticalizado e metas de simulados."
    },
    "tenentebmsamuel": {
        "nome": "Tenente Samuel | Mentoria Militar",
        "foco": "PMPE, CBMPE e Militares",
        "comoEncontrei": "Micro-Mentor (10k seg) • Instagram/WhatsApp",
        "bio": "Oficial militar que orienta candidatos com cronogramas e mentoria para oficiais e soldados."
    },
    "junior.aguia41": {
        "nome": "Prof. Maurício Junior | Mentoria Águia 41",
        "foco": "PMPE e Carreiras Policiais",
        "comoEncontrei": "Micro-Mentor (24k seg) • Instagram/Reels",
        "bio": "Coordenador da Mentoria Águia 41 focada exclusivamente em Soldado PMPE e bombeiros."
    },
    "vitorbarbozamsp": {
        "nome": "Vitor Barboza | Mentoria Policial",
        "foco": "PMGO e Carreiras Policiais",
        "comoEncontrei": "Micro-Mentor (5.9k seg) • Instagram/Linktree",
        "bio": "Mentor de estudos táticos para PMGO e polícias do Centro-Oeste, ensinando organização de matérias."
    },
    "prof.gilbertosoares": {
        "nome": "Prof. Gilberto Soares | Mentoria PMSC",
        "foco": "Soldado e Oficial PMSC",
        "comoEncontrei": "Micro-Mentor (13k seg) • Instagram/Linktree",
        "bio": "Professor e mentor focado em editais da Polícia Militar de Santa Catarina (PMSC)."
    },
    "objetivo01mentoria": {
        "nome": "Objetivo 01 | Mentoria Policial",
        "foco": "PMSC e Carreiras Policiais",
        "comoEncontrei": "Micro-Mentor (3.0k seg) • Instagram/Reels",
        "bio": "Mentoria com acompanhamento semanal para concursos de segurança pública e bombeiros em SC."
    },
    "qgmentoria": {
        "nome": "QG Mentoria | Concursos Policiais",
        "foco": "PMSC, PMPR e Policiais",
        "comoEncontrei": "Micro-Mentor (4.5k seg) • Instagram/Linktree",
        "bio": "Mentoria estratégica e ciclo de estudos para aprovação na PMSC e polícias estaduais."
    },
    "mentoriaemconcursos": {
        "nome": "Fernando Descovi | Mentoria em Concursos",
        "foco": "PMSC e Carreiras Policiais",
        "comoEncontrei": "Micro-Mentor (3.3k seg) • Instagram/Linktree",
        "bio": "Mentor independente para carreiras policiais com acompanhamento de metas diárias."
    },
    "operacaopernambuco": {
        "nome": "Rafael Rocha | Operação Pernambuco",
        "foco": "PMPE e PCPE",
        "comoEncontrei": "Micro-Mentor (727 seg) • Instagram/Direct",
        "bio": "Projeto regional de mentoria e acompanhamento individual para Soldado PMPE."
    },
    "andrezacaetanomentoria": {
        "nome": "Andreza Caetano | Mentoria Policial",
        "foco": "Carreiras Policiais e Segurança",
        "comoEncontrei": "Micro-Mentor (3.7k seg) • Linktree/Instagram",
        "bio": "Mentora individual de planejamento e rotina para concursos policiais."
    },
    "mentor.policial": {
        "nome": "Mentor Policial | Carreiras Policiais",
        "foco": "PM, PC e Polícia Penal",
        "comoEncontrei": "Micro-Mentor (961 seg) • Instagram/Direct",
        "bio": "Acompanhamento individualizado e ciclo de estudos para candidatos a carreiras policiais."
    },
    "foco.gcm": {
        "nome": "Foco GCM | Guarda Civil Municipal",
        "foco": "Guarda Municipal e Segurança Urbana",
        "comoEncontrei": "Micro-Mentor (291 seg) • Instagram/Direct",
        "bio": "Mentoria de nicho específica para Guardas Civis Municipais com cadernos de leis municipais."
    }
}

seen_handles = set()
final_leads = []

# Merge all sources
all_raw = batch1 + batch2 + batch3

for item in all_raw:
    h = item['handle'].strip().lower().lstrip('@').rstrip('.,_/')
    if h in seen_handles or h in existing_handles:
        continue
    
    followers = item.get('followers')
    if followers is None or followers < 100 or followers > 25000:
        continue
    
    meta = police_metadata.get(h)
    if meta:
        nome = meta['nome']
        comoEncontrei = meta['comoEncontrei']
        obs = f"👥 ~{followers:,} seguidores | Foco: {meta['foco']}. {meta['bio']}".replace(',', '.')
    else:
        clean_name = item.get('name', f"Mentor @{h}")
        nome = clean_name
        comoEncontrei = f"Micro-Mentor ({followers:,} seg) • Instagram".replace(',', '.')
        obs = f"👥 ~{followers:,} seguidores | Mentor independente de Carreiras Policiais. Bio: {item.get('raw_desc', '')[:120]}".replace(',', '.')

    seen_handles.add(h)
    final_leads.append({
        "nome": nome,
        "instagram": h,
        "nicho": "Carreiras Policiais",
        "comoEncontrei": comoEncontrei,
        "observacoes": obs,
        "prioridade": "alta"
    })

print(f"Total verified micro-mentors compiled: {len(final_leads)}")

# Sort by followers count roughly or by name
output_path = r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\lote_micro_policial.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(final_leads, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(final_leads)} micro-mentors to {output_path}!")
