"""Descarga las páginas de eventos de Ticketmaster Perú (1 petición por segundo).

Los slugs salen de la portada y las páginas de categoría (raw/tm_event_slugs.txt).
"""
import time, pathlib, requests

RAIZ = pathlib.Path(__file__).parent
PAGINAS = RAIZ / "raw" / "tm_pages"
PAGINAS.mkdir(parents=True, exist_ok=True)
sesion = requests.Session()
sesion.headers["User-Agent"] = "Mozilla/5.0 (prototipo tiquetera; contacto dponcedeleonf)"

slugs = [l.strip().split("event/")[-1] for l in open(RAIZ / "raw" / "tm_event_slugs.txt") if l.strip()]
for i, slug in enumerate(slugs, 1):
    destino = PAGINAS / f"{slug}.html"
    if destino.exists():
        continue
    try:
        r = sesion.get(f"https://www.ticketmaster.pe/event/{slug}", timeout=30)
        if r.status_code == 200:
            destino.write_text(r.text, encoding="utf-8")
        else:
            print(r.status_code, slug, flush=True)
    except requests.RequestException as e:
        print("error", slug, e, flush=True)
    time.sleep(1)
    if i % 25 == 0:
        print(f"{i}/{len(slugs)}", flush=True)
print("listo", flush=True)
