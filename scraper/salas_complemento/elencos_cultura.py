"""Recorre la agenda de Elencos Nacionales del Ministerio de Cultura (elencos.cultura.pe)
mes a mes y guarda cada evento con su lugar en raw/salas_complemento/elencos_eventos.json.
Uso: python3 salas_complemento/elencos_cultura.py 202609 202610 202611 202612 202701"""
import json, re, sys, pathlib
from bs4 import BeautifulSoup
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from bajar import bajar, texto, CACHE

meses = sys.argv[1:] or ["202609", "202610", "202611", "202612"]
eventos = {}
for m in meses:
    url = f"https://elencos.cultura.pe/eventos/{m}?tid=All"
    html = bajar(url)
    s = BeautifulSoup(html, "html.parser")
    for a in s.find_all("a", href=True):
        if "/evento/" in a["href"]:
            u = a["href"] if a["href"].startswith("http") else "https://elencos.cultura.pe" + a["href"]
            u = u.replace("/index.php/", "/")
            eventos.setdefault(u, {"mes": m})
out = []
for u, ev in eventos.items():
    t = texto(bajar(u))
    cuerpo = t.split("Compañía de Ballet de Trujillo\nEventos\nContacto\n", 1)[-1]
    cuerpo = cuerpo.split("¡Más cerca de ti!")[0]
    lineas = cuerpo.splitlines()
    ev.update(url=u, titulo=lineas[0] if lineas else None, texto=cuerpo[:3000])
    m = re.search(r"Día y Hora\n(.+?)\n", cuerpo)
    ev["fecha"] = m.group(1) if m else None
    m = re.search(r"Lugar:\n(.+?)\n(.+?)\n", cuerpo)
    ev["lugar"] = (m.group(1) + " | " + m.group(2)) if m else None
    out.append(ev)
    print(ev["fecha"], "|", ev["titulo"], "|", ev["lugar"], "|", u)
(CACHE / "elencos_eventos.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
