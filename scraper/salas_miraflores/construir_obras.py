"""Arma data/extraido/salas_miraflores.json con la cartelera nueva de los espacios de Miraflores.

Entradas (todas en raw/salas_miraflores/, generadas por los otros scripts de esta carpeta):
  cocodrilo.json (cocodrilo.py), jazzzone_modales.json (jazzzone.js), y fichas leídas a mano
  de webs de salas, Diario Correo, Caretas, Infobae, En Lima, Entrada Libre y Teleticket.
Las sinopsis están escritas para este archivo (no copiadas).
Se descarta todo lo que ya esté en data/catalogo.json para la misma sala (comparación por título).
"""
import json, re, pathlib, unicodedata, datetime

R = pathlib.Path(__file__).resolve().parent.parent
RAW = R / "raw/salas_miraflores"
HOY = "2026-10-29"
DESDE = "2026-09-17"   # seis semanas atrás


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def obra(sala, titulo, fuente, url, tipo, sinopsis, inicio, fin, horario, precio=None, url_compra=None, generos=(),
         elenco=(), ficha=(), artistas=(), productora=None, duracion=None, edad=None):
    return {
        "id": f"mfl-{slug(sala)}-{slug(titulo)}"[:120],
        "fuente": fuente, "url": url, "url_compra": url_compra, "incluir": True,
        "titulo": titulo, "tipo": tipo, "generos": list(generos)[:3], "sinopsis": sinopsis,
        "elenco": [{"nombre": n, "personaje": p} for n, p in elenco],
        "ficha": [{"nombre": n, "rol": r} for n, r in ficha],
        "artistas": list(artistas), "productora": productora,
        "sala": sala, "distrito": "Miraflores", "ciudad": "Lima",
        "duracion_min": duracion, "edad_minima": edad,
        "horario_texto": horario, "temporada": {"inicio": inicio, "fin": fin},
        "precio_desde": precio, "imagen": None,
    }


E = lambda *ns: [(n, None) for n in ns]   # elenco sin personaje
OBRAS = []
add = OBRAS.append

# ---------------------------------------------------------------- Teatro La Plaza (web de la sala)
add(obra("Teatro La Plaza", "Prima Facie", "web de la sala", "https://laplaza.com.pe/obras-archive/prima-facie-2026/", "teatro",
         "Unipersonal sobre una abogada penalista que, tras vivir una agresión, descubre desde el otro lado las grietas del sistema que defendía. Una pieza intensa sobre justicia, verdad y consentimiento.",
         "2026-08-11", "2026-09-27", "Mar a sáb 8 p. m.; dom 7 p. m.", generos=["drama", "unipersonal"],
         elenco=E("Wendy Vásquez Larraín"), ficha=[("Juan Carlos Fisher", "dirección"), ("Rómulo Assereto", "otro"), ("Analucía Rodríguez", "otro")],
         duracion=90, edad=16))
add(obra("Teatro La Plaza", "Perseo (dos reinas y un funeral)", "web de la sala", "https://laplaza.com.pe/obras-archive/perseo-dos-reinas-y-un-funeral/", "comedia",
         "Comedia negra de trasnoche en la que dos leyendas del café teatro quedan atrapadas en la discoteca donde empezaron y deben salvar el pellejo. Un homenaje desenfadado a la memoria queer limeña.",
         "2026-08-28", "2026-09-26", "Vie y sáb 10:30 p. m.", generos=["comedia negra", "trasnoche"],
         elenco=E("Coco Marusix", "Naamin Timoyco", "La Langosta"),
         ficha=[("Mario Saldaña", "dramaturgia"), ("Mario Saldaña", "dirección"), ("Ernesto Pimentel", "producción"), ("Sandra Begué", "coreografía")], edad=18))
add(obra("Teatro La Plaza", "Sala de Parto 2026: lecturas dramatizadas", "prensa", "https://entradalibre.me/event/temporal/", "teatro",
         "Cinco noches del encuentro de dramaturgia de La Plaza con lecturas de textos nuevos: Temporal, Cómo nombrar un ave palestina, La ideología de la ornitorrinca, Mor y Amor eterno. Entrada libre.",
         "2026-09-29", "2026-10-03", "29 sep al 3 oct, 8 p. m.", precio=0, generos=["dramaturgia peruana", "lectura dramatizada"],
         ficha=[("Caro Black Tam", "dramaturgia"), ("Verony Centeno", "dirección"), ("Camila Abufom Saba", "dramaturgia"), ("Malu Gil", "dirección"),
                ("Patricia Romero Figueroa", "dramaturgia"), ("Patricia Romero Figueroa", "dirección"), ("Carenn Cabrera", "dramaturgia"), ("Emmy Linnéa", "dramaturgia")]))

# ---------------------------------------------------------------- Británico (web de la sala)
add(obra("Auditorio Británico Miraflores", "Victoria, un nuevo musical", "web de la sala", "https://britanico.edu.pe/cultural/eventos/victoria-un-nuevo-musical/", "musical",
         "Musical de canciones originales sobre una mujer que levantó un imperio en un mundo de hombres y ve cómo su pasado amenaza con derrumbarlo. Protagoniza Cynthia Bravo.",
         "2026-09-17", "2026-09-27", "Jue a sáb 8:30 p. m.; dom 8 p. m.", precio=45, generos=["musical", "drama"],
         elenco=E("Cynthia Bravo"), ficha=[("Malu Gil", "dramaturgia"), ("Ángela Mesa", "dramaturgia"), ("Sebastián Abad", "música"),
                                          ("Malu Gil", "dirección"), ("Alessandra Rodríguez", "música")], edad=16))
add(obra("Auditorio Británico Miraflores", "El niño cuentahistorias", "web de la sala", "https://britanico.edu.pe/cultural/eventos/el-nino-cuentahistorias/", "infantil",
         "Un niño armado con una libreta les cuenta sus historias a una roca, un ratón y una lluvia llorona, y en ese juego va asomando su propia historia. Obra familiar ganadora del Premio Nacional de Dramaturgia 2025.",
         "2026-09-26", "2026-10-11", "Sáb y dom 4 p. m.", precio=40, generos=["familiar", "teatro infantil"],
         elenco=E("Luisa Caldas", "Ethel Requejo", "Aries Córdova", "Miranda Valenza"),
         ficha=[("Henry Sotomayor", "dramaturgia"), ("Henry Sotomayor", "dirección"), ("Fantasía Guevara", "otro"), ("Paulo Ramírez", "música")], edad=2))
add(obra("Cultural Station (Británico)", "Octubre criollo: Blanca Galdos", "web de la sala", "https://britanico.edu.pe/cultural/eventos/octubre-criollo-concierto/", "concierto",
         "Concierto gratuito por el mes de la canción criolla en el que Blanca Galdos repasa clásicos del cancionero peruano con guitarra y percusión.",
         "2026-10-28", "2026-10-28", "Mié 28 oct, 7:30 p. m.", precio=0, generos=["música criolla"],
         artistas=["Blanca Galdos", "Juan Briceño", "Carlos Octavio Ticona Alfaro"], edad=10))
