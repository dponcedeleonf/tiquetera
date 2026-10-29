"""Diario Correo: recorre páginas de etiqueta, baja cada nota y guarda fecha + texto de las que mencionan salas de Miraflores."""
import json, re, sys, pathlib, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from red import bajar, texto
from bs4 import BeautifulSoup
R = pathlib.Path(__file__).resolve().parent.parent
B = "https://diariocorreo.pe"
etiquetas = sys.argv[1:] or ["teatro-de-lucia", "teatro-canout", "centro-cultural-ricardo-palma", "teatro-julieta", "nuevo-teatro-julieta",
    "teatro-britanico", "teatro-la-plaza", "miraflores", "obra-teatral", "teatro", "stand-up-comedy", "stand-up", "lima-comedy-club",
    "jazz-zone", "alianza-francesa", "icpna", "teatro-marsano", "musical", "comedia", "conciertos", "agenda-cultural", "danza"]
MIRA = re.compile(r"Miraflores|Lucía|Canout|Ricardo Palma|Julieta|Británico|La Plaza|Comedy Club|Jazz Zone|Alianza Francesa|ICPNA|Campo Abierto|Auditorio Miraflores|Cocodrilo|Larco|4 Queens|Humo", re.I)
destino = R / "raw/salas_miraflores/correo.json"
try: notas = json.load(open(destino))
except Exception: notas = {}
for et in etiquetas:
    h = bajar(f"{B}/noticias/{et}/")
    for l in dict.fromkeys(re.findall(r'href="(/[a-z-]+/[a-z0-9-]+-noticia/?)"', h)):
        u = B + l
        if u in notas: continue
        a = bajar(u)
        if not a: continue
        s = BeautifulSoup(a, "html.parser")
        m = s.find("meta", {"property": "article:published_time"}) or s.find("meta", {"name": "cXenseParse:recs:publishtime"})
        fecha = m["content"][:10] if m else (re.search(r'"datePublished":"([\d-]{10})', a) or [None, None])[1]
        cuerpo = " ".join(p.get_text(" ", strip=True) for p in s.select("p"))
        notas[u] = {"fecha": fecha, "titulo": s.title.get_text(strip=True) if s.title else "", "texto": cuerpo[:6000], "etiqueta": et}
        json.dump(notas, open(destino, "w"), ensure_ascii=False, indent=1)
for u, n in sorted(notas.items(), key=lambda x: x[1]["fecha"] or ""):
    if (n["fecha"] or "") >= "2026-08-01" and MIRA.search(n["titulo"] + n["texto"]):
        print(n["fecha"], n["titulo"][:110], "|", u)
