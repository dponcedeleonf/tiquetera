"""Descarga páginas para complementar la cartelera de salas (Marsano, municipales, regiones).

Uso:
  python3 salas_complemento/bajar.py URL [--render] [--html] [--links PATRON] [--espera MS]

- Caché en raw/salas_complemento/<host>/ (si existe no se vuelve a pedir).
- Máximo 1 petición por segundo por host (se guarda la hora de la última petición por host).
- Bloquea joinnus.com y sus marcas blancas (entradas.laplaza.com.pe); nunca las pide.
- No se usa para Facebook ni Instagram.
- --render usa Playwright (salas_web/render.js) para páginas armadas con JavaScript.
- Por defecto imprime el texto visible; --links PATRON imprime los enlaces cuyo href o texto contiene PATRON.
"""
import hashlib, json, pathlib, re, subprocess, sys, time, urllib.parse
import requests
from bs4 import BeautifulSoup

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CACHE = RAIZ / "raw" / "salas_complemento"
RENDER = RAIZ / "salas_web" / "render.js"
UA = "Mozilla/5.0 (prototipo tiquetera; recoleccion lenta de cartelera)"
PROHIBIDOS = re.compile(r"joinnus\.com|entradas\.laplaza\.com\.pe|facebook\.com|instagram\.com|fb\.com", re.I)
ULTIMO = CACHE / "_ultimo.json"


def _archivo(url, render):
    p = urllib.parse.urlparse(url)
    base = re.sub(r"[^a-zA-Z0-9_-]+", "_", p.path + "_" + p.query).strip("_")[:90] or "index"
    dig = hashlib.md5(url.encode()).hexdigest()[:8]
    return CACHE / p.netloc.lower() / f"{base}_{dig}{'_js' if render else ''}.html"


def _esperar(host):
    try:
        ult = json.loads(ULTIMO.read_text())
    except (OSError, ValueError):
        ult = {}
    falta = 1.1 - (time.time() - ult.get(host, 0))
    if falta > 0:
        time.sleep(falta)
    ult[host] = time.time()
    CACHE.mkdir(parents=True, exist_ok=True)
    ULTIMO.write_text(json.dumps(ult))


def bajar(url, render=False, espera_ms=4000):
    if PROHIBIDOS.search(urllib.parse.urlparse(url).netloc):
        raise SystemExit(f"URL prohibida, no se pide: {url}")
    destino = _archivo(url, render)
    if destino.exists():
        return destino.read_text(encoding="utf-8", errors="ignore")
    _esperar(urllib.parse.urlparse(url).netloc.lower())
    if render:
        r = subprocess.run(["node", str(RENDER), url, str(espera_ms)], capture_output=True, text=True, timeout=150)
        if r.returncode != 0:
            print("error render", r.stderr[-400:], file=sys.stderr)
            return ""
        html = r.stdout
    else:
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=40)
        except requests.RequestException as e:
            print("error", e, file=sys.stderr)
            return ""
        if r.status_code != 200:
            print("HTTP", r.status_code, url, file=sys.stderr)
            return ""
        if not r.encoding or r.encoding.lower() == "iso-8859-1":
            r.encoding = r.apparent_encoding
        html = r.text
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(html, encoding="utf-8")
    return html


def texto(html):
    s = BeautifulSoup(html, "html.parser")
    for t in s(["script", "style", "noscript", "svg"]):
        t.decompose()
    lineas = [l.strip() for l in s.get_text("\n").splitlines()]
    return "\n".join(l for l in lineas if l)


def enlaces(html, base, patron):
    s = BeautifulSoup(html, "html.parser")
    vistos = set()
    for a in s.find_all("a", href=True):
        href = urllib.parse.urljoin(base, a["href"])
        t = " ".join(a.get_text(" ").split())
        if (re.search(patron, href, re.I) or re.search(patron, t, re.I)) and href not in vistos:
            vistos.add(href)
            print(href, "|", t[:120])


if __name__ == "__main__":
    args = sys.argv[1:]
    url = args[0]
    render = "--render" in args
    espera = int(args[args.index("--espera") + 1]) if "--espera" in args else 4000
    html = bajar(url, render, espera)
    if "--html" in args:
        print(html)
    elif "--links" in args:
        enlaces(html, url, args[args.index("--links") + 1])
    else:
        print(texto(html))
