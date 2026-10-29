"""Utilidades compartidas para leer la cartelera en la web propia de cada sala.

- Caché en raw/salas_web/<host>/ (si el archivo existe no se vuelve a pedir).
- Máximo 1 petición por segundo por host.
- Nunca pide nada a joinnus.com (su robots.txt bloquea bots de IA).
- Tope de ~30 páginas por sala (contador por clave de sala).
- render=True usa Playwright (Node) para páginas armadas con JavaScript.
"""
import hashlib, json, pathlib, re, subprocess, time, urllib.parse
import requests

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CACHE = RAIZ / "raw" / "salas_web"
UA = "Mozilla/5.0 (prototipo tiquetera; recoleccion lenta de cartelera)"
TOPE_POR_SALA = 30

_sesion = requests.Session()
_sesion.headers["User-Agent"] = UA
_ultimo = {}
_conteo = {}


class Bloqueado(Exception):
    pass


def _host(url):
    return urllib.parse.urlparse(url).netloc.lower()


# Subdominios de las salas que en realidad sirven Joinnus (marca blanca).
JOINNUS_MARCA_BLANCA = {"entradas.laplaza.com.pe"}


def prohibida(url):
    h = _host(url)
    return "joinnus.com" in h or h in JOINNUS_MARCA_BLANCA


def _archivo(url, render):
    h = _host(url)
    resto = urllib.parse.urlparse(url)
    base = re.sub(r"[^a-zA-Z0-9_-]+", "_", (resto.path + "_" + resto.query + "_" + resto.fragment)).strip("_")[:90] or "index"
    dig = hashlib.md5(url.encode()).hexdigest()[:8]
    return CACHE / h / f"{base}_{dig}{'_js' if render else ''}.html"


def _esperar(host):
    t = _ultimo.get(host, 0)
    falta = 1.1 - (time.time() - t)
    if falta > 0:
        time.sleep(falta)
    _ultimo[host] = time.time()


def bajar(url, sala="?", render=False, espera_ms=3000):
    """Devuelve el HTML (str) o "" si falla. Usa caché."""
    if prohibida(url):
        raise Bloqueado(url)
    destino = _archivo(url, render)
    if destino.exists():
        return destino.read_text(encoding="utf-8", errors="ignore")
    if _conteo.get(sala, 0) >= TOPE_POR_SALA:
        print(f"[tope] {sala}: no se pide {url}")
        return ""
    _conteo[sala] = _conteo.get(sala, 0) + 1
    _esperar(_host(url))
    destino.parent.mkdir(parents=True, exist_ok=True)
    if render:
        r = subprocess.run(["node", str(pathlib.Path(__file__).parent / "render.js"), url, str(espera_ms)],
                           capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            print("error render", url, r.stderr[-300:])
            return ""
        html = r.stdout
    else:
        try:
            r = _sesion.get(url, timeout=40)
        except requests.RequestException as e:
            print("error", url, e)
            return ""
        if r.status_code != 200:
            print(r.status_code, url)
            return ""
        r.encoding = r.apparent_encoding if not r.encoding or r.encoding.lower() == "iso-8859-1" else r.encoding
        html = r.text
    if re.search(r"<link rel=\"canonical\" href=\"https://www\.joinnus\.com", html[:5000]):
        print("[joinnus] la URL sirve una página de Joinnus; se descarta:", url)
        return ""
    destino.write_text(html, encoding="utf-8")
    print("ok", len(html), url)
    return html


def bajar_json(url, sala="?"):
    t = bajar(url, sala)
    try:
        return json.loads(t) if t else None
    except ValueError:
        return None
