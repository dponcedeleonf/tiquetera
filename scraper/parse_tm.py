"""Convierte las páginas descargadas de Ticketmaster Perú en registros.

Ticketmaster publica un JSON-LD de tipo Event (nombre, sala, dirección, fechas de inicio y fin)
y el resto (precios, elenco, horarios) va en texto libre, que se guarda para extraerlo con IA.
Salida: data/ticketmaster.json
"""
import json
import pathlib
import re

from bs4 import BeautifulSoup

RAIZ = pathlib.Path(__file__).parent
PAGINAS = RAIZ / "raw" / "tm_pages"
SALIDA = RAIZ / "data" / "ticketmaster.json"


def parsear(slug, html):
    ld = {}
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try:
            datos = json.loads(m.group(1))
        except ValueError:
            continue
        if isinstance(datos, dict) and datos.get("@type") == "Event":
            ld = datos
            break
    s = BeautifulSoup(html, "html.parser")
    og = lambda p: (s.find("meta", property=f"og:{p}") or {}).get("content")
    for t in s(["script", "style", "noscript", "svg"]):
        t.decompose()
    texto = " ".join(s.get_text(" ").split()) if s.body else ""
    texto = texto.replace("Disculpa, detectamos actividad sospechosa Cancelar compra", "")
    lugar = ld.get("location") or {}
    direccion = lugar.get("address") or {}
    return {
        "fuente": "ticketmaster",
        "url": f"https://www.ticketmaster.pe/event/{slug}",
        "titulo": ld.get("name") or og("title"),
        "lugar": lugar.get("name"),
        "direccion": direccion.get("streetAddress"),
        "localidad": direccion.get("addressLocality"),
        "inicio": ld.get("startDate"),
        "fin": ld.get("endDate"),
        "fechas_texto": ld.get("description"),
        "imagen": ld.get("image") or og("image"),
        "descripcion": texto[:8000],
    }


def main():
    registros = [parsear(p.stem, p.read_text(encoding="utf-8", errors="ignore"))
                 for p in sorted(PAGINAS.glob("*.html"))]
    SALIDA.parent.mkdir(exist_ok=True)
    json.dump(registros, open(SALIDA, "w"), ensure_ascii=False, indent=1)
    print(f"{len(registros)} eventos -> {SALIDA}")


if __name__ == "__main__":
    main()
