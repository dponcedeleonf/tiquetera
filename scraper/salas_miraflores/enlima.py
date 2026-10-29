"""En Lima (agenda cultural): recorre /calendario-cultural/dia/<fecha> y junta eventos en Miraflores (no exposiciones)."""
import json, re, sys, pathlib, datetime, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from red import bajar
from bs4 import BeautifulSoup
R = pathlib.Path(__file__).resolve().parent.parent
ini, fin = datetime.date(2026, 9, 17), datetime.date(2026, 12, 31)
eventos = {}
d = ini
while d <= fin:
    h = bajar(f"https://enlima.pe/calendario-cultural/dia/{d.isoformat()}?page=1")
    s = BeautifulSoup(h, "html.parser")
    for tr in s.select("table tr"):
        tds = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
        a = tr.find("a", href=re.compile(r"/agenda-cultural/"))
        if len(tds) < 6 or not a: continue
        hora, tipo, nombre, lugar, distrito, precio = tds[:6]
        if "Miraflores" not in distrito or tipo.lower().startswith("exposici"): continue
        u = "https://enlima.pe" + a["href"] if a["href"].startswith("/") else a["href"]
        e = eventos.setdefault(u, {"url": u, "nombre": nombre, "tipo": tipo, "lugar": lugar, "precio": precio, "fechas": []})
        e["fechas"].append((d.isoformat(), hora))
    d += datetime.timedelta(days=1)
json.dump(list(eventos.values()), open(R / "raw/salas_miraflores/enlima.json", "w"), ensure_ascii=False, indent=1)
for e in sorted(eventos.values(), key=lambda x: x["lugar"]):
    print(e["lugar"], "|", e["nombre"], "|", e["tipo"], "|", e["fechas"][0][0], "→", e["fechas"][-1][0], len(e["fechas"]), "|", e["precio"])
