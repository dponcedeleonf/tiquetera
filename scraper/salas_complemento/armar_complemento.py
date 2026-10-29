"""Arma data/extraido/salas_complemento.json y agrega las salas nuevas al final de data/salas.json.

Los datos se recogieron a mano (29/10/2026) con WebSearch/WebFetch y con los scripts de esta carpeta
(bajar.py, gobpe_buscar.py, gobpe_nota.py, nota_prensa.py, elencos_cultura.py, geocodificar.py).
Fuentes: notas de prensa de la MML (gob.pe), agenda de Elencos Nacionales del Ministerio de Cultura,
web del Ballet Municipal de Lima, y prensa (Diario UNO, Infobae, Caretas, Correo, Altavoz, El Búho,
Radio Onda Azul, Jornada, Limeo). No se abrió Joinnus, Facebook ni Instagram: sus URL solo se anotan.

- Descarta obras que ya estén en catalogo.json para la misma sala (título normalizado, sin subtítulo).
- Solo agrega a salas.json las salas cuyo nombre/alias no exista ya; en las existentes solo
  completa campos que estén en null (COMPLETAR).
Uso: python3 salas_complemento/armar_complemento.py
"""
import json, pathlib, re, unicodedata

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DATA = RAIZ / "data"
SALIDA = DATA / "extraido" / "salas_complemento.json"


