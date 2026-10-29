"""Baja el listado /todos de Teleticket y lista eventos en salas de Miraflores que no estén en tt_listing.json."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from red import bajar
from bs4 import BeautifulSoup
R = pathlib.Path(__file__).resolve().parent.parent
html = bajar("https://teleticket.com.pe/todos")
soup = BeautifulSoup(html, "html.parser")
viejos = {e["url"] for e in json.load(open(R / "raw/tt_listing.json"))}
out = []
for art in soup.select('article[id^="event_"]'):
    a = art.find("a"); href = a["href"]
    url = "https://teleticket.com.pe" + href if href.startswith("/") else href
    d = art.select_one("p.descripcion"); lugar = d.get_text(" ", strip=True) if d else ""
    f = art.select_one("p.fecha")
    out.append({"url": url, "titulo": art.find("h3").get_text(strip=True), "lugar": lugar,
                "fechas": f.get_text(" ", strip=True) if f else "", "nuevo": url not in viejos})
json.dump(out, open(R / "raw/salas_miraflores/tt_listado_actual.json", "w"), ensure_ascii=False, indent=1)
print(len(out), "eventos;", sum(o["nuevo"] for o in out), "no estaban en tt_listing.json")
for o in out:
    if o["nuevo"]: print(o["titulo"], "|", o["lugar"], "|", o["fechas"])
