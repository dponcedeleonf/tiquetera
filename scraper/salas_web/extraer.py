"""Cartelera de salas que publican su programación en su propia web.

Uso:
    python3 salas_web/extraer.py            # usa la caché raw/salas_web/ y baja lo que falte
    python3 salas_web/extraer.py --ver      # además imprime un resumen por obra

Salida: data/extraido/salas_web.json

Cómo funciona:
- Cada función `sala_*` lee la página de cartelera de una sala (y la ficha de cada obra)
  con comun.bajar(): caché en disco, 1 petición/seg por host, tope de ~30 páginas por sala,
  y bloqueo de joinnus.com (solo se anotan sus enlaces, nunca se abren).
- De la web se sacan los datos "duros": título, URL, enlace de compra, imagen, fechas,
  horario y precio cuando aparecen.
- curado.json (escrito a mano) aporta lo editorial: sinopsis propia, tipo, géneros,
  elenco/ficha limpios y correcciones. Lo que está en curado.json tiene prioridad.
  Una obra nueva sin entrada en curado.json sale con sinopsis null y se avisa en consola.
- Para borrar la caché y volver a recolectar: rm -r raw/salas_web
"""
import json, re, sys, pathlib, unicodedata
from bs4 import BeautifulSoup

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from comun import bajar, RAIZ  # noqa: E402

HOY = "2026-10-29"
DESDE = "2026-09-17"   # hoy menos 6 semanas: se incluyen obras que terminaron desde esta fecha
ANIO = 2026
SALIDA = RAIZ / "data" / "extraido" / "salas_web.json"
SALAS = {s["nombre"]: s for s in json.load(open(RAIZ / "data" / "salas.json", encoding="utf-8"))}

# ---------------------------------------------------------------- utilidades

MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8,
         "set": 9, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
RE_MES = r"(ene(?:ro)?|feb(?:rero)?|mar(?:zo)?|abr(?:il)?|may(?:o)?|jun(?:io)?|jul(?:io)?|ago(?:sto)?|set(?:iembre)?|sep(?:tiembre)?|oct(?:ubre)?|nov(?:iembre)?|dic(?:iembre)?)\b\.?"


def slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def rango(texto, anio=ANIO):
    """'Del 17 de octubre al 06 de diciembre' -> ('2026-10-17', '2026-12-06').
    Si solo hay una fecha y el texto dice 'desde', el fin queda None."""
    t = texto.lower()
    fechas, pend = [], []
    for m in re.finditer(r"\b(\d{1,2})\b(?!:)|" + RE_MES + r"|\b(20\d\d)\b", t):
        if m.group(1):
            pend.append([int(m.group(1)), None, None])
        elif m.group(2):
            mes = MESES[m.group(2)[:3]]
            for p in pend:
                p[1] = mes
            fechas += pend; pend = []
        elif m.group(3):
            for f in fechas:
                if f[2] is None:
                    f[2] = int(m.group(3))
    fechas = [f"{(f[2] or anio):04d}-{f[1]:02d}-{f[0]:02d}" for f in fechas if f[1]]
    if not fechas:
        return None, None
    if len(fechas) == 1:
        return fechas[0], (None if "desde" in t else fechas[0])
    return fechas[0], fechas[-1]


def sopa(html):
    return BeautifulSoup(html or "", "lxml")


def texto(html):
    s = sopa(html)
    for x in s(["script", "style", "noscript", "svg"]):
        x.decompose()
    return s.get_text("\n", strip=True)


def og(html, prop="og:image"):
    m = sopa(html).find("meta", property=prop)
    return m.get("content") if m else None


def enlaces(html, patron):
    vistos = []
    for a in sopa(html).find_all("a", href=True):
        h = a["href"].replace("&amp;", "&").replace(" ", "")
        if re.search(patron, h, re.I) and h not in vistos:
            vistos.append(h)
    return vistos


def compra(html, preferir=r"joinnus\.com/events|teleticket\.com\.pe/|ticketmaster\.pe/event|passline\.com"):
    e = enlaces(html, preferir)
    return e[0].split("?utm")[0] if e else None


def tras(txt, etiqueta):
    """Valor que sigue a 'Etiqueta:' cuando la etiqueta empieza una línea
    (el valor puede venir en la misma línea o en la siguiente, con o sin ':')."""
    m = re.search(r"(?:^|\n)" + re.escape(etiqueta) + r"\s*(?::[ \t]*\n?|\n[ \t]*:[ \t]*\n?|\n)[ \t]*([^\n]+)", txt)
    return m.group(1).strip(" :") if m else None


