import urllib.request
import urllib.parse
import re
import json
import html
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

FB_UA = 'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)'

# Targeted search queries by niche
QUERIES = [
    # 1. Tribunais Estaduais (TJSP, TJMG, TJPE, TRT, MPU)
    ("Tribunais", "mentoria TJSP"),
    ("Tribunais", "mentoria escrevente TJSP"),
    ("Tribunais", "mentoria TRT"),
    ("Tribunais", "cronograma TJSP aprovado"),
    ("Tribunais", "mentoria analista judiciario"),
    ("Tribunais", "mentoria TJMG"),
    ("Tribunais", "mentoria MPU"),
    ("Tribunais", "mentoria TJPE"),
    ("Tribunais", "mentoria TJBA"),
    ("Tribunais", "mentoria TRF"),

    # 2. Saúde / Enfermagem
    ("Saúde / Enfermagem", "mentoria EBSERH"),
    ("Saúde / Enfermagem", "mentoria enfermagem concursos"),
    ("Saúde / Enfermagem", "cronograma EBSERH enfermagem"),
    ("Saúde / Enfermagem", "mentoria residencia enfermagem"),
    ("Saúde / Enfermagem", "enfermeira aprovada mentoria"),
    ("Saúde / Enfermagem", "mentoria saude concursos"),

    # 3. Pedagogia / Educação
    ("Pedagogia / Educação", "mentoria pedagogia concurso"),
    ("Pedagogia / Educação", "mentoria concurso professor"),
    ("Pedagogia / Educação", "cronograma concurso pedagogia"),
    ("Pedagogia / Educação", "mentoria professor prefeitura"),
    ("Pedagogia / Educação", "mentoria concurso educacao"),
    ("Pedagogia / Educação", "aprovada concurso professor mentoria"),

    # 4. Prefeituras / Área Administrativa
    ("Prefeituras / Adm", "mentoria concurso prefeitura"),
    ("Prefeituras / Adm", "cronograma concurso prefeitura"),
    ("Prefeituras / Adm", "mentoria agente administrativo"),
    ("Prefeituras / Adm", "mentoria guarda municipal"),
    ("Prefeituras / Adm", "mentoria assistente administrativo prefeitura"),
    ("Prefeituras / Adm", "cronograma assistente de gestao de politicas publicas"),

    # 5. Fiscal / Controle
    ("Fiscal / Controle", "mentoria auditor fiscal"),
    ("Fiscal / Controle", "mentoria ISS concurso"),
    ("Fiscal / Controle", "mentoria sefaz aprovado"),
    ("Fiscal / Controle", "cronograma auditor fiscal"),
    ("Fiscal / Controle", "mentoria analista tributario"),

    # 6. Redação / Isoladas
    ("Redação / Isoladas", "mentoria redacao concurso"),
    ("Redação / Isoladas", "mentoria discursiva tribunais"),
    ("Redação / Isoladas", "mentoria redacao tjsp"),
    ("Redação / Isoladas", "correcao discursiva concurso mentoria"),
    ("Redação / Isoladas", "mentoria portugues para concursos"),
    ("Redação / Isoladas", "mentoria rlm concurso")
]

print(f"Starting YouTube Search across {len(QUERIES)} targeted queries...")

video_targets = []
seen_vids = set()

for niche, q in QUERIES:
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', content)
            count = 0
            for vid in ids[:8]:
                if vid not in seen_vids:
                    seen_vids.add(vid)
                    video_targets.append((vid, niche, q))
                    count += 1
            print(f"Query '{q}' ({niche}) -> Added {count} videos (Total: {len(video_targets)})")
    except Exception as e:
        print(f"Error querying '{q}': {e}")
    time.sleep(0.5)

print(f"\nTotal unique videos collected: {len(video_targets)}")

with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\yt_targets.json', 'w', encoding='utf-8') as f:
    json.dump(video_targets, f, ensure_ascii=False, indent=2)
