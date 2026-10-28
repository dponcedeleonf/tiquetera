"""Descarga las páginas de eventos de Teleticket listadas en raw/tt_listing.json.

Va despacio (1 petición por segundo) y guarda cada HTML en raw/pages/.
Las landings especiales (URLs sin /evento/) enlazan a páginas /evento/CODIGO;
esas también se descargan.
"""
import json, re, time, pathlib, requests

RAIZ = pathlib.Path(__file__).parent
PAGINAS = RAIZ / "raw" / "pages"
PAGINAS.mkdir(parents=True, exist_ok=True)
sesion = requests.Session()
sesion.headers["User-Agent"] = "Mozilla/5.0 (prototipo tiquetera; contacto dponcedeleonf)"

def nombre_archivo(url):
    return re.sub(r"[^a-zA-Z0-9_-]+", "_", url.split("teleticket.com.pe/")[-1]).strip("_")[:150] + ".html"

def bajar(url):
    destino = PAGINAS / nombre_archivo(url)
    if destino.exists():
        return destino.read_text(encoding="utf-8", errors="ignore")
    try:
        r = sesion.get(url, timeout=30)
        time.sleep(1)
    except requests.RequestException as e:
        print("error", url, e)
        return ""
    if r.status_code != 200:
        print(r.status_code, url)
        return ""
    destino.write_text(r.text, encoding="utf-8")
    return r.text

listado = json.load(open(RAIZ / "raw" / "tt_listing.json"))
extra = set()
for i, ev in enumerate(listado, 1):
    html = bajar(ev["url"])
    if "/evento/" not in ev["url"]:
        for codigo in set(re.findall(r'href="(?:https://teleticket\.com\.pe)?/evento/([A-Z]{2,4}\d{2,4})"', html)):
            extra.add("https://teleticket.com.pe/evento/" + codigo)
    if i % 25 == 0:
        print(f"{i}/{len(listado)}", flush=True)
print("subpáginas de landings:", len(extra), flush=True)
for url in sorted(extra):
    bajar(url)
print("listo", flush=True)