def nombres(lista):
    """'A, B y C.' -> ['A', 'B', 'C']"""
    if not lista:
        return []
    lista = re.sub(r"\.\s*$", "", lista.strip())
    partes = re.split(r",\s*|\s+y\s+", lista)
    return [p.strip() for p in partes if p.strip()]


def obra(sala, titulo, url, **kw):
    s = SALAS[sala]
    base = {
        "id": f"sala-{slug(sala)}-{slug(titulo)}", "fuente": "web de la sala", "url": url,
        "url_compra": None, "incluir": True, "titulo": titulo, "tipo": "teatro", "generos": [],
        "sinopsis": None, "elenco": [], "ficha": [], "artistas": [], "productora": None,
        "sala": sala, "distrito": s["distrito"], "ciudad": "Lima", "duracion_min": None,
        "edad_minima": None, "horario_texto": None, "temporada": {"inicio": None, "fin": None},
        "precio_desde": None, "imagen": None,
    }
    for k, v in kw.items():
        if k in ("inicio", "fin"):
            base["temporada"][k] = v
        else:
            base[k] = v
    return base


def vigente(o):
    fin = o["temporada"]["fin"] or o["temporada"]["inicio"]
    return fin is None or fin >= DESDE or o["temporada"]["fin"] is None


# ---------------------------------------------------------------- salas

def sala_la_plaza():
    S, B = "Teatro La Plaza", "https://laplaza.com.pe/"
    portada = bajar(B + "que-hay-2022/", "laplaza")
    urls = enlaces(portada, r"laplaza\.com\.pe/obras-archive/")
    # Obras de La Plaza Joven (infantiles) que pueden seguir en temporada
    joven = bajar(B + "la-plaza-joven/", "laplaza")
    for u in enlaces(joven, r"obras-archive/.*-2026/$|obras-archive/luminos/$"):
        if u not in urls:
            urls.append(u)
    salida = []
    for u in urls:
        h = bajar(u, "laplaza")
        t = texto(h)
        cuerpo = t.split("Descripción del proyecto", 1)[-1].strip()
        lineas = cuerpo.split("\n")
        titulo = lineas[0].strip()
        fechas = next((l for l in lineas[1:6] if re.search(r"(desde|del|estreno)\s.*\d", l, re.I)), "")
        ini, fin = rango(fechas) if fechas else (None, None)
        if not ini:
            continue  # sin fechas en Lima (ej. giras, archivo)
        hor = tras(cuerpo, "Horarios")
        elenco = tras(cuerpo, "Elenco")
        edad = re.search(r"a partir de (?:los )?(\d+) años", cuerpo)
        salida.append(obra(S, titulo.title() if titulo.isupper() else titulo, u, url_compra=compra(h),
                           imagen=og(h), inicio=ini, fin=fin, horario_texto=hor,
                           elenco=[{"nombre": n, "personaje": None} for n in nombres(elenco)],
                           edad_minima=int(edad.group(1)) if edad else None))
    return salida


def sala_britanico():
    S, B = "Teatro Británico", "https://britanico.edu.pe/cultural/"
    pag = bajar(B + "teatro/", "britanico")
    s = sopa(pag)
    salida, vistos = [], set()
    for li in s.select("li.wp-block-britanico-bloques-multisitio-multisite-post__item"):
        a = li.find("h3").find("a") if li.find("h3") else None
        tag = li.select_one("[class*=__content__tag]")
        if not a or not tag:
            continue
        ini, fin = rango(tag.get_text(" ", strip=True))
        if not ini or (fin or ini) < DESDE or a["href"] in vistos:
            continue
        vistos.add(a["href"])
        h = bajar(a["href"].replace("&#038;", "&"), "britanico")
        t = texto(h)
        titulo = a.get_text(" ", strip=True)
        precios = [float(x) for x in re.findall(r"General:?\s*\n?\s*S/\s*([\d.]+)", t)]
        lugar = tras(t, "Lugar")
        salida.append(obra(S, titulo, og(h, "og:url") or a["href"], url_compra=compra(h, r"joinnus\.com/events"),
                           imagen=og(h), inicio=ini, fin=fin,
                           precio_desde=min(precios) if precios else (0 if "Ingreso gratuito" in t else None),
                           _lugar=lugar))
    return salida


