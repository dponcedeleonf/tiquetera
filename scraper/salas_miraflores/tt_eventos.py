"""Lee fichas sueltas de Teleticket (URLs halladas en buscadores) y muestra recinto y fechas."""
import re, sys, pathlib, json, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from red import bajar, texto
R = pathlib.Path(__file__).resolve().parent.parent
cat = json.load(open(R / "data/catalogo.json"))
urls_cat = {f["url"] for o in cat["obras"] for f in o["fuentes"]}
out = []
for u in sys.argv[1:]:
    t = texto(bajar(u))
    i = t.find("×"); cab = [l.strip() for l in t[i:i + 900].split("\n") if l.strip()][:8]
    fechas = re.findall(r"\d{2}-\d{2}-\d{4}", " ".join(cab))
    rec = re.search(r"Recinto:\s*([^\n]+)", t)
    out.append({"url": u, "cab": cab, "fechas": fechas, "recinto": rec.group(1).strip() if rec else None, "en_catalogo": u in urls_cat})
    print(u.split("/evento/")[-1][:60], "|", cab[1:4], "|", fechas, "|", (rec.group(1)[:60] if rec else None), "| cat" if u in urls_cat else "")
p = R / "raw/salas_miraflores/tt_eventos.json"
prev = json.load(open(p)) if p.exists() else []
json.dump(prev + out, open(p, "w"), ensure_ascii=False, indent=1)
