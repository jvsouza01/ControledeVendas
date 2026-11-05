import json
import os

with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\existing_handles.json', 'r', encoding='utf-8') as f:
    existing_handles = set(json.load(f))

all_leads = {}

# 1. Base verified list
base_leads = [
    {
        "nome": "Antonio do Tribunal",
        "instagram": "antoniodotribunal",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Micro-Mentor (3.7k seg) • Linktree/Instagram",
        "observacoes": "👥 ~3,702 seguidores | Servidor do TJSP, oferece acompanhamento individual, cronogramas e materiais focados na Vunesp. Bio: Antonio do Tribunal (@antoniodotribunal)",
        "prioridade": "alta"
    },
    {
        "nome": "Lucas Matsueda",
        "instagram": "matsueda.concursos",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Micro-Mentor (14k seg) • Instagram/Bio",
        "observacoes": "👥 ~14,000 seguidores | Mentor de concursos e tribunais, oferece metodologia de estudo e cronograma estratégico individualizado.",
        "prioridade": "alta"
    },
    {
        "nome": "Nathalia Mariano",
        "instagram": "naprocuradoria",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Micro-Mentor (15k seg) • Instagram/Bio",
        "observacoes": "👥 ~15,000 seguidores | Mentoria e acompanhamento individual para Procuradorias e Tribunais. Metas personalizadas e simulados.",
        "prioridade": "alta"
    },
    {
        "nome": "Andre Nascimento",
        "instagram": "andrenascimentoconcursos",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Micro-Mentor (8k seg) • Canva Site/Instagram",
        "observacoes": "👥 ~7,979 seguidores | Mentor de concursos públicos e tribunais, landing page no Canva e atendimento individual.",
        "prioridade": "alta"
    },
    {
        "nome": "Trilha da Aprovação",
        "instagram": "mentoriatrilhadaaprovacao",
        "nicho": "Prefeituras / Adm",
        "comoEncontrei": "Micro-Mentor (800 seg) • Canva Site/WhatsApp",
        "observacoes": "👥 ~808 seguidores | Mentoria de estudos e acompanhamento personalizado para concursos administrativos e municipais.",
        "prioridade": "alta"
    },
    {
        "nome": "Mente de Concurseiro",
        "instagram": "mentedeconcurseiro_oficial",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Micro-Mentor (5.4k seg) • YouTube/Linktree",
        "observacoes": "👥 ~5,411 seguidores | Planejamento de estudos, cronogramas e mentoria prática para tribunais e concursos públicos.",
        "prioridade": "alta"
    },
    {
        "nome": "Fernanda Barbosa",
        "instagram": "proffernandabarbosa",
        "nicho": "Saúde / Enfermagem",
        "comoEncontrei": "Micro-Mentor (1.3k seg) • Instagram/Bio",
        "observacoes": "👥 ~1,347 seguidores | Professora e mentora de enfermagem para concursos e residências / EBSERH.",
        "prioridade": "alta"
    },
    {
        "nome": "Elvino Magalhães",
        "instagram": "elvino.magalhaes",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Micro-Mentor (4.3k seg) • Instagram/Bio",
        "observacoes": "👥 ~4,281 seguidores | Servidor público de tribunal, mentoria de rotina, produtividade e foco para tribunais.",
        "prioridade": "alta"
    },
    {
        "nome": "Jhonatan",
        "instagram": "profjhonatan",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Micro-Mentor (1k seg) • Instagram/Bio",
        "observacoes": "👥 ~1,046 seguidores | Professor e mentor focado em preparação para carreiras de apoio de tribunais.",
        "prioridade": "alta"
    },
    {
        "nome": "José Alexandre Vieira",
        "instagram": "profalexandre",
        "nicho": "Fiscal / Controle",
        "comoEncontrei": "Micro-Mentor (430 seg) • Instagram/Bio",
        "observacoes": "👥 ~437 seguidores | Professor e mentor para concursos fiscais e tributários.",
        "prioridade": "alta"
    }
]

for b in base_leads:
    h = b['instagram'].lower()
    if h not in existing_handles:
        all_leads[h] = b

# 2. Add from JSON files
files = [
    r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\new_matches.json',
    r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\new_matches_2.json',
    r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\new_matches_3.json'
]

for f_path in files:
    if os.path.exists(f_path):
        with open(f_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                h = item['instagram'].lower()
                if h not in existing_handles and h not in all_leads:
                    all_leads[h] = {
                        "nome": item['nome'],
                        "instagram": h,
                        "nicho": item['nicho'],
                        "comoEncontrei": item['comoEncontrei'],
                        "observacoes": item['observacoes'],
                        "prioridade": "alta"
                    }

print(f"Total compiled unique leads: {len(all_leads)}")
for h, l in all_leads.items():
    print(f"  @{h} - {l['nome']} [{l['nicho']}]")