def sala_pucp():
    S, B = "Centro Cultural PUCP", "https://centrocultural.pucp.edu.pe/"
    datos = json.loads(bajar(B + "calendario/data.php?menu=174&start=2026-09-14&end=2027-02-01", "pucp") or "[]")
    por_url = {}
    for e in datos:
        por_url.setdefault(e["urls"], []).append(e["start"][:10])
    salida = []
    for u, dias in por_url.items():
        h = bajar(u, "pucp")
        t = texto(h)
        titulo = next(e["title"] for e in datos if e["urls"] == u)
        temp = tras(t, "TEMPORADA") or ""
        ini, fin = rango(temp) if temp else (min(dias), max(dias))
        lineas = t.split("TEMPORADA", 1)[-1].split("\n")
        hor = lineas[2] if len(lineas) > 2 else None
        gen = re.search(r"General(?: preventa)?\s*S/\s*([\d.]+)", t)
        salida.append(obra(S, titulo.title(), u, url_compra=compra(h), imagen=og(h), inicio=ini, fin=fin,
                           horario_texto=hor, precio_desde=float(gen.group(1)) if gen else None))
    return salida


def sala_gtn():
    import gtn_calendario
    S, B = "Gran Teatro Nacional", "https://granteatronacional.pe/evento/"
    salida = []
    for e in gtn_calendario.recolectar():
        if "mantenimiento" in e["slug"]:
            continue
        h = bajar(B + e["slug"], "gtn")
        if not h:
            continue  # sin ficha descargada (tope de páginas): se omite
        t = texto(h)
        if "esta fecha se encuentra ocupada por un evento programado" in t:
            continue  # fecha reservada sin espectáculo anunciado
        titulo = sopa(h).find("h1").get_text(" ", strip=True)
        cuerpo = t.split("A+\nA\n", 1)[-1]
        hor = " / ".join(l for l in cuerpo.split("\n")[:4] if re.search(r"\d\s*(a|p)\.\s?m\.", l))
        k, j = t.find("Costo entradas"), t.find("VISÍTANOS")
        precios = [float(x) for x in re.findall(r"S/\.?\s*([\d]+(?:\.\d+)?)", t[k:j])] if k > 0 else []
        gratis = re.search(r"(ingreso|entrada) (libre|gratuito)", t, re.I)
        fechas = sorted(f for f, _ in e["funciones"])
        edad = re.search(r"Edad recomendada:\s*\+(\d+)", t)
        salida.append(obra(S, titulo, B + e["slug"], url_compra=compra(h), imagen=og(h),
                           inicio=fechas[0], fin=fechas[-1], horario_texto=hor or None,
                           precio_desde=min(precios) if precios else (0 if gratis else None),
                           edad_minima=int(edad.group(1)) if edad else None, _categoria=e["cat"]))
    return salida


def sala_apj():
    import apj_agenda
    S = "Teatro Peruano Japonés"
    salida = []
    for u, h in apj_agenda.fichas().items():
        t = texto(h)
        cuerpo = t.split("Categorías:", 1)[-1] if "Categorías:" in t else t
        m = re.search(r"\n(\d\d/\d\d/\d{4})\n(.+)\n", cuerpo)
        fecha = "-".join(reversed(m.group(1).split("/"))) if m else None
        img = re.search(r'src="(https://www\.apj\.org\.pe/photos/shares/Teatro/Cartelera/[^"]+)"', h)
        dias, hora = tras(t, "Días"), tras(t, "Horario")
        salida.append(obra(S, m.group(2).strip() if m else u, u, url_compra=compra(h), imagen=img.group(1) if img else None,
                           inicio=fecha, fin=fecha, productora=tras(t, "Presenta"),
                           horario_texto=f"{dias} {hora}" if dias and hora else None, _entradas=tras(t, "Entradas")))
    return salida


def sala_lucia():
    S, B = "Teatro de Lucía", "https://teatrodelucia.com/"
    bajar(B, "lucia")
    datos = json.loads(bajar(B + "data/cartelera.json", "lucia") or "{}")
    salida = []
    for o in datos.get("obras", []):
        fns = sorted(f["fecha"] for f in o.get("funciones", []) if "demo" not in (f.get("nota") or "").lower())
        ini = fns[0] if fns else o.get("temporada_desde")
        fin = fns[-1] if fns else o.get("temporada_hasta")
        precios = [t["precio"] for t in o.get("tarifas", []) if t.get("precio") and not t.get("agotada")
                   and re.search(r"regular|general|adulto$", t["nombre"], re.I)]
        salida.append(obra(S, o["titulo"].title(), B + "#cartelera", url_compra=o.get("url_joinnus"),
                           imagen=B + o["poster"] if o.get("poster") else None, inicio=ini, fin=fin,
                           productora=o.get("compania") or None, precio_desde=min(precios) if precios else None,
                           _funciones=[(f["fecha"], f["hora"]) for f in o.get("funciones", [])]))
    return salida


