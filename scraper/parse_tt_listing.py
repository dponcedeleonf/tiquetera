"""Extrae las tarjetas de eventos del listado 'todos' de Teleticket."""
import json, sys
from bs4 import BeautifulSoup

soup = BeautifulSoup(open(sys.argv[1], encoding="utf-8", errors="ignore"), "html.parser")
eventos, vistos = [], set()
for art in soup.select('article[id^="event_"]'):
    a = art.find("a")
    href = a["href"]
    if href in vistos:
        continue
    vistos.add(href)
    desc = art.select_one("p.descripcion")
    lugar, _, categoria = desc.get_text(" ", strip=True).partition(" / ") if desc else ("", "", "")
    track = a.get("data-ga-tracking", "")
    codigo = track.split("EventoID:")[1].split("-")[0] if "EventoID:" in track else None
    img = art.find("img")
    eventos.append({
        "url": "https://teleticket.com.pe" + href if href.startswith("/") else href,
        "codigo": codigo,
        "titulo": art.find("h3").get_text(strip=True),
        "lugar": lugar,
        "categoria": categoria,
        "fechas_texto": art.select_one("p.fecha").get_text(" ", strip=True) if art.select_one("p.fecha") else "",
        "imagen": img["src"] if img else None,
    })
json.dump(eventos, sys.stdout, ensure_ascii=False, indent=1)
