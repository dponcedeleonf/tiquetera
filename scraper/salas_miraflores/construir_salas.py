"""Arma data/salas_miraflores.json: espacios escénicos de Miraflores que no están en data/salas.json,
más fichas completas de salas que ya están allí pero a las que se les completaron datos (ver 'notas').
No modifica salas.json. Coordenadas: raw/salas_miraflores/coordenadas.json (geocodificar.py, Nominatim),
solo cuando OSM ubicó el número exacto; si solo halló la calle se deja null."""
import json, pathlib, copy

R = pathlib.Path(__file__).resolve().parent.parent
salas = json.load(open(R / "data/salas.json"))
por_nombre = {s["nombre"]: s for s in salas}
NOM = "https://nominatim.openstreetmap.org/"


def sala(nombre, alias, direccion, tipo, descripcion, web=None, instagram=None, url_cartelera=None, ticketera=(), coordenadas=None,
         fuente=(), confianza="media", estado="activa", notas=None, aforo=None):
    return {"nombre": nombre, "alias": list(alias), "ciudad": "Lima", "distrito": "Miraflores", "direccion": direccion, "tipo": tipo,
            "aforo_aprox": aforo, "descripcion_corta": descripcion, "web": web, "instagram": instagram, "url_cartelera": url_cartelera,
            "ticketera": list(ticketera), "coordenadas": coordenadas, "fuente": list(fuente), "confianza": confianza, "estado": estado, "notas": notas}


