"""Busca coordenadas de los espacios en Nominatim (OpenStreetMap) por NOMBRE dentro de Barranco.
Solo acepta resultados que sean un lugar con nombre (no una calle) y que estén en Barranco. 1 petición/segundo.
Salida: ../raw/barranco/geocod.json
"""
import json, time, pathlib, requests, unicodedata
RAIZ = pathlib.Path(__file__).resolve().parent.parent
S = requests.Session(); S.headers['User-Agent'] = 'tiquetera-prototipo/1.0 (dponcedeleonf)'
NOMBRES = ['La Noche de Barranco', 'Sargento Pimienta', 'El Dragón', 'Centro de Convenciones Bianca', 'Bianca',
           'Centro de Convenciones Barranco', 'Aforo', 'La Casa Roja', 'Casa Bulbo', 'Sala Osma', 'Barranco Bar',
           'Peña Don Porfirio', 'Don Porfirio', 'La Oficina', 'Del Carajo', 'Posada del Mirador', 'Teatro Esencia',
           'Quilla', 'Capital Restobar', 'El Roble', 'La Candelaria', 'Teatro Barranco', 'PayaCasa']
def n(s): return ''.join(c for c in unicodedata.normalize('NFKD', s.lower()) if not unicodedata.combining(c))
out = {}
for nombre in NOMBRES:
    r = S.get('https://nominatim.openstreetmap.org/search', params={'q': nombre + ', Barranco, Lima, Peru', 'format': 'json', 'limit': 5, 'addressdetails': 1}, timeout=30)
    time.sleep(1.2)
    cands = []
    for x in r.json():
        if x.get('class') == 'highway':
            continue
        if 'barranco' not in n(x.get('display_name', '')):
            continue
        cands.append({'name': x.get('name'), 'class': x.get('class'), 'type': x.get('type'), 'lat': x['lat'], 'lon': x['lon'], 'display': x['display_name'][:140]})
    out[nombre] = cands
    print(nombre, '->', [(c['name'], c['type'], c['lat'], c['lon']) for c in cands][:3])
json.dump(out, open(RAIZ / 'raw' / 'barranco' / 'geocod.json', 'w'), ensure_ascii=False, indent=1)