def sala_icpna():
    B = "https://www.icpna.edu.pe/"
    datos = json.loads(bajar(B + "api/events/v1/entries?date_from=2026-09-17&date_to=2027-01-31&limit=50&offset=0", "icpna") or "{}")
    salida = []
    for e in datos.get("data", []):
        if not set(e.get("categories_slug", [])) & {"teatro", "danza", "artes-escenicas"}:
            continue
        u = f"{B}cultural/evento/{e['slug']}/"
        h = bajar(u, "icpna")
        t = texto(h)
        img = (((e.get("featured_image") or {}).get("default") or {}).get("file") or {}).get("url")
        edad = re.search(r"Mayores de (\d+) años", h)
        # La ficha no dice en qué sede es la función: se asume el auditorio de Miraflores (ver curado.json)
        salida.append(obra("ICPNA Miraflores (Auditorio)", e["name"].title(), u, url_compra=e.get("buy_ticket_url"),
                           imagen=("https:" + img) if img and img.startswith("//") else img,
                           inicio=e["start_date"][:10], fin=(e.get("end_date") or "")[:10] or None,
                           edad_minima=int(edad.group(1)) if edad else None, _texto=t[:0]))
    return salida


def sala_cce():
    """El CCE Lima tiene su sede cerrada por obras: todo lo que publica ocurre en otros lugares.
    Se revisan las fichas de 'Escénicas' y solo se aceptarían las que digan que son en el CCE."""
    B = "https://ccelima.aecid.es"
    pag = bajar(B + "/web/cc-lima/detalle-categorias/-/categories/7623813", "cce")
    salida = []
    for u in re.findall(r'href="(/web/cc-lima/w/[^"]+)"', pag)[:5]:
        h = bajar(B + u, "cce")
        lugar = tras(texto(h), "Lugar") or ""
        if re.search(r"Centro Cultural de España|Natalio S[aá]nchez", lugar, re.I):
            print("[cce] revisar a mano, es en la sala:", B + u)
    return salida


def sala_alianza_francesa():
    S, B = "Teatro de la Alianza Francesa de Lima", "https://aflima.org.pe/"
    lista = bajar(B + "eventos?categoria%5B%5D=artes-escenicas&categoria%5B%5D=danza-contemporanea&categoria%5B%5D=miscelaneo&categoria%5B%5D=eventos", "af")
    salida = []
    for u in enlaces(lista, r"aflima\.org\.pe/evento/"):
        h = bajar(u, "af")
        t = texto(h)
        lugar = tras(t, "MODO/LUGAR") or ""
        img = re.search(r"https://aflima\.org\.pe/wp-content/uploads/20\d\d/\d\d/[\w-]+-banner\.jpg", h)
        if "Teatro" in lugar and "Teatro" in (t.split("MODO/LUGAR")[-1][:120]):
            ini, fin = rango(tras(t, "FECHA") or "")
            titulo = re.sub(r"\s+[-–|]\s+Alianza Francesa.*$", "", og(h, "og:title") or "")
            salida.append(obra(S, titulo, u,
                               url_compra=compra(h), imagen=img.group(0) if img else None, inicio=ini, fin=fin,
                               horario_texto=tras(t, "HORARIO")))
        elif "novtec" in u:
            # Festival: solo los espectáculos que van en el Teatro de la AF
            for m in re.finditer(r"\n([A-ZÁÉÍÓÚ ]{4,})\n([^\n]*\d{1,2}[^\n]*de noviembre[^\n]*)\nTeatro Alianza Francesa[^\n]*\n[^\n]*\nEspectáculo", t):
                titulo, cuando = m.group(1).strip(), m.group(2)
                ini, fin = rango(cuando)
                img2 = re.search(r"https://aflima\.org\.pe/wp-content/uploads/20\d\d/\d\d/" + slug(titulo) + r"-detalle\.jpg", h)
                cmp = [x for x in enlaces(h, r"joinnus\.com/events") if slug(titulo) in x]
                salida.append(obra(S, titulo.title(), u, url_compra=cmp[0] if cmp else None,
                                   imagen=img2.group(0) if img2 else None, inicio=ini, fin=fin,
                                   horario_texto=re.sub(r"^.*?,\s*", "", cuando)))
    return salida


