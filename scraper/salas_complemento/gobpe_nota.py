"""Imprime el cuerpo de una nota de prensa de gob.pe (título, fecha y texto).
Uso: python3 salas_complemento/gobpe_nota.py URL"""
import re, sys, pathlib
from bs4 import BeautifulSoup
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from bajar import bajar

html = bajar(sys.argv[1])
s = BeautifulSoup(html, "html.parser")
h1 = s.find("h1")
print("TITULO:", h1.get_text(" ", strip=True) if h1 else None)
fecha = s.find(string=re.compile(r"\d{1,2} de \w+ de 20\d\d"))
print("FECHA:", fecha.strip() if fecha else None)
cuerpo = s.select_one("#main .feed-content, article, .description, #main")
for t in cuerpo(["script", "style"]):
    t.decompose()
txt = "\n".join(l.strip() for l in cuerpo.get_text("\n").splitlines() if l.strip())
print(txt[:6000])
