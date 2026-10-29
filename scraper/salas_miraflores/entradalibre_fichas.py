"""Lee las fichas de Entrada Libre seleccionadas (artes escénicas y música en Miraflores) y muestra lugar y datos."""
import json, re, sys, pathlib, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from red import bajar, texto
R = pathlib.Path(__file__).resolve().parent.parent
d = json.load(open(R / "raw/salas_miraflores/entradalibre.json"))
COD = ("DA", "TE", "MU", "KI", "PO", "IL")
fichas = []
for x in d:
    if x["fecha"] < "2026-09-17" or not x.get("url") or x["codigo"][:2] not in COD: continue
    t = texto(bajar(x["url"]))
    lin = [l.strip() for l in t.split("\n") if l.strip()]
    # recorte: desde el título hasta 'Compartir' o similar
    try: i = next(k for k, l in enumerate(lin) if l.lower().startswith(("fecha", "inicio")))
    except StopIteration: i = 0
    cuerpo = "\n".join(lin[max(0, i - 15): i + 60])
    x["ficha"] = cuerpo
    fichas.append(x)
    print("#####", x["fecha"], x["codigo"], x["url"]); print(cuerpo[:1800]); print()
json.dump(fichas, open(R / "raw/salas_miraflores/entradalibre_fichas.json", "w"), ensure_ascii=False, indent=1)
