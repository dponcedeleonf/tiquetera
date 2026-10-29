"""Gran Teatro Nacional: arma la lista de eventos (slug, fechas, categoría) desde /calendario/AAAAMM."""
import re, sys, json, collections
sys.path.insert(0, __import__("os").path.dirname(__file__))
from comun import bajar

DESDE = "2026-09-17"   # hoy (29-10-2026) menos 6 semanas
MESES = ["202609", "202610", "202611", "202612", "202701"]
EXCLUIR_CAT = {"Montaje", "Accesible", "Descanso", "Noticias"}


def eventos_mes(html):
    for td in re.finditer(r'date-date="(\d{4}-\d{2}-\d{2})"(.*?)</td>', html, re.S):
        fecha, cuerpo = td.group(1), td.group(2)
        for m in re.finditer(r'<time datetime="[\dT:-]+Z">([^<]+)</time>\s*<div>.*?href="/evento/([^"]+)">\s*([^<]+?)</a>.*?<img alt="[^"]*" src="([^"]+)".*?category\s*[^"]*">\s*([^<]+?)\s*</div>', cuerpo, re.S):
            hora, slug, titulo, img, cat = m.groups()
            yield dict(fecha=fecha, hora=hora.strip(), slug=slug, titulo=titulo.strip(), img=img, cat=cat.strip())


def recolectar():
    por_slug = collections.OrderedDict()
    for mes in MESES:
        html = bajar(f"https://granteatronacional.pe/calendario/{mes}" if mes != "202610" else "https://granteatronacional.pe/calendario", "gtn")
        for e in eventos_mes(html):
            if e["fecha"] < DESDE or e["cat"] in EXCLUIR_CAT:
                continue
            if re.search(r"montaje|visita gtn", e["titulo"], re.I):
                continue
            d = por_slug.setdefault(e["slug"], {**e, "funciones": []})
            if (e["fecha"], e["hora"]) not in d["funciones"]:
                d["funciones"].append((e["fecha"], e["hora"]))
    return list(por_slug.values())


if __name__ == "__main__":
    evs = recolectar()
    for e in evs:
        print(e["slug"], "|", e["cat"], "|", e["funciones"])
    print(len(evs))
