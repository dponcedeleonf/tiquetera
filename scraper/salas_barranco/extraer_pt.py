# Imprime la parte útil (título, sala, sinopsis, ficha, funciones) de las páginas de Puro Teatro renderizadas.
import sys, glob, re, json, os
d = sys.argv[1]
pat = sys.argv[2] if len(sys.argv) > 2 else 'puroteatro_pe_obra_teatral_'
for f in sorted(glob.glob(os.path.join(d, pat + '*.txt'))):
    t = open(f, encoding='utf-8').read()
    url = t.split('\n', 1)[0]
    a = t.find('Volver a cartelera'); b = t.find('🎭 Guía')
    body = t[a + 18:b] if a >= 0 else t[:1500]
    body = re.sub(r'Compartir obra\nCompartir en Facebook\nCompartir en X\nCopiar enlace\n', '', body)
    body = re.sub(r'\n\s*\n+', '\n', body)
    lk = json.load(open(f[:-4] + '.links.json'))
    compra = [h for tx, h in lk['links'] if 'BOLETER' in tx.upper()]
    print('=' * 8, url); print(body.strip()); print('COMPRA:', compra[:2]); print('IMG:', lk['meta'].get('og:image'))
