"""Busca noticias en gob.pe (por institución) y lista título, fecha y URL.
Uso: python3 salas_complemento/gobpe_buscar.py <institucion> "<termino>" [paginas]
Lee el JSON window.initialData que la página de búsqueda trae embebido."""
import json, re, sys, urllib.parse, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from bajar import bajar

inst, term = sys.argv[1], sys.argv[2]
pags = int(sys.argv[3]) if len(sys.argv) > 3 else 1
filtro = sys.argv[4] if len(sys.argv) > 4 else None  # regex opcional sobre el título
for p in range(1, pags + 1):
    url = ("https://www.gob.pe/busquedas?contenido[]=noticias&institucion[]=%s&term=%s&sort_by=recent&sheet=%d"
           % (inst, urllib.parse.quote(term), p))
    html = bajar(url)
    m = re.search(r"window\.initialData=(\{.*?\});?\s*</script>", html, re.S)
    if not m:
        print("sin datos", url); break
    d = json.loads(m.group(1))
    res = d["data"]["attributes"].get("results", [])
    if not res:
        break
    for r in res:
        fecha = (r.get("publication") or r.get("date") or "").strip()
        h = (r.get("title") or "") + (r.get("url") or "")
        href = re.search(r'href="([^"]+)"', h)
        titulo = re.sub(r"<[^>]+>", "", h).strip()
        if filtro and not re.search(filtro, titulo, re.I):
            continue
        print(fecha, "|", titulo, "|", ("https://www.gob.pe" + href.group(1)) if href else "")