add(obra("Teatro Británico", "El Reino de Dios está entre los árboles", "web de la sala", "https://britanico.edu.pe/cultural/eventos/el-reino-de-dios-esta-entre-los-arboles/", "concierto",
         "La cantautora La Lá presenta en vivo su quinto álbum, un disco que decidió no publicar en plataformas y que solo puede escucharse en concierto.",
         "2026-11-13", "2026-11-13", "Vie 13 nov, 8 p. m.", precio=45, generos=["canción de autor"],
         artistas=["La Lá", "Tate Passaro", "César Gabriel Riveros", "Daira Bismark", "Leo Barraza", "Junior Pacora"]))
add(obra("Cultural Station (Británico)", "Danza de la Esperanza", "web de la sala", "https://britanico.edu.pe/cultural/eventos/danza-de-la-esperanza-noviembre/", "danza",
         "Función de fin de año del programa Danza de la Esperanza, en la que niños y jóvenes bailan danza contemporánea acompañados por la Orquesta Sinfónica del Británico. Ingreso libre.",
         "2026-11-21", "2026-11-21", "Sáb 21 nov, 7 p. m.", precio=0, generos=["danza contemporánea"],
         artistas=["Danza de la Esperanza", "Orquesta Sinfónica del BRITÁNICO"]))

# ---------------------------------------------------------------- Alianza Francesa
add(obra("Teatro de la Alianza Francesa de Lima", "Las bodas de Fígaro", "prensa",
         "https://diariocorreo.pe/cultura/las-bodas-de-figaro-llega-a-lima-exodo-teatro-presenta-el-clasico-frances-de-beaumarchais-noticia/", "teatro",
         "Éxodo Teatro monta la comedia de Beaumarchais: un día de enredos en el castillo del conde Almaviva, donde los sirvientes conspiran para frustrar sus avances sobre la novia de Fígaro.",
         "2026-08-13", "2026-09-26", "Jue a sáb 8 p. m.", generos=["comedia", "clásico"],
         elenco=[("Fernando Luque", "Fígaro")], ficha=[("Pierre-Augustin de Beaumarchais", "dramaturgia"), ("Jean Pierre Gamarra", "dirección"), ("Lorenzo Albani", "escenografía")],
         productora="Éxodo Teatro", duracion=110, edad=12))
add(obra("Teatro de la Alianza Francesa de Lima", "El percusionista ciego", "web de la sala", "https://aflima.org.pe/evento/el-percusionista-ciego/", "teatro",
         "Un músico que se orienta por el sonido y conversa con el mar ve alterado su mundo por una presencia inesperada. Teatro con percusión en vivo y paisaje sonoro, en la Sala Lumière.",
         "2026-10-06", "2026-10-13", "6, 7, 12 y 13 oct, 8 p. m. (Sala Lumière)", generos=["teatro sonoro", "música en vivo"],
         elenco=E("Lucho Ramírez", "Gabriel Mujica", "Lina Fuentes"),
         ficha=[("Lucho Ramírez", "dirección"), ("Lucho Ramírez", "dramaturgia"), ("Manongo Mujica", "música"), ("Terje Evensen", "música"),
                ("Juan José Salazar", "otro"), ("Víctor Checa", "otro"), ("Arabela Bartra", "producción")]))
add(obra("Teatro de la Alianza Francesa de Lima", "Ciclo de Jazz Europeo: Nuevo Perú", "web de la sala", "https://aflima.org.pe/evento/ciclo-de-jazz-europeo/", "concierto",
         "Jean Pierre Magnet, Chino Figueroa y César Ballumbrosio abren el Ciclo de Jazz Europeo con un concierto que cruza el jazz con ritmos de la costa y los Andes. Ingreso libre.",
         "2026-10-28", "2026-10-28", "Mié 28 oct, 8 p. m.", precio=0, generos=["jazz", "fusión peruana"],
         artistas=["Jean Pierre Magnet", "Chino Figueroa", "César Ballumbrosio"]))
add(obra("Teatro de la Alianza Francesa de Lima", "BABEL", "web de la sala", "https://aflima.org.pe/evento/novtec-x-festival-de-arte-y-cultura-digital/", "concierto",
         "Cierre del festival NOVTEC: concierto audiovisual inmersivo de la compañía francesa ENTER.black sobre la comunicación entre culturas, con un episodio creado para el Perú junto a Chaska Paucar. En el Espacio Libertad de la Alianza.",
         "2026-11-21", "2026-11-21", "Sáb 21 nov, 8 p. m. (Espacio Libertad)", generos=["audiovisual", "electrónica"],
         artistas=["ENTER.black", "Fanny Fortage", "Harry Clunet-Farlow", "Chaska Paucar"], duracion=60, edad=12))

# ---------------------------------------------------------------- ICPNA
add(obra("ICPNA Miraflores (Auditorio)", "Danza del fuego", "prensa", "https://entradalibre.me/event/danza-del-fuego/", "danza",
         "Performance de danza inspirada en la muestra «Soñar con fuego» de María Abaddon, que explora el cuerpo fragmentado y la violencia con guiños a la ciencia ficción. Entrada libre.",
         "2026-09-19", "2026-09-19", "Sáb 19 set, 7 p. m.", precio=0, generos=["danza contemporánea", "performance"],
         elenco=E("María José Hernández", "Joel Astacio"), ficha=[("Juan Pablo Rodríguez", "coreografía")]))

# ---------------------------------------------------------------- Teatro de Lucía
add(obra("Teatro de Lucía", "I.D.I.O.T.A.", "prensa", "https://diariocorreo.pe/cultura/sandra-bernasconi-y-armando-machuca-protagonizan-idiota-fechas-y-entradas-noticia/", "teatro",
         "Un hombre en apuros acepta una prueba psicológica bien pagada y termina atrapado en un juego de reglas cambiantes con una psicóloga enigmática. Thriller con humor negro de Jordi Casanovas.",
         "2026-08-20", "2026-09-20", "Jue a sáb 8 p. m.; dom 7 p. m.", precio=30, generos=["thriller", "humor negro"],
         elenco=E("Sandra Bernasconi", "Armando Machuca"), ficha=[("Jordi Casanovas", "dramaturgia"), ("David Carrillo", "dirección")],
         url_compra=None))
add(obra("Teatro de Lucía", "La eternidad en tus ojos", "prensa", "https://caretas.pe/entretenimiento/eternidad-en-tus-ojos-teatro-de-lucia/", "teatro",
         "Vuelve la obra de Eduardo Adrianzén sobre el amor secreto entre una profesora y su alumno, que atraviesa los años de violencia en Lima y regresa décadas después. Seis funciones.",
         "2026-11-23", "2026-12-02", "Lun a mié 8 p. m.", precio=30, generos=["drama", "romance"],
         elenco=E("Milena Alva", "Alejandra Saba", "Jano Baca", "Joel Calderón"),
         ficha=[("Eduardo Adrianzén", "dramaturgia"), ("Giovanni Arce", "dirección"), ("Alejandra Saba", "producción")]))

