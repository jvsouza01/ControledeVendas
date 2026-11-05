#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Busca ao Vivo de Mentores de Concursos
Ecossistema Trajetória - Controle de Vendas CRM
"""

import sys
import os
import re
import json
import base64
import urllib.parse
import urllib.request
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# Garante suporte nativo a UTF-8 no stdout mesmo em terminais Windows (cp1252)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Blocklist estrita de cursinhos gigantes, plataformas gerais e rotas internas do Instagram
BLOCKLIST_GIGANTES = {
    # Rotas internas do Instagram
    "p", "reel", "reels", "stories", "explore", "tv", "accounts",
    "login", "developer", "about", "legal", "terms", "privacy", "direct", "share",
    "directory", "press", "help", "aboutus", "support", "tags", "locations", "settings",

    # Grandes cursinhos e portais corporativos
    "estrategiaconcursos", "grancursosonline", "alfaconcursos", "direcaoconcursos",
    "focusconcursos", "qconcursos", "tecconcursos", "ceisc_", "damasioeducacional",
    "cers", "cersconcursos", "profgersonaragao", "metododeaprovacao", "renatomatias",
    "braboconcursos", "concurseiro_fora_da_caixa", "metodoresolve", "concursosnobrasil",
    "pciconcursos", "folhadirigida", "nova_concursos", "degraucultural", "centraldeconcursos",
    "editorajuspodivm", "juspodivm", "saraivaeducacao", "kultivi", "kultiviedu",

    # Perfis Famosos / Grandes Players
    "profexemplo", "profbrunobezerra", "professora_fabianafirmino", "profarthurlima",
    "professorafernandabarboza", "professorannunciato", "portuguesparadesesperados",
    "professorfelippeloureiro", "fabianopereiraprof", "mateusandrade.me", "concursopmoficial",

    # Domínios e plataformas genéricas
    "youtube", "google", "facebook", "twitter", "whatsapp", "tiktok", "apple", "microsoft",
    "linktreebrasil", "linktree", "kiwify", "hotmart", "sympla", "eduzz", "monetizze",
    "instagram", "linkedin", "pinterest", "spotify", "t.me", "telegram"
}

# Micro-mentores calibrados de fallback/enriquecimento (extraídos do minerar_mentores.py)
CALIBRATED_SEEDS = [
    {
        "nome": "Prof. Ayres Barros",
        "instagram": "ayresbarros",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Kiwify + YouTube",
        "prioridade": "alta",
        "observacoes": "Mentor independente especialista em Polícia Penal e PC. Vende mentoria individual e cronograma na Kiwify."
    },
    {
        "nome": "João Lisboa",
        "instagram": "joaolisboa_concursos",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": "Fundador do Projeto Bravo. Mentoria focada em PCPR, PCSC e polícias civis do Sul."
    },
    {
        "nome": "FX Concursos (Prof. Flavio)",
        "instagram": "fxconcursospublicos",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Meta Ads / Página de Vendas",
        "prioridade": "alta",
        "observacoes": "Mentoria e preparação regional focada em Soldado e Oficial CFO PMMG."
    },
    {
        "nome": "Otávio Souza (Tropa OBA)",
        "instagram": "pmminas",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Hotmart + Instagram",
        "prioridade": "alta",
        "observacoes": "Mentoria OBA focada em Soldado PMMG e CBMMG. Vende planejamento e simulados."
    },
    {
        "nome": "Miguel Ângelo",
        "instagram": "miguelangelopmmg",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "media",
        "observacoes": "Mentoria Mapeada PMMG. Policial da ativa que orienta concurseiros em turmas pequenas."
    },
    {
        "nome": "Método PM (Soldado PMESP)",
        "instagram": "metodopm",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": "Mentoria independente para Soldado da Polícia Militar de SP (PMESP)."
    },
    {
        "nome": "Vagnão (Bizu com Vagnão)",
        "instagram": "bizu_com_vagnao",
        "nicho": "Carreiras Policiais",
        "comoEncontrei": "Hotmart + YouTube",
        "prioridade": "alta",
        "observacoes": "Oficial PMESP com mentoria e guia de revisão para Soldado e Barro Branco."
    },
    {
        "nome": "Prof. Renan Duarte",
        "instagram": "profrenanduarte",
        "nicho": "Tribunais e Judiciário",
        "comoEncontrei": "Hotmart + YouTube",
        "prioridade": "alta",
        "observacoes": "Mentor independente para TJSP, TRFs e TRE Unificado. Vende cronogramas verticais."
    },
    {
        "nome": "Método Tribunais (Mariana)",
        "instagram": "metodotribunais",
        "nicho": "Tribunais e Judiciário",
        "comoEncontrei": "Linktree + Instagram",
        "prioridade": "alta",
        "observacoes": "Aprovada em TRT que orienta técnicos e analistas judiciários em turmas reduzidas."
    },
    {
        "nome": "Prof. Diego Fiscal",
        "instagram": "diegofiscalconcursos",
        "nicho": "Fiscal e Controle",
        "comoEncontrei": "Kiwify + Instagram",
        "prioridade": "alta",
        "observacoes": "Auditor Fiscal com mentoria para SEFAZ e Receita Federal."
    },
    {
        "nome": "Mentoria INSS descomplicada",
        "instagram": "mentoriainss",
        "nicho": "Carreiras Administrativas",
        "comoEncontrei": "Hotmart + Instagram",
        "prioridade": "alta",
        "observacoes": "Preparatório e mentoria de questões focado no edital de Técnico do Seguro Social."
    }
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

def clean_handle(handle):
    if not handle:
        return None
    h = handle.strip().lower()
    h = re.sub(r'[^a-zA-Z0-9_\.]', '', h)
    h = h.strip('._')
    if len(h) < 3 or len(h) > 30:
        return None
    if h in BLOCKLIST_GIGANTES:
        return None
    if any(h.startswith(prefix) for prefix in ['reel', 'p_', 'tag_', 'explore_']):
        return None
    return h

def format_mentor_name(handle, raw_title=None):
    if raw_title:
        clean_title = re.sub(r'<[^>]+>', '', raw_title)
        clean_title = clean_title.split('|')[0].split('–')[0].split('-')[0].split('•')[0].strip()
        if len(clean_title) >= 4 and not clean_title.lower().startswith(('instagram', 'vídeo', 'curso')):
            return clean_title
    # Gera nome humanizado a partir do handle
    parts = handle.replace('_', ' ').replace('.', ' ').split()
    capitalized = " ".join(p.capitalize() for p in parts)
    if "mentor" in handle.lower():
        return capitalized
    return f"Prof. {capitalized}"

def decode_bing_u(u_str):
    try:
        padded = u_str + '=' * (4 - len(u_str) % 4)
        return base64.b64decode(padded.replace('-', '+').replace('_', '/')).decode('utf-8', errors='ignore')
    except Exception:
        return ""

def search_bing(query):
    leads = []
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            algos = re.findall(r'<li class="b_algo".*?</li>', html, re.DOTALL)
            for a in algos:
                u_m = re.search(r'u=a1([a-zA-Z0-9_\-]+)', a)
                link = decode_bing_u(u_m.group(1)) if u_m else ""
                title_m = re.search(r'<h2[^>]*>(.*?)</h2>', a)
                title = title_m.group(1) if title_m else ""
                snippet_m = re.search(r'<p[^>]*>(.*?)</p>', a)
                snippet = re.sub(r'<[^>]+>', '', snippet_m.group(1)).strip() if snippet_m else ""
                
                ig_match = re.search(r'instagram\.com/([a-zA-Z0-9_\.]{3,30})', link + " " + a)
                lt_match = re.search(r'linktr\.ee/([a-zA-Z0-9_\.]{3,30})', link + " " + a)
                kw_match = re.search(r'kiwify\.com\.br/[a-zA-Z0-9_\.\-]+', link + " " + a)
                
                ig = clean_handle(ig_match.group(1)) if ig_match else None
                if not ig and lt_match:
                    ig = clean_handle(lt_match.group(1))
                
                if ig:
                    nome = format_mentor_name(ig, title)
                    obs = f"Encontrado via Bing Web Search | {snippet[:120]}"
                    if kw_match:
                        obs += f" | Checkout Kiwify: https://{kw_match.group(0)}"
                    leads.append({
                        "nome": nome,
                        "instagram": ig,
                        "comoEncontrei": "Bing Web Search",
                        "observacoes": obs,
                        "prioridade": "alta"
                    })
    except Exception:
        pass
    return leads

def search_ddg(query):
    leads = []
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            uddgs = re.findall(r'uddg=([^&"\']+)', html)
            for u in uddgs:
                decoded = urllib.parse.unquote(u)
                ig_m = re.search(r'instagram\.com/([a-zA-Z0-9_\.]{3,30})', decoded)
                lt_m = re.search(r'linktr\.ee/([a-zA-Z0-9_\.]{3,30})', decoded)
                ig = clean_handle(ig_m.group(1)) if ig_m else None
                if not ig and lt_m:
                    ig = clean_handle(lt_m.group(1))
                if ig:
                    leads.append({
                        "nome": format_mentor_name(ig),
                        "instagram": ig,
                        "comoEncontrei": "DuckDuckGo HTML",
                        "observacoes": f"Link encontrado em busca ao vivo no DuckDuckGo: {decoded}",
                        "prioridade": "alta"
                    })
    except Exception:
        pass
    return leads

def search_yahoo(query):
    leads = []
    url = f"https://br.search.yahoo.com/search?p={urllib.parse.quote(query)}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            rus = re.findall(r'RU=([^/]+)/RK', html)
            for ru in rus:
                decoded = urllib.parse.unquote(ru)
                ig_m = re.search(r'instagram\.com/([a-zA-Z0-9_\.]{3,30})', decoded)
                lt_m = re.search(r'linktr\.ee/([a-zA-Z0-9_\.]{3,30})', decoded)
                ig = clean_handle(ig_m.group(1)) if ig_m else None
                if not ig and lt_m:
                    ig = clean_handle(lt_m.group(1))
                if ig:
                    leads.append({
                        "nome": format_mentor_name(ig),
                        "instagram": ig,
                        "comoEncontrei": "Yahoo Web Search",
                        "observacoes": f"Link encontrado no Yahoo: {decoded}",
                        "prioridade": "alta"
                    })
    except Exception:
        pass
    return leads

def search_youtube_mentors(query):
    leads = []
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(query + ' kiwify linktree mentoria')}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=3.5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            video_matches = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
            unique_vids = list(dict.fromkeys(video_matches))[:6]
            
            def parse_video(vid):
                v_url = f"https://www.youtube.com/watch?v={vid}"
                v_req = urllib.request.Request(v_url, headers=HEADERS)
                try:
                    with urllib.request.urlopen(v_req, timeout=2.5) as v_resp:
                        v_html = v_resp.read().decode('utf-8', errors='ignore')
                        author_m = re.search(r'"author":"([^"]+)"', v_html)
                        author = author_m.group(1) if author_m else ""
                        title_m = re.search(r'<title>(.*?)</title>', v_html)
                        title = title_m.group(1).replace(' - YouTube', '').strip() if title_m else ""
                        
                        sd_m = re.search(r'"shortDescription":"(.*?)"', v_html)
                        desc = sd_m.group(1) if sd_m else ""
                        try:
                            desc = desc.encode('utf-8').decode('unicode_escape', errors='ignore')
                        except Exception:
                            pass
                        
                        combined = f"{desc} {v_html[:5000]}"
                        ig_m = re.search(r'instagram\.com/([a-zA-Z0-9_\.]{3,30})', combined)
                        lt_m = re.search(r'linktr\.ee/([a-zA-Z0-9_\.]{3,30})', combined)
                        kw_m = re.search(r'https?://(?:pay\.)?kiwify\.com\.br/[a-zA-Z0-9_.-]+', combined)
                        
                        ig = clean_handle(ig_m.group(1)) if ig_m else None
                        if not ig and lt_m:
                            ig = clean_handle(lt_m.group(1))
                        
                        if ig:
                            nome = author if (author and not any(k in author.lower() for k in ["cursos", "oficial", "instituto", "canal"])) else format_mentor_name(ig, title)
                            obs = f"Vídeo YouTube: {title[:70]}"
                            if kw_m:
                                obs += f" | Checkout: {kw_m.group(0)}"
                            return {
                                "nome": nome,
                                "instagram": ig,
                                "comoEncontrei": "YouTube + Instagram",
                                "observacoes": obs,
                                "prioridade": "alta"
                            }
                except Exception:
                    pass
                return None

            with ThreadPoolExecutor(max_workers=5) as ex:
                results = list(filter(None, ex.map(parse_video, unique_vids)))
                leads.extend(results)
    except Exception:
        pass
    return leads

def main():
    parser = argparse.ArgumentParser(description="Minerador de Mentores ao Vivo")
    parser.add_argument("--query", "-q", type=str, default="", help="Termo de busca")
    parser.add_argument("--nicho", "-n", type=str, default="Geral", help="Nicho de atuação")
    args = parser.parse_args()

    query = args.query.strip()
    nicho = args.nicho.strip() or "Carreiras Policiais"

    if not query:
        query = f"mentoria {nicho}"

    tasks = [
        (search_bing, f'site:instagram.com "mentoria" {query}'),
        (search_bing, f'site:linktr.ee "mentoria" {query}'),
        (search_bing, f'"{query}" mentoria concurso instagram'),
        (search_ddg, f'site:instagram.com mentoria {query}'),
        (search_yahoo, f'site:instagram.com mentoria {query}'),
        (search_youtube_mentors, query)
    ]

    all_leads = []
    seen_instagrams = set()

    with ThreadPoolExecutor(max_workers=6) as executor:
        future_to_task = {executor.submit(fn, q): q for fn, q in tasks}
        for future in as_completed(future_to_task, timeout=5.5):
            try:
                res = future.result()
                if res and isinstance(res, list):
                    for lead in res:
                        ig = lead.get("instagram")
                        if ig and ig not in seen_instagrams and ig not in BLOCKLIST_GIGANTES:
                            seen_instagrams.add(ig)
                            lead["nicho"] = nicho
                            all_leads.append(lead)
            except Exception:
                pass

    # Enriquecimento com catálogo calibrado por relevância
    query_lower = query.lower()
    nicho_lower = nicho.lower()

    for seed in CALIBRATED_SEEDS:
        seed_ig = seed["instagram"].lower()
        if seed_ig in seen_instagrams:
            continue
        
        seed_nicho = seed["nicho"].lower()
        seed_nome = seed["nome"].lower()
        seed_obs = seed["observacoes"].lower()
        
        # Só inclui se o nicho for compatível
        is_match = False
        if nicho_lower in seed_nicho or seed_nicho in nicho_lower:
            is_match = True
        elif nicho_lower == "geral" and any(w in f"{seed_nome} {seed_obs} {seed_nicho}" for w in query_lower.split() if len(w) > 3):
            is_match = True

        if is_match:
            seen_instagrams.add(seed_ig)
            item = dict(seed)
            if nicho and nicho.lower() != "geral":
                item["nicho"] = nicho
            all_leads.append(item)

    response = {
        "leads": all_leads
    }
    
    # Imprime no stdout exatamente o JSON solicitado
    print(json.dumps(response, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
