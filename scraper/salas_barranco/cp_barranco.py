"""Descarga de Conciertos Perú (blog musical, WordPress) los eventos de locales de Barranco publicados
desde junio de 2026 y extrae la fecha del evento del texto. 1 petición/segundo.
Salida: ../raw/barranco/cp/eventos_barranco.json
"""
import json, re, time, html, pathlib, requests
RAIZ = pathlib.Path(__file__).resolve().parent.parent
OUT = RAIZ / 'raw' / 'barranco' / 'cp'
S = requests.Session(); S.headers['User-Agent'] = 'Mozilla/5.0 (prototipo tiquetera; contacto dponcedeleonf)'
LOCALES = {24454: 'Aforo Barranco', 23987: 'Aforo Barranco', 18801: 'Aforo Barranco', 20110: 'Aforo Barranco',
           22812: 'Barranco Arena', 26712: 'Barranco Bar', 24426: 'Centro de Convenciones Barranco',
           8523: 'Centro de Convenciones Barranco', 25741: 'Centro de Convenciones Barranco',
           16238: 'Dédalo Café Barranco', 24672: 'El Dragón de Barranco', 24817: 'El Dragón de Barranco',
           24047: 'Escenario Barranco', 23588: 'La Estación de Barranco', 9094: 'La Noche de Barranco',
           26189: 'Parque Municipal de Barranco', 23524: 'Red Cervecera de Barranco',
           9030: 'Sargento Pimienta', 8558: 'Centro de Convenciones Bianca', 24102: 'Casa Bulbo',
           23867: 'La Casa Roja', 9449: 'La Peña del Carajo', 24055: 'Sala Osma', 23982: 'Casa Bagre',
           23752: 'Casa Poco Floro'}
MESES = {m: i for i, m in enumerate(['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
                                      'setiembre', 'octubre', 'noviembre', 'diciembre'], 1)}
MESES['septiembre'] = 9

def texto(h):
    return ' '.join(html.unescape(re.sub(r'<[^>]+>', ' ', h or '')).split())

def fechas(t, anio_pub):
    out = []
    for d, m, a in re.findall(r'\b(\d{1,2}) de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|setiembre|septiembre|octubre|noviembre|diciembre)(?: (?:de|del) (\d{4}))?', t, re.I):
        a = int(a) if a else anio_pub
        out.append(f'{a:04d}-{MESES[m.lower()]:02d}-{int(d):02d}')
    return sorted(set(out))

eventos = []
for lid, nombre in LOCALES.items():
    pagina = 1
    while True:
        r = S.get('https://conciertosperu.com.pe/wp-json/wp/v2/eventos', params={
            'local': lid, 'per_page': 50, 'page': pagina, 'after': '2026-05-01T00:00:00',
            '_fields': 'id,date,link,title,content,excerpt,local,artista'}, timeout=40)
        time.sleep(1.1)
        if r.status_code != 200:
            break
        lote = r.json()
        for e in lote:
            t = texto(e['content']['rendered'])
            eventos.append({'local_id': lid, 'local': nombre, 'publicado': e['date'][:10], 'url': e['link'],
                            'titulo': html.unescape(e['title']['rendered']), 'resumen': texto(e['excerpt']['rendered']),
                            'fechas': fechas(t, int(e['date'][:4])), 'texto': t[:2500],
                            'enlaces': re.findall(r'href="([^"]+)"', e['content']['rendered'])})
        if len(lote) < 50:
            break
        pagina += 1
    print(nombre, lid, 'acumulado', len(eventos), flush=True)
json.dump(eventos, open(OUT / 'eventos_barranco.json', 'w'), ensure_ascii=False, indent=1)