# ---------------------------------------------------------------- Nuevo Teatro Julieta
add(obra("Nuevo Teatro Julieta", "Lo nunca visto", "prensa", "https://enlima.pe/agenda-cultural/artes-escenicas/lo-nunca-visto", "teatro",
         "Una profesora de danza a punto de cerrar su escuela convoca a dos exalumnas en mal momento para montar un último espectáculo. Comedia con toques de absurdo, debut de Fiorella Pennano como directora.",
         "2026-09-24", "2026-10-11", "8 p. m.", generos=["comedia", "teatro del absurdo"],
         elenco=E("Claudia Berninzon", "Kareen Spano", "Tamara Jhiareth"),
         ficha=[("José Troncoso", "dramaturgia"), ("Fiorella Pennano", "dirección")], productora="Animalien", duracion=75))
add(obra("Nuevo Teatro Julieta", "99 consejos", "prensa", "https://diariocorreo.pe/cultura/obra-99-consejos-desde-el-22-de-octubre-en-el-nuevo-teatro-julieta-noticia/", "comedia",
         "Una autora de autoayuda a punto de lanzar su libro sobre maternidad ve tambalear su propia familia cuando sale a la luz un secreto. Tragicomedia de Eduardo Adrianzén.",
         "2026-10-22", "2026-11-08", "Jue a dom 8 p. m.", generos=["comedia", "drama familiar"],
         url_compra="https://www.joinnus.com/events/theater/lima-99-consejos-78847",
         elenco=E("Ximena Arroyo", "Sebastián Monteghirfo", "Haysen Percovich", "Gia Rosalino", "Leandro Hernández"),
         ficha=[("Eduardo Adrianzén", "dramaturgia"), ("Haysen Percovich", "dirección"), ("Marco Paulo Meléndez", "dirección")],
         productora="Asociación Cultural La Pasión"))
add(obra("Nuevo Teatro Julieta", "Frankenstein", "prensa", "https://www.infobae.com/peru/2026/10/23/agenda-cultural-en-lima-del-23-al-30-de-octubre-ferias-musica-criolla-y-propuestas-de-halloween/", "infantil",
         "Versión familiar de la novela de Mary Shelley para Halloween: una niña le pide a su padre que le cuente la historia, con humor y un mensaje sobre aceptar al diferente.",
         "2026-10-24", "2026-11-01", "Sáb y dom 4 p. m.", precio=45, generos=["familiar", "halloween"],
         elenco=E("Bruno Odar", "Matías Spitzer", "Bianca Bazo")))

# ---------------------------------------------------------------- Centro Cultural Ricardo Palma
add(obra("Centro Cultural Ricardo Palma", "Los engaños de Escapín", "prensa",
         "https://diariocorreo.pe/cultura/teatro-los-enganos-de-escapin-la-comedia-de-moliere-que-vuelve-al-teatro-con-enredos-y-humor-obra-ricardo-palma-centro-cultural-noticia/", "comedia",
         "La comedia de Molière sobre dos jóvenes enamorados y un sirviente astuto que estafa a sus padres tacaños para salvarlos de matrimonios arreglados.",
         None, "2026-09-28", "Vie a lun 8 p. m.; dom 7 p. m.", precio=50, generos=["comedia", "clásico"],
         elenco=E("Martín Velásquez", "Angelita Velásquez", "Mario Velásquez", "Juan Carlos Díaz", "Víctor Acurio", "Sergio Delgado", "Alexandra Garcés", "Verónica Infantes"),
         ficha=[("Molière", "dramaturgia"), ("Omar Velásquez", "dirección")]))
add(obra("Centro Cultural Ricardo Palma", "Palmo a Palma: tradiciones a la criolla", "prensa", "https://caretas.pe/entretenimiento/palmo-a-palma-tradiciones-ricardo-palma-musica-criolla/", "musical",
         "Espectáculo musical que convierte quince Tradiciones Peruanas de Ricardo Palma en canciones criollas originales, con el propio Palma como narrador en escena.",
         "2026-10-02", "2026-10-26", "16 funciones del 2 al 26 oct (Sala Julio Ramón Ribeyro)", generos=["musical", "música criolla"],
         url_compra="https://www.joinnus.com/events/theater/lima-palmo-a-palma-tradiciones-a-la-criolla-78933",
         elenco=[("Paco Varela", "Ricardo Palma"), ("Lúa Rodríguez", "Clemencia"), ("Taís Egúsquiza", None), ("Rodrigo Terry", None), ("Santiago Srebo", None), ("Gianella Tellez", None)],
         ficha=[("Carlos Fuller", "dramaturgia"), ("Carlos Fuller", "música"), ("Carlos Fuller", "dirección"), ("Santiago Linares", "música"),
                ("Ximena Fernandini", "coreografía"), ("Jordan Saldaña", "coreografía")], duracion=110))

# ---------------------------------------------------------------- Teatro Canout, Campo Abierto, Lima Comedy Club
add(obra("Teatro Canout", "Walls: El día que me olvides tour", "prensa", "https://caretas.pe/entretenimiento/walls-llega-lima-primera-vez-concierto-octubre/", "concierto",
         "Primer concierto en el Perú del cantautor español Walls, con el pop rock noventero de su gira «El día que me olvides».",
         "2026-10-11", "2026-10-11", "Dom 11 oct", generos=["pop rock"], artistas=["Walls"]))
add(obra("Asociación Cultural Campo Abierto", "El acústico del Lobo Feroz", "teleticket", "https://teleticket.com.pe/evento/el-acustico-del-lobo-feroz", "infantil",
         "Concierto acústico para niños: el lobo Lobualdo Ferozino y el cerdito Pepo intentan tocar para todo el bosque mientras otros personajes no dejan de interrumpir.",
         "2026-11-08", "2026-11-29", "Dom 5 p. m.", precio=28, url_compra="https://teleticket.com.pe/evento/el-acustico-del-lobo-feroz",
         generos=["familiar", "música"], duracion=60))
add(obra("Lima Comedy Club", "Gran Gala Internacional", "teleticket", "https://teleticket.com.pe/evento/gran-gala-internacional", "stand-up",
         "Noche que mezcla stand-up y magia con tres artistas de España, Perú y México. Consumo mínimo en el local.",
         "2027-02-20", "2027-02-20", "Sáb 20 feb, 7 p. m.", precio=85, url_compra="https://teleticket.com.pe/evento/gran-gala-internacional",
         generos=["stand-up", "magia"], artistas=["Adrián Lima", "Jhony Jackson", "Christian Allen"], edad=10))

# ---------------------------------------------------------------- Espacios nuevos
add(obra("Club de Teatro de Lima", "Nosotros lo hicimos bien", "prensa",
         "https://diariocorreo.pe/cultura/obra-teatral-nosotros-lo-hicimos-bien-se-estrena-en-lima-fechas-horario-y-entradas-noticia/", "teatro",
         "Tres parejas comparten una velada con vino y, entre conversaciones, salen a flote miedos al compromiso y rutinas desgastadas. Parte del público se sienta en mesas dentro de la escena.",
         "2026-09-06", "2026-09-27", "Dom 4 p. m.", generos=["drama", "comedia"],
         elenco=E("Diego Bronstein", "Raúl Castagneto", "Isabel Chappell", "Eliana Fry García-Pacheco", "Wenddy Nishimazuruga", "Patricio Villavicencio"),
         ficha=[("Renato Fernández Vasallo", "dramaturgia"), ("Renato Fernández Vasallo", "dirección"), ("Renato Fernández Vasallo", "producción"), ("Oskaranibal O'Higgins", "producción")]))
