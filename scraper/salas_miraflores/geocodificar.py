"""Coordenadas de las salas nuevas con Nominatim (OpenStreetMap), 1 petición por segundo."""
import json, sys, time, pathlib, requests
R = pathlib.Path(__file__).resolve().parent.parent
direcciones = {
    "Cocodrilo Verde": "Calle Francisco de Paula Camino 226, Miraflores, Lima, Peru",
    "Jazz Zone": "Avenida La Paz 656, Miraflores, Lima, Peru",
    "Rock And Pez": "Avenida Alfredo Benavides 2824, Miraflores, Lima, Peru",
    "Asociación Cultural Campo Abierto": "Calle General Recavarren 560, Miraflores, Lima, Peru",
    "Club de Teatro de Lima": "Avenida 28 de Julio 183, Miraflores, Lima, Peru",
    "Casa Tovar": "Calle Manuel Tovar 255, Miraflores, Lima, Peru",
    "Centro Cultural Cayetano Heredia": "Avenida Armendáriz 445, Miraflores, Lima, Peru",
    "Lugar de la Memoria (LUM)": "Lugar de la Memoria, la Tolerancia y la Inclusión Social, Miraflores, Lima",
    "Anfiteatro Chabuca Granda (Parque Kennedy)": "Parque Kennedy, Miraflores, Lima, Peru",
    "Ritual Virtual": "Calle Esperanza 339, Miraflores, Lima, Peru",
    "4 Queens": "Calle Manuel Bonilla 138, Miraflores, Lima, Peru",
    "Auditorio Británico Miraflores": "Calle Bellavista 531, Miraflores, Lima, Peru",
    "Cultural Station (Británico)": "Calle Bellavista 538, Miraflores, Lima, Peru",
    "Lima Comedy Club": "Avenida Alfredo Benavides 345, Miraflores, Lima, Peru",
    "Nuevo Teatro Julieta": "Pasaje Porta 132, Miraflores, Lima, Peru",
    "Colegio Hosanna": "Avenida Grau 441, Miraflores, Lima, Peru",
    "Auditorio Juana Alarco de Dammert": "Avenida Alfredo Benavides 2315, Miraflores, Lima, Peru",
}
s = requests.Session(); s.headers["User-Agent"] = "prototipo-tiquetera/1.0 (recoleccion lenta)"
out = {}
for k, q in direcciones.items():
    r = s.get("https://nominatim.openstreetmap.org/search", params={"q": q, "format": "json", "limit": 1}, timeout=30)
    j = r.json() if r.ok else []
    out[k] = {"lat": round(float(j[0]["lat"]), 5), "lng": round(float(j[0]["lon"]), 5), "osm": j[0].get("display_name")} if j else None
    print(k, "->", out[k]); time.sleep(1.2)
json.dump(out, open(R / "raw/salas_miraflores/coordenadas.json", "w"), ensure_ascii=False, indent=1)
