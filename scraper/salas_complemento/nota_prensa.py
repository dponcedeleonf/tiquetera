"""Imprime fecha de publicación (meta/JSON-LD) y el texto principal de una nota de prensa.
Uso: python3 salas_complemento/nota_prensa.py URL [max_caracteres]"""
import json, re, sys, pathlib
from bs4 import BeautifulSoup
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from bajar import bajar

url = sys.argv[1]
tope = int(sys.argv[2]) if len(sys.argv) > 2 else 3500
html = bajar(url)
s = BeautifulSoup(html, "html.parser")
fecha = None
for m in s.find_all("meta"):
    if m.get("property") in ("article:published_time",) or m.get("name") in ("date", "pubdate", "publish-date"):
        fecha = m.get("content"); break
if not fecha:
    m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', html)
    fecha = m.group(1) if m else None
h1 = s.find("h1")
print("URL:", url)
print("FECHA:", fecha)
print("TITULO:", h1.get_text(" ", strip=True) if h1 else None)
cuerpo = s.find("article") or s.select_one(".entry-content, .post-content, .td-post-content, main") or s
ps = [p.get_text(" ", strip=True) for p in cuerpo.find_all(["p", "li", "h2", "h3"])]
txt = "\n".join(p for p in ps if len(p) > 25)
print(txt[:tope])
print("=" * 60)
