"""Une lo extraído por la IA con las funciones y arma el catálogo del prototipo.

Entradas: data/lotes/*.json (funciones, url), data/extraido/*.json (IA), data/musica.json,
          data/teleticket.json y data/ticketmaster.json (imágenes), data/salas.json (opcional).
Salida: data/catalogo.json con tres colecciones conectadas por slug: obras, salas y personas.
"""
import json
import pathlib
import re
import unicodedata
from collections import defaultdict

RAIZ = pathlib.Path(__file__).parent
DATA = RAIZ / "data"


def slug(texto):
    texto = unicodedata.normalize("NFKD", texto or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", texto).strip("-")


def clave_sala(nombre):
    """Clave tolerante: 'TEATRO PERUANO JAPONES' y 'Teatro Peruano Japonés' dan lo mismo."""
    s = slug(nombre)
    s = re.sub(r"^(teatro|auditorio|centro-cultural|c-c)-", "", s)
    return s


def imagenes():
    img = {}
    for r in json.load(open(DATA / "teleticket.json")):
        d = r.get("detalle") or {}
        url = d.get("imagen") or r.get("imagen")
        for clave in (r["url"], d.get("url_canonica")):
            if clave and url:
                img[clave] = url
    for r in json.load(open(DATA / "ticketmaster.json")):
        if r.get("imagen"):
            img[r["url"]] = r["imagen"]
    return img


def cargar_salas_investigadas():
    ruta = DATA / "salas.json"
    if not ruta.exists():
        return {}, []
    salas = json.load(open(ruta))
    indice = {}
    for s in salas:
        for nombre in [s["nombre"], *(s.get("alias") or [])]:
            indice[clave_sala(nombre)] = s
    return indice, salas


def sala_de_lugar(lugar):
    """'TEATRO CANOUT - MIRAFLORES - LIMA' -> ('TEATRO CANOUT', 'Miraflores', 'Lima')"""
    partes = [p.strip() for p in re.split(r"\s+[-–]\s+", lugar) if p.strip()]
    nombre = partes[0] if partes else lugar
    ciudad = partes[-1].title() if len(partes) > 1 else None
    distrito = partes[1].title() if len(partes) > 2 else None
    return nombre, distrito, ciudad


def main():
    entradas = {}
    for ruta in sorted((DATA / "lotes").glob("lote_*.json")):
        for ev in json.load(open(ruta)):
            entradas[ev["id"]] = ev
    extraidos = []
    for ruta in sorted((DATA / "extraido").glob("lote_*.json")):
        extraidos += json.load(open(ruta))
    img = imagenes()
    indice_salas, salas_investigadas = cargar_salas_investigadas()

    obras, salas, personas = {}, {}, {}
    roles_persona = defaultdict(set)

    def registrar_sala(nombre, distrito, ciudad):
        investigada = indice_salas.get(clave_sala(nombre))
        if investigada:
            nombre, distrito, ciudad = investigada["nombre"], investigada.get("distrito") or distrito, investigada.get("ciudad") or ciudad
        clave = clave_sala(nombre)
        if clave not in salas:
            salas[clave] = {
                "slug": slug(nombre), "nombre": nombre, "distrito": distrito, "ciudad": ciudad or "Lima",
                **({k: investigada.get(k) for k in ("direccion", "tipo", "aforo_aprox", "descripcion_corta", "web",
                                                    "instagram", "ticketera", "coordenadas")} if investigada else {}),
                "obras": [],
            }
        return salas[clave]

    def registrar_persona(nombre, rol, obra_slug):
        nombre = " ".join((nombre or "").split())
        if len(nombre) < 3:
            return None
        clave = slug(nombre)
        p = personas.setdefault(clave, {"slug": clave, "nombre": nombre, "roles": [], "obras": []})
        roles_persona[clave].add(rol)
        if obra_slug not in p["obras"]:
            p["obras"].append(obra_slug)
        return clave

    def agregar_obra(base, ev):
        titulo = base["titulo"]
        sala = registrar_sala(base.get("sala") or sala_de_lugar(ev["lugar"])[0],
                              base.get("distrito"), base.get("ciudad"))
        obra_slug = slug(titulo)
        existente = obras.get(obra_slug)
        if existente and existente["sala"] != sala["slug"]:
            obra_slug = f"{obra_slug}-{sala['slug']}"
            existente = obras.get(obra_slug)
        funciones = [{**f, "sala": sala["slug"]} for f in ev.get("funciones", [])]
        if existente:
            # La misma obra en dos fuentes: se suman funciones y fuentes.
            existente["fuentes"].append({"fuente": ev["fuente"], "url": ev["url"]})
            existente["funciones"] += [f for f in funciones if f not in existente["funciones"]]
            return
        obra = {
            "slug": obra_slug,
            "titulo": titulo,
            "tipo": base.get("tipo") or "otro",
            "generos": base.get("generos") or [],
            "sinopsis": base.get("sinopsis"),
            "sala": sala["slug"],
            "ciudad": sala["ciudad"],
            "imagen": img.get(ev["url"]),
            "duracion_min": base.get("duracion_min"),
            "edad_minima": base.get("edad_minima"),
            "horario_texto": base.get("horario_texto"),
            "temporada": base.get("temporada") or {"inicio": None, "fin": None},
            "precio_desde": base.get("precio_desde"),
            "productora": base.get("productora"),
            "funciones": funciones,
            "fuentes": [{"fuente": ev["fuente"], "url": ev["url"]}],
            "elenco": [], "ficha": [], "artistas": [],
        }
        for e in base.get("elenco") or []:
            if (p := registrar_persona(e.get("nombre"), "actuación", obra_slug)):
                obra["elenco"].append({"persona": p, "personaje": e.get("personaje")})
        for f in base.get("ficha") or []:
            if (p := registrar_persona(f.get("nombre"), f.get("rol") or "otro", obra_slug)):
                obra["ficha"].append({"persona": p, "rol": f.get("rol")})
        for a in base.get("artistas") or []:
            if (p := registrar_persona(a, "artista", obra_slug)):
                obra["artistas"].append(p)
        if obra["precio_desde"] is None:
            precios = [pr["precio_min"] for f in funciones for pr in f.get("precios", [])
                       if "CONADIS" not in pr["categoria"].upper() and "DISCAPACIDAD" not in pr["categoria"].upper()]
            obra["precio_desde"] = min(precios) if precios else None
        obras[obra_slug] = obra
        sala["obras"].append(obra_slug)

    for x in extraidos:
        ev = entradas.get(x["id"])
        if ev and x.get("incluir", True) and x.get("titulo"):
            agregar_obra(x, ev)

    for ev in json.load(open(DATA / "musica.json")):
        nombre, distrito, ciudad = sala_de_lugar(ev["lugar"])
        fechas = sorted(f["fecha"] for f in ev["funciones"] if f.get("fecha"))
        titulo = ev["titulo"].title() if ev["titulo"].isupper() else ev["titulo"]
        agregar_obra({"titulo": titulo, "tipo": "concierto", "sala": nombre.title() if nombre.isupper() else nombre,
                      "distrito": distrito, "ciudad": ciudad,
                      "temporada": {"inicio": fechas[0] if fechas else None, "fin": fechas[-1] if fechas else None}}, ev)

    for clave, p in personas.items():
        p["roles"] = sorted(roles_persona[clave])

    catalogo = {
        "generado": "2026-10-29",
        "obras": sorted(obras.values(), key=lambda o: (o["temporada"].get("inicio") or "9999", o["titulo"])),
        "salas": sorted(salas.values(), key=lambda s: -len(s["obras"])),
        "personas": sorted(personas.values(), key=lambda p: (-len(p["obras"]), p["nombre"])),
        "salas_sin_cartelera": [s for s in salas_investigadas if clave_sala(s["nombre"]) not in salas],
    }
    json.dump(catalogo, open(DATA / "catalogo.json", "w"), ensure_ascii=False, indent=1)
    print(f"{len(obras)} obras, {len(salas)} salas, {len(personas)} personas, "
          f"{len(catalogo['salas_sin_cartelera'])} salas investigadas sin cartelera actual")


if __name__ == "__main__":
    main()
