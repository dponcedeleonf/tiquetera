"""Descarga con caché y 1 petición/seg por host. Nunca pide Joinnus ni marca blanca, ni Facebook/Instagram."""
import hashlib, pathlib, re, subprocess, sys, time, urllib.parse
import requests

RAIZ = pathlib.Path(__file__).resolve().parent.parent
CACHE = RAIZ / "raw" / "salas_miraflores"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
PROHIBIDOS = ("joinnus.com", "entradas.laplaza.com.pe", "facebook.com", "instagram.com")
_s = requests.Session(); _s.headers["User-Agent"] = UA
_ult = {}

def host(u): return urllib.parse.urlparse(u).netloc.lower()

def prohibida(u):
    h = host(u)
    return any(p in h for p in PROHIBIDOS)

def archivo(u, render=False):
    p = urllib.parse.urlparse(u)
    base = re.sub(r"[^a-zA-Z0-9_-]+", "_", p.path + "_" + p.query).strip("_")[:90] or "index"
    return CACHE / host(u) / f"{base}_{hashlib.md5(u.encode()).hexdigest()[:8]}{'_js' if render else ''}.html"

def bajar(u, render=False, espera_ms=4000, refrescar=False):
    if prohibida(u):
        raise ValueError("URL prohibida: " + u)
    f = archivo(u, render)
    if f.exists() and not refrescar:
        return f.read_text(encoding="utf-8", errors="ignore")
    h = host(u); falta = 1.1 - (time.time() - _ult.get(h, 0))
    if falta > 0: time.sleep(falta)
    _ult[h] = time.time()
    f.parent.mkdir(parents=True, exist_ok=True)
    try:
        if render:
            r = subprocess.run(["node", str(pathlib.Path(__file__).parent / "render.js"), u, str(espera_ms)],
                               capture_output=True, text=True, timeout=150)
            html = r.stdout
        else:
            r = _s.get(u, timeout=40); r.encoding = r.apparent_encoding if not r.encoding or r.encoding.lower()=="iso-8859-1" else r.encoding
            html = r.text if r.status_code == 200 else ""
            if r.status_code != 200: print(f"[{r.status_code}] {u}", file=sys.stderr)
    except Exception as e:
        print(f"[err] {u}: {e}", file=sys.stderr); html = ""
    if html: f.write_text(html, encoding="utf-8")
    return html

def texto(html):
    from bs4 import BeautifulSoup
    s = BeautifulSoup(html, "html.parser")
    for t in s(["script", "style", "noscript"]): t.decompose()
    return re.sub(r"\n\s*\n+", "\n", s.get_text("\n")).strip()

if __name__ == "__main__":
    # uso: python3 http.py URL [render] -> imprime texto
    u = sys.argv[1]; r = len(sys.argv) > 2 and sys.argv[2] == "render"
    print(texto(bajar(u, render=r)))