add(obra("Casa Tovar", "El origen del mundo", "prensa", "https://entradalibre.me/event/el-origen-del-mundo/", "teatro",
         "Obra breve en la que una pareja amanece convertida en los primeros habitantes de la Tierra, en un cruce de sueño y realidad con humor y erotismo. Ingreso libre.",
         "2026-09-22", "2026-09-22", "Mar 22 set, 7 p. m.", precio=0, generos=["teatro breve", "surrealismo"],
         elenco=E("Valeria Argandoña", "Marcelo Espinoza"), ficha=[("Bruno Villarreal", "dramaturgia")]))
add(obra("Lugar de la Memoria (LUM)", "Érase una mujer sin huayruros", "web de la sala", "https://lum.cultura.pe/actividades/agenda-septiembre-2026", "teatro",
         "Unipersonal que acompaña a una mujer víctima de feminicidio en un tránsito entre la vida y la muerte, guiada por voces femeninas que la ayudan a resignificar su historia. Ingreso libre.",
         "2026-09-25", "2026-09-25", "Vie 25 set, 7 p. m.", precio=0, generos=["unipersonal", "memoria"],
         ficha=[("Huandy Laguna Ibarra", "dirección")], edad=15))
add(obra("Anfiteatro Chabuca Granda (Parque Kennedy)", "Punk en el Kennedy", "prensa", "https://entradalibre.me/event/punk-en-el-kennedy/", "concierto",
         "Tarde gratuita de punk en el anfiteatro del Parque Kennedy con Aero*pajitas, 40 gramos y los uruguayos Trotsky Vengarán.",
         "2026-10-10", "2026-10-10", "Sáb 10 oct, 4 p. m.", precio=0, generos=["punk"], artistas=["Aero*pajitas", "40 gramos", "Trotsky Vengarán"]))
add(obra("Ritual Virtual", "La peña de los sintes", "prensa", "https://entradalibre.me/event/la-pena-de-los-sintes-5/", "concierto",
         "Encuentro de música electrónica experimental con micro recitales y sesiones abiertas: se puede ir a escuchar o llevar el propio sintetizador. Entrada libre.",
         "2026-11-03", "2026-11-03", "Mar 3 nov, 8 p. m.", precio=0, generos=["electrónica", "experimental"]))

CAY = "Centro Cultural Cayetano Heredia"
for t, u, ini, hora, tipo, gen, sin, art in [
    ("Nunamanta", "nunamanta", "2026-09-24", "7:30 p. m.", "concierto", ["lírico", "folklore"],
     "La soprano Airam Aquino Portales se une a la orquesta de instrumentos populares Qallay y a los bailarines de Sumaq Tusuy Perú en un concierto que mezcla canto lírico y tradición andina.",
     ["Airam Aquino Portales", "Qallay", "Sumaq Tusuy Perú"]),
    ("Aquarela Brasileira", "aquarela-brasileira", "2026-09-30", "7:30 p. m.", "concierto", ["música brasileña"],
     "La cantante Cristhiane de Lis y su grupo recorren la música popular de Brasil con invitados brasileños.",
     ["Cristhiane de Lis", "Diego Varillas", "Paulo Chávez", "Jesús Ruiz", "Lucía Seijas", "Tiago Abreu", "Karllos Neon"]),
    ("Nuestras voces", "nuestras-voces", "2026-10-01", "7:30 p. m.", "concierto", ["coral"],
     "Concierto del coro de la Universidad Nacional de Folklore José María Arguedas, formado por estudiantes y cantantes invitados.",
     ["Coro de la Universidad Nacional de Folklore José María Arguedas"]),
    ("Cuarteto Armonía", "cuarteto-armonia", "2026-10-06", "7:30 p. m.", "concierto", ["música de cámara", "clásica"],
     "El cuarteto de cuerdas Armonía presenta un programa con obras de Haydn y Brahms.",
     ["Carlos Costa", "María Elena Pacheco", "Roberto González", "Christian Requejo"]),
    ("Saco: un homenaje al jazz peruano", "saco-un-homenaje-al-jazz-peruano", "2026-10-21", "7:30 p. m.", "concierto", ["jazz", "vals"],
     "Banjo y violín recrean la Lima de los años veinte a través de la obra de Carlos A. Saco, cuando el vals, el ragtime y el jazz empezaban a mezclarse.", []),
    ("Paalo en concierto", "paalo-en-concierto", "2026-10-22", "7:30 p. m.", "concierto", ["clásica", "piano"],
     "Paalo toca sus composiciones para piano y cuerdas junto a obras peruanas poco difundidas rescatadas por su ONG Flores Lunares.", ["Paalo"]),
    ("Señorío de la Zarzuela", "senorio-de-la-zarzuela", "2026-10-23", "7:30 p. m.", "concierto", ["zarzuela", "lírico"],
     "Velada de zarzuela con humor y nostalgia a cargo de la agrupación El Señorío de la Zarzuela.", ["El Señorío de la Zarzuela"]),
    ("Orquesta Filarmónica Infanto-Juvenil", "orquesta-filarmonica-infanto-juvenil", "2026-10-24", "7 p. m.", "concierto", ["orquesta", "clásica"],
     "Concierto de la orquesta de 55 músicos de 11 a 18 años dirigida por Lila Arroyo Torres.", ["Orquesta Filarmónica Infanto-Juvenil del Perú", "Lila Arroyo Torres"]),
    ("Esquinas Brillantes: bebop en Lima", "esquinas-brillantes-bebop-en-lima", "2026-10-27", "7:30 p. m.", "concierto", ["jazz", "bebop"],
     "Quinteto de músicos de la escena limeña que revisita las composiciones de Thelonious Monk.",
     ["Diego Arcadio", "Sergio Cardozo", "Julio Flavio Maza", "Jerónimo Morán", "Carlos Santiago"]),
]:
    d = datetime.date.fromisoformat(ini)
    dia = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"][d.weekday()]
    mes = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "set", "oct", "nov", "dic"][d.month - 1]
    add(obra(CAY, t, "prensa", f"https://entradalibre.me/event/{u}/", tipo, sin + " Ingreso libre.", ini, ini,
             f"{dia} {d.day} {mes}, {hora}", precio=0, generos=gen, artistas=art))


# ---------------------------------------------------------------- utilidades de fecha/hora
DIAS = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "set", "oct", "nov", "dic"]


def hora_fmt(h):
    m = re.match(r"\s*(\d{1,2}):(\d{2})\s*([ap])\.?\s*m", h or "", re.I)
    if not m:
        m2 = re.match(r"\s*(\d{1,2}):(\d{2})", h or "")
        if not m2: return None
        hh, mm = int(m2.group(1)), m2.group(2)
        suf = "p. m." if hh >= 12 else "a. m."
        hh = hh - 12 if hh > 12 else hh
        return f"{hh}{'' if mm == '00' else ':' + mm} {suf}"
    hh, mm, ap = int(m.group(1)), m.group(2), m.group(3).lower()
    return f"{hh}{'' if mm == '00' else ':' + mm} {ap}. m."


