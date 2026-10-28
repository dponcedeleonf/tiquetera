"""Convierte las páginas descargadas de Teleticket en registros ordenados.

Entrada: raw/tt_listing.json y raw/pages/*.html (ver fetch_tt.py).
Salida: data/teleticket.json, un registro por página de evento con funciones y precios.
"""
import html as htmlmod
import json
import pathlib
import re

from bs4 import BeautifulSoup

RAIZ = pathlib.Path(__file__).parent
PAGINAS = RAIZ / "raw" / "pages"
SALIDA = RAIZ / "data" / "teleticket.json"

MESES = {m: i for i, m in enumerate(
    ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
     "setiembre", "octubre", "noviembre", "diciembre"], 1)}
MESES["septiembre"] = 9


def texto(nodo, sep=" "):
    return " ".join(nodo.get_text(sep).split()) if nodo else ""


def anios_del_listado(fechas_texto):
    """'28 de octubre 2026 - 20 de noviembre 2026' -> [(10, 2026), (11, 2026)]"""
    return [(MESES[m], int(a)) for m, a in re.findall(r"de (\w+) (\d{4})", fechas_texto.lower()) if m in MESES]


def inferir_anio(mes, extremos):
    """Las funciones no traen año: se toma el del rango del listado que encaje."""
    if not extremos:
        return None
    (m0, a0), (m1, a1) = extremos[0], extremos[-1]
    if a0 == a1:
        return a0
    return a0 if mes >= m0 else a1


def precios_de(html_precios):
    """'<strong>REGULAR:</strong>&nbsp;&nbsp;S/ 42.00 - S/ 126.00 ...'
    -> [{'categoria': 'REGULAR', 'precio_min': 42.0, 'precio_max': 126.0}]"""
    limpio = htmlmod.unescape(re.sub(r"<[^>]+>", " ", html_precios or ""))
    numero = lambda x: float(x.replace(",", ""))
    return [{"categoria": c.strip(), "precio_min": numero(a), "precio_max": numero(b or a)}
            for c, a, b in re.findall(r"([A-ZÁÉÍÓÚÑ0-9 .\-/]+?):\s*S/\s*([\d.,]+)(?:\s*-\s*S/\s*([\d.,]+))?", limpio)]


def parsear(html, extremos):
    s = BeautifulSoup(html, "html.parser")
    og = lambda p: (s.find("meta", property=f"og:{p}") or {}).get("content")
    canonical = s.find("link", rel="canonical")
    codigos = re.findall(r"EventoID=([A-Z0-9]+)", html)

    funciones = []
    for card in s.select("#funciones-listado-accordion > .card"):
        dia = texto(card.select_one("strong.name"))
        mes_hora = texto(card.select_one("time"))
        m = re.match(r"(\w+)\s+(\d{1,2}:\d{2})", mes_hora)
        n = re.search(r"(\d{1,2})", dia)
        if not (m and n):
            continue
        mes = MESES.get(m.group(1).lower())
        anio = inferir_anio(mes, extremos) if mes else None
        header = card.select_one(".card-header")
        funciones.append({
            "fecha": f"{anio:04d}-{mes:02d}-{int(n.group(1)):02d}" if (mes and anio) else None,
            "hora": m.group(2),
            "disponible": not ("disabled" in (header.get("class") or [])),
            "precios": precios_de(str(card.select_one("#prices") or "")),
        })

    # Si no hubo acordeón, intentar con el objeto JS horasPorFecha.
    if not funciones:
        js = re.search(r"var horasPorFecha = (\{.*?\});\s*\n", html, re.S)
        if js:
            try:
                for lista in json.loads(js.group(1)).values():
                    for f in lista:
                        fecha, hora = f["Fecha"].split("T")
                        funciones.append({"fecha": fecha, "hora": hora[:5], "disponible": True,
                                          "precios": precios_de(f.get("HtmlPrecios"))})
            except (ValueError, KeyError):
                pass

    descripcion = s.select_one(".slider-content")
    if descripcion:
        descripcion = texto(descripcion, "\n")
    else:
        # Landing especial con formato libre: se guarda el texto visible para extraerlo con IA.
        for t in s(["script", "style", "noscript"]):
            t.decompose()
        descripcion = texto(s.body, "\n")[:8000] if s.body else ""
    return {
        "titulo": texto(s.select_one("h2.h1")) or (og("title") or "").removeprefix("Entradas ").strip(),
        "codigo": codigos[0] if codigos else None,
        "url_canonica": canonical["href"] if canonical else og("url"),
        "imagen": og("image"),
        "meta_descripcion": og("description"),
        "descripcion": descripcion,
        "funciones": funciones,
    }


def archivo_de(url):
    return PAGINAS / (re.sub(r"[^a-zA-Z0-9_-]+", "_", url.split("teleticket.com.pe/")[-1]).strip("_")[:150] + ".html")


def main():
    listado = json.load(open(RAIZ / "raw" / "tt_listing.json"))
    registros = []
    for ev in listado:
        ruta = archivo_de(ev["url"])
        detalle = parsear(ruta.read_text(encoding="utf-8", errors="ignore"), anios_del_listado(ev["fechas_texto"])) if ruta.exists() else {}
        registros.append({"fuente": "teleticket", **ev, "detalle": detalle})
    SALIDA.parent.mkdir(exist_ok=True)
    json.dump(registros, open(SALIDA, "w"), ensure_ascii=False, indent=1)
    con_func = sum(1 for r in registros if r["detalle"].get("funciones"))
    print(f"{len(registros)} eventos, {con_func} con funciones -> {SALIDA}")


if __name__ == "__main__":
    main()
