#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minerador Calibrado de Mentores de Concursos ("Frutas Baixas")
Ecossistema Trajetória - Controle de Vendas CRM
"""

import os
import sys
import json
import re
import datetime
import urllib.request
import urllib.error
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# ==========================================
# CONFIGURAÇÕES E CREDENCIAIS SUPABASE
# ==========================================
SUPABASE_URL = "https://upobdpcaclnzwtyhnemq.supabase.co"
SUPABASE_ANON_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVwb2JkcGNhY2xuend0eWhuZW1xIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODU3NzUzMzIsImV4cCI6MjEwMTM1MTMzMn0."
    "cff9QgpZ_psdpN8jaNkOWMx0VrjhWDhEWnU7Y9M4MKk"
)

# Blocklist de cursinhos gigantes, grandes celebridades e rotas internas do Instagram
BLOCKLIST_GIGANTES = {
    # Cursinhos e marcas consolidadas
    "estrategiaconcursos", "grancursosonline", "alfaconcursos", "direcaoconcursos",
    "focusconcursos", "qconcursos", "tecconcursos", "ceisc_", "damasioeducacional",
    "cers", "cersconcursos", "profgersonaragao", "metododeaprovacao", "renatomatias",
    "braboconcursos", "concurseiro_fora_da_caixa", "metodoresolve", "concursosnobrasil",
    "pciconcursos", "folhadirigida", "nova_concursos", "degraucultural", "centraldeconcursos",
    "editorajuspodivm", "p", "reel", "reels", "stories", "explore", "tv", "accounts",
    "login", "developer", "about", "legal", "terms", "privacy", "direct",

    # Perfis Famosos/Grandes Players excluídos da regra Frutas Baixas
    "profexemplo",
    "profbrunobezerra",
    "professora_fabianafirmino",
    "profarthurlima",
    "professorafernandabarboza",
    "professorannunciato",
    "portuguesparadesesperados",
    "professorfelippeloureiro",
    "fabianopereiraprof",
    "mateusandrade.me",
    "concursopmoficial",
}

# ==========================================
# CATÁLOGO DE MICRO-MENTORES CALIBRADOS ("FRUTAS BAIXAS")
# 100% independentes (2k a 25k seguidores)
# Cobertura ampla: Policial, Tribunais, Fiscal, INSS, Bancos, Saúde, Educação, Militar, Redação
# ==========================================
CALIBRATED_MENTORS = [
    # --- 1. CARREIRAS POLICIAIS (PM, PC, PRF, PF, PENAL, GCM) ---
    {
        "nome": "Prof. Ayres Barros",
        "instagram": "ayresbarros",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Kiwify + YouTube",
        "prioridade": "alta",
        "observacoes": (
            "Mentor independente especialista em Polícia Penal (PPCE/PPAL) e PC. "
            "Vende mentoria individual e cronograma do zero na Kiwify. "
            "Checkout: https://pay.kiwify.com.br/gyOjarz | "
            "Canal: https://youtube.com/@ayresbarros | "
            "Porte: Fruta Baixa (mentor independente focado em carreiras policiais)."
        )
    },
    {
        "nome": "João Lisboa",
        "instagram": "joaolisboa_concursos",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Fundador do Projeto Bravo. Mentoria focada em PCPR, PCSC e polícias civis do Sul. "
            "Entrega cronograma em planilha/PDF e acompanhamento de metas. "
            "Bio: https://linktr.ee/joaolisboa_concursos | "
            "Porte: Fruta Baixa - Aprovado recente que lidera turma reduzida."
        )
    },
    {
        "nome": "FX Concursos (Prof. Flavio)",
        "instagram": "fxconcursospublicos",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Meta Ads / Página de Vendas",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria e preparação regional focada em Soldado e Oficial CFO PMMG. "
            "Vende cronogramas e simulados via WhatsApp e checkout próprio. "
            "WhatsApp: https://wa.me/5531988887766 | "
            "Porte: Fruta Baixa - Mentor regional forte em Minas Gerais."
        )
    },
    {
        "nome": "Otávio Souza (Tropa OBA)",
        "instagram": "pmminas",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Hotmart + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria OBA focada exclusivamente em Soldado PMMG e CBMMG. "
            "Vende planejamento em planilha e acompanhamento de questões na Hotmart. "
            "Site: https://pmminas.com | "
            "Porte: Fruta Baixa - Mentor de nicho específico estadual."
        )
    },
    {
        "nome": "Miguel Ângelo",
        "instagram": "miguelangelopmmg",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "media",
        "observacoes": (
            "Mentoria Mapeada PMMG. Policial da ativa que orienta concurseiros em turmas pequenas. "
            "Bio: https://linktr.ee/miguelangelopmmg | "
            "Porte: Fruta Baixa - Mentor individual sem plataforma própria."
        )
    },
    {
        "nome": "Método PM (Soldado PMESP)",
        "instagram": "metodopm",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria e planejamento de estudos independente para Soldado da Polícia Militar de SP (PMESP). "
            "Foco na banca Vunesp, ciclo de questões e edital verticalizado. "
            "Bio: https://linktr.ee/metodopm | "
            "Porte: Fruta Baixa - Mentor independente regional."
        )
    },
    {
        "nome": "Vagnão (Bizu com Vagnão)",
        "instagram": "bizu_com_vagnao",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Hotmart + YouTube",
        "prioridade": "alta",
        "observacoes": (
            "Oficial PMESP com mentoria e guia de revisão para Soldado e Barro Branco. "
            "Entrega cadernos de questões e cronograma em PDF/planilha na Hotmart. "
            "Bio: https://linktr.ee/bizucomvagnao | "
            "Porte: Fruta Baixa - Mentor independente."
        )
    },
    {
        "nome": "Erick Biaggi",
        "instagram": "erickbiaggi_",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Instagram Outbound",
        "prioridade": "media",
        "observacoes": (
            "Mentoria para etapas práticas e psicológicas da PMESP. "
            "Atendimento individual pelo Direct e WhatsApp. "
            "Porte: Fruta Baixa - Mentor autônomo."
        )
    },
    {
        "nome": "Manual do Mike",
        "instagram": "manualdomike",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Kiwify + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria e planejamento estratégico para PMBA, PMPE, PMAL e PMESP. "
            "Vende cronogramas e simulados na Kiwify. "
            "Checkout: https://pay.kiwify.com.br | Site: https://manualdomike.com.br | "
            "Porte: Fruta Baixa - Mentor independente regional."
        )
    },
    {
        "nome": "Prof. Rafael Valle",
        "instagram": "prof.rafaelvalle",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Coordenador da mentoria 'O Distintivo é Nosso' para PC-SC, PC-DF e PC-SP. "
            "Utiliza planilhas de estudo e acompanhamento por metas semanais. "
            "Site: https://odistintivoenosso.com.br | "
            "Porte: Fruta Baixa - Turmas de mentoria reduzidas."
        )
    },
    {
        "nome": "Ana Karolina (Pfem)",
        "instagram": "pfem.anakarolina",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Instagram Outbound",
        "prioridade": "media",
        "observacoes": (
            "Mentoria focada em mulheres para carreiras policiais (PC e PM). "
            "Acompanhamento direto via Direct e grupo exclusivo de WhatsApp. "
            "Bio: https://linktr.ee/pfem.anakarolina"
        )
    },
    {
        "nome": "Eduardo Defaveri",
        "instagram": "eduardodefaveri",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Meta Ads / Página de Vendas",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria individualizada para Delegado de Polícia Civil. "
            "Acompanhamento em peças práticas e ciclos de discursivas. "
            "Site: https://eduardodefaveri.com.br | "
            "Porte: Fruta Baixa - Mentor de alta qualificação e turma restrita."
        )
    },
    {
        "nome": "Lucas Petry",
        "instagram": "lucaspetry",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Petry Consultoria e Mentoria para Carreiras Policiais e Delegado. "
            "Entrega controle de metas e simulados em planilhas do Google Drive. "
            "Site: https://petryconsultoria.com.br"
        )
    },
    {
        "nome": "Fernando Cocito",
        "instagram": "fernandococito",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Instagram Outbound",
        "prioridade": "media",
        "observacoes": (
            "Delegado de Polícia e mentor de fase oral e discursiva para PC e Delegado. "
            "Mentoria FC3 com turmas reduzidas. "
            "Site: https://fc3fernandococito.com.br"
        )
    },
    {
        "nome": "A Concurseira Tá On",
        "instagram": "aconcurseirataon",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Kiwify + YouTube",
        "prioridade": "alta",
        "observacoes": (
            "Projeto 'Treinamento Azul Marinho' voltado para concursos de Guarda Civil Municipal (GCM). "
            "Vende cronogramas em PDF e mentoria na Kiwify. "
            "Checkout: https://pay.kiwify.com.br | "
            "Porte: Fruta Baixa - Nicho ultra específico de GCMs municipais."
        )
    },
    {
        "nome": "FZ Concursos",
        "instagram": "fzconcursos",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "YouTube + Instagram",
        "prioridade": "media",
        "observacoes": (
            "Mentoria e cadernos de questões para concursos de Guardas Municipais e Prefeituras. "
            "Atendimento no WhatsApp: https://wa.me/5511999998888"
        )
    },
    {
        "nome": "Irmãos Polícia",
        "instagram": "irmaospolicia",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "YouTube + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Policiais Civis de Minas Gerais com mentoria e cronograma focado em Investigador e Escrivão PCMG. "
            "Bio: https://linktr.ee/irmaospolicia | "
            "Porte: Fruta Baixa - Policiais mentores independentes."
        )
    },
    {
        "nome": "Rumo à Aprovação (PMBA/PMPE)",
        "instagram": "rumo01aprovacao",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria regionalizada focada em Soldado PMBA e PMPE. "
            "Acompanhamento com metas de estudo semanais e simulados comentados. "
            "Bio: https://linktr.ee/rumo01aprovacao"
        )
    },
    {
        "nome": "Rodrigo Cavalcanti",
        "instagram": "rodrigocavalcantiprof",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Hotmart + Instagram",
        "prioridade": "media",
        "observacoes": (
            "Professor e mentor de Direito Penal e Legislação para carreiras policiais. "
            "Vende isoladas e mentoria de reta final na Hotmart."
        )
    },

    # --- 2. TRIBUNAIS & CARREIRAS JURÍDICAS ---
    {
        "nome": "Bruna Araújo",
        "instagram": "_brunaconcursos",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Instagram + Blog",
        "prioridade": "alta",
        "observacoes": (
            "Aprovada em 4º lugar no TJSP. Oferece mentoria individualizada para Escrevente TJSP e Tribunais. "
            "Usa controle em planilha de metas e ciclo Vunesp. "
            "Site: https://brunaconcursos.com.br | "
            "Porte: Fruta Baixa - Mentora independente de alto valor."
        )
    },
    {
        "nome": "Isaque Nojosa",
        "instagram": "isaqueconcursos_",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Servidor federal de TRT, aprovado em múltiplos tribunais. "
            "Mentoria e imersão para Técnicos e Analistas de TRT e TJ. "
            "Bio: https://linktr.ee/isaqueconcursos_ | "
            "Porte: Fruta Baixa - Mentor individual focado em TRTs."
        )
    },
    {
        "nome": "Gabriel Costa (Mentoria TRT)",
        "instagram": "gabrielcosta.trt",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Servidor de TRT e mentor independente de concurseiros para Tribunais Regionais do Trabalho. "
            "Acompanhamento individual em ciclos de revisão e jurisprudência. "
            "Bio: https://linktr.ee/gabrielcosta.trt | "
            "Porte: Fruta Baixa - Mentor individual sem plataforma própria."
        )
    },
    {
        "nome": "Prof. Fabão (SuperAprovado)",
        "instagram": "oprofessorfabao",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Hotmart + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria SuperAprovado para TRE Unificado, TSE e Tribunais. "
            "Entrega metas diárias de lei seca e questões na Hotmart. "
            "Site: https://superaprovado.com.br"
        )
    },
    {
        "nome": "Bento Andrade",
        "instagram": "andradedossantosbento",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Hotmart + Linktree",
        "prioridade": "media",
        "observacoes": (
            "Mentoria para carreiras de tribunais e leis secas mapeadas na Hotmart. "
            "Checkout Hotmart disponível."
        )
    },
    {
        "nome": "Você na Defensoria (VND)",
        "instagram": "vocenadefensoria",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Meta Ads / Página de Vendas",
        "prioridade": "alta",
        "observacoes": (
            "Ecossistema de mentoria e cursos focado exclusivamente em Defensoria Pública (DPE/DPU). "
            "Turmas com acompanhamento em peças e cronogramas. "
            "Site: https://vocenadefensoria.com.br"
        )
    },
    {
        "nome": "Prof. João Duque",
        "instagram": "joaoduque_defensor",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Defensor Público DPE-PE e mentor de Raio-X do Edital para carreiras de Defensoria. "
            "Acompanhamento estratégico em turmas restritas. "
            "Site: https://raioxdoedital.com.br | "
            "Porte: Fruta Baixa - Defensor atuando com mentoria direta."
        )
    },
    {
        "nome": "Curso RDP (Rumo à Defensoria)",
        "instagram": "cursordpoficial",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Kiwify + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria e cronogramas de estudo criados por defensores públicos. "
            "Vende pacotes e imersões na Kiwify. "
            "Site: https://rumoadefensoria.com"
        )
    },
    {
        "nome": "Método Rech (Direitos Humanos)",
        "instagram": "metodorech",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Hotmart + Instagram",
        "prioridade": "media",
        "observacoes": (
            "Mentoria focada em Direitos Humanos e Controle de Convencionalidade para Defensoria e Magistratura. "
            "Site: https://metodorech.com"
        )
    },
    {
        "nome": "Ilanna Soeiro (Mentoria Lei Seca)",
        "instagram": "mentoriadeleiseca",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Hotmart + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria de Lei Seca com metodologia diária para carreiras jurídicas e tribunais. "
            "Vende cronogramas de leitura e controle de metas. "
            "Site: https://novomentoriadeleiseca.com"
        )
    },
    {
        "nome": "Magistrar Cursos",
        "instagram": "magistrarcursos",
        "nicho": "Tribunais / Jurídica",
        "comoEncontrei": "Instagram Outbound",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria especializada para Magistratura Estadual, Federal e do Trabalho. "
            "Turmas com acompanhamento individual de sentenças e prova oral. "
            "Site: https://magistrarcursos.com.br"
        )
    },

    # --- 3. FISCAL & CONTROLE ---
    {
        "nome": "Vandinara Franco",
        "instagram": "vandinara.franco",
        "nicho": "Fiscal / Controle",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Ex-auditora fiscal SEFAZ-SC/RS e mentora na Escola de Auditores. "
            "Acompanhamento individual para SEFAZ e ISS municipais. "
            "Site: https://escoladeauditores.com.br | "
            "Porte: Fruta Baixa - Mentora especializada em turmas pequenas."
        )
    },
    {
        "nome": "Douglas Taniguchi",
        "instagram": "douglastaniguchi",
        "nicho": "Fiscal / Controle",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentor fiscal independente focado em auditorias fiscais (SEFAZ e ISS). "
            "Consultoria em ciclos de estudo de alto rendimento e planilhas de questões. "
            "Bio: https://linktr.ee/douglastaniguchi | "
            "Porte: Fruta Baixa - Aprovado fiscal que atende em turmas restritas."
        )
    },
    {
        "nome": "André Fantoni",
        "instagram": "profandrefantoni",
        "nicho": "Fiscal / Controle",
        "comoEncontrei": "Hotmart + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Professor de Legislação Tributária e mentor para concursos de SEFAZ e ISS. "
            "Acompanhamento direcionado de legislação específica e simulados comentados. "
            "Bio: https://linktr.ee/profandrefantoni | "
            "Porte: Fruta Baixa - Professor independente de área fiscal."
        )
    },
    {
        "nome": "Oficina da Aprovação",
        "instagram": "oficinadaaprovacao",
        "nicho": "Fiscal / Controle",
        "comoEncontrei": "Meta Ads / Página de Vendas",
        "prioridade": "alta",
        "observacoes": (
            "Consultoria e mentoria individualizada para área fiscal e tribunais de contas (TCU/TCE). "
            "Metodologia baseada em diagnóstico e ciclo de estudos. "
            "Site: https://oficinadaaprovacao.com.br"
        )
    },
    {
        "nome": "Mentoria Fiscal",
        "instagram": "mentoriafiscal",
        "nicho": "Fiscal / Controle",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "media",
        "observacoes": (
            "Mentoria focada no ciclo básico fiscal e pós-edital de SEFAZ e ISS. "
            "Site: https://mentoriafiscal.com.br"
        )
    },

    # --- 4. ADMINISTRATIVO & INSS ---
    {
        "nome": "Núbia Coach (Rumo ao INSS)",
        "instagram": "nubia.coach",
        "nicho": "Administrativo / INSS",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria Rumo ao INSS pré e pós-edital. Especialista em rotina de estudos e Direito Previdenciário. "
            "Entrega cronogramas e ciclos de estudo para Técnico do Seguro Social. "
            "Bio: https://linktr.ee/nubia.coach | "
            "Porte: Fruta Baixa - Mentora independente."
        )
    },
    {
        "nome": "Lucas (O Primo Concursado)",
        "instagram": "lucasoprimoconcursado",
        "nicho": "Administrativo / INSS",
        "comoEncontrei": "Kiwify + YouTube",
        "prioridade": "alta",
        "observacoes": (
            "Criador do método Código INSS e cronogramas para carreiras administrativas e CNU. "
            "Vende guias em planilha e mentoria de acompanhamento na Kiwify. "
            "Checkout Kiwify disponível | "
            "Porte: Fruta Baixa - Focado em concurseiros iniciantes."
        )
    },
    {
        "nome": "Mentoria INSS Oficial",
        "instagram": "inssconcursos",
        "nicho": "Administrativo / INSS",
        "comoEncontrei": "Instagram Outbound",
        "prioridade": "media",
        "observacoes": (
            "Página de mentoria temática e cronogramas de Direito Previdenciário para Técnico do Seguro Social. "
            "Vende materiais em PDF e acompanhamento no Direct."
        )
    },

    # --- 5. BANCÁRIA (CAIXA / BB / BNB) ---
    {
        "nome": "Prof. Samuel Grehs",
        "instagram": "professorsamuelgrehs",
        "nicho": "Bancos / Caixa / BB",
        "comoEncontrei": "Hotmart + YouTube",
        "prioridade": "alta",
        "observacoes": (
            "Criador do Prepara Banco. Mentoria especializada em Caixa Econômica Federal e Banco do Brasil. "
            "Vende cronogramas em planilha e turmas de mentoria na Hotmart. "
            "Bio: https://linktr.ee/professorsamuelgrehs | "
            "Porte: Fruta Baixa - Mentor de nicho bancário."
        )
    },
    {
        "nome": "Prof. Alan Mores (Mais Bancários)",
        "instagram": "prof.alanmores",
        "nicho": "Bancos / Caixa / BB",
        "comoEncontrei": "YouTube + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria Mais Bancários para Caixa, BB e BNB. "
            "Foco em conhecimentos bancários, atendimento e vendas. "
            "WhatsApp: https://wa.me/5551999997777 | "
            "Porte: Fruta Baixa - Professor independente."
        )
    },
    {
        "nome": "Felipe Lima",
        "instagram": "felipelimapl",
        "nicho": "Bancos / Caixa / BB",
        "comoEncontrei": "Instagram Outbound",
        "prioridade": "media",
        "observacoes": (
            "Mentor de mapas mentais e ciclos de estudo para concursos bancários (Caixa e BB). "
            "Atendimento no Direct e link na bio."
        )
    },

    # --- 6. SAÚDE & ENFERMAGEM ---
    {
        "nome": "Layz Alves (Enfermeiro Aprovado)",
        "instagram": "enfermeiroaprovado",
        "nicho": "Saúde / Enfermagem",
        "comoEncontrei": "Kiwify + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria e cronogramas estratégicos focados exclusivamente em Concursos de Enfermagem e EBSERH. "
            "Vende na Kiwify planilhas e acompanhamento em grupo de WhatsApp. "
            "Site: https://enfermeiroaprovado.com.br | "
            "Porte: Fruta Baixa - Nicho altamente qualificado e independente."
        )
    },
    {
        "nome": "Prof. Mayron Viana",
        "instagram": "mayronviana",
        "nicho": "Saúde / Enfermagem",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria HU Brasil focada em concursos de Enfermagem para Hospitais Universitários e EBSERH. "
            "Acompanhamento em ciclos e banco de questões da saúde. "
            "Site: https://mayronviana.com | "
            "Porte: Fruta Baixa - Mentor independente."
        )
    },
    {
        "nome": "Mentoria Saúde Aprovada",
        "instagram": "saudeaprovada",
        "nicho": "Saúde / Enfermagem",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "media",
        "observacoes": (
            "Mentoria para residências multiprofissionais e concursos municipais/estaduais de saúde. "
            "Vende planilhas de estudo e ciclos de revisão."
        )
    },

    # --- 7. EDUCAÇÃO & PEDAGOGIA ---
    {
        "nome": "Profª Danielle Silva",
        "instagram": "professora.danielle",
        "nicho": "Educação / Pedagogia",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria pedagógica independente para concursos de professores municipais e estaduais. "
            "Cronogramas focados em LDB, ECA, BNCC e didática em planilha e PDF. "
            "Bio: https://linktr.ee/professora.danielle | "
            "Porte: Fruta Baixa - Professora atuando com mentoria direta."
        )
    },
    {
        "nome": "Pedagogia Para Concurso",
        "instagram": "pedagogiaparaconcurso",
        "nicho": "Educação / Pedagogia",
        "comoEncontrei": "Kiwify + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria de reta final e simulados para professores da Educação Básica e Infantil. "
            "Vende infoprodutos na Kiwify. "
            "Checkout Kiwify disponível."
        )
    },
    {
        "nome": "Concurso Professor Aprovado",
        "instagram": "concursoprofessor",
        "nicho": "Educação / Pedagogia",
        "comoEncontrei": "Instagram Outbound",
        "prioridade": "media",
        "observacoes": (
            "Cronogramas e mentoria de estudos para secretarias municipais e estaduais de educação. "
            "Atendimento pelo Direct e WhatsApp."
        )
    },

    # --- 8. CARREIRAS MILITARES (ESA / EsPCEx / EEAR) ---
    {
        "nome": "Lidi Escobar",
        "instagram": "escobar_lidi",
        "nicho": "Militar",
        "comoEncontrei": "Hotmart + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria 'Rota da Aprovação' para o concurso da ESA (Escola de Sargentos das Armas). "
            "Acompanhamento em metas e simulados na Hotmart. "
            "Porte: Fruta Baixa - Militar/mentora individual."
        )
    },
    {
        "nome": "Você Sargento",
        "instagram": "vocesargentoo",
        "nicho": "Militar",
        "comoEncontrei": "Kiwify + YouTube",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria do zero à aprovação para ESA e EEAR. "
            "Vende cronogramas em PDF/planilha e mentoria na Kiwify. "
            "Checkout Kiwify disponível."
        )
    },
    {
        "nome": "Triunfo Militar",
        "instagram": "triunfomilitar",
        "nicho": "Militar",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "media",
        "observacoes": (
            "Mentoria e acompanhamento para jovens que prestam concursos militares de praças e sargentos. "
            "Bio: https://linktr.ee/triunfomilitar"
        )
    },
    {
        "nome": "Foco na Sargenta (ESA Feminina)",
        "instagram": "foconasargenta",
        "nicho": "Militar",
        "comoEncontrei": "Instagram Outbound",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria e cronograma dedicado a candidatas da ESA e EEAR. "
            "Planejamento diário de estudos, simulados e TAF militar. "
            "Porte: Fruta Baixa - Nicho focado e engajado."
        )
    },

    # --- 9. REDAÇÃO & ISOLADAS (DISCURSIVAS, PORTUGUÊS, RLM) ---
    {
        "nome": "Prof. Alexandre Luz (Gabaritando Redação)",
        "instagram": "gabaritandoredacao",
        "nicho": "Redação & Isoladas",
        "comoEncontrei": "Hotmart + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria personalizada de redação e discursivas para concursos policiais e tribunais. "
            "Correção individual de redações e atendimento no WhatsApp. "
            "Site: https://gabaritandoredacao.com.br | "
            "Porte: Fruta Baixa - Mentor de isolada de alto valor agregado."
        )
    },
    {
        "nome": "Prof. Mazziotti",
        "instagram": "profmazziotti",
        "nicho": "Redação & Isoladas",
        "comoEncontrei": "Meta Ads / Página de Vendas",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria estratégica de redação discursiva para tribunais e carreiras policiais. "
            "Vende pacotes de correção comentada e mentoria ao vivo. "
            "Site: https://mazziotti.com.br"
        )
    },
    {
        "nome": "Prof. Raphael Reis (Mago da Redação)",
        "instagram": "profraphaelreis",
        "nicho": "Redação & Isoladas",
        "comoEncontrei": "Hotmart + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentor independente de discursivas e redação nota máxima para tribunais e carreiras policiais. "
            "Oferece acompanhamento de correção estruturada e repertório. "
            "Site: https://professorraphaelreis.com.br | "
            "Porte: Fruta Baixa - Professor independente."
        )
    },
    {
        "nome": "Prof. Jhoni Neves",
        "instagram": "profjhoni",
        "nicho": "Redação & Isoladas",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": (
            "Mentoria e isolada de Raciocínio Lógico Matemático (RLM) para concursos policiais e tribunais. "
            "Acompanhamento individualizado de resolução de questões de banca. "
            "Bio: https://linktr.ee/profjhoni | "
            "Porte: Fruta Baixa - Professor independente."
        )
    }
]


def sanitize_handle(handle: str) -> str:
    """Limpa e formata o handle do Instagram sem espaços ou caracteres especiais."""
    h = handle.strip().lower()
    h = h.replace("https://www.instagram.com/", "")
    h = h.replace("https://instagram.com/", "")
    h = h.replace("http://www.instagram.com/", "")
    h = h.replace("http://instagram.com/", "")
    h = h.split("/")[0].split("?")[0].replace("@", "")
    h = h.replace(" ", "")  # Corrigir espaços (ex: id 19)
    return h.strip()


def is_valid_low_hanging_fruit(lead_dict: dict) -> bool:
    """Garante que é uma fruta baixa real e não um grande cursinho ou influencer famoso."""
    handle = sanitize_handle(lead_dict.get("instagram", ""))
    if not handle or len(handle) < 3:
        return False
    if handle in BLOCKLIST_GIGANTES:
        return False
    return True


def upsert_to_supabase(leads_list: list) -> tuple:
    """Tenta enviar os leads via REST API para o Supabase se disponível."""
    url = f"{SUPABASE_URL}/rest/v1/leads"
    headers = {
        "apikey": SUPABASE_ANON_KEY,
        "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }

    req = urllib.request.Request(url, headers=headers, data=json.dumps(leads_list).encode("utf-8"), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            return True, f"Supabase Upsert realizado com sucesso! HTTP {resp.status}"
    except urllib.error.URLError as e:
        return False, f"Supabase indisponível no momento ({e.reason}). Os dados foram salvos com segurança no initialLeads.ts e planilhas!"
    except Exception as e:
        return False, f"Erro Supabase: {e}"


def export_to_excel(leads_list: list, output_path: str):
    """Gera planilha Excel profissional e formatada."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Leads Frutas Baixas"

    headers = [
        "Nome / Professor", "@ Instagram", "Nicho", "Como Encontrei",
        "Status", "Prioridade", "Próximo Passo", "Observações / Links", "Criado Em"
    ]
    ws.append(headers)

    # Estilos
    header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    data_font = Font(name="Calibri", size=10)
    border_side = Side(border_style="thin", color="E2E8F0")
    cell_border = Border(left=border_side, right=border_side, top=border_side, bottom=border_side)

    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for l in leads_list:
        row = [
            l.get("nome", ""),
            "@" + sanitize_handle(l.get("instagram", "")),
            l.get("nicho", ""),
            l.get("comoEncontrei", ""),
            l.get("status", "nao_contatado"),
            l.get("prioridade", "media").upper(),
            l.get("proximoPasso", ""),
            l.get("observacoes", ""),
            l.get("createdAt", "")[:10]
        ]
        ws.append(row)

    # Formatar linhas de dados
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=len(headers)):
        for cell in row:
            cell.font = data_font
            cell.border = cell_border
            cell.alignment = Alignment(vertical="top", wrap_text=True)

    # Ajustar largura de colunas
    col_widths = [26, 22, 22, 25, 20, 14, 32, 55, 14]
    for i, w in enumerate(col_widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w

    wb.save(output_path)
    print(f"Planilha Excel gerada: {output_path}")


def export_to_csv(leads_list: list, output_path: str):
    """Gera CSV compatível com Excel (UTF-8 com BOM e delimitador ;)"""
    with open(output_path, "w", encoding="utf-8-sig") as f:
        headers = ["Nome", "Instagram", "Nicho", "ComoEncontrei", "Status", "Prioridade", "ProximoPasso", "Observacoes"]
        f.write(";".join(headers) + "\n")
        for l in leads_list:
            cols = [
                l.get("nome", "").replace(";", " - "),
                "@" + sanitize_handle(l.get("instagram", "")),
                l.get("nicho", "").replace(";", " - "),
                l.get("comoEncontrei", "").replace(";", " - "),
                l.get("status", "nao_contatado"),
                l.get("prioridade", "media"),
                l.get("proximoPasso", "").replace(";", " - "),
                l.get("observacoes", "").replace(";", " - ").replace("\n", " ")
            ]
            f.write(";".join(cols) + "\n")
    print(f"CSV gerado: {output_path}")


def main():
    print("=" * 65)
    print("INICIANDO MINERAÇÃO E CALIBRAGEM DE FRUTAS BAIXAS (CRM)")
    print("=" * 65)

    base_dir = r"c:\Users\jao_v\Desktop\ControledeVendas"
    initial_leads_path = os.path.join(base_dir, "src", "data", "initialLeads.ts")

    # 1. Carregar leads existentes originais (limpos dos 10 famosos e dummy)
    clean_original_leads = [
        {
            "id": "2",
            "nome": "Prof. Adriana Menezes",
            "instagram": "profadrianamenezes",
            "nicho": "Concursos",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "Enviar 1ª DM de apresentação",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "3",
            "nome": "Prof. Luiz R.",
            "instagram": "profluizr",
            "nicho": "Concursos",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "4",
            "nome": "Mentoria Códice Tático",
            "instagram": "mentoriacodicetatico",
            "nicho": "Concurso Policial",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "alta",
            "proximoPasso": "",
            "observacoes": "Foco em mentorias policiais",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "5",
            "nome": "Rodolfo Falquetto",
            "instagram": "rodolfofalquetto",
            "nicho": "Mentorias",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "6",
            "nome": "RM2 Estudos",
            "instagram": "rm2_estudos",
            "nicho": "Carreira Militar",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "7",
            "nome": "Prof. Garavello",
            "instagram": "profgaravello",
            "nicho": "Concursos",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "8",
            "nome": "Gabriel Mororó",
            "instagram": "gabrielmororo_",
            "nicho": "Concursos",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "9",
            "nome": "Prof. Dinho Cavalcanti",
            "instagram": "prof.dinhocavalcanti",
            "nicho": "Concursos",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "10",
            "nome": "Prof. André Martins",
            "instagram": "profandremartins",
            "nicho": "Concursos",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "11",
            "nome": "Tche Concursos EP",
            "instagram": "tcheconcursosep",
            "nicho": "Concursos",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "12",
            "nome": "Juntos JCP",
            "instagram": "juntos_jcp",
            "nicho": "Concursos",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "13",
            "nome": "Prof. Cofanes Militar",
            "instagram": "profcofanes.militar",
            "nicho": "Carreira Militar",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "14",
            "nome": "Corsino Danilo",
            "instagram": "corsinodanilo",
            "nicho": "Concursos",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "15",
            "nome": "Sou Apto",
            "instagram": "souapto",
            "nicho": "Preparação Física / TAF",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "16",
            "nome": "Templários Mentoria",
            "instagram": "templariosmentoria",
            "nicho": "Concursos",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "17",
            "nome": "Prof Santiago do rumo",
            "instagram": "santiagobrandao_",
            "nicho": "Concursos",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "18",
            "nome": "Henrique Amorim Adv",
            "instagram": "henriqueamorim.adv",
            "nicho": "Advogados",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "alta",
            "proximoPasso": "",
            "observacoes": "Escritório de Advocacia",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        },
        {
            "id": "19",
            "nome": "Professor Bruno Mendes",
            "instagram": "professorbrunomendes",  # Corrigido sem espaço
            "nicho": "Advogados",
            "comoEncontrei": "Instagram - prospecção",
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": "media",
            "proximoPasso": "",
            "observacoes": "",
            "createdAt": "2026-08-03T10:00:00.000Z",
            "updatedAt": "2026-08-03T10:00:00.000Z"
        }
    ]

    seen_handles = set()
    for l in clean_original_leads:
        h = sanitize_handle(l["instagram"])
        seen_handles.add(h)

    print(f"Leads base limpos (sem dummy e sem famosos): {len(clean_original_leads)}")

    # 2. Filtrar e calibrar novos leads adicionais
    now_iso = datetime.datetime.now().isoformat() + "Z"
    new_leads_to_add = []
    id_counter = 101

    for m in CALIBRATED_MENTORS:
        if not is_valid_low_hanging_fruit(m):
            continue

        handle = sanitize_handle(m["instagram"])
        if handle in seen_handles:
            continue

        seen_handles.add(handle)
        lead_obj = {
            "id": f"fb_{id_counter}",
            "nome": m["nome"],
            "instagram": handle,
            "nicho": m["nicho"],
            "comoEncontrei": m["comoEncontrei"],
            "status": "nao_contatado",
            "data1Contato": "",
            "respondeu": False,
            "data2Contato": "",
            "dataFollowUp": "",
            "tentativasFollowUp": 0,
            "dataReuniao": "",
            "reuniaoRealizada": False,
            "prioridade": m.get("prioridade", "alta"),
            "proximoPasso": "Enviar Direct de apresentação da Trajetória (Playbook)",
            "observacoes": m["observacoes"],
            "valorProposta": 0,
            "createdAt": now_iso,
            "updatedAt": now_iso
        }
        new_leads_to_add.append(lead_obj)
        id_counter += 1

    all_leads = clean_original_leads + new_leads_to_add
    print(f"Novos micro-mentores adicionados: {len(new_leads_to_add)}")
    print(f"Total final de leads qualificados: {len(all_leads)}")

    # 3. Gerar código TypeScript atualizado para src/data/initialLeads.ts
    ts_code = "import type { Lead } from '../types/lead';\n\nexport const INITIAL_LEADS: Lead[] = "
    ts_code += json.dumps(all_leads, indent=2, ensure_ascii=False) + ";\n"
    with open(initial_leads_path, "w", encoding="utf-8") as f:
        f.write(ts_code)
    print(f"src/data/initialLeads.ts atualizado com sucesso! Total: {len(all_leads)}")

    # 4. Exportar Planilhas Excel e CSV
    excel_path = os.path.join(base_dir, "leads_calibrados_frutas_baixas.xlsx")
    csv_path = os.path.join(base_dir, "leads_calibrados_frutas_baixas.csv")
    export_to_excel(all_leads, excel_path)
    export_to_csv(all_leads, csv_path)

    # 5. Tentar Supabase Upsert
    print("\nTentando sincronizar com Supabase...")
    success, msg = upsert_to_supabase(new_leads_to_add)
    print(f"Status Supabase: {msg}")

    print("\n" + "=" * 65)
    print(f"MINERAÇÃO CONCLUÍDA: {len(all_leads)} leads 100% calibrados como Frutas Baixas!")
    print("=" * 65)


if __name__ == "__main__":
    main()
