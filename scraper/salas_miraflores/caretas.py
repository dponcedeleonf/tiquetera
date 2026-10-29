"""Caretas (WordPress): lee notas por URL vía REST (slug) y muestra el texto plano."""
import json, re, sys, pathlib, warnings, html as H
warnings.filterwarnings("ignore")
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from red import bajar
from bs4 import BeautifulSoup
for u in sys.argv[1:]:
    slug = u.rstrip("/").split("/")[-1]
    j = json.loads(bajar(f"https://caretas.pe/wp-json/wp/v2/posts?slug={slug}&_fields=date,link,title,content") or "[]")
    for e in j:
        t = BeautifulSoup(e["content"]["rendered"], "html.parser").get_text(" ", strip=True)
        print("#####", e["date"][:10], H.unescape(e["title"]["rendered"]), e["link"]); print(t[:3000]); print()