def horario(funciones):
    """funciones: lista de (fecha_iso, hora_texto) -> 'Vie 18 set, 8 p. m.' o '18 set, 17 oct y 7 nov; 8 p. m.'"""
    fs = sorted(set(funciones))
    def clave_h(h):
        m = re.match(r"(\d+)(?::(\d+))?\s*([ap])", h)
        hh = int(m.group(1)) % 12 + (12 if m.group(3) == "p" else 0)
        return (hh if hh >= 6 else hh + 24) * 60 + int(m.group(2) or 0)   # madrugada al final
    horas = sorted({h for _, h in fs if h}, key=clave_h)
    if len(fs) == 1:
        d = datetime.date.fromisoformat(fs[0][0])
        return f"{DIAS[d.weekday()]} {d.day} {MESES[d.month - 1]}" + (f", {fs[0][1]}" if fs[0][1] else "")
    por_mes = {}
    for f, _ in fs:
        d = datetime.date.fromisoformat(f)
        por_mes.setdefault((d.year, d.month), []).append(d.day)
    partes = []
    for (y, m), ds in por_mes.items():
        ds = sorted(set(ds))
        txt = ", ".join(map(str, ds[:-1])) + (" y " if len(ds) > 1 else "") + str(ds[-1])
        partes.append(f"{txt} {MESES[m - 1]}")
    hs = (", ".join(horas[:-1]) + " y " + horas[-1]) if len(horas) > 1 else "".join(horas)
    return "; ".join(partes) + (f"; {hs}" if hs else "")


