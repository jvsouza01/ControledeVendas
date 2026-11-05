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
    current_verified = {x['handle']: x for x in json.load(f)}

print(f"Already verified in list: {len(current_verified)}")
print(f"Existing handles in initialLeads.ts: {len(existing_handles)}")

candidate_catalog = [
    ("ayresbarros", "Prof. Ayres Barros", "Kiwify + YouTube", "Mentor independente especialista em Polícia Penal (PPCE/PPAL) e PC. Vende mentoria individual e cronograma na Kiwify."),
    ("joaolisboa_concursos", "João Lisboa | Projeto Bravo", "Linktree + Instagram", "Fundador do Projeto Bravo. Mentoria focada em PCPR, PCSC e polícias civis."),
    ("fxconcursospublicos", "FX Concursos (Prof. Flavio)", "Página de Vendas / WhatsApp", "Mentoria e preparação regional focada em Soldado e Oficial CFO PMMG."),
    ("pmminas", "Otávio Souza | Método OBA", "Hotmart + Instagram", "Mentoria focada exclusivamente em Soldado PMMG e CBMMG."),
    ("miguelangelopmmg", "Miguel Ângelo | Mapeada PMMG", "Linktree + Instagram", "Mentoria Mapeada PMMG. Policial da ativa que orienta concurseiros em turmas pequenas."),
    ("metodopm", "Método PM (Soldado PMESP)", "Linktree + Instagram", "Mentoria independente para Soldado PMESP. Foco na Vunesp e edital verticalizado."),
    ("bizu_com_vagnao", "Vagnão | Bizu com Vagnão", "Hotmart + YouTube", "Oficial PMESP com mentoria e guia de revisão para Soldado e Barro Branco."),
    ("erickbiaggi_", "Erick Biaggi", "Instagram Outbound", "Mentoria para etapas práticas e psicológicas da PMESP."),
    ("manualdomike", "Manual do Mike", "Kiwify + Instagram", "Mentoria e planejamento estratégico para PMBA, PMPE, PMAL e PMESP."),
    ("prof.rafaelvalle", "Prof. Rafael Valle", "Linktree + Instagram", "Coordenador da mentoria 'O Distintivo é Nosso' para PC-SC, PC-DF e PC-SP."),
    ("pfem.anakarolina", "Ana Karolina (Pfem)", "Instagram Outbound", "Mentoria focada em mulheres para carreiras policiais (PC e PM)."),
    ("eduardodefaveri", "Eduardo Defaveri", "Página de Vendas", "Mentoria individualizada para Delegado de Polícia Civil."),
    ("lucaspetry", "Lucas Petry | Petry Consultoria", "Linktree + Instagram", "Petry Consultoria e Mentoria para Carreiras Policiais e Delegado."),
    ("fernandococito", "Fernando Cocito | FC3", "Instagram Outbound", "Delegado de Polícia e mentor de fase oral e discursiva para PC."),
    ("aconcurseirataon", "A Concurseira Tá On", "Kiwify + YouTube", "Projeto Treinamento Azul Marinho voltado para Guarda Civil Municipal (GCM)."),
    ("fzconcursos", "FZ Concursos", "WhatsApp + YouTube", "Mentoria e cadernos de questões para concursos de Guardas Municipais e Prefeituras."),
    ("irmaospolicia", "Irmãos Polícia (PCMG)", "Linktree + Instagram", "Policiais Civis de MG com mentoria e cronograma focado em Investigador e Escrivão PCMG."),
    ("rumo01aprovacao", "Rumo à Aprovação", "Linktree + Instagram", "Mentoria regionalizada focada em Soldado PMBA e PMPE."),
    ("rodrigocavalcantiprof", "Prof. Rodrigo Cavalcanti", "Hotmart + Instagram", "Professor e mentor de Direito Penal e Legislação para carreiras policiais."),
    # Extra police mentors known from regional markets
    ("mentoria.barbosa", "Mentoria Barbosa", "Instagram Outbound", "Mentoria focada em Soldado PMBA."),
    ("conteudos.pmba", "Conteúdos PMBA", "Instagram Outbound", "Mentoria e cronograma para PMBA."),
    ("ferreira_34ba", "Ferreira Mentoria PM e PCBA", "Instagram Outbound", "Mentoria individual para PMBA e PCBA."),
    ("mentor.policial", "Mentor Policial", "Instagram Outbound", "Mentoria para carreiras policiais."),
    ("mentoriapmce", "Mentoria PMCE", "Instagram Outbound", "Mentoria para Soldado PMCE."),
    ("mentoriapmpb", "Mentoria PMPB", "Instagram Outbound", "Mentoria para Soldado PMPB."),
    ("mentoriapmma", "Mentoria PMMA", "Instagram Outbound", "Mentoria para Soldado PMMA."),
    ("mentoriapmpa", "Mentoria PMPA", "Instagram Outbound", "Mentoria para Soldado PMPA."),
    ("mentoriapmrn", "Mentoria PMRN", "Instagram Outbound", "Mentoria para Soldado PMRN."),
    ("mentoriapmgo", "Mentoria PMGO", "Instagram Outbound", "Mentoria para Soldado PMGO."),
    ("mentoriapmtocantins", "Mentoria PMTO", "Instagram Outbound", "Mentoria para Soldado PMTO."),
    ("gcm_brasil_oficial", "GCM Brasil Oficial", "Instagram Outbound", "Mentoria e preparação para Guardas Municipais."),
    ("mentoriagcm", "Mentoria GCM", "Instagram Outbound", "Mentoria e cronogramas para GCM."),
    ("mentoriapoliciarecruta", "Mentoria Recruta Policial", "Instagram Outbound", "Mentoria e cronograma para PMs do Nordeste."),
    ("missaopolicia", "Missão Polícia", "Instagram Outbound", "Mentoria e acompanhamento para concursos policiais."),
    ("policiapenalmentor", "Polícia Penal Mentor", "Instagram Outbound", "Mentoria específica para Polícia Penal estadual."),
    ("tatico_concursos", "Tático Concursos", "Instagram Outbound", "Mentoria focada em Soldado e Oficial PM."),
    ("mentoria_pmba_oficial", "Mentoria PMBA", "Instagram Outbound", "Mentoria para PMBA."),
    ("aprovados.pmba", "Aprovados PMBA", "Instagram Outbound", "Mentoria e dicas para PMBA."),
    ("aprovados.pmpe", "Aprovados PMPE", "Instagram Outbound", "Mentoria e dicas para PMPE."),
    ("foco.gcm", "Foco GCM", "Instagram Outbound", "Mentoria para Guardas Civis Municipais.")
]

