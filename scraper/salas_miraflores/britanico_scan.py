"""Revisa los eventos del Británico (REST) publicados desde agosto 2026 y marca los que ocurren en sedes de Miraflores."""
import json, re, sys, pathlib, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from red import bajar, texto
R = pathlib.Path(__file__).resolve().parent.parent
links = {}
for p in range(1, 9):
    t = json.loads(bajar(f"https://britanico.edu.pe/cultural/wp-json/wp/v2/bri-evt-evento?per_page=20&page={p}&_fields=date,link,title") or "[]")
    if not isinstance(t, list) or not t: break
    for e in t: links[e["link"]] = e["date"][:10]
for extra in ["https://britanico.edu.pe/cultural/eventos/victoria-un-nuevo-musical/", "https://britanico.edu.pe/cultural/eventos/el-nino-cuentahistorias/",
              "https://britanico.edu.pe/cultural/eventos/coro-del-britanico-noviembre-2026/", "https://britanico.edu.pe/cultural/eventos/karaoke-britanico-noviembre-2026/"]:
    links.setdefault(extra, "2026-09-01")
res = []
for u, d in sorted(links.items(), key=lambda x: x[1]):
    if d < "2026-08-01": continue
    t = texto(bajar(u)); i = t.find("Eventos\n"); j = t.find("¿Te gusta este evento?"); c = t[i:j]
    mira = re.findall(r"[^\n]*(?:Miraflores|Teatro Británico|Cultural Station)[^\n]*", c)
    res.append({"url": u, "mira": mira, "cuerpo": c})
    print(d, u.split("/eventos/")[1], "|", sorted(set(m.strip()[:50] for m in mira))[:4])
json.dump(res, open(R / "raw/salas_miraflores/britanico_scan.json", "w"), ensure_ascii=False, indent=1)
