import urllib.request
import urllib.parse
import re
import json

queries = [
    # Tribunais
    'mentoria TJSP concurso',
    'mentoria TRT concurso',
    'mentoria TJMG concurso',
    'mentoria MPU concurso',
    'cronograma TJSP escrevente',
    'cronograma TRT analista',
    
    # Saúde / Enfermagem
    'mentoria EBSERH enfermagem',
    'cronograma EBSERH aprovado',
    'mentoria residencia enfermagem',
    'mentoria enfermagem concursos',
    
    # Pedagogia / Magistério
    'mentoria pedagogia concurso',
    'mentoria concurso professor',
    'cronograma pedagogia concurso',
    
    # Prefeituras / Adm
    'mentoria concurso prefeitura',
    'cronograma concurso prefeitura',
    'mentoria agente administrativo',
    
    # Redação / Isoladas
    'mentoria redação concurso',
    'mentoria discursiva concurso',
    'mentoria redação tjsp',
    'mentoria redação trt',
    
    # Fiscal / Controle
    'mentoria auditor fiscal iss',
    'mentoria sefaz aprovado',
    'cronograma auditor fiscal'
]

video_ids = set()
for q in queries:
    url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            ids = re.findall(r'"videoId":"([a-zA-Z0-9_-]{11})"', html)
            for vid in ids[:8]:
                video_ids.add(vid)
    except Exception as e:
        print(f"Error for {q}: {e}")

print(f"Total video IDs collected: {len(video_ids)}")
with open(r'c:\Users\jao_v\Desktop\ControledeVendas\minerador\yt_video_ids.json', 'w', encoding='utf-8') as f:
    json.dump(list(video_ids), f)