NUEVAS = [
    sala("Cocodrilo Verde", ["Cocodrilo Verde Lounge", "Cocodrilo Verde Bar"], "Calle Francisco de Paula Camino 226, Miraflores", "bar/club",
         "Bar lounge de música en vivo con 25 años en Miraflores; de martes a sábado programa tributos, rock, salsa, criollo, jazz y algún stand-up.",
         web="https://cocodriloverde.com/", instagram="https://www.instagram.com/cocodriloverdel/", url_cartelera="https://cocodriloverde.com/cartelera/",
         ticketera=["WhatsApp", "Joinnus", "Passline", "Ticketmaster", "Atrápalo"],
         fuente=["https://cocodriloverde.com/", "https://cocodriloverde.com/cartelera/", "https://cocodriloverde.com/cpt_conciertos-sitemap.xml"],
         confianza="alta",
         notas="La web publica cada show con fecha, hora y precio (sitemap de 'conciertos'). La mayoría se reserva por WhatsApp (enlaces wa.link); algunos van por Joinnus, Passline, Atrápalo, Ticketmaster o saund.live. Consumo mínimo S/50 por persona (S/25 estudiantes). Coordenadas no halladas en OSM."),
    sala("Jazz Zone", ["Jazz Zone Perú", "JAZZ ZONE", "JAZZZONE DE MIRAFLORES", "Jazz Zone - Pasaje el Suche"], "Av. La Paz 656, Pasaje El Suche, Miraflores", "bar/club",
         "Club de jazz del Pasaje El Suche con música en vivo casi todas las noches: jazz afroperuano, salsa, tributos de rock, teatro de pequeño formato y stand-up.",
         web="https://www.jazzzoneperu.com/", instagram="https://www.instagram.com/jazzzoneperu", url_cartelera="https://www.jazzzoneperu.com/#programacion-mensual",
         ticketera=["Teleticket", "Joinnus", "WhatsApp", "Atrápalo", "Vaope"], coordenadas={"lat": -12.12387, "lng": -77.02728},
         fuente=["https://www.jazzzoneperu.com/", "https://teleticket.com.pe/evento/nos-casamos-la-cagamos-jazz-zone-2026", NOM],
         confianza="alta",
         notas="La programación mensual de la web se carga en un modal por fecha (Livewire); se leyó con Playwright (jazzzone.js). Cada show enlaza a su propio canal de venta (Teleticket, Joinnus, Atrápalo, Vaope, ticketya.pe, jazzperu.org o WhatsApp). Consumo mínimo S/40 por persona (S/60 los jueves de jazz afroperuano)."),
    sala("Asociación Cultural Campo Abierto", ["Campo Abierto", "ASOCIACIÓN CULTURAL CAMPO ABIERTO", "ASOCIACIÓN CULTURAL CAMPO ABIERTO - MIRAFLORES - LIMA"],
         "Calle General Recavarren 560, Miraflores", "independiente",
         "Casa con jardín dedicada sobre todo al teatro infantil de fin de semana (versiones de cuentos clásicos), con temporadas ocasionales para adultos.",
         ticketera=["Teleticket"],
         fuente=["https://teleticket.com.pe/evento/el-acustico-del-lobo-feroz", "https://diariocorreo.pe/noticias/obra-teatral/"],
         notas="Sin web propia (campoabierto.pe es otra empresa, de miel). Difunde por redes sociales. En 2026 también acogió 'Dos siglos de sobremesa' (desde el 6 de marzo) y 'El tiempo todo locura', según Correo. Coordenadas no confirmadas (OSM la ubicó en Surquillo)."),
    sala("Rock And Pez", ["Rock and Pez", "Rock & Pez", "Rock And Pez - MIRAFLORES - LIMA"], "Av. Alfredo Benavides 2824-2826, Miraflores", "bar/club",
         "Restobar de la cuadra 28 de Benavides con noches de tributos y conciertos de rock y pop en formato cena-show.",
         ticketera=["Teleticket"],
         fuente=["https://teleticket.com.pe/evento/tributo-a-bon-jovi-av-alfredo-benavides-2826-miraflores", "https://teleticket.com.pe/evento/dioses-del-rock-rock-and-pez"],
         notas="Fichas de Teleticket indican consumo mínimo de S/40 por persona. Sin web ni redes verificadas. Coordenadas no confirmadas (OSM solo ubicó la avenida)."),
    sala("Club de Teatro de Lima", ["Club del Teatro de Lima"], "Av. 28 de Julio 183, Miraflores", "independiente",
         "Escuela de teatro de larga trayectoria con sala propia en Miraflores, donde se presentan montajes de sus egresados y producciones independientes.",
         web="https://clubdeteatrodelima.com/", ticketera=["WhatsApp"], coordenadas={"lat": -12.12553, "lng": -77.03243},
         fuente=["https://clubdeteatrodelima.com/", "https://diariocorreo.pe/cultura/obra-teatral-nosotros-lo-hicimos-bien-se-estrena-en-lima-fechas-horario-y-entradas-noticia/", NOM],
         notas="Activa en 2026: en setiembre presentó 'Nosotros lo hicimos bien' (preventa por WhatsApp de la producción). La web se centra en cursos; no publica cartelera."),
    sala("Auditorio Británico Miraflores", ["Auditorio BRITÁNICO Miraflores", "Auditorio Miraflores (Británico)", "Británico · Miraflores"],
         "Calle Bellavista 531, Miraflores", "institucional",
         "Auditorio de la sede Miraflores del Británico, junto al Teatro Británico, con temporadas cortas de teatro, musicales, obras familiares y conciertos.",
         web="https://britanico.edu.pe/cultural/", url_cartelera="https://britanico.edu.pe/cultural/eventos/", ticketera=["Joinnus", "entrada libre"],
         fuente=["https://britanico.edu.pe/cultural/eventos/victoria-un-nuevo-musical/", "https://entradalibre.me/event/octubre-criollo-2/"],
         notas="Es un espacio distinto del Teatro Británico (Bellavista 527); la web del Británico permite filtrar 'Auditorio Miraflores'. Número 531 según Entrada Libre."),
    sala("Cultural Station (Británico)", ["Studio Cultural Station", "Cultural Station"], "Calle Bellavista 538, Miraflores", "institucional",
         "Espacio multiuso del Británico frente a su sede de Miraflores: conciertos gratuitos, danza, cine al aire libre y ferias.",
         web="https://britanico.edu.pe/cultural/", url_cartelera="https://britanico.edu.pe/cultural/eventos/", ticketera=["entrada libre"],
         fuente=["https://britanico.edu.pe/sedes/", "https://britanico.edu.pe/cultural/eventos/octubre-criollo-concierto/"],
         notas="Horario de martes a domingo de 1 a 9 p. m. según la página de sedes del Británico."),
    sala("Casa Tovar", ["Sala Tovar", "Casa del Adulto Mayor Tovar"], "Calle Manuel Tovar 255, Miraflores", "municipal",
         "Sala de la Casa del Adulto Mayor de la Municipalidad de Miraflores, que acoge temporadas teatrales y funciones gratuitas del taller de teatro municipal.",
         ticketera=["entrada libre"],
         fuente=["https://www.miraflores.gob.pe/miraflores-presenta-temporada-teatral-con-propuestas-inspiradas-en-la-historia-y-tradicion-peruana/",
                 "https://www.miraflores.gob.pe/miraflores-abre-una-nueva-temporada-de-teatro-gratuito-para-toda-la-comunidad/",
                 "https://entradalibre.me/event/el-origen-del-mundo/"],
         notas="En 2026 tuvo 'Tradiciones en salsa verde' (hasta el 15 de junio), el taller de teatro del adulto mayor (14 al 16 de julio) y 'El origen del mundo' (22 de setiembre). Programación irregular."),
    sala("Lugar de la Memoria (LUM)", ["LUM", "Lugar de la Memoria, la Tolerancia y la Inclusión Social"], "Bajada San Martín 151, Miraflores", "estatal",
         "Museo del Ministerio de Cultura sobre el periodo de violencia 1980-2000; su auditorio programa teatro, música y cine con ingreso libre.",
         web="https://lum.cultura.pe/", url_cartelera="https://lum.cultura.pe/actividades/agenda-septiembre-2026", ticketera=["entrada libre"],
         coordenadas={"lat": -12.11005, "lng": -77.05369},
         fuente=["https://lum.cultura.pe/", "https://lum.cultura.pe/actividades/agenda-septiembre-2026", NOM],
         confianza="alta", notas="Publica una agenda mensual en su web (la última disponible al 29/10/2026 es la de setiembre)."),
    sala("Centro Cultural Cayetano Heredia", ["Centro Cultural Cayetano", "Centro Cultural de la UPCH", "Casa Honorio Delgado"],
         "Av. Armendáriz 445, Miraflores", "universitaria",
         "Centro cultural de la Universidad Peruana Cayetano Heredia con conciertos gratuitos casi semanales: cámara, jazz, coros, zarzuela y música peruana.",
         ticketera=["entrada libre"], coordenadas={"lat": -12.13406, "lng": -77.02636},
         fuente=["https://entradalibre.me/event/cuarteto-armonia/", "https://entradalibre.me/event/esquinas-brillantes-bebop-en-lima/", NOM],
         notas="Sin web de agenda localizada; difunde por redes y por la agenda de Entrada Libre. Algunas funciones piden inscripción previa."),
    sala("Anfiteatro Chabuca Granda (Parque Kennedy)", ["Anfiteatro del Parque Kennedy", "Parque Kennedy"], "Parque Kennedy (Parque 7 de Junio), Miraflores", "municipal",
         "Anfiteatro al aire libre del Parque Kennedy donde la municipalidad y colectivos programan conciertos y espectáculos gratuitos.",
         ticketera=["entrada libre"], coordenadas={"lat": -12.12178, "lng": -77.03042},
         fuente=["https://entradalibre.me/event/punk-en-el-kennedy/", NOM],
         confianza="baja", notas="Programación esporádica; la municipalidad la anuncia en las redes de Cultura Miraflores. Coordenadas del parque, no del anfiteatro."),
    sala("Ritual Virtual", [], "Calle Esperanza 339, Miraflores", None,
         "Espacio de Miraflores que acoge encuentros de música electrónica experimental y conversatorios con música en vivo.",
         ticketera=["entrada libre"], fuente=["https://entradalibre.me/event/la-pena-de-los-sintes-5/", "https://entradalibre.me/event/ruidos-mentales/"],
         confianza="baja", notas="Tipo de local no confirmado (no se halló web). 'La peña de los sintes' va por su quinta edición, lo que sugiere un ciclo recurrente."),
    sala("4 Queens", ["4 Queens Lucky Bar", "4 QUEENS - MIRAFLORES - LIMA"], "Calle Manuel Bonilla 138, Miraflores", "bar/club",
         "Bar de coctelería cerca del Parque Kennedy que suma noches de stand-up y shows de comedia.",
         ticketera=["Teleticket", "Joinnus"], fuente=["https://teleticket.com.pe/evento/empareja2-4-queens-calle-manuel-bonilla-138"],
         confianza="baja",
         notas="Teleticket tuvo el show 'Empareja2' (consumo mínimo S/40); la ficha ya no muestra fecha. No se halló cartelera en fuentes permitidas; un agregador (limeo.pe) lista shows de stand-up en oct-nov 2026, sin confirmar."),
    sala("Auditorio Juana Alarco de Dammert", ["Auditorio del colegio Juana Alarco de Dammert"], "Av. Alfredo Benavides 2315, Miraflores", "institucional",
         "Auditorio de la institución educativa Juana Alarco de Dammert que se alquila para funciones de teatro infantil.",
         ticketera=["Teleticket"], coordenadas={"lat": -12.12675, "lng": -77.00834},
         fuente=["https://teleticket.com.pe/evento/el-sastrecito-valiente-auditorio-juana-alarco-de-dammert", NOM],
         confianza="media", notas="Uso eventual (en el catálogo figura 'El sastrecito valiente', noviembre 2026). Otras fuentes dan el número 2320."),
    sala("Colegio Hosanna", ["COLEGIO HOSANNA"], "Av. Grau 441, Miraflores", "institucional",
         "Colegio de Miraflores que vende por Teleticket su espectáculo escolar de fin de año.",
         ticketera=["Teleticket"], fuente=["https://teleticket.com.pe/evento/hosanna-magia-en-el-escenario-colegio-hosanna"],
         confianza="baja", notas="No es una sala de programación regular; se incluye solo porque aparece en el catálogo (función escolar del 20 y 21 de noviembre de 2026)."),
]