# ---------------------------------------------------------------- Cocodrilo Verde (web de la sala)
# clave: fragmento del slug de la ficha -> (grupo, título limpio, tipo, géneros, sinopsis, artistas)
COCO = [
    ("99-toto", "99 ToTo: el tributo", "concierto", ["rock", "tributo"], "Siete músicos de la escena local recrean los éxitos de Toto, de «Africa» a «Rosanna», en formato íntimo.", ["99"]),
    ("glammers-one-hit", "Glammers: One Hit Wonders", "concierto", ["rock", "pop", "tributo"], "La banda Glammers repasa canciones que hicieron famosos a sus autores con un solo éxito y luego arma fiesta de rock y pop.", ["Glammers"]),
    ("glammers-especial-de-the-beatles", "Glammers: especial de The Beatles", "concierto", ["rock", "tributo"], "Glammers dedica la noche a The Beatles y cierra con éxitos de rock y pop de los ochenta y noventa.", ["Glammers"]),
    ("agi-tc-rock-a-las-8", "AGI-TC: Rock a las 8", "concierto", ["pop rock"], "AGI-TC Antes de Usar propone un viernes temprano de rock en vivo para empezar el fin de semana.", ["AGI-TC Antes de Usar"]),
    ("agi-tc-tributo", "AGI-TC: tributo a Guns N' Roses y AC/DC", "concierto", ["hard rock", "tributo"], "Los himnos de Guns N' Roses y AC/DC en versión de la banda AGI-TC.", ["AGI-TC Antes de Usar"]),
    ("agi-tc-pop-rock", "AGI-TC: pop rock", "concierto", ["pop rock"], "Set de pop rock clásico y actual a cargo de AGI-TC.", ["AGI-TC Antes de Usar"]),
    ("letal", "Letal: lo mejor del rock and roll", "concierto", ["rock", "tributo"], "Letal repasa el rock de los setenta y ochenta con canciones de Heart, Blondie, Kiss, AC/DC y Van Halen.", ["Letal"]),
    ("flashback", "Flashback: vuelven los buenos tiempos", "concierto", ["rock", "pop"], "Banda de covers con himnos de Queen, ABBA, Soda Stereo, The Beatles y otros clásicos para cantar de principio a fin.", ["Flashback"]),
    ("contraband", "Contraband: a classic rock experience", "concierto", ["rock clásico", "tributo"], "Grandes temas de Aerosmith, Toto, Deep Purple, Queen y Cream en una noche de rock clásico.", ["Contraband"]),
    ("moncho-calderon", "Moncho Calderón: Corazón mío", "concierto", ["pop rock", "cantautor"], "El cantautor Moncho Calderón presenta sus canciones y estrena en vivo «Corazón mío» junto a su autor, Willy Noriega.", ["Moncho Calderón", "Willy Noriega"]),
    ("deoderwan", "Deoderwan: rock n' roll", "concierto", ["rock and roll"], "Koki Bonilla y su banda tocan rock and roll de autor con espíritu clásico.", ["Deoderwan", "Koki Bonilla"]),
    ("imperdibles", "Imperdibles: Convocatoria 80's", "concierto", ["rock en español"], "Noche de rock en español de los ochenta y noventa a cargo de Imperdibles.", ["Imperdibles"]),
    ("sonora-paez", "La Sonora Páez: fiesta cubana", "concierto", ["salsa", "son cubano"], "Salsa, rumba y chachachá en vivo para bailar sin pausa.", ["La Sonora Páez"]),
    ("banda-cocodrilo", "Banda Cocodrilo: una banda, mil ritmos", "concierto", ["fusión", "bailable"], "La banda residente de la casa mezcla salsa, cumbia, rock y reggae en un set bailable.", ["Banda Cocodrilo"]),
    ("martes-sessions", "Banda Cocodrilo: una banda, mil ritmos", "concierto", ["fusión", "bailable"], "La banda residente de la casa mezcla salsa, cumbia, rock y reggae en un set bailable.", ["Banda Cocodrilo"]),
    ("homenaje-a-los-beatles", "Homenaje a los Beatles y canciones de mi vida", "concierto", ["pop rock", "tributo"], "Recital que rescata canciones menos conocidas de The Beatles junto a composiciones propias.", []),
    ("nicolle-la-rumba", "Nicolle La Rumba: El origen", "concierto", ["salsa", "balada"], "Nicolle La Rumba estrena un show personal que repasa su camino musical entre salsa, pop y baladas.", ["Nicolle La Rumba"]),
    ("4u-tributo", "4U: tributo a U2", "concierto", ["rock", "tributo"], "Banda tributo que recorre clásicos de U2 en el formato de la gira Vértigo.", ["4U"]),
    ("banda-venus", "Banda Venus: éxitos del pop, rock y disco", "concierto", ["pop", "disco"], "Melanie Craff y Banda Venus cantan a Donna Summer, Cyndi Lauper, Madonna y Alaska y Dinarama.", ["Banda Venus", "Melanie Craff"]),
    ("alessandra-panizo", "Alessandra Panizo: una noche tropical", "concierto", ["tropical"], "Alessandra Panizo vuelve a los escenarios tras trece años con un show de música tropical.", ["Alessandra Panizo"]),
    ("randy-feijoo", "Randy Feijoo: Romántico", "concierto", ["balada", "romántica"], "Baladas y canciones románticas en formato acústico para cantar y dedicar.", ["Randy Feijoo"]),
    ("alfredo-galvez", "Alfredo Gálvez: Castellanazos", "concierto", ["rock en español"], "El locutor Alfredo Gálvez canta himnos del rock en español y cuenta las historias detrás de ellos.", ["Alfredo Gálvez"]),
    ("aria-bohemia", "Aria Bohemia: tributo a la balada rock en español", "concierto", ["balada", "rock"], "Repertorio de baladas en español de José José a La Oreja de Van Gogh.", ["Aria Bohemia"]),
    ("cielo-gris-wave", "Cielo Gris Wave: lo mejor del new wave", "concierto", ["new wave", "ochentas"], "Éxitos del new wave y los ochenta en vivo.", ["Cielo Gris Wave"]),
    ("screaming-chicks-la-maquina", "Screaming Chicks: La máquina del tiempo", "concierto", ["rock", "pop"], "Clásicos de rock y pop de los ochenta con una banda liderada por dos voces femeninas.", ["Screaming Chicks"]),
    ("screaming-chicks-presenta", "Screaming Chicks: ¡Esta canción me la sé!", "concierto", ["rock", "pop"], "Temas de rock y pop en inglés y español pensados para corear.", ["Screaming Chicks"]),
    ("rubik", "Rubik para grandes y chicos", "concierto", ["rock", "pop"], "Rock y pop de los ochenta con un bloque de canciones de series de televisión.", ["Rubik"]),
    ("copas-mias", "Copas mías: Sofía con Z", "concierto", ["música criolla"], "Sofía con Z mezcla repertorio criollo e internacional con un homenaje a Pepe Villalobos.", ["Sofía con Z"]),
    ("pilar-de-la-hoz", "Pilar de la Hoz: Días de cine", "concierto", ["bandas sonoras"], "Pilar de la Hoz canta temas de películas con piano, batería y bajo.", ["Pilar de la Hoz"]),
    ("saurio", "Saurio: lo mejor del rock en inglés y español", "concierto", ["rock clásico"], "Rock de los ochenta y noventa, de Depeche Mode a AC/DC.", ["Saurio"]),
    ("the-doors", "The Doors: homenaje", "concierto", ["rock", "tributo"], "Noche dedicada a los grandes éxitos de The Doors.", []),
    ("onda-rocks", "Onda Rocks: la música de tu vida", "concierto", ["rock", "pop"], "Clásicos del rock y pop de los setenta, ochenta y noventa.", ["Onda Rocks"]),
    ("criollo-goes-jazz", "Criollo goes jazz", "concierto", ["jazz", "música criolla"], "Agustín Rojas y Carlos Enrique arreglan valses y clásicos criollos con improvisación jazzística.", ["Agustín Rojas", "Carlos Enrique"]),
    ("los-mancilla", "Los Mancilla: el legado", "concierto", ["bolero", "balada"], "Padre e hijo cantan baladas, boleros y canciones del recuerdo a dúo y en solitario.", ["Julio César Mancilla", "César Mancilla"]),
    ("silvio-a-la-carta", "Silvio a la carta", "concierto", ["trova"], "Recorrido por las canciones de Silvio Rodríguez y la canción latinoamericana.", []),
    ("luis-loz", "Imaginary Friends con Luis Loz", "concierto", ["rock alternativo", "indie"], "La banda chilena Imaginary Friends toca por primera vez en el Perú; abre Luis Loz.", ["Imaginary Friends", "Luis Loz"]),
    ("del-vals-al-bolero", "Del vals al bolero", "concierto", ["bolero", "vals criollo"], "Valses criollos, boleros clásicos y son en una noche de música del recuerdo.", ["Mariella Fonseca", "Abel Páez"]),
    ("vr-5", "VR-5 y sus amigos", "concierto", ["rock en español"], "Rock de los ochenta y pachanga con VR-5 y la banda invitada The Remakers. Ingreso libre.", ["VR-5", "The Remakers"]),
    ("willy-terry", "Willy Terry y su conjunto", "concierto", ["música criolla"], "Valses, polkas y festejos para celebrar el Día de la Canción Criolla.", ["Willy Terry"]),
    ("jam-afroperuano", "Jam afroperuano: Día de la Canción Criolla", "concierto", ["afroperuano", "música criolla"], "Pepe Santa Cruz dirige una jam de música afroperuana y criolla con improvisación.", ["Pepe Santa Cruz", "Lessia Limas"]),
    ("amenopausica", "Amenopaúsica", "stand-up", ["stand-up", "humor"], "Fabiola Arteaga convierte la menopausia en tema de stand-up, entre la risa y la información.", ["Fabiola Arteaga"]),
    ("timeline", "Timeline: lo mejor de los 70 y 80 del rock", "concierto", ["rock clásico"], "The Timeline Band enfrenta el rock clásico de los setenta con el dance rock de los ochenta.", ["The Timeline Band"]),
    ("326-salsa", "326 Salsa: lo mejor de la salsa", "concierto", ["salsa"], "Salsa de la época dorada con temas de Oscar de León, Grupo Niche y El Gran Combo.", ["326 Salsa"]),
    ("alejandra-reyes-mi-voz", "Alejandra Reyes: Mi voz en un sueño, 4 años", "concierto", ["cumbia", "salsa"], "Alejandra Reyes celebra cuatro años de su show con una noche solo de música bailable.", ["Alejandra Reyes"]),
    ("mariella-kohn", "Mariella Köhn en concierto", "concierto", ["fusión", "música peruana"], "Recital acústico de Mariella Köhn entre vals, landó, bossa nova, jazz y bolero.", ["Mariella Köhn"]),
    ("room-66", "Room 66: grandes hits de los 80 y 90", "concierto", ["rock", "pop"], "Rock y pop en inglés y español de los ochenta a los dos mil.", ["Room 66"]),
    ("danitse", "Danitse: concierto de cámara", "concierto", ["canción de autor", "indie folk"], "Danitse repasa veinte años de carrera con arreglos de cámara y temas de su álbum «Augurio».", ["Danitse"]),
    ("amor-despecho", "Amor, despecho y mucha salsa", "concierto", ["salsa"], "Salsa y canciones de despecho para cantar y bailar.", []),
    ("aliens", "Aliens en concierto", "concierto", ["pop", "rock"], "Pop y rock clásico en inglés y español, de The Eagles a Pedro Suárez-Vértiz.", ["Aliens"]),
    ("matias-canales", "Matías Canales y Los Descabellados: Melancolía y ruido bello", "concierto", ["indie pop"], "La banda presenta las canciones de su último disco y algunas sorpresas.", ["Matías Canales y Los Descabellados"]),
]


def precio_num(t):
    m = re.search(r"([\d]+(?:\.\d+)?)", (t or "").replace(",", ""))
    return float(m.group(1)) if m else None


coco = json.load(open(RAW / "cocodrilo.json"))
grupos = {}
for e in coco:
    if not e.get("fecha") or e["fecha"] < DESDE or re.search(r"privado|cerrado", e.get("titulo") or "", re.I):
        continue
    clave = next((c for c in COCO if c[0] in e["url"]), None)
    if not clave:
        print("SIN GRUPO cocodrilo:", e["url"]); continue
    g = grupos.setdefault(clave[1], {"meta": clave, "ev": []})
    g["ev"].append(e)
