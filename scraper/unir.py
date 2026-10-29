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
    s = re.sub(r"^(teatro|auditorio|centro-cultural|centro-de-convenciones|c-c|cc)-", "", s)
    return s


def clave_persona(nombre):
    """Une variantes de escritura: 'Yvonne Fraysinett' e 'Ivonne Frayssinet' dan la misma clave."""
    return re.sub(r"(.)\1+", r"\1", slug(nombre).replace("y", "i"))


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
        clave = clave_persona(nombre)
        p = personas.setdefault(clave, {"slug": slug(nombre), "nombre": nombre, "roles": [], "obras": []})
        roles_persona[clave].add(rol)
        if obra_slug not in p["obras"]:
            p["obras"].append(obra_slug)
        return p["slug"]

    def sumar_personas(obra, base):
        """Agrega elenco, ficha y artistas que la obra aún no tenga."""
        ya = {e["persona"] for e in obra["elenco"]} | {f["persona"] for f in obra["ficha"]} | set(obra["artistas"])
        for e in base.get("elenco") or []:
            if (p := registrar_persona(e.get("nombre"), "actuación", obra["slug"])) and p not in ya:
                obra["elenco"].append({"persona": p, "personaje": e.get("personaje")})
                ya.add(p)
        for f in base.get("ficha") or []:
            if (p := registrar_persona(f.get("nombre"), f.get("rol") or "otro", obra["slug"])) and p not in ya:
                obra["ficha"].append({"persona": p, "rol": f.get("rol")})
                ya.add(p)
        for a in base.get("artistas") or []:
            if (p := registrar_persona(a, "artista", obra["slug"])) and p not in ya:
                obra["artistas"].append(p)
                ya.add(p)

    def precio_minimo(funciones):
        precios = [pr["precio_min"] for f in funciones for pr in f.get("precios", [])
                   if "CONADIS" not in pr["categoria"].upper() and "DISCAPACIDAD" not in pr["categoria"].upper()]
        return min(precios) if precios else None

    def agregar_obra(base, ev):
        titulo = base["titulo"]
        sala = registrar_sala(base.get("sala") or sala_de_lugar(ev["lugar"])[0],
                              base.get("distrito"), base.get("ciudad"))
        # Una obra = una producción. Las giras y las fuentes repetidas se juntan por título;
        # cada función recuerda en qué sala es.
        obra_slug = slug(titulo)
        funciones = [{**f, "sala": sala["slug"]} for f in ev.get("funciones", [])]
        fuente = {"fuente": ev["fuente"], "url": ev["url"], "sala": sala["slug"], "url_compra": base.get("url_compra")}
        obra = obras.get(obra_slug)
        if obra:
            obra["fuentes"].append(fuente)
            obra["funciones"] += [f for f in funciones if f not in obra["funciones"]]
            if sala["slug"] not in obra["salas"]:
                obra["salas"].append(sala["slug"])
            t, nueva = obra["temporada"], base.get("temporada") or {}
            if nueva.get("inicio") and (not t.get("inicio") or nueva["inicio"] < t["inicio"]):
                t["inicio"] = nueva["inicio"]
            if nueva.get("fin") and (not t.get("fin") or nueva["fin"] > t["fin"]):
                t["fin"] = nueva["fin"]
            precios = [p for p in (obra["precio_desde"], base.get("precio_desde"), precio_minimo(funciones)) if p is not None]
            obra["precio_desde"] = min(precios) if precios else None
            for campo in ("sinopsis", "imagen", "duracion_min", "edad_minima", "horario_texto", "productora"):
                obra[campo] = obra[campo] or (img.get(ev["url"]) or base.get("imagen") if campo == "imagen" else base.get(campo))
            sumar_personas(obra, base)
        else:
            obra = {
                "slug": obra_slug,
                "titulo": titulo,
                "tipo": base.get("tipo") or "otro",
                "generos": base.get("generos") or [],
                "sinopsis": base.get("sinopsis"),
                "sala": sala["slug"],
                "salas": [sala["slug"]],
                "ciudad": sala["ciudad"],
                "imagen": img.get(ev["url"]) or base.get("imagen"),
                "duracion_min": base.get("duracion_min"),
                "edad_minima": base.get("edad_minima"),
                "horario_texto": base.get("horario_texto"),
                "temporada": dict(base.get("temporada") or {"inicio": None, "fin": None}),
                "precio_desde": base.get("precio_desde") if base.get("precio_desde") is not None else precio_minimo(funciones),
                "productora": base.get("productora"),
                "funciones": funciones,
                "fuentes": [fuente],
                "elenco": [], "ficha": [], "artistas": [],
            }
            obras[obra_slug] = obra
            sumar_personas(obra, base)
        if obra_slug not in sala["obras"]:
            sala["obras"].append(obra_slug)

    for x in extraidos:
        ev = entradas.get(x["id"])
        if ev and x.get("incluir", True) and x.get("titulo"):
            agregar_obra(x, ev)

    # Cartelera publicada en las webs de las propias salas (ver salas_web/).
    ruta_salas_web = DATA / "extraido" / "salas_web.json"
    if ruta_salas_web.exists():
        for x in json.load(open(ruta_salas_web)):
            if x.get("incluir", True) and x.get("titulo"):
                agregar_obra(x, {"fuente": x["fuente"], "url": x["url"], "lugar": x["sala"], "funciones": []})

    for ev in json.load(open(DATA / "musica.json")):
        nombre, distrito, ciudad = sala_de_lugar(ev["lugar"])
        fechas = sorted(f["fecha"] for f in ev["funciones"] if f.get("fecha"))
        titulo = re.sub(r"\s*\|\s*teleticket.*$", "", ev["titulo"], flags=re.I).strip()
        titulo = titulo.title() if titulo.isupper() else titulo
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
