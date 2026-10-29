# Extrae texto legible (título, fecha, cuerpo) de una página de prensa guardada. Uso: python3 texto_html.py archivo.html [max_chars]
import sys, re, json
from bs4 import BeautifulSoup
s = BeautifulSoup(open(sys.argv[1], encoding='utf-8', errors='ignore').read(), 'html.parser')
fecha = None
for sc in s.find_all('script', type='application/ld+json'):
    try:
        d = json.loads(sc.string or '')
        for x in (d if isinstance(d, list) else [d]):
            fecha = fecha or x.get('datePublished')
    except Exception:
        pass
for t in s(['script', 'style', 'noscript', 'nav', 'footer', 'header', 'aside']): t.decompose()
art = s.find('article') or s.body
txt = '\n'.join(l.strip() for l in art.get_text('\n').splitlines() if len(l.strip()) > 2)
print('TITLE:', s.title.string if s.title else None, '| FECHA:', fecha)
print(txt[:int(sys.argv[2]) if len(sys.argv) > 2 else 4000])