def sala_aaa():
    S, B = "Asociación de Artistas Aficionados (AAA)", "https://aaalima.pe/"
    pag = bajar(B + "programacion/", "aaa")
    salida = []
    for a in sopa(pag).find_all("a", href=True):
        if a.get_text(strip=True) != "+ información":
            continue
        u = a["href"]
        h = bajar(u, "aaa")
        t = texto(h).split("Tiktok", 1)[-1]
        lineas = t.split("\n")
        titulo = lineas[1].strip()
        fechas = next((l for l in lineas if re.search(r"^\d{1,2}(,| al | de ).*", l)), "")
        ini, fin = rango(fechas)
        dur = re.search(r"Duración:\s*\n?(\d+) minutos", t)
        reparto = tras(t, "Reparto")
        ficha = []
        for etq, rol in (("Dirección", "dirección"), ("Adaptación", "adaptación")):
            v = tras(t, etq)
            if v and not v.lower().startswith("creación colectiva"):
                ficha.append({"nombre": v, "rol": rol})
        img = re.search(r"https://aaalima\.pe/wp-content/uploads/20\d\d/\d\d/[\w-]+(?<!-\d{3}x\d{3})\.jpg", h)
        salida.append(obra(S, titulo, u, url_compra=compra(h), imagen=img.group(0) if img else None,
                           inicio=ini, fin=fin, horario_texto=tras(t, "Horario"),
                           duracion_min=int(dur.group(1)) if dur else None, ficha=ficha,
                           elenco=[{"nombre": n, "personaje": None} for n in nombres(reparto)]))
    return salida


# Sala(s) que cubre cada función: si una falla, se conservan sus obras de la corrida anterior.
SALA_DE = {"sala_la_plaza": ["Teatro La Plaza"], "sala_britanico": ["Teatro Británico"], "sala_pucp": ["Centro Cultural PUCP"],
           "sala_gtn": ["Gran Teatro Nacional"], "sala_apj": ["Teatro Peruano Japonés"], "sala_lucia": ["Teatro de Lucía"],
           "sala_icpna": ["ICPNA Miraflores (Auditorio)", "ICPNA Lima Centro (Auditorio)"], "sala_cce": ["Centro Cultural de España en Lima"],
           "sala_alianza_francesa": ["Teatro de la Alianza Francesa de Lima"], "sala_aaa": ["Asociación de Artistas Aficionados (AAA)"]}

SALAS_WEB = [sala_la_plaza, sala_britanico, sala_pucp, sala_gtn, sala_apj, sala_lucia, sala_icpna,
             sala_cce, sala_alianza_francesa, sala_aaa]

# ---------------------------------------------------------------- armado


def main(ver=False):
    curado = json.load(open(AQUI / "curado.json", encoding="utf-8"))
    excluir = set(curado.pop("_excluir", []))
    curado = {k: v for k, v in curado.items() if not k.startswith("_")}
    try:
        anterior = json.loads(SALIDA.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        anterior = []
    todas, sin_curar = [], []
    for f in SALAS_WEB:
        try:
            obras = f()
        except Exception as ex:  # una sala rota no debe tumbar al resto
            previas = [o for o in anterior if o["sala"] in SALA_DE.get(f.__name__, [])]
            print(f"[error] {f.__name__}: {ex!r} -> se conservan {len(previas)} obras de la corrida anterior")
            todas += previas
            continue
        print(f"{f.__name__}: {len(obras)} obras en la web")
        for o in obras:
            if o["id"] in excluir:
                continue
            c = curado.get(o["id"])
            if c is None:
                if not vigente(o):
                    continue
                sin_curar.append(o["id"])
            else:
                for k, v in c.items():
                    if k == "temporada":
                        o["temporada"].update(v)
                    else:
                        o[k] = v
            for k in [k for k in o if k.startswith("_")]:
                o.pop(k)
            todas.append(o)
            if ver:
                print("   ", o["id"], o["temporada"], o["url_compra"])
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(json.dumps(todas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    json.loads(SALIDA.read_text(encoding="utf-8"))  # verificación: JSON válido
    print(f"\n{len(todas)} obras -> {SALIDA}")
    if sin_curar:
        print("Sin entrada en curado.json (falta sinopsis/tipo):", *sin_curar, sep="\n  ")


if __name__ == "__main__":
    main(ver="--ver" in sys.argv)
