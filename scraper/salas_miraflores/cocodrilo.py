"""Cocodrilo Verde (bar de música en vivo, Miraflores): lee el sitemap de conciertos y extrae cada ficha."""
import json, re, sys, pathlib, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from red import bajar, texto
from bs4 import BeautifulSoup
R = pathlib.Path(__file__).resolve().parent.parent
sm = bajar("https://cocodriloverde.com/cpt_conciertos-sitemap.xml")
pares = re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", sm)
out = []
for u, lm in pares:
    if lm < "2026-08-01" or u.rstrip("/").endswith("/conciertos"): continue
    h = bajar(u)
    if not h: continue
    s = BeautifulSoup(h, "html.parser")
    t = texto(h)
    lineas = [l.strip() for l in t.split("\n") if l.strip()]
    def tras(et, n=1):
        for i, l in enumerate(lineas):
            if l.startswith(et): return " ".join(lineas[i + 1:i + 1 + n])
        return None
    fecha = re.search(r"(\d{2})/(\d{2})/(\d{4})", tras("Fecha del evento:", 2) or "")
    precio = re.search(r"S/\.?\s*([\d.]+)", " ".join(lineas[:80]).replace("S/. ", "S/."))
    compra = [a.get("href") for a in s.find_all("a") if "Comprar" in a.get_text()]
    out.append({"url": u, "titulo": next((lineas[i-1] for i, l in enumerate(lineas) if l.startswith("Entrada general")), None),
                "fecha": f"{fecha.group(3)}-{fecha.group(2)}-{fecha.group(1)}" if fecha else None,
                "hora": tras("Hora:"), "precio": tras("Entrada general:", 2), "compra": compra,
                "genero": tras("Género musical"), "integrantes": tras("Integrantes", 2),
                "texto": "\n".join(lineas)[:3000]})
    print(out[-1]["fecha"], out[-1]["hora"], "|", out[-1]["titulo"], "|", out[-1]["precio"], "|", compra[:1])
json.dump(out, open(R / "raw/salas_miraflores/cocodrilo.json", "w"), ensure_ascii=False, indent=1)
