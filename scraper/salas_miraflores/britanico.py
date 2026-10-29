"""Británico Cultural: recorre agenda y teatro (incl. histórico) y extrae lugar/fechas de cada evento."""
import json, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from red import bajar, texto
R = pathlib.Path(__file__).resolve().parent.parent
listados = ["https://britanico.edu.pe/cultural/eventos/"] + [f"https://britanico.edu.pe/cultural/eventos/page/{p}/" for p in (2, 3)] + \
    ["https://britanico.edu.pe/cultural/eventos/categoria/teatro/?historico=1",
     "https://britanico.edu.pe/cultural/eventos/categoria/teatro/page/2/?historico=1"]
urls = []
for l in listados:
    for u in re.findall(r'href="(https://britanico\.edu\.pe/cultural/eventos/[a-z0-9-]+/)"', bajar(l)):
        if "/categoria/" in u or "/page/" in u: continue
        if u not in urls: urls.append(u)
out = []
for u in urls:
    t = texto(bajar(u))
    i = t.find("Eventos\n"); j = t.find("¿Te gusta este evento?")
    cuerpo = t[i:j]
    out.append({"url": u, "cuerpo": cuerpo})
json.dump(out, open(R / "raw/salas_miraflores/britanico_eventos.json", "w"), ensure_ascii=False, indent=1)
for o in out:
    lug = sorted(set(re.findall(r"(Auditorio [^\n]+|Teatro Británico[^\n]*|Cultural Station[^\n]*)", o["cuerpo"])))
    print(o["url"].split("/eventos/")[1], "|", [l[:40] for l in lug][:6])
