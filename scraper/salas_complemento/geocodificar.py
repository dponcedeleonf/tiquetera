"""Consulta Nominatim (OpenStreetMap) para obtener coordenadas de las salas nuevas.
1 petición cada 1,2 s (política de uso de Nominatim). Imprime los candidatos.
Uso: python3 salas_complemento/geocodificar.py "consulta 1" "consulta 2" ..."""
import json, sys, time
import requests

UA = "prototipo-tiquetera/1.0 (recoleccion lenta de cartelera)"
for q in sys.argv[1:]:
    r = requests.get("https://nominatim.openstreetmap.org/search",
                     params={"q": q, "format": "jsonv2", "limit": 4, "countrycodes": "pe", "addressdetails": 1},
                     headers={"User-Agent": UA}, timeout=30)
    print("###", q)
    for x in r.json():
        print("  ", x["lat"], x["lon"], "|", x.get("category"), x.get("type"), "|", x["display_name"][:160])
    time.sleep(1.2)