def slug(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def clave_titulo(t):
    t = re.split(r"\s*[:–—(]\s*|\s+-\s+", t or "")[0]
    return slug(t)


def obra(sala, titulo, **k):
    base = {
        "id": f"comp-{slug(sala)}-{slug(titulo)}",
        "fuente": k.pop("fuente"),
        "url": k.pop("url"),
        "url_compra": k.pop("url_compra", None),
        "incluir": True,
        "titulo": titulo,
        "tipo": k.pop("tipo"),
        "generos": k.pop("generos", []),
        "sinopsis": k.pop("sinopsis"),
        "elenco": [{"nombre": n, "personaje": p} for n, p in k.pop("elenco", [])],
        "ficha": [{"nombre": n, "rol": r} for n, r in k.pop("ficha", [])],
        "artistas": k.pop("artistas", []),
        "productora": k.pop("productora", None),
        "sala": sala,
        "distrito": k.pop("distrito"),
        "ciudad": k.pop("ciudad"),
        "duracion_min": k.pop("duracion_min", None),
        "edad_minima": k.pop("edad_minima", None),
        "horario_texto": k.pop("horario_texto", None),
        "temporada": {"inicio": k.pop("inicio"), "fin": k.pop("fin")},
        "precio_desde": k.pop("precio_desde", None),
        "imagen": None,
    }
    assert not k, k
    return base


TML = dict(distrito="Cercado de Lima", ciudad="Lima")
SEG = dict(distrito="Cercado de Lima", ciudad="Lima")

OBRAS = [
    # ---------------- Teatro Municipal de Lima ----------------
    obra("Teatro Municipal de Lima", "El lago de los cisnes",
         fuente="prensa", url="https://diariouno.pe/2026/09/10/el-lago-de-los-cisnes-regresa-al-teatro-municipal-de-lima/",
         url_compra="https://teleticket.com.pe/el-lago-de-los-cisnes",
         tipo="danza", generos=["ballet", "clásico"],
         sinopsis="El Ballet Municipal de Lima retomó el clásico de Tchaikovsky sobre el príncipe Sigfrido y Odette, la joven convertida en cisne. Cuatro funciones contaron con la orquesta del teatro en vivo.",
         elenco=[("Nicolai Gorodiski", None)],
         ficha=[("Carlos Valcárcel", "dirección"), ("Marius Petipa", "coreografía"), ("Lev Ivanov", "coreografía"),
                ("Piotr Tchaikovsky", "música"), ("Carlos Calleja", "otro")],
         artistas=["Ballet Municipal de Lima", "Orquesta Sinfónica del Teatro Municipal de Lima"],
         productora="Ballet Municipal de Lima", edad_minima=5,
         horario_texto="16 funciones; con orquesta: 26 y 27 set 6 p. m., 1 y 2 oct 8 p. m.",
         inicio="2026-09-11", fin="2026-10-03", precio_desde=20, **TML),
    obra("Teatro Municipal de Lima", "Romeo y Julieta",
         fuente="prensa", url="https://www.infobae.com/peru/2026/10/17/romeo-y-julieta-con-oscar-yepez-y-maria-grazia-gamarra-en-el-teatro-municipal-de-lima-fecha-y-precio-de-entradas/",
         url_compra="https://www.passline.com/eventos/romeo-y-julieta-09-de-octubre-al-08-de-noviembre",
         tipo="teatro", generos=["drama", "clásico", "tragedia"],
         sinopsis="Éxodo Teatro lleva a Shakespeare por un camino más sombrío: la historia de los amantes de Verona se cuenta desde la violencia y el azar que los rodean, más que desde el romance.",
         elenco=[("Óscar Yépez", "Romeo"), ("María Grazia Gamarra", "Julieta"), ("Alonso Cano", "Mercucio"),
                 ("Fernando Luque", "Teobaldo"), ("Amaranta Kun", "Cupido"), ("Sebastián Rubio", "Paris")],
         ficha=[("William Shakespeare", "dramaturgia"), ("Jean Pierre Gamarra", "dirección"), ("Lorenzo Albani", "escenografía")],
         productora="Éxodo Teatro", duracion_min=120, edad_minima=12,
         horario_texto="Jue a sáb 8 p. m., dom 7 p. m.",
         inicio="2026-10-09", fin="2026-11-08", precio_desde=10, **TML),
    obra("Teatro Municipal de Lima", "Svetlana Smolina: recital de piano",
         fuente="prensa", url="https://diariouno.pe/2026/09/23/de-los-grandes-escenarios-del-mundo-a-lima-la-virtuosa-pianista-rusa-svetlana-smolina-llega-al-teatro-municipal/",
         url_compra="https://www.ticketmaster.pe/event/la-deslumbrante-pianista-de-rusia-svetlana-smolina-home",
         tipo="concierto", generos=["música clásica", "piano"],
         sinopsis="Recital único de la pianista rusa, que asumió la fecha de la temporada internacional tras la cancelación de Daniil Trifonov.",
         artistas=["Svetlana Smolina"], productora="TQ Producciones",
         horario_texto="Lun 26 oct, 8 p. m.", inicio="2026-10-26", fin="2026-10-26", **TML),

    # ---------------- Teatro Segura ----------------
    obra("Teatro Segura", "Alicia, siempre Alicia – Edición 2026",
         fuente="municipalidad", url="https://www.gob.pe/institucion/munilima/noticias/1444218-entradas-desde-s-20-la-musica-y-el-legado-de-alicia-maguina-llegan-al-teatro-segura-este-20-de-setiembre",
         url_compra="https://teleticket.com.pe/evento/alicia-siempre-alicia-teatro-segura-2026",
         tipo="concierto", generos=["música criolla", "música peruana"],
         sinopsis="Una noche dedicada a las canciones de Alicia Maguiña, cuya obra fue declarada Patrimonio Cultural de la Nación, en las voces de varios intérpretes de la música peruana.",
         ficha=[("Santiago Coco Linares", "dirección"), ("Santiago Coco Linares", "producción")],
         artistas=["Julie Freundt", "Nancy Manchego", "Julio Humala", "Lalo Arroyo", "Jorge Luis Jasso",
                   "Blanca Galdós", "Françoise Rodríguez"],
         horario_texto="Dom 20 set, 6 p. m.", inicio="2026-09-20", fin="2026-09-20", precio_desde=20, **SEG),
    obra("Teatro Segura", "Cosa Nuestra: Historia de la Salsa Criolla",
         fuente="prensa", url="https://caretas.pe/cultura/cosa-nuestra-en-el-teatro-segura/",
         tipo="concierto", generos=["salsa", "música criolla"],
         sinopsis="Concierto de gala con el que Cosa Nuestra repasa su mezcla de salsa y canción criolla, con varios cantantes invitados y baile en escena.",
         artistas=["Cosa Nuestra", "Tito Manrique", "Carlos Mosquera", "Sofía con Z", "José Francisco Valdelomar",
                   "Alex Ramírez", "Noelia Herencia", "Celeste Manrique"],
         horario_texto="Sáb 24 oct, 8 p. m.", inicio="2026-10-24", fin="2026-10-24", **SEG),
    obra("Teatro Segura", "A Jaranear en el Segura",
         fuente="municipalidad", url="https://www.gob.pe/institucion/munilima/noticias/1464359-a-celebrar-la-cancion-criolla-municipalidad-de-lima-organiza-espectaculos-musicales-talleres-y-actividades-para-toda-la-familia",
         url_compra="https://www.joinnus.com/events/concerts/lima-a-jaranear-en-el-segura-79394",
         tipo="concierto", generos=["música criolla"],
         sinopsis="Función por el Día de la Canción Criolla con tres nombres conocidos del género, parte de la programación municipal 'Lima de Jarana Criolla'.",
         artistas=["Los Doltons", "Marco Romero", "Los Kipus"],
         horario_texto="Sáb 31 oct, 6 p. m.", inicio="2026-10-31", fin="2026-10-31", **SEG),
    obra("Teatro Segura", "We The Lion 10 años – Unplugged",
         fuente="prensa", url="https://limeo.pe/evento/we-the-lion-10-anos-unplugged-en-el-teatro-segura-2026-12-05",
         url_compra="https://www.joinnus.com/events/concerts/lima-we-the-lion-10-anos-unplugged-en-el-teatro-segura-79361",
         tipo="concierto", generos=["pop", "rock", "acústico"],
         sinopsis="La banda limeña celebra una década con un concierto acústico acompañado por un ensamble sinfónico y nuevos arreglos de sus canciones.",
         artistas=["We The Lion"],
         horario_texto="Sáb 5 dic, 4 p. m. y 8 p. m.", inicio="2026-12-05", fin="2026-12-05", **SEG),
    obra("Teatro Segura", "Concierto de la Orquesta Sinfónica Nacional",
         fuente="ministerio de cultura", url="https://elencos.cultura.pe/evento/concierto-teatro-segura",
         tipo="concierto", generos=["música sinfónica"],
         sinopsis="La Orquesta Sinfónica Nacional sale del Gran Teatro Nacional para un concierto en el Centro Histórico, con director invitado; el programa aún no se ha publicado.",
         artistas=["Orquesta Sinfónica Nacional"], productora="Ministerio de Cultura",
         horario_texto="Mié 9 dic, 8 p. m.", inicio="2026-12-09", fin="2026-12-09", **SEG),
    obra("Teatro Segura", "Gala de Navidad de los Elencos Nacionales",
         fuente="ministerio de cultura", url="https://elencos.cultura.pe/evento/gala-de-navidad-3",
         tipo="concierto", generos=["navidad", "folklore", "música sinfónica"],
         sinopsis="Tres elencos del Ministerio de Cultura comparten escenario en una gala navideña que junta danza folclórica, orquesta juvenil y coro de niños.",
         artistas=["Ballet Folclórico Nacional", "Orquesta Sinfónica Nacional Juvenil Bicentenario", "Coro Nacional de Niños"],
         productora="Ministerio de Cultura",
         horario_texto="Mié 16 a vie 18 dic, 8 p. m.", inicio="2026-12-16", fin="2026-12-18", **SEG),

    # ---------------- Teatro Municipal del Cusco ----------------
    obra("Teatro Municipal del Cusco", "Festival Indomesticable 2026: Pachamama y sus alquimistas",
         fuente="prensa", url="https://altavoz.pe/culturales/gladis-huaman-soprano-del-bicentenario-participa-en-el-festival-indomesticable-2026-en-calca-y-cusco/",
         tipo="otro", generos=["festival", "artes escénicas", "performance"],
         sinopsis="Festival de artes escénicas sobre memoria y territorio, con funciones nocturnas, talleres e intervenciones de artistas de Perú, Brasil, Chile y México; en Cusco usó el Teatro Municipal, la Casa de la Cultura y espacios públicos.",
         ficha=[("Carlos Cruz", "dirección"), ("Oswaldo Povea", "dirección"), ("Mauricio Rueda", "dirección")],
         artistas=["Gladis Huamán", "Genifer Gerhardt", "Fernando Montanares", "Regina Maciel", "Carlos Cruz",
                   "Oswaldo Povea", "Mauricio Rueda"],
         productora="Transdisciplinar Escénicas",
         horario_texto="Funciones nocturnas; talleres por la mañana",
         inicio="2026-09-29", fin="2026-10-01", precio_desde=0, distrito="Cusco", ciudad="Cusco"),

    # ---------------- Teatro Municipal de Arequipa ----------------
    obra("Teatro Municipal de Arequipa", "Pájaros en la cabeza",
         fuente="prensa", url="https://diariocorreo.pe/edicion/arequipa/wendy-ramos-llega-a-arequipa-con-pajaros-en-la-cabeza-noticia/",
         tipo="show", generos=["unipersonal", "conferencia"],
         sinopsis="Wendy Ramos presenta su charla escénica sobre la creatividad cotidiana y el miedo a equivocarse, pensada para cualquier público y no solo para artistas.",
         elenco=[("Wendy Ramos", None)], duracion_min=90,
         horario_texto="Vie 16 oct", inicio="2026-10-16", fin="2026-10-16",
         distrito="Arequipa (Cercado)", ciudad="Arequipa"),

    # ---------------- Teatro Municipal de Puno (nueva) ----------------
    obra("Teatro Municipal de Puno", "Charangueando Puno 2026",
         fuente="prensa", url="https://radioondaazul.com/charangueando-puno-2026-reunira-a-charanguistas-en-concierto-gratuito-en-el-teatro-municipal/",
         tipo="concierto", generos=["charango", "música andina"],
         sinopsis="Segunda edición de este encuentro de charanguistas puneños, con un invitado limeño y un taller previo; un concierto gratuito de unas dos horas.",
         ficha=[("Ubi Espinosa", "producción")], artistas=["Percy Rojas Villadeza"],
         duracion_min=120, horario_texto="Jue 24 set, 6:30 p. m.",
         inicio="2026-09-24", fin="2026-09-24", precio_desde=0, distrito="Puno", ciudad="Puno"),
    obra("Teatro Municipal de Puno", "III Festival Multicultural Pawa Raymi",
         fuente="prensa", url="https://radioondaazul.com/puno-celebra-el-iii-festival-multicultural-pawa-raymi-con-artistas-de-varios-paises/",
         tipo="danza", generos=["festival", "danza", "multicultural"],
         sinopsis="Galas nocturnas de danza con elencos de China, Colombia, México y de varias regiones del Perú, acompañadas de talleres para estudiantes de arte en Puno y Juliaca.",
         artistas=["Rubén Saraza", "Marisol Zumeta"],
         horario_texto="Galas de 5 a 9 p. m.", inicio="2026-10-14", fin="2026-10-18", distrito="Puno", ciudad="Puno"),

    # ---------------- Cine Teatro Municipal de Huamanga (nueva) ----------------
    obra("Cine Teatro Municipal de Huamanga", "Ámame en Ayacucho",
         fuente="prensa", url="https://jornada.com.pe/sofy-alista-presentacion-en-el-teatro-municipal-con-amame-en-ayacucho-y-agota-zona-platinium/",
         tipo="concierto", generos=["pop", "música andina"],
         sinopsis="La cantautora ayacuchana SÖFY presenta su propuesta de pop con quechua y sonidos andinos, junto a varios artistas invitados.",
         artistas=["SÖFY", "Avril Navarro", "Atuq Sisa", "Karla Sofía", "Pooster"],
         horario_texto="Dom 27 set, 5 p. m.", inicio="2026-09-27", fin="2026-09-27", precio_desde=30,
         distrito="Ayacucho", ciudad="Ayacucho"),
    obra("Cine Teatro Municipal de Huamanga", "Dos leyendas del huayno ayacuchano",
         fuente="prensa", url="https://jornada.com.pe/trio-ayacucho-y-los-heraldos-de-puquio-compartiran-escenario-en-huamanga/",
         tipo="concierto", generos=["huayno", "música andina"],
         sinopsis="El Trío Ayacucho y Los Heraldos de Puquio comparten una noche dedicada al huayno de la región.",
         artistas=["Trío Ayacucho", "Los Heraldos de Puquio"],
         horario_texto="Mié 28 oct, 7 p. m.", inicio="2026-10-28", fin="2026-10-28",
         distrito="Ayacucho", ciudad="Ayacucho"),

    # ---------------- Tacna: Centro de Convenciones Jorge Basadre (nombre del catálogo) ----------------
    obra("C.C. Jorge Basadre Grohmann", "Los Panchos: Nostalgia Tour",
         fuente="prensa", url="https://diariocorreo.pe/espectaculos/los-panchos-regresan-al-peru-conciertos-en-tacna-y-lima-en-noviembre-de-2026-noticia/",
         url_compra="https://lospanchosnostalgiatour.com/nostalgia-tour/tacna",
         tipo="concierto", generos=["bolero"],
         sinopsis="El trío de boleros, hoy encabezado por Gabriel Vargas, repasa su repertorio clásico de requinto y armonías vocales.",
         artistas=["Los Panchos", "Gabriel Vargas", "José Carlos Reyes", "Miguel Ángel Pardo"],
         horario_texto="Dom 1 nov, 8 p. m.", inicio="2026-11-01", fin="2026-11-01",
         distrito="Tacna", ciudad="Tacna"),
]


# ------------------------------- Salas nuevas -------------------------------
SALAS_NUEVAS = [
    {
        "nombre": "Teatro Municipal de Puno",
        "alias": ["TEATRO MUNICIPAL DE PUNO", "Teatro Municipal Puno"],
        "ciudad": "Puno", "distrito": "Puno",
        "direccion": "Esquina Jr. Arequipa con Jr. Deza, Puno",
        "tipo": "municipal", "aforo_aprox": 701,
        "descripcion_corta": "Teatro de la Municipalidad Provincial de Puno, abierto en 1915 y remodelado; recibe festivales de danza, conciertos de música andina y teatro regional, muchas veces con ingreso libre.",
        "web": None, "instagram": None, "url_cartelera": None,
        "ticketera": ["entrada libre"],
        "coordenadas": None,
        "fuente": ["https://www.deperu.com/esparcimiento/teatros/teatro-municipal-de-puno-5312",
                   "https://radioondaazul.com/malestar-por-ingreso-restringido-a-evento-cultural-en-teatro-municipal-de-puno/",
                   "https://radioondaazul.com/charangueando-puno-2026-reunira-a-charanguistas-en-concierto-gratuito-en-el-teatro-municipal/",
                   "https://radioondaazul.com/puno-celebra-el-iii-festival-multicultural-pawa-raymi-con-artistas-de-varios-paises/"],
        "confianza": "media", "estado": "activa",
        "notas": "Aforo 701 (426 platea baja y 275 platea alta) según DePerú; Radio Onda Azul habla de 700 butacas (mayo 2026). Sin web propia: difunde por Facebook (https://www.facebook.com/Teatro-Municipal-PUNO-1635298496736811/, no consultado). Muchas funciones son gratuitas; en algunas la DDC Puno reparte entradas en sus oficinas. Coordenadas no verificadas (no está en OSM).",
    },
    {
        "nombre": "Cine Teatro Municipal de Huamanga",
        "alias": ["Teatro Municipal de Huamanga", "Cine Teatro Municipal", "Cine Municipal de Huamanga",
                  "Teatro Municipal de Ayacucho"],
        "ciudad": "Ayacucho", "distrito": "Ayacucho",
        "direccion": "Portal Municipal 44, Parque Sucre (Plaza de Armas), Ayacucho",
        "tipo": "municipal", "aforo_aprox": 320,
        "descripcion_corta": "Sala de la Municipalidad Provincial de Huamanga en el Portal Municipal de la plaza principal; acoge conciertos de música ayacuchana, festivales de la canción y teatro local.",
        "web": None, "instagram": None, "url_cartelera": None,
        "ticketera": ["reserva telefónica con el organizador"],
        "coordenadas": {"lat": -13.16041, "lng": -74.22511},
        "fuente": ["https://www.deperu.com/esparcimiento/teatros/cine-teatro-municipal-de-huamanga-5325",
                   "https://www.gob.pe/institucion/munihuamanga/noticias/1457964-huamanga-se-prepara-para-vibrar-con-el-xxxii-festival-de-la-cancion-ayacuchana",
                   "https://jornada.com.pe/teatros-cerrados-salas-convertidas-en-depositos-y-nulo-apoyo-institucional-la-crisis-del-arte-en-ayacucho/",
                   "https://jornada.com.pe/trio-ayacucho-y-los-heraldos-de-puquio-compartiran-escenario-en-huamanga/",
                   "https://nominatim.openstreetmap.org/"],
        "confianza": "media", "estado": "activa",
        "notas": "Aforo 320 según DePerú; en nov. 2025 Jornada informó que había perdido la mayor parte de sus butacas y equipamiento, así que el aforo real puede ser menor. La prensa lo llama indistintamente 'Teatro Municipal' o 'Cine Teatro Municipal'. No hay ticketera: cada organizador vende o reserva por teléfono. La municipalidad publica su agenda en Facebook (munihuamanga) y gob.pe.",
    },
    {
        "nombre": "Centro de Convenciones Jorge Basadre Grohmann",
        "alias": ["C.C. Jorge Basadre Grohmann", "C.C. JORGE BASADRE GROHMANN - TACNA", "Centro Cultural Jorge Basadre",
                  "CENTRO CULTURAL JORGE BASADRE - TACNA", "Centro de Convenciones Jorge Basadre", "Teatro Jorge Basadre"],
        "ciudad": "Tacna", "distrito": "Tacna",
        "direccion": "Calle Blondell 114, Tacna",
        "tipo": "estatal", "aforo_aprox": None,
        "descripcion_corta": "Centro de convenciones del Gobierno Regional de Tacna, reabierto en 2025; con el Teatro Municipal cerrado, es el principal escenario de la ciudad para conciertos, ballet y comedia.",
        "web": None, "instagram": None, "url_cartelera": None,
        "ticketera": ["Teleticket", "Passline"],
        "coordenadas": {"lat": -18.01462, "lng": -70.25309},
        "fuente": ["https://radiouno.pe/noticias/250080/tacna-proxima-a-inaugurar-nuevo-centro-de-convenciones-jorge-basadre",
                   "https://teleticket.com.pe/evento/mar-de-copas-en-tacna-cc-jorge-basadre-grohmann",
                   "https://diariocorreo.pe/espectaculos/los-panchos-regresan-al-peru-conciertos-en-tacna-y-lima-en-noviembre-de-2026-noticia/",
                   "https://nominatim.openstreetmap.org/"],
        "confianza": "media", "estado": "activa",
        "notas": "Lo administra el Gobierno Regional de Tacna (nota de Radio Uno, ago. 2025). Dirección y coordenadas según OpenStreetMap. Teleticket lo lista como 'C.C. Jorge Basadre Grohmann' y también como 'Centro Cultural Jorge Basadre'; Correo lo llamó 'Teatro Jorge Basadre'. Aforo no encontrado.",
    },
    {
        "nombre": "Teatro Municipal de Tacna",
        "alias": ["Teatro Municipal Doctor Luis Cavagnaro Orellana", "TEATRO MUNICIPAL DE TACNA"],
        "ciudad": "Tacna", "distrito": "Tacna",
        "direccion": "Pasaje Calderón de la Barca y calle 2 de Mayo, frente a la plaza MacLean, Tacna",
        "tipo": "municipal", "aforo_aprox": None,
        "descripcion_corta": "Teatro histórico de la Municipalidad Provincial de Tacna, levantado entre 1859 y 1870 y declarado monumento en 1972; está cerrado desde abril de 2025 por el mal estado del edificio.",
        "web": None, "instagram": None, "url_cartelera": None,
        "ticketera": [],
        "coordenadas": {"lat": -18.00993, "lng": -70.24922},
        "fuente": ["https://es.wikipedia.org/wiki/Teatro_Municipal_de_Tacna",
                   "https://larepublica.pe/sociedad/2025/04/07/clausuran-teatro-municipal-de-tacna-por-pesimo-estado-de-infraestructura-116186",
                   "https://radiouno.pe/noticias/281618/teatro-municipal-de-tacna-queda-en-espera-por-falta-de-presupuesto/",
                   "https://nominatim.openstreetmap.org/"],
        "confianza": "alta", "estado": "cerrada",
        "notas": "Clausurado el 7 de abril de 2025. En agosto de 2026 el Ministerio de Cultura dijo que la restauración queda en espera por falta de presupuesto (emergencia por El Niño) y que buscará APP u Obras por Impuestos. Renombrado en 2022 en honor a Luis Cavagnaro Orellana.",
    },
    {
        "nombre": "Teatro Municipal de Piura",
        "alias": ["Nuevo Teatro Municipal de Piura", "TEATRO MUNICIPAL DE PIURA"],
        "ciudad": "Piura", "distrito": "Piura",
        "direccion": "Frente a la plaza Salaverry, barrio de La Mangachería, Piura",
        "tipo": "municipal", "aforo_aprox": 804,
        "descripcion_corta": "Nuevo teatro de la Municipalidad Provincial de Piura, en construcción desde noviembre de 2025 en el lugar del antiguo, que colapsó; el proyecto contempla 804 butacas y foso para orquesta.",
        "web": None, "instagram": None, "url_cartelera": None,
        "ticketera": [],
        "coordenadas": None,
        "fuente": ["https://www.gob.pe/institucion/munipiura/noticias/1297101-piura-inicia-la-construccion-de-su-nuevo-teatro-municipal",
                   "https://www.gob.pe/institucion/munipiura/noticias/1442742-nuevo-teatro-municipal-avanza-con-infraestructura-de-alto-nivel-y-se-perfila-como-referente-cultural-del-norte"],
        "confianza": "alta", "estado": "en_obras",
        "notas": "Aforo es el del proyecto (804 butacas, 10 espacios para silla de ruedas). Avance físico de 28 % al 10/09/2026; plazo de obra de 540 días. Sin programación hasta su apertura; los espectáculos de gira en Piura usan auditorios privados o universitarios. Dirección exacta no publicada.",
    },
    {
        "nombre": "Teatro Cajamarca",
        "alias": ["Teatro Municipal de Cajamarca", "TEATRO CAJAMARCA"],
        "ciudad": "Cajamarca", "distrito": "Cajamarca",
        "direccion": "Esquina Jr. Junín y Jr. Arequipa, Cajamarca",
        "tipo": "estatal", "aforo_aprox": None,
        "descripcion_corta": "Teatro centenario del centro histórico de Cajamarca, a cargo de la Dirección de Cultura; está cerrado desde 2012 por fallas estructurales.",
        "web": None, "instagram": None, "url_cartelera": None,
        "ticketera": [],
        "coordenadas": None,
        "fuente": ["https://www.regioncajamarca.gob.pe/portal/noticias/det/9331",
                   "https://www.deperu.com/esparcimiento/teatros/teatro-cajamarca-5318"],
        "confianza": "media", "estado": "cerrada",
        "notas": "En agosto de 2024 el Gobierno Regional anunció su rehabilitación por Obras por Impuestos con Southern Perú (S/ 8,06 millones); no se hallaron avances en 2025-2026. Dirección según DePerú (fuente única). No se identificó otro teatro público activo en la ciudad.",
    },
    {
        "nombre": "Teatro Dos de Mayo",
        "alias": ["Teatro 2 de Mayo", "Teatro Dos de Mayo de Chiclayo"],
        "ciudad": "Chiclayo", "distrito": "Chiclayo",
        "direccion": "Calle Alfredo Lapoint 909, Chiclayo",
        "tipo": "institucional", "aforo_aprox": None,
        "descripcion_corta": "Teatro histórico de Chiclayo, de 1878, propiedad de la Sociedad de Beneficencia; está clausurado y muy deteriorado, a la espera de un proyecto de restauración.",
        "web": None, "instagram": None, "url_cartelera": None,
        "ticketera": [],
        "coordenadas": None,
        "fuente": ["https://www.deperu.com/esparcimiento/teatros/teatro-dos-de-mayo-de-chiclayo-5313",
                   "https://www.gob.pe/institucion/munichiclayo/noticias/1015899-comision-realiza-visita-al-local-del-teatro-dos-de-mayo"],
        "confianza": "media", "estado": "cerrada",
        "notas": "Chiclayo no tiene teatro municipal. En 2024 la municipalidad encabezó una comisión para restaurarlo; en la visita se constató el robo de casi todas las butacas. Los espectáculos de gira van a auditorios de colegios y universidades privadas o al Teatro Moline.",
    },
]

# Campos en null de salas existentes que se completan con datos verificados.
COMPLETAR = {
    "Teatro Municipal del Cusco": {"web": "https://teatro-municipal.cusco.gob.pe/"},
}


def main():
    cat = json.load(open(DATA / "catalogo.json"))
    salas_json = json.load(open(DATA / "salas.json"))

    # Títulos ya presentes por sala (catálogo + obras extraídas de webs de salas).
    sala_slug = {}
    for s in cat["salas"]:
        sala_slug[slug(s["nombre"])] = s["slug"]
    for s in salas_json:
        for n in [s["nombre"], *s.get("alias", [])]:
            sala_slug.setdefault(slug(n), slug(s["nombre"]))
    obras_cat = {o["slug"]: o for o in cat["obras"]}
    ya = set()
    for s in cat["salas"]:
        for o in s["obras"]:
            ya.add((s["slug"], clave_titulo(obras_cat[o]["titulo"])))

    salida, descartadas = [], []
    for o in OBRAS:
        clave = (sala_slug.get(slug(o["sala"]), slug(o["sala"])), clave_titulo(o["titulo"]))
        if clave in ya:
            descartadas.append(o["titulo"])
            continue
        salida.append(o)
    ids = [o["id"] for o in salida]
    assert len(ids) == len(set(ids)), "ids repetidos"
    SALIDA.write_text(json.dumps(salida, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(salida)} obras -> {SALIDA}  (descartadas por duplicado: {descartadas})")

    # salas.json: completar nulls y agregar nuevas al final
    existentes = {slug(n) for s in salas_json for n in [s["nombre"], *s.get("alias", [])]}
    for s in salas_json:
        for campo, valor in COMPLETAR.get(s["nombre"], {}).items():
            if s.get(campo) is None:
                s[campo] = valor
                print(f"completado {s['nombre']}.{campo}")
    agregadas = []
    for s in SALAS_NUEVAS:
        if slug(s["nombre"]) in existentes:
            print("ya existe:", s["nombre"])
            continue
        salas_json.append(s)
        agregadas.append(s["nombre"])
    (DATA / "salas.json").write_text(json.dumps(salas_json, ensure_ascii=False, indent=2), encoding="utf-8")
    print("salas agregadas:", agregadas)


if __name__ == "__main__":
    main()