for titulo, g in grupos.items():
    _, t, tipo, gen, sin, art = g["meta"]
    ev = sorted(g["ev"], key=lambda e: e["fecha"])
    funcs = [(e["fecha"], hora_fmt((e.get("hora") or "").split("-")[0])) for e in ev]
    precios = [p for p in (precio_num(e.get("precio")) for e in ev) if p is not None]
    compra = next((c for e in reversed(ev) for c in e.get("compra") or [] if c), None)
    futuro = [e for e in ev if e["fecha"] >= HOY]
    url = (futuro[0] if futuro else ev[-1])["url"]
    add(obra("Cocodrilo Verde", t, "web de la sala", url, tipo, sin, ev[0]["fecha"], ev[-1]["fecha"], horario(funcs),
             precio=min(precios) if precios else None, url_compra=compra, generos=gen, artistas=art))

# ---------------------------------------------------------------- Jazz Zone (web de la sala, modales de programación)
JZ = "https://www.jazzzoneperu.com/"
for t, tipo, gen, sin, funcs, precio, compra, art in [
    ("The Beatles y Paul McCartney: tributo con Carlos Guerrero", "concierto", ["rock", "tributo"],
     "Carlos Guerrero repasa los clásicos de The Beatles y de la carrera solista de Paul McCartney.", [("2026-09-18", "7:30 p. m.")], None,
     "https://vaope.com/eventos/rock/the-beatles-paul-mccartney-tributo-en-vivo-con-carlos-guerrero-en-miraflores", ["Carlos Guerrero"]),
    ("Tributo a Zoé y especial León Larregui", "concierto", ["rock", "tributo"], "Noche de rock dedicada a Zoé y a la carrera solista de León Larregui.",
     [("2026-09-19", "10:30 p. m.")], 40, "https://vaope.com/eventos/rock/tributo-a-zoe-y-especial-a-leon-larregui-en-miraflores", []),
    ("Lo mejor de Charly García", "concierto", ["rock en español", "tributo"],
     "El Hijo de la Lágrima recorre los clásicos de Charly García con un bloque dedicado a Serú Girán, Sui Generis y La Máquina de Hacer Pájaros.",
     [("2026-09-26", "8 p. m.")], None, None, ["El Hijo de la Lágrima"]),
    ("Charly García 75: la fiesta continúa", "concierto", ["rock en español", "tributo"],
     "El Hijo de la Lágrima vuelve para celebrar los 75 años de Charly García con un repertorio pensado para la fiesta.",
     [("2026-11-13", "8 p. m.")], None, None, ["El Hijo de la Lágrima"]),
    ("Jazz afroperuano con Gabriel Alegría Sexteto", "concierto", ["jazz", "afroperuano"],
     "Cada jueves el sexteto de Gabriel Alegría toca jazz afroperuano en dos funciones, una cita fija del club.",
     [("2026-10-01", "8 p. m."), ("2026-10-01", "10 p. m."), ("2026-10-15", "8 p. m."), ("2026-10-15", "10:30 p. m."),
      ("2026-10-22", "8 p. m."), ("2026-10-22", "10:30 p. m."), ("2026-10-29", "8 p. m."), ("2026-10-29", "10:30 p. m.")], 65, "https://jazzperu.org/", ["Gabriel Alegría Sexteto"]),
    ("Lo mejor de The Beatles y del rock clásico en inglés", "concierto", ["rock", "tributo"],
     "La Banda del Sargento toca clásicos de The Beatles y del rock en inglés.", [("2026-10-02", "8:30 p. m.")], 50, None, ["La Banda del Sargento"]),
    ("The Country Music Tribute", "concierto", ["country", "rock clásico"],
     "La International Blues Band rinde homenaje a Johnny Cash, Hank Williams, Kenny Rogers y otras leyendas del country y el rock clásico.",
     [("2026-10-02", "10:30 p. m."), ("2026-10-10", "10:30 p. m.")], 50,
     "https://vaope.com/eventos/conciertos/the-country-music-tribute-billy-ray-cyrus-johnny-cash-hank-williams-y-mas-en-miraflores", ["International Blues Band"]),
    ("Extraña pareja", "teatro", ["comedia"], "Comedia sobre un matrimonio de muchos años al que una propuesta del marido pone de cabeza, entre celos, manipulación y cambios de humor.",
     [("2026-10-03", "7 p. m."), ("2026-10-18", "7 p. m.")], 30, None, []),
    ("Se acabaron las ex-cusas", "stand-up", ["stand-up"], "El comediante Alex Román cuenta en clave de humor cómo dejó todo para dedicarse al arte.",
     [("2026-10-03", "8 p. m.")], 30, "https://teleticket.com.pe/evento/se-acabaron-las-excusas-jazz-zone-2026", ["Alex Román"]),
    ("Lima Jazz Fest 2026", "concierto", ["jazz", "latin jazz"],
     "Semana de festival con un concierto por noche: Óscar Barcelli, Defensores del Morro con Jonathan Montes, Raúl Pineda, Latinandó con Elías Coutinho y Los Jazzy Bros con Aníbal Seminario.",
     [("2026-10-05", "8 p. m."), ("2026-10-06", "8 p. m."), ("2026-10-07", "8 p. m."), ("2026-10-08", "8 p. m."), ("2026-10-09", "8 p. m.")], None,
     "https://www.joinnus.com/events/festivales/lima-lima-jazz-fest-2026-78390",
     ["Óscar Barcelli", "Defensores del Morro", "Jonathan Montes", "Raúl Pineda", "Latinandó", "Elías Coutinho", "Los Jazzy Bros", "Aníbal Seminario"]),
    ("Café sin azúcar", "teatro", ["comedia", "drama familiar"], "Una abuela, su nieto y una herencia inesperada dan pie a una historia familiar agridulce.",
     [("2026-10-11", "7 p. m."), ("2026-10-12", "8 p. m.")], None, None, []),
    ("Marco Musical Estelar", "concierto", ["música criolla"], "El Centro Cultural Musical Miraflores presenta a su grupo estelar en una noche de música en vivo.",
     [("2026-10-13", "8:30 p. m.")], 30, None, ["Alejandro Velásquez", "Wayo Álvarez", "Edson Rosales", "Carlos Zaga"]),
    ("El efecto Ja", "stand-up", ["stand-up"], "Show de graduación del taller de stand-up de Humor en Serio, con comediantes que debutan.",
     [("2026-10-14", "8 p. m.")], None, None, []),
    ("Jam afroperuano", "concierto", ["afroperuano"], "Los miércoles, una jam de música afroperuana donde el público puede sumarse a tocar.",
     [("2026-10-14", "10 p. m."), ("2026-10-21", "10 p. m."), ("2026-10-28", "10 p. m.")], 40, None, []),
    ("Catarsis ¡el festival!", "show", ["rock", "stand-up"], "Noche que junta un tributo a los noventa, el rock de Dudó y el stand-up musical del Dr. Medina.",
     [("2026-10-16", "7 p. m.")], None, None, ["Dudó", "Dr. Medina"]),
    ("Indie Rock Festival 2026", "concierto", ["indie rock"], "Los Fasos tocan canciones de The Strokes, The Killers, Arctic Monkeys, Tame Impala y otras bandas indie.",
     [("2026-10-16", "10:30 p. m.")], 40, "https://vaope.com/eventos/conciertos/indie-rock-festival-2026-en-miraflores", ["Los Fasos"]),
    ("Banda sonora de nuestras vidas", "concierto", ["pop", "baladas"], "Universo Voz reúne a varios cantantes para recorrer canciones que marcaron época.",
     [("2026-10-17", "7 p. m.")], 30, None, ["Universo Voz"]),
    ("El versus de la salsa con Afinke Orquesta", "concierto", ["salsa"], "Afinke Orquesta enfrenta la salsa dura con la salsa romántica en una noche para bailar.",
     [("2026-10-17", "10:45 p. m.")], 50, "https://wa.link/do2oo9", ["Afinke Orquesta"]),
    ("Los Bardos de América", "concierto", ["música criolla"], "Grupo de música criolla llegado de Miami, presentado por el Centro Cultural Musical Miraflores.",
     [("2026-10-20", "8:30 p. m.")], 30, None, ["Los Bardos de América"]),
    ("El sonido de la música", "concierto", ["pop", "baladas"], "Show con canciones en inglés, del recuerdo y contemporáneas.", [("2026-10-23", "7:30 p. m.")], 35, None, []),
    ("Salsa dura: rumbón sabroso", "concierto", ["salsa"], "La Efectiva toca salsa dura para bailarines avanzados.", [("2026-10-23", "10:30 p. m.")], 50, "http://wa.me/51998675432", ["La Efectiva"]),
    ("Homenaje a George Harrison", "concierto", ["rock", "tributo"], "Los Harrisongs recorren la obra de George Harrison con The Beatles, como solista y con los Traveling Wilburys.",
     [("2026-10-24", "10:30 p. m.")], 35, "https://www.joinnus.com/events/concerts/lima-homenaje-a-george-harrison-79391", ["Los Harrisongs"]),
    ("Día de la Canción Criolla con el Centro Cultural Musical Miraflores", "concierto", ["música criolla"], "Velada de música criolla por el Día de la Canción Criolla.",
     [("2026-10-27", "8:30 p. m.")], 50, None, []),
    ("Noches con Andrés Prado", "concierto", ["jazz", "música latinoamericana"], "El guitarrista Andrés Prado presenta su disco «Barranquino» entre jazz, música popular latinoamericana e improvisación.",
     [("2026-10-28", "8 p. m.")], None, None, ["Andrés Prado"]),
    ("Feliz cumpleaños John Lennon", "concierto", ["rock", "tributo"], "We All Together celebra a John Lennon con lo mejor de su obra y de The Beatles.",
     [("2026-10-30", "7:30 p. m.")], None, "https://vaope.com/eventos/rock/feliz-cumpleanos-john-lennon-en-miraflores", ["We All Together"]),
    ("Fuerza Gigante Orquesta", "concierto", ["salsa"], "Juan Núñez y Fuerza Gigante Orquesta tocan sus éxitos de salsa.",
     [("2026-10-30", "10 p. m.")], 55, "https://vaope.com/eventos/conciertos/juan-nunez-fuerza-gigante-orquesta-en-miraflores", ["Fuerza Gigante Orquesta", "Juan Núñez"]),
    ("Salsa de rompe y raja", "concierto", ["salsa", "música criolla"], "Afinke Orquesta mezcla salsa con un bloque de música criolla para cerrar octubre.",
     [("2026-10-31", "10:45 p. m.")], None, "https://wa.link/do2oo9", ["Afinke Orquesta"]),
    ("Quinteto de Kevin Zúñiga", "concierto", ["jazz", "latin jazz"], "Concierto central de la gira peruana de Kevin Zúñiga con nuevos arreglos de jazz y latin jazz.",
     [("2026-11-03", "8 p. m.")], None, None, ["Kevin Zúñiga"]),
    ("Salsa andina: Orquesta Segovia", "concierto", ["salsa", "folklore"], "Segovia Orquesta presenta su producción que cruza salsa y folclor; invitado, Cosa Nuestra de Tito Manrique.",
     [("2026-11-04", "8 p. m.")], 50, "https://ticketya.pe/events/info/4", ["Segovia Orquesta", "Cosa Nuestra"]),
    ("Yo soy Los Panchos", "concierto", ["bolero", "tributo"], "Homenaje al bolero con el trío Los Cox y una aparición de Yo Soy Rafael.",
     [("2026-11-06", "8 p. m.")], None, "https://vaope.com/eventos/conciertos/noche-de-boleros-tributo-a-los-panchos-trio-los-cox-y-a-rafael-en-jazz-zone-miraflores", ["Trío Los Cox"]),
    ("Yo soy Matt Bellamy: Muse", "concierto", ["rock alternativo", "tributo"], "Show tributo a Muse.",
     [("2026-11-06", "10:30 p. m.")], None, "https://vaope.com/eventos/rock/yo-soy-matt-bellamy-tributo-a-muse-en-jazz-zone-miraflores", []),
    ("Mujeres en el cabaret", "musical", ["musical", "comedia"], "Musical entre drama, comedia y burlesque: en un burdel del Centro de Lima el dueño aparece muerto y tres mujeres son sospechosas.",
     [("2026-11-15", "7 p. m.")], None, None, []),
    ("Back to the 80's", "concierto", ["rock", "ochentas"], "Carlitos Mendoza canta himnos del rock ochentero.", [("2026-11-18", "7:30 p. m.")], 40, None, ["Carlitos Mendoza"]),
]:
    fs = sorted(f for f, _ in funcs)
    add(obra("Jazz Zone", t, "web de la sala", JZ, tipo, sin, fs[0], fs[-1], horario(funcs), precio=precio, url_compra=compra, generos=gen, artistas=art))
