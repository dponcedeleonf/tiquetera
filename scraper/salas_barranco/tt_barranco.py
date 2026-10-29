"""Descarga y resume páginas de evento de Teleticket (Barranco) que NO están en el listado actual,
incluidas funciones ya pasadas. 1 petición por segundo.
Uso: python3 tt_barranco.py urls_tt.txt  -> ../raw/barranco/tt/*.html y ../raw/barranco/tt_resumen.json
"""
import sys, re, json, time, html as H, pathlib, requests
from bs4 import BeautifulSoup
RAIZ = pathlib.Path(__file__).resolve().parent.parent
DIR = RAIZ / 'raw' / 'barranco' / 'tt'; DIR.mkdir(parents=True, exist_ok=True)
S = requests.Session(); S.headers['User-Agent'] = 'Mozilla/5.0 (prototipo tiquetera; contacto dponcedeleonf)'
sys.path.insert(0, str(RAIZ))
from parse_tt import precios_de

def nombre(url):
    return re.sub(r'[^a-zA-Z0-9_-]+', '_', url.split('teleticket.com.pe/')[-1]).strip('_')[:150] + '.html'

def bajar(url):
    p = DIR / nombre(url)
    if p.exists():
        return p.read_text(encoding='utf-8', errors='ignore')
    r = S.get(url, timeout=30); time.sleep(1.1)
    if r.status_code != 200:
        print(r.status_code, url); return ''
    p.write_text(r.text, encoding='utf-8'); return r.text

def campo(txt, etiqueta):
    m = re.search(etiqueta + r'\s*:?\s*\n(.+)', txt)
    return m.group(1).strip() if m else None

out = []
SALIDA = sys.argv[2] if len(sys.argv) > 2 else 'tt_resumen.json'
for url in [u.strip() for u in open(sys.argv[1]) if u.strip()]:
    h = bajar(url)
    if not h: continue
    s = BeautifulSoup(h, 'html.parser')
    meta = (s.find('meta', attrs={'name': 'description'}) or {}).get('content') or (s.find('meta', property='og:description') or {}).get('content')
    for t in s(['script', 'style', 'noscript']): t.decompose()
    txt = '\n'.join(l.strip() for l in s.get_text('\n').splitlines() if l.strip())
    i = txt.find('RESEÑA DEL EVENTO'); j = txt.find('INFORMACIÓN IMPORTANTE')
    resena = txt[i + 17:j].strip() if i >= 0 else None
    precios = precios_de(re.sub(r'\n', ' ', txt))
    fechas = re.findall(r'(\d{2}-\d{2}-\d{4}(?: al \d{2}-\d{2}-\d{4})?)\s+(\d{1,2}:\d{2})\s*Hrs', txt)
    out.append({
        'url': url,
        'titulo': (s.find('meta', property='og:title') or {}).get('content'),
        'meta': H.unescape(meta or ''),
        'recinto': campo(txt, 'Recinto'),
        'hora': campo(txt, 'Hora de inicio'),
        'duracion': campo(txt, 'Duración aproximada'),
        'publico': campo(txt, 'Público recomendado'),
        'organiza': campo(txt, 'Organiza'),
        'fechas_hrs': fechas[:10],
        'precios': precios[:8],
        'resena': (resena or '')[:1800],
        'imagen': (s.find('meta', property='og:image') or {}).get('content'),
    })
    print('ok', url)
json.dump(out, open(RAIZ / 'raw' / 'barranco' / SALIDA, 'w'), ensure_ascii=False, indent=1)
