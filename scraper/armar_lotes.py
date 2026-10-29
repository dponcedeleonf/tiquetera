"""Une Teleticket y Ticketmaster y arma lotes para la extracción con IA.

Descarta deportes y tours (no son espectáculos) y recorta textos largos.
Los conciertos de Teleticket no pasan por la IA (el artista ya es el título): van a data/musica.json.
Salida: data/lotes/lote_NN.json, cada uno con ~46 eventos.
"""
import json
import pathlib

RAIZ = pathlib.Path(__file__).parent
DATA = RAIZ / "data"
LOTES = DATA / "lotes"
TAM_LOTE = 46
MUSICA = {"Música", "Rock", "Conciertos", "Festival"}
EXCLUIR_CATEGORIAS = {"Deportes", "Fútbol"}
EXCLUIR_LUGARES = ("RUTAS INCAS", "LIKE XPLORER", "PUNTO DE REUNI", "PUNTO DE  REUNI")


def eventos():
    for r in json.load(open(DATA / "teleticket.json")):
        if r["categoria"] in EXCLUIR_CATEGORIAS or r["lugar"].upper().startswith(EXCLUIR_LUGARES):
            continue
        d = r.get("detalle") or {}
        yield {
            "id": f"tt-{d.get('codigo') or r['codigo'] or r['url'].rsplit('/', 1)[-1]}",
            "fuente": "teleticket",
            "url": r["url"],
            "titulo": d.get("titulo") or r["titulo"],
            "categoria_fuente": r["categoria"],
            "lugar": r["lugar"],
            "fechas_texto": r["fechas_texto"],
            "funciones": d.get("funciones", []),
            "texto": (d.get("descripcion") or "")[:3000],
        }
    for r in json.load(open(DATA / "ticketmaster.json")):
        yield {
            "id": "tm-" + r["url"].rsplit("/", 1)[-1],
            "fuente": "ticketmaster",
            "url": r["url"],
            "titulo": r["titulo"],
            "categoria_fuente": None,
            "lugar": " - ".join(x for x in (r["lugar"], r["direccion"], r["localidad"]) if x),
            "fechas_texto": " / ".join(x for x in (r["fechas_texto"], r["inicio"], r["fin"]) if x),
            "funciones": [],
            "texto": r["descripcion"][:3000],
        }


def main():
    todos, musica = [], []
    for ev in eventos():
        (musica if ev["categoria_fuente"] in MUSICA else todos).append(ev)
    json.dump(musica, open(DATA / "musica.json", "w"), ensure_ascii=False, indent=1)
    LOTES.mkdir(parents=True, exist_ok=True)
    for viejo in LOTES.glob("lote_*.json"):
        viejo.unlink()
    for i in range(0, len(todos), TAM_LOTE):
        json.dump(todos[i:i + TAM_LOTE], open(LOTES / f"lote_{i // TAM_LOTE + 1:02d}.json", "w"),
                  ensure_ascii=False, indent=1)
    print(f"{len(musica)} conciertos aparte; {len(todos)} eventos en {(len(todos) - 1) // TAM_LOTE + 1} lotes")


if __name__ == "__main__":
    main()