# Salas que ya están en salas.json y a las que se les completan datos
ACTUALIZAR = {
    "Teatro Larco": dict(estado="cerrada", confianza="media", web=None,
        fuente_extra=["https://nexoinmobiliario.pe/departamentos/miraflores/larco-1036-atemporal-flats-miraflores-3753",
                      "https://urbania.pe/inmueble/proyecto/ememvein-proyecto-proyecto-vertical-en-miraflores-lima-miraflores-libre-inmobiliaria-145344623"],
        notas="Se completó 'estado': en Av. Larco 1036 se construye el edificio 'Larco 1036 Atemporal Flats' (Libre Inmobiliaria; 'en construcción', entrega prevista 2027-2028 según portales inmobiliarios), así que la sala ya no existe en ese predio. Tampoco hay funciones 2025-2026 en Teleticket, prensa ni agendas; su ficha en enlima.pe solo conserva teléfono y Facebook. No se halló nota oficial de cierre."),
    "Teatro de Lucía": dict(instagram="https://www.instagram.com/teatrodelucia/",
        fuente_extra=["https://teatrodelucia.com/data/cartelera.json"],
        ticketera=["Joinnus", "web propia", "boletería", "WhatsApp"],
        notas="Se completó 'instagram' con el perfil enlazado en la propia web (data/cartelera.json, que también da X/Twitter @TeatrodeLucia). La reserva directa en la web se paga con Yape; las tarifas con descuento se compran solo en Joinnus. Tiene 2 espacios para silla de ruedas en la fila J."),
    "Centro Cultural Ricardo Palma": dict(instagram="https://www.instagram.com/cultura.miraflores/",
        fuente_extra=["https://www.miraflores.gob.pe/los-servicios/cultura-y-turismo/"],
        notas="Se completó 'instagram' con la cuenta de la Gerencia de Cultura de Miraflores (cultura.miraflores), que la web municipal señala como canal de su programación; el centro no tiene cuenta propia verificada. Su sala de funciones es el Auditorio/Sala Julio Ramón Ribeyro. La ticketera depende de la producción (Joinnus, Teleticket o boletería)."),
    "ICPNA Miraflores (Auditorio)": dict(ticketera=["Joinnus"],
        fuente_extra=["https://www.icpna.edu.pe/api/events/v1/entries?date_from=2026-09-17&date_to=2027-01-31&limit=50&offset=0"],
        notas="Se completó 'ticketera': la API de eventos del ICPNA da como enlace de compra de 'Fedra' una página de Joinnus. Algunas actividades (danza, FILIJ) son de ingreso libre."),
}
salida = []
for s in NUEVAS:
    if s["nombre"] in por_nombre:
        print("ya está en salas.json, se omite como nueva:", s["nombre"]); continue
    salida.append(s)
for nombre, cambios in ACTUALIZAR.items():
    if nombre not in por_nombre:
        print("no está en salas.json:", nombre); continue
    s = copy.deepcopy(por_nombre[nombre])
    extra = cambios.pop("fuente_extra", [])
    nota = cambios.pop("notas")
    s.update(cambios)
    s["fuente"] = s["fuente"] + [u for u in extra if u not in s["fuente"]]
    s["notas"] = nota + (" Nota previa: " + por_nombre[nombre]["notas"] if por_nombre[nombre].get("notas") else "")
    salida.append(s)
claves = list(salas[0].keys())
for s in salida:
    assert list(s.keys()) == claves, (s["nombre"], list(s.keys()))
dest = R / "data/salas_miraflores.json"
dest.write_text(json.dumps(salida, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
json.loads(dest.read_text())
print(len(salida), "salas ->", dest)
