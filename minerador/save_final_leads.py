import json
import re
import html
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\existing_handles.json', 'r', encoding='utf-8') as f:
    existing_handles = set(h.lower().strip() for h in json.load(f))

# All verified leads
raw_leads = [
    # 1. Tribunais / Jurídica
    {
        "nome": "Antonio do Tribunal",
        "instagram": "antoniodotribunal",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 3702,
        "comoEncontrei": "Micro-Mentor (3.7k seg) • Linktree/Instagram",
        "observacoes": "👥 ~3,702 seguidores | Servidor do TJSP, oferece acompanhamento individual, cronogramas e materiais focados na banca Vunesp para escrevente e oficial."
    },
    {
        "nome": "Lucas Matsueda",
        "instagram": "matsueda.concursos",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 14000,
        "comoEncontrei": "Micro-Mentor (14k seg) • Instagram/Bio",
        "observacoes": "👥 ~14,000 seguidores | Mentor de concursos e tribunais, metodologia de planejamento e cronograma estratégico individualizado."
    },
    {
        "nome": "Nathalia Mariano",
        "instagram": "naprocuradoria",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 15000,
        "comoEncontrei": "Micro-Mentor (15k seg) • Instagram/Bio",
        "observacoes": "👥 ~15,000 seguidores | Mentoria e acompanhamento individual para Procuradorias e Tribunais. Metas personalizadas e simulados."
    },
    {
        "nome": "Andre Nascimento",
        "instagram": "andrenascimentoconcursos",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 7979,
        "comoEncontrei": "Micro-Mentor (8k seg) • Canva Site/WhatsApp",
        "observacoes": "👥 ~7,979 seguidores | Mentor de concursos públicos e tribunais, landing page própria no Canva e cronograma de metas diárias."
    },
    {
        "nome": "Elvino Magalhães",
        "instagram": "elvino.magalhaes",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 4281,
        "comoEncontrei": "Micro-Mentor (4.3k seg) • Instagram/Bio",
        "observacoes": "👥 ~4,281 seguidores | Servidor público de tribunal, mentoria de rotina, produtividade, foco e planejamento estratégico para tribunais."
    },
    {
        "nome": "Jhonatan",
        "instagram": "profjhonatan",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 1046,
        "comoEncontrei": "Micro-Mentor (1k seg) • Instagram/Bio",
        "observacoes": "👥 ~1,046 seguidores | Professor e mentor focado em preparação para carreiras judiciárias e tribunais estaduais/federais."
    },
    {
        "nome": "Mente de Concurseiro",
        "instagram": "mentedeconcurseiro_oficial",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 5411,
        "comoEncontrei": "Micro-Mentor (5.4k seg) • YouTube/Linktree",
        "observacoes": "👥 ~5,411 seguidores | Planejamento de estudos, cronogramas e mentoria prática para tribunais e carreiras de apoio."
    },
    {
        "nome": "Foco no TJSP",
        "instagram": "foconotjsp",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 374,
        "comoEncontrei": "Micro-Mentor (370 seg) • Instagram Verificado",
        "observacoes": "👥 ~374 seguidores | Perfil nichado em preparação estratégica e cronograma de reta final para Escrevente Técnico Judiciário do TJSP."
    },
    {
        "nome": "Escrevente TJSP",
        "instagram": "escreventetjsp",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 2373,
        "comoEncontrei": "Micro-Mentor (2.4k seg) • Instagram Verificado",
        "observacoes": "👥 ~2,373 seguidores | Especialista em Escrevente TJSP, oferece rotina de estudos, lei seca esquematizada e acompanhamento de simulados."
    },
    {
        "nome": "Luiz Carlos",
        "instagram": "profluizcarlos",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 2402,
        "comoEncontrei": "Micro-Mentor (2.4k seg) • Instagram Verificado",
        "observacoes": "👥 ~2,402 seguidores | Professor e mentor para carreiras jurídicas e de tribunais, cronogramas por ciclos e mentoria individual."
    },
    {
        "nome": "Concurso TJMG",
        "instagram": "concursotjmg",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 5300,
        "comoEncontrei": "Micro-Mentor (5.3k seg) • Instagram Verificado",
        "observacoes": "👥 ~5,300 seguidores | Mentor e materiais focados no Tribunal de Justiça de Minas Gerais (TJMG Oficial e Analista), cronogramas e acompanhamento."
    },
    {
        "nome": "Tribunais Concursos",
        "instagram": "tribunaisconcursos",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 757,
        "comoEncontrei": "Micro-Mentor (760 seg) • Instagram Verificado",
        "observacoes": "👥 ~757 seguidores | Orientação para concursos de tribunais de justiça e regionais (TRT, TRE, TJ), planejamento de ciclos."
    },
    {
        "nome": "Oficial de Justiça Brasil",
        "instagram": "oficialdejustica",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 1715,
        "comoEncontrei": "Micro-Mentor (1.7k seg) • Instagram Verificado",
        "observacoes": "👥 ~1,715 seguidores | Focado na carreira de Oficial de Justiça (TJSP, TRT, Federais), cronogramas e mentoria prática de prova."
    },
    {
        "nome": "Mentoria para Tribunais",
        "instagram": "mentoriaparatribunais",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 5388,
        "comoEncontrei": "Micro-Mentor (5.4k seg) • Instagram Verificado",
        "observacoes": "👥 ~5,388 seguidores | Programa de mentoria dedicado para concursos do Judiciário (TJs, TRFs e TRTs), acompanhamento de metas."
    },
    {
        "nome": "Hamad Mentoria",
        "instagram": "h3w",
        "nicho": "Tribunais / Jurídica",
        "seguidores": 994,
        "comoEncontrei": "Micro-Mentor (1k seg) • YouTube/Instagram",
        "observacoes": "👥 ~994 seguidores | Criador e mentor de concursos públicos, orientações práticas de organização de estudo e rotina de aprovação."
    },

    # 2. Saúde / Enfermagem
    {
        "nome": "Fernanda Barbosa",
        "instagram": "proffernandabarbosa",
        "nicho": "Saúde / Enfermagem",
        "seguidores": 1347,
        "comoEncontrei": "Micro-Mentor (1.3k seg) • Instagram/Bio",
        "observacoes": "👥 ~1,347 seguidores | Professora e mentora de enfermagem para concursos e residências / EBSERH, cronogramas e mapas mentais."
    },
    {
        "nome": "Enf. Concurseira",
        "instagram": "enf.concurseira",
        "nicho": "Saúde / Enfermagem",
        "seguidores": 1211,
        "comoEncontrei": "Micro-Mentor (1.2k seg) • Instagram Verificado",
        "observacoes": "👥 ~1,211 seguidores | Enfermeira aprovada, compartilha rotina, cronogramas de estudo para EBSERH e mentorias de enfermagem."
    },
    {
        "nome": "Enfermeiro Concurseiro",
        "instagram": "enfermeiroconcurseiro",
        "nicho": "Saúde / Enfermagem",
        "seguidores": 837,
        "comoEncontrei": "Micro-Mentor (840 seg) • Instagram Verificado",
        "observacoes": "👥 ~837 seguidores | Acompanhamento e direcionamento focado em concursos públicos da área da saúde e enfermagem hospitalar."
    },
    {
        "nome": "Mentoria Enfermagem",
        "instagram": "mentoriaenfermagem",
        "nicho": "Saúde / Enfermagem",
        "seguidores": 1922,
        "comoEncontrei": "Micro-Mentor (1.9k seg) • Instagram Verificado",
        "observacoes": "👥 ~1,922 seguidores | Programa de mentoria especializada para enfermeiros que buscam aprovação na EBSERH e prefeituras."
    },
    {
        "nome": "Concurso de Enfermagem",
        "instagram": "concursoenfermagem",
        "nicho": "Saúde / Enfermagem",
        "seguidores": 310,
        "comoEncontrei": "Micro-Mentor (310 seg) • Instagram Verificado",
        "observacoes": "👥 ~310 seguidores | Curso e mentoria preparatória para técnicos e enfermeiros concursados, planejamento de metas."
    },
    {
        "nome": "Enfermeiros Concurseiros",
        "instagram": "enfermeirosconcurseiros",
        "nicho": "Saúde / Enfermagem",
        "seguidores": 550,
        "comoEncontrei": "Micro-Mentor (550 seg) • Instagram Verificado",
        "observacoes": "👥 ~550 seguidores | Comunidade e acompanhamento para concurseiros da enfermagem, resumos de legislação do SUS e mentoria."
    },
    {
        "nome": "EBSERH Concurso",
        "instagram": "ebserhconcurso",
        "nicho": "Saúde / Enfermagem",
        "seguidores": 2242,
        "comoEncontrei": "Micro-Mentor (2.2k seg) • Instagram Verificado",
        "observacoes": "👥 ~2,242 seguidores | Focado na aprovação na rede EBSERH, cronogramas intensivos pós-edital e cadernos de questões IBFC/FGV."
    },
    {
        "nome": "Resumo de Enfermagem",
        "instagram": "resumodeenfermagem",
        "nicho": "Saúde / Enfermagem",
        "seguidores": 420,
        "comoEncontrei": "Micro-Mentor (420 seg) • Instagram Verificado",
        "observacoes": "👥 ~420 seguidores | Materiais esquematizados, flashcards e mentoria de fixação de conteúdos para área de saúde pública."
    },
    {
        "nome": "Concurso EBSERH Reta Final",
        "instagram": "ebserh2024",
        "nicho": "Saúde / Enfermagem",
        "seguidores": 925,
        "comoEncontrei": "Micro-Mentor (920 seg) • Instagram Verificado",
        "observacoes": "👥 ~925 seguidores | Preparação e cronograma acelerado para concursos da EBSERH, legislação aplicada e planos de tiro."
    },

    # 3. Pedagogia / Magistério
    {
        "nome": "Professor Aprovado",
        "instagram": "professoraprovado",
        "nicho": "Pedagogia / Educação",
        "seguidores": 2992,
        "comoEncontrei": "Micro-Mentor (3k seg) • Instagram Verificado",
        "observacoes": "👥 ~2,992 seguidores | Mentoria e cronogramas focados em concursos docentes, LDB, BNCC e conhecimentos pedagógicos municipais."
    },
    {
        "nome": "Concursos Para Professores",
        "instagram": "concursoprofessores",
        "nicho": "Pedagogia / Educação",
        "seguidores": 5087,
        "comoEncontrei": "Micro-Mentor (5.1k seg) • Instagram Verificado",
        "observacoes": "👥 ~5,087 seguidores | Acompanhamento e direcionamento de estudos para concursos de prefeituras e secretarias estaduais de educação."
    },

    # 4. Prefeituras / Área Administrativa
    {
        "nome": "Trilha da Aprovação",
        "instagram": "mentoriatrilhadaaprovacao",
        "nicho": "Prefeituras / Adm",
        "seguidores": 808,
        "comoEncontrei": "Micro-Mentor (800 seg) • Canva Site/WhatsApp",
        "observacoes": "👥 ~808 seguidores | Mentoria de estudos e acompanhamento personalizado para concursos administrativos e de prefeituras."
    },
    {
        "nome": "Concurso Prefeituras",
        "instagram": "concursoprefeituras",
        "nicho": "Prefeituras / Adm",
        "seguidores": 548,
        "comoEncontrei": "Micro-Mentor (550 seg) • Instagram Verificado",
        "observacoes": "👥 ~548 seguidores | Mentor focado em concursos municipais, editais de prefeituras e câmaras do interior, cronogramas práticos."
    },
    {
        "nome": "Concurso Municipal",
        "instagram": "concursomunicipal",
        "nicho": "Prefeituras / Adm",
        "seguidores": 746,
        "comoEncontrei": "Micro-Mentor (750 seg) • Instagram Verificado",
        "observacoes": "👥 ~746 seguidores | Orientação para cargos administrativos e de nível médio de prefeituras municipais, mapas e apostilas."
    },

    # 5. Redação / Português / Isoladas
    {
        "nome": "Paulo Costa",
        "instagram": "prof.paulocosta",
        "nicho": "Redação / Isoladas",
        "seguidores": 789,
        "comoEncontrei": "Micro-Mentor (780 seg) • Instagram Verificado",
        "observacoes": "👥 ~789 seguidores | Professor de redação e discursivas para concursos e tribunais, correção individualizada e feedback em vídeo."
    },
    {
        "nome": "Mentoria de Redação",
        "instagram": "mentoriaderedacao",
        "nicho": "Redação / Isoladas",
        "seguidores": 544,
        "comoEncontrei": "Micro-Mentor (540 seg) • Instagram Verificado",
        "observacoes": "👥 ~544 seguidores | Mentoria de redação para concursos públicos com correções analíticas, padrão Cebraspe, FCC e Vunesp."
    },
    {
        "nome": "Redação para Concurso",
        "instagram": "redacaoparaconcurso",
        "nicho": "Redação / Isoladas",
        "seguidores": 1471,
        "comoEncontrei": "Micro-Mentor (1.5k seg) • Instagram Verificado",
        "observacoes": "👥 ~1,471 seguidores | Focado em técnicas de escrita nota 10, estrutura dissertativa e mentoria individual para provas discursivas."
    },
    {
        "nome": "Português Concursos",
        "instagram": "portuguesconcursos",
        "nicho": "Redação / Isoladas",
        "seguidores": 3045,
        "comoEncontrei": "Micro-Mentor (3k seg) • Instagram Verificado",
        "observacoes": "👥 ~3,045 seguidores | Mentor e professor de Língua Portuguesa para concursos de tribunais e administrativos, isoladas e mentoria."
    },
    {
        "nome": "RLM para Concursos",
        "instagram": "rlmparaconcursos",
        "nicho": "Redação / Isoladas",
        "seguidores": 1132,
        "comoEncontrei": "Micro-Mentor (1.1k seg) • Instagram Verificado",
        "observacoes": "👥 ~1,132 seguidores | Mentoria e resolução esquematizada de Raciocínio Lógico e Matemática para certames públicos."
    },

    # 6. Fiscal / Controle
    {
        "nome": "José Alexandre Vieira",
        "instagram": "profalexandre",
        "nicho": "Fiscal / Controle",
        "seguidores": 437,
        "comoEncontrei": "Micro-Mentor (430 seg) • Instagram/Bio",
        "observacoes": "👥 ~437 seguidores | Professor e mentor para concursos fiscais (ISS e SEFAZ), consultoria individual de ciclos de auditor."
    }
]

# Verify deduplication and exclusions
final_leads = []
seen_handles = set()

for l in raw_leads:
    h = l['instagram'].lower().strip()
    if h in seen_handles:
        continue
    if h in existing_handles:
        print(f"Skipping already existing handle: @{h}")
        continue
    
    seen_handles.add(h)
    final_leads.append({
        "nome": l['nome'],
        "instagram": h,
        "nicho": l['nicho'],
        "comoEncontrei": l['comoEncontrei'],
        "observacoes": l['observacoes'],
        "prioridade": "alta"
    })

print(f"\nFinal Verified Count: {len(final_leads)} leads ready to save!")

output_path = r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\lote_micro_outros.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(final_leads, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {len(final_leads)} micro-mentors to {output_path}!")