googlebot_headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}

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

verified_catalog = []

for item in candidate_catalog:
    h = item[0].lower()
    if h in existing_handles:
        print(f"Skipping @{h} (already in initialLeads.ts)")
        continue
    if h in current_verified:
        print(f"Already in current_verified: @{h}")
        continue
    
    # Check Instagram followers
    url = f"https://www.instagram.com/{h}/"
    req = urllib.request.Request(url, headers=googlebot_headers)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            meta_desc = re.search(r'<meta (?:property="og:description"|name="description") content="([^"]+)"', content)
            raw_desc = html_lib.unescape(meta_desc.group(1)) if meta_desc else ""
            f_count = parse_follower_count(raw_desc)
            if f_count is not None:
                if 200 <= f_count <= 25000:
                    print(f"✅ Verified: @{h} -> {f_count} followers | {item[1]}")
                    verified_catalog.append({
                        'handle': h,
                        'name': item[1],
                        'comoEncontrei': item[2],
                        'observacoes': f"👥 ~{f_count:,} seguidores | {item[3]}".replace(',', '.'),
                        'followers': f_count,
                        'prioridade': 'alta'
                    })
                else:
                    print(f"❌ Size check failed @{h}: {f_count}")
            else:
                # If profile exists but follower count wasn't parsed (e.g. private or no snippet)
                title_m = re.search(r'<title>(.*?)</title>', content)
                t = title_m.group(1) if title_m else ""
                if "Instagram" in t and "Page Not Found" not in t:
                    print(f"ℹ️ Active profile without count: @{h} -> {t}")
    except Exception as e:
        # print(f"@{h} err: {e}")
        pass
    time.sleep(0.4)

print(f"\nNew verified catalog additions: {len(verified_catalog)}")
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\verified_catalog_batch.json', 'w', encoding='utf-8') as f:
    json.dump(verified_catalog, f, ensure_ascii=False, indent=2)
