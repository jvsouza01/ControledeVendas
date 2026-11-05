#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditor de Perfis do Instagram (Frutas Baixas vs Dead/Famous)
Ecossistema Trajetória - Controle de Vendas CRM
"""

import sys
import os
import re
import json
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

USER_AGENTS = [
    "TelegramBot (like TwitterBot)",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Twitterbot/1.0",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
]

def parse_followers(text):
    if not text:
        return None, ""
    m = re.search(r'([0-9.,]+[KkMm]?)\s+(?:seguidores|followers)', text, re.IGNORECASE)
    if not m:
        return None, ""
    raw = m.group(1).upper()
    try:
        if 'M' in raw:
            val = float(raw.replace('M', '').replace(',', '.')) * 1_000_000
        elif 'K' in raw:
            val = float(raw.replace('K', '').replace(',', '.')) * 1_000
        else:
            clean = raw.replace('.', '').replace(',', '')
            val = float(clean)
        return int(val), raw
    except Exception:
        return None, raw

def check_instagram_handle(lead):
    handle = lead["instagram"].strip().lstrip('@')
    url = f"https://www.instagram.com/{handle}/"
    
    result = {
        "id": lead["id"],
        "nome": lead["nome"],
        "instagram": handle,
        "nicho": lead.get("nicho", ""),
        "url": url,
        "exists": False,
        "title": "",
        "og_title": "",
        "og_description": "",
        "followers_count": None,
        "followers_raw": "",
        "status_code": None,
        "category": "DEAD", # DEAD, FAMOUS, APPROVED
        "reason": ""
    }

    # Tenta com os User-Agents especificados
    success = False
    for ua in USER_AGENTS:
        req = urllib.request.Request(url, headers={
            'User-Agent': ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        })
        try:
            with urllib.request.urlopen(req, timeout=4.5) as resp:
                result["status_code"] = resp.getcode()
                html = resp.read().decode('utf-8', errors='ignore')

                og_title_m = re.search(r'<meta\s+property="og:title"\s+content="([^"]*)"', html)
                og_desc_m = re.search(r'<meta\s+property="og:description"\s+content="([^"]*)"', html)
                title_tag_m = re.search(r'<title>(.*?)</title>', html)

                title_val = title_tag_m.group(1) if title_tag_m else ""
                og_title_val = og_title_m.group(1) if og_title_m else ""
                og_desc_val = og_desc_m.group(1) if og_desc_m else ""

                result["title"] = title_val
                result["og_title"] = og_title_val
                result["og_description"] = og_desc_val

                # Se temos og:title ou og:description contendo o handle ou seguidores, o perfil existe!
                if og_title_val or (og_desc_val and ('seguidores' in og_desc_val.lower() or 'followers' in og_desc_val.lower())):
                    result["exists"] = True
                    followers_num, followers_raw = parse_followers(og_desc_val)
                    result["followers_count"] = followers_num
                    result["followers_raw"] = followers_raw
                    success = True
                    break
                elif title_val and title_val.strip().lower() != "instagram":
                    # Título customizado com nome do perfil
                    result["exists"] = True
                    followers_num, followers_raw = parse_followers(og_desc_val)
                    result["followers_count"] = followers_num
                    result["followers_raw"] = followers_raw
                    success = True
                    break
        except urllib.error.HTTPError as e:
            result["status_code"] = e.code
            if e.code == 404:
                # Perfil definitivamente não existe
                result["exists"] = False
                result["reason"] = "HTTP 404 - Perfil Inexistente"
                return result
        except Exception as e:
            result["reason"] = str(e)
            time.sleep(0.3)

    if not result["exists"]:
        result["category"] = "DEAD"
        result["reason"] = "Não retornou metadados de perfil (página vazia / redirecionamento / não existe)"
    else:
        f_count = result["followers_count"]
        if f_count is not None and f_count > 25_000:
            result["category"] = "FAMOUS"
            result["reason"] = f"Possui {result['followers_raw']} seguidores (> 25.000)"
        else:
            result["category"] = "APPROVED"
            result["reason"] = f"Aprovado: {result['followers_raw'] or 'perfil ativo'} seguidores (<= 25.000)"

    return result

def extract_fb_leads_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex para capturar cada objeto Lead individual
    pattern = re.compile(
        r'\{\s*"id":\s*"(fb_[^"]+)",\s*"nome":\s*"([^"]+)",\s*"instagram":\s*"([^"]+)",\s*"nicho":\s*"([^"]+)"',
        re.DOTALL
    )

    leads = []
    for m in pattern.finditer(content):
        leads.append({
            "id": m.group(1),
            "nome": m.group(2),
            "instagram": m.group(3),
            "nicho": m.group(4)
        })
    return leads

def main():
    base_dir = r"c:\Users\jao_v\Desktop\ControledeVendas"
    leads_path = os.path.join(base_dir, "src", "data", "initialLeads.ts")
    output_json_path = os.path.join(base_dir, "minerador", "auditoria_initial_leads.json")

    print(f"Lendo leads de: {leads_path}")
    leads = extract_fb_leads_from_file(leads_path)
    print(f"Total de leads 'fb_' encontrados: {len(leads)}")

    print(f"\nIniciando auditoria ao vivo no Instagram de {len(leads)} perfis...")
    t0 = time.time()

    results = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(check_instagram_handle, lead): lead for lead in leads}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            status_icon = "❌ DEAD" if res["category"] == "DEAD" else ("⭐ FAMOUS" if res["category"] == "FAMOUS" else "✅ OK")
            followers_str = f"({res['followers_raw']})" if res['followers_raw'] else ""
            print(f"[{status_icon}] @{res['instagram']:<25} {followers_str:<12} | {res['nome']}")

    # Ordena pelo ID
    def parse_id(item):
        try:
            return int(item["id"].replace("fb_", ""))
        except:
            return 9999
    results.sort(key=parse_id)

    dead_handles = [r for r in results if r["category"] == "DEAD"]
    famous_handles = [r for r in results if r["category"] == "FAMOUS"]
    approved_handles = [r for r in results if r["category"] == "APPROVED"]

    summary = {
        "audited_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_audited": len(results),
        "total_dead": len(dead_handles),
        "total_famous": len(famous_handles),
        "total_approved": len(approved_handles),
        "dead_handles": dead_handles,
        "famous_handles": famous_handles,
        "approved_handles": approved_handles,
        "all_results": results
    }

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    elapsed = time.time() - t0
    print("\n" + "="*70)
    print(f"AUDITORIA CONCLUÍDA EM {elapsed:.2f}s!")
    print(f"Total Auditados: {len(results)}")
    print(f"❌ DEAD HANDLES (Quebrados/Não abrem): {len(dead_handles)}")
    print(f"⭐ FAMOUS HANDLES (> 25k seguidores): {len(famous_handles)}")
    print(f"✅ APPROVED HANDLES (Micro-mentores válidos <= 25k): {len(approved_handles)}")
    print(f"Arquivo salvo em: {output_json_path}")
    print("="*70)

if __name__ == "__main__":
    main()
