"""Entrada Libre (agenda de eventos gratuitos): usa los nombres de archivo de sus afiches
(AAMMDD + tipo + distrito, p. ej. 261104POPRMIRFRE) para hallar eventos en Miraflores (MIR) y lee cada ficha."""
import json, re, sys, pathlib, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from red import bajar, texto
R = pathlib.Path(__file__).resolve().parent.parent
B = "https://entradalibre.me/wp-json/wp/v2/"
medios = []
for p in range(1, 30):
    t = bajar(f"{B}media?per_page=100&page={p}&after=2026-08-20T00:00:00&_fields=id,date,post,source_url,title")
    try: j = json.loads(t)
    except Exception: break
    if not isinstance(j, list) or not j: break
    medios += j
mira = [m for m in medios if re.match(r"\d{6}[A-Z]{4}MIR", m["source_url"].rsplit("/", 1)[-1])]
print(len(medios), "afiches;", len(mira), "en Miraflores")
out = []
for m in mira:
    f = m["source_url"].rsplit("/", 1)[-1]
    fecha = "20" + f[:2] + "-" + f[2:4] + "-" + f[4:6]
    link = None
    if m.get("post"):
        # el afiche cuelga de una ficha 'event' (tipo no expuesto en REST); se busca por id
        h = bajar(f"https://entradalibre.me/?p={m['post']}")
        mm = re.search(r'<link rel="canonical" href="([^"]+)"', h)
        link = mm.group(1) if mm else None
        txt = texto(h)
    else:
        txt = ""
    out.append({"archivo": f, "fecha": fecha, "codigo": f[6:10], "url": link, "texto": txt[:4000]})
    print(fecha, f[6:10], f, "|", link)
json.dump(out, open(R / "raw/salas_miraflores/entradalibre.json", "w"), ensure_ascii=False, indent=1)