for o in OBRAS:
    if o["titulo"] == "Mujeres en el cabaret": o["productora"] = "Vicky Paz Producciones"


# ---------------------------------------------------------------- filtros y control
def norm(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    t = re.split(r"[:\-–(]", t)[0]
    return re.sub(r"[^a-z0-9]+", " ", t).strip()


cat = json.load(open(R / "data/catalogo.json"))
salas_slug = {s["nombre"]: s["slug"] for s in cat["salas"]}
por_sala = {}
for o in cat["obras"]:
    for s in o["salas"]:
        por_sala.setdefault(s, set()).add(norm(o["titulo"]))
final, vistos = [], set()
for o in OBRAS:
    s = salas_slug.get(o["sala"])
    if s and norm(o["titulo"]) in por_sala.get(s, set()):
        print("ya en catálogo, se omite:", o["sala"], "|", o["titulo"]); continue
    if (o["temporada"]["fin"] or "9999") < DESDE:
        print("fuera de ventana:", o["titulo"]); continue
    if o["id"] in vistos:
        raise SystemExit("id repetido: " + o["id"])
    vistos.add(o["id"])
    assert o["tipo"] in {"teatro", "comedia", "stand-up", "musical", "danza", "opera", "concierto", "circo", "infantil", "folklore", "show", "otro"}, o["tipo"]
    assert "joinnus" not in o["url"] and "instagram" not in o["url"] and "facebook" not in o["url"], o
    final.append(o)
dest = R / "data/extraido/salas_miraflores.json"
dest.write_text(json.dumps(final, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
json.loads(dest.read_text())
from collections import Counter
print(len(final), "obras ->", dest)
for k, v in Counter(o["sala"] for o in final).most_common(): print(f"  {v:3d}  {k}")
