"""Arma data/salas_barranco.json: espacios escénicos de Barranco que no están en data/salas.json, más
las salas de Barranco que ya están allí pero a las que se les pudo completar algún dato (ver 'notas').
No modifica salas.json. Descripciones escritas a mano. Coordenadas: solo las que Nominatim (OSM)
devolvió como lugar con nombre y número coincidente (raw/barranco/geocod.json); si no, null.
"""
import json, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
OSM = 'https://nominatim.openstreetmap.org/'
CP = 'https://conciertosperu.com.pe/'


def sala(nombre, alias, direccion, tipo, descripcion, ticketera, fuente, confianza, estado, notas,
         web=None, instagram=None, url_cartelera=None, coordenadas=None, aforo=None):
    return {'nombre': nombre, 'alias': alias, 'ciudad': 'Lima', 'distrito': 'Barranco', 'direccion': direccion,
            'tipo': tipo, 'aforo_aprox': aforo, 'descripcion_corta': descripcion, 'web': web, 'instagram': instagram,
            'url_cartelera': url_cartelera, 'ticketera': ticketera,
            'coordenadas': {'lat': coordenadas[0], 'lng': coordenadas[1]} if coordenadas else None,
            'fuente': fuente, 'confianza': confianza, 'estado': estado, 'notas': notas}


SALAS = [
    # ------------------------------------------------ ya en salas.json, con datos completados
    sala('Teatro Barranco', ['TEATRO BARRANCO', 'TEATRO BARRANCO - BARRANCO - LIMA', 'Teatro Barranco 2.0', 'Teatro de Barranco',
                             'Teatro Barranco S.A.C.'],
         'Av. Almirante Miguel Grau 701, Barranco', 'independiente',
         'Sala barranquina con comedias, cabaret y montajes de pequeño formato; su ciclo Kortas reúne obras breves de creadores emergentes.',
         ['Passline', 'Teleticket', 'Joinnus', 'WhatsApp'],
         ['https://www.passline.com/productora/teatro-barranco-755463861', 'https://www.passline.com/sitio-evento/rodeados-de-amor-568357',
          'https://puroteatro.pe/teatro-en-barranco',
          'https://diariocorreo.pe/cultura/mesa-tomada-20-llega-al-teatro-barranco-con-amores-rupturas-y-enredos-noticia/',
          'https://diariouno.pe/2026/10/24/obra-dirigida-por-martin-velasquez-marvelat-vuelve-al-teatro-barranco/',
          'https://www.instagram.com/teatro.barranco/'],
         'alta', 'activa',
         'Completado: ticketera (la propia sala vende por Passline como productora "Teatro Barranco S.A.C."; otras obras usan Joinnus, '
         'Teleticket o WhatsApp) y url_cartelera = su listado de Passline. El buscador indexa una web teatrobarranco.pe ("Inicio - Teatro '
         'Barranco"), pero no resolvió desde esta sesión: queda sin confirmar y no se pone en "web". Ojo: en catalogo.json, conciertos del '
         'Centro de Convenciones Barranco (Av. República de Panamá 220: Elefante, Giant Rooks, La Joaqui, Miguel Tapia) quedaron asignados '
         'por error a esta sala.',
         instagram='https://www.instagram.com/teatro.barranco/',
         url_cartelera='https://www.passline.com/productora/teatro-barranco-755463861'),
    sala('Teatro Racional', ['Cine Teatro irRacional', 'Teatro Racional Barranco', 'Teatro irRacional'],
         'Av. José Balta 170, Barranco', 'independiente',
         'Pequeña sala de cámara en Barranco, reabierta en 2025; programa teatro contemporáneo de producciones independientes como Yestoquelotro y Pánico Escénico.',
         ['Joinnus'],
         ['https://puroteatro.pe/obra-teatral/sofia-y-el-dano-que-habitamos',
          'https://diariocorreo.pe/cultura/trampolin-regresa-a-barranco-con-cuatro-funciones-en-el-teatro-racional-noticia/',
          'https://diariocorreo.pe/cultura/los-cuatro-letras-david-carrillo-estrena-comedia-dramatica-sobre-amistad-y-memoria-en-barranco-noticia/',
          'https://www.instagram.com/cineteatroirracional/', OSM],
         'media', 'activa',
         'Completado: ticketera (Joinnus, según la ficha de "Sofía y el daño que habitamos" en Puro Teatro) y actividad 2026 (Los Cuatro Letras '
         'en junio, Trampolín en agosto, Sofía y el daño que habitamos en noviembre). Dirección dudosa: Puro Teatro dice "Avenida Balta 170" y '
         'Diario Correo (ago. 2026) "Balta 123".',
         instagram='https://www.instagram.com/cineteatroirracional/', coordenadas=(-12.14258, -77.01705)),

    # ------------------------------------------------ espacios nuevos (no están en salas.json)
    sala('Centro de Convenciones Bianca', ['C.C. Bianca', 'CC Bianca', 'C.C. BIANCA - BARRANCO - LIMA', 'Bianca',
                                           'CENTRO DE CONVENCIONES BIANCA - BARRANCO - LIMA'],
         'Av. Almirante Miguel Grau 135, Barranco', 'bar/club',
         'Local de eventos con mesas y consumo mínimo que programa casi cada semana conciertos de baladas, criollo, cumbia y música andina, almuerzos show y comedias de figuras de TV.',
         ['Teleticket', 'Joinnus', 'Ticketmaster'],
         ['https://teleticket.com.pe/evento/ellas-en-concierto-en-bianca-cc-bianca',
          'https://teleticket.com.pe/sebuscamaridocamaafuera-bianca2026',
          'https://elcomercio.pe/luces/teatro/laura-huarcayo-y-carlos-vilchez-debutan-en-el-teatro-con-la-comedia-cero-migajeros-ultimas-noticia/',
          'https://limatimes.pe/agenda-cultural/2026/10/29/diosdado-gaitan-llega-con-su-canto-andino-a-barranco/',
          'https://www.ticketmaster.pe/event/manuel-donayre-tradicion-y-sabor-venta-general', OSM],
         'alta', 'activa',
         'Consumo mínimo habitual de S/ 40 por persona, mesas numeradas y compartidas. Tiene varios niveles (2do y 3er piso, boxes, palcos). '
         'Ticketmaster da la dirección solo como "Av. Almte. Miguel Grau". Sin web ni Instagram verificados.',
         coordenadas=(-12.1507204, -77.0205044)),
    sala('Centro de Convenciones Barranco', ['CC Barranco', 'CCB', 'Centro de Convenciones de Barranco',
                                             'CENTRO DE CONVENCIONES BARRANCO - BARRANCO - LIMA', 'Barranco Arena'],
         'Av. República de Panamá 220, Barranco', 'comercial',
         'Recinto de conciertos y eventos de formato mediano, con dos pisos de pie y zona VIP; recibe sobre todo giras internacionales de pop, urbano, rock e indie.',
         ['Joinnus', 'Teleticket', 'Ticketmaster', 'Passline', 'Digital Ticket'],
         ['https://ccbarranco.com/', CP + 'ccb-centro-de-convenciones-barranco/', 'https://teleticket.com.pe/kidd-voodoo',
          'https://www.ticketmaster.pe/event/giant-rooks-home', 'https://www.instagram.com/ccbarranco/'],
         'alta', 'activa',
         'Su web es comercial (alquiler de espacios: Salón 1, Salón 2, Terraza, Backstage) y no publica cartelera ("No hay eventos registrados"); '
         'la programación la anuncian las productoras de cada concierto. Aforo no publicado. "Barranco Arena" aparece como alias en Conciertos Perú '
         '(sin confirmar que sea el mismo local). En catalogo.json varios de sus conciertos quedaron asignados por error a "Teatro Barranco".',
         web='https://ccbarranco.com/', instagram='https://www.instagram.com/ccbarranco/'),
    sala('Centro Cultural La Candelaria', ['La Candelaria', 'La Candelaria Perú', 'Centro Cultural La Candelaria - Barranco'],
         'Av. Bolognesi 292, Barranco', 'comercial',
         'Restaurante espectáculo de folclore peruano con elenco de danzas de costa, sierra y selva y orquesta en vivo, con tardes y noches de show varios días a la semana.',
         ['Ticketmaster', 'WhatsApp', 'correo'],
         ['https://lacandelariaperu.com/espectaculos/', 'https://lacandelariaperu.com/contacto/',
          'https://www.ticketmaster.pe/event/noches-de-folklore---jueves-viernes-y-sabados-en-la-candelaria-2026-venta-general'],
         'alta', 'activa',
         'Horarios de show según su web: tardes sáb y dom 1-6 p. m.; noches jue 7 p. m.-12 a. m., vie y sáb 8 p. m.-2 a. m. Reservas por WhatsApp '
         '(+51 919 291 818) y reservas@lacandelariaperu.com. También dicta talleres de danza.',
         web='https://lacandelariaperu.com/', instagram='https://www.instagram.com/lacandelariaperu/',
         url_cartelera='https://lacandelariaperu.com/espectaculos/'),
    sala('Capital Restobar', ['Capital RESTOBAR', 'Capital Restobar Barranco', 'Capital RESTOBAR - BARRANCO - LIMA'],
         'Av. Almirante Miguel Grau 680, Barranco', 'bar/club',
         'Restobar que funciona como teatro bar: temporadas de comedias musicales y de enredo producidas por La X Productora.',
         ['Teleticket'],
         ['https://teleticket.com.pe/evento/el-adivino%E2%80%93-una-comedia-terrorifica-capital-restobar',
          'https://teleticket.com.pe/evento/electro-showck-%E2%80%93-la-comedia-de-alto-voltaje-capital-restobar'],
         'media', 'activa',
         'Programación continua de La X Productora en 2026 (Electro Showck sep-oct, El adivino oct-nov). Sin web ni redes verificadas.'),
    sala('Roble de Barranco', ['El Roble de Barranco', 'EL ROBLE DE BARRANCO - BARRANCO - LIMA', 'ROBLE DE BARRANCO - BARRANCO - LIMA', 'El Roble'],
         'Pasaje Sánchez Carrión 147 (Boulevard de Barranco), Barranco', 'bar/club',
         'Restobar del Boulevard de Barranco que programa almuerzos show criollos, tributos y unipersonales de humor.',
         ['Teleticket'],
         ['https://teleticket.com.pe/evento/feliz-dia-de-la-cancion-criolla-con-los-kipus-el-roble-de-barranco',
          'https://teleticket.com.pe/evento/ni-toxica-ni-mensa-sin-filtro-2da-temporada-roble-de-barranco-'],
         'media', 'activa',
         'En catalogo.json aparece duplicado como "Roble de Barranco" y "El Roble De Barranco": es el mismo local. Dirección: Teleticket da '
         'Psje. Sánchez Carrión 147 en una página y Sánchez Carrión 173 en otra. Consumo mínimo S/ 35 en almuerzos show.'),
    sala('Aforo Barranco', ['Aforo', 'Aforo Bar', 'Centro Cultural Aforo', 'Aforo de Barranco', 'AFORO BARRANCO - BARRANCO - LIMA'],
         'Av. Almirante Miguel Grau 264, Barranco', 'bar/club',
         'Bar y sala de conciertos que también acoge stand-up y teatro inmersivo; en 2026 recibió giras pequeñas de pop y urbano.',
         ['Teleticket', 'Passline', 'Boletía', 'WhatsApp'],
         ['https://www.gatoencerrado.net/el-1-de-octubre-se-estrena-terapia-blanquiazvl-en-barranco/',
          CP + 'dimitri-y-las-brujas-en-lima-2026/', CP + 'giru-mad-fleiva-en-lima-2026/',
          'https://teleticket.com.pe/evento/gupers-music-fest',
          'https://diariocorreo.pe/miscelanea/la-gupipollada-gupi-organiza-pollada-show-con-comedia-yunza-y-banda-en-vivo-en-barranco-noticia/'],
         'media', 'activa',
         'Gato Encerrado lo llama "Centro Cultural Aforo". Usa varias ticketeras según el productor, incluida Boletía. Sin web ni Instagram verificados.'),
    sala('La Noche de Barranco', ['La Noche', 'Bar La Noche de Barranco'], 'Pasaje Sánchez Carrión 199, Barranco', 'bar/club',
         'Bar histórico del Boulevard con sala de conciertos aparte; programa varias noches por semana a bandas de rock, pop independiente, criollo y fusión.',
         ['Joinnus', 'Passline', 'WhatsApp'],
         [CP + 'local/la-noche-de-barranco/', 'https://www.passline.com/venue/la-noche-de-barranco',
          'https://diariocorreo.pe/espectaculos/black-sugar-y-anen-reggae-se-unen-en-funky-kingston-con-concierto-en-barranco-noticia/'],
         'alta', 'activa',
         'Uno de los espacios con más fechas de Barranco (22 conciertos entre el 17-09 y fin de noviembre de 2026). Cada banda vende por su cuenta: '
         'Joinnus, Passline, Yape/Plin o WhatsApp. Su web (lanochedebarranco.com) no respondió; no se verificó Instagram.'),
    sala('Sargento Pimienta', ['Sargento Pimienta de Barranco', 'Sargento Pimienta Rock Bar', 'El Sargento'],
         'Av. Francisco Bolognesi 757, Barranco', 'bar/club',
         'Bar rockero fundado en 1975 y luego trasladado a Barranco; referente del rock peruano que hoy recibe bandas locales y giras argentinas.',
         ['Joinnus'],
         ['https://www.sargentopimienta.com.pe/historia/', CP + 'onda-vaga-amuletos-de-cristal-lima-2026/', OSM],
         'alta', 'activa',
         'Su web remite la agenda a eventos de Facebook (en la práctica difunde por redes). Dirección tomada de OpenStreetMap; la web no la publica.',
         web='https://www.sargentopimienta.com.pe/', instagram='https://www.instagram.com/sargentpimienta/',
         coordenadas=(-12.1437993, -77.0186685)),
    sala('El Dragón de Barranco', ['El Dragón', 'Dragón de Barranco', 'Escena Dragón'], 'Calle Nicolás de Piérola 168, Barranco', 'bar/club',
         'Bar cultural de música en vivo (jazz, electrónica, cumbia psicodélica) que, con el ciclo Escena Dragón, también programa temporadas de teatro breve.',
         ['Joinnus', 'WhatsApp'],
         ['https://puroteatro.pe/obra-teatral/con-ketchup-antes-de-parir', CP + 'space-cake-en-el-dragon-de-barranco-2026/',
          'https://diariocorreo.pe/espectaculos/hit-la-rosa-regresa-a-los-escenarios-con-un-concierto-en-dragon-de-barranco-noticia/', OSM],
         'media', 'activa',
         'Temporada teatral "Escena Dragón" (producción general Fátima Producciones) con tres obras breves; la entrada da acceso a las tres e '
         'incluye una bebida. Solo se halló fecha para "(Con ketchup) Antes de parir"; las otras dos ("¡No aplaudas!" de Angie Orihuela y '
         '"¡Lleve su huayruro, casera!" de Bruno Timarchi Ynoñán) no tienen fechas publicadas.',
         coordenadas=(-12.1413838, -77.0208977)),
    sala('La Casa Roja', ['La Casa Roja de Barranco', 'Casa Roja'], 'Av. Francisco Bolognesi 296, Barranco', 'independiente',
         'Casona que funciona como espacio de conciertos independientes, fiestas de colectivos y, desde noviembre de 2026, teatro inmersivo de terror.',
         ['Joinnus', 'WhatsApp'],
         [CP + 'oney1-en-lima-2026/', CP + 'bqestia-soundsystem-10-anos/',
          'https://limatimes.pe/agenda-cultural/2026/10/26/teatro-en-barranco-peru-oculto-un-viaje-ancestral-hacia-lo-desconocido/'],
         'media', 'activa',
         'Algunas fiestas venden por mensaje directo en Instagram. Sin web ni redes propias verificadas.'),
    sala('Casa Bulbo', ['Casa Bulbo Barranco'], 'Av. Francisco Bolognesi 660, Barranco', 'independiente',
         'Espacio cultural pequeño con ciclos de teatro breve y performance (como "Noche de Creadoras") y algunos conciertos.',
         ['WhatsApp'],
         ['https://limatimes.pe/agenda-cultural/2026/10/08/esta-semana-estrenan-la-obra-miedo-a-volar-en-casa-bulbo-de-barranco/',
          'https://diariocorreo.pe/cultura/las-cunadas-comedia-sobre-una-boda-caotica-llega-a-casa-bulbo-en-barranco-noticia/',
          'https://diariocorreo.pe/cultura/velas-al-mar-llega-a-casa-bulbo-en-barranco-noticia/'],
         'media', 'activa',
         'Programación teatral en abril, mayo y octubre de 2026; entradas solo por WhatsApp. Sin web ni redes verificadas.'),
    sala('Sala Osma', ['Sala Osma Barranco'], 'Av. Pedro de Osma 203, Barranco', 'independiente',
         'Sala de conciertos chica dedicada a bandas peruanas de rock e indie, con lanzamientos de discos casi todos los jueves.',
         ['Joinnus', 'WhatsApp'],
         [CP + 'wan-en-sala-osma-2026/', CP + 'marzenit-rabia-sala-osma-2026/', CP + 'fragil-en-sala-osma-2026/'],
         'media', 'activa',
         'Algunos conciertos son gratuitos con registro previo. Sin web ni redes verificadas.'),
    sala('Barranco Bar', [], 'Plaza Butters 291, Barranco', 'bar/club',
         'Bar de Barranco con noches de salsa y orquestas en vivo, con zonas de mesas y boxes.',
         ['Viapase'],
         [CP + 'gian-marco-en-barranco-bar-2026/',
          'https://www.infobae.com/peru/2026/10/28/gian-marco-llevara-su-nueva-etapa-salsera-a-tres-escenarios-ineditos-de-lima-en-noviembre/'],
         'baja', 'activa',
         'Solo se encontró un evento (Gian Marco, 8-11-2026). OpenStreetMap ubica un "Barranco Bar" en la Av. Jorge Chávez, lo que no coincide '
         'con Plaza Butters 291: no se ponen coordenadas. No se confirmó programación regular.'),
    sala('Sala Quilla', ['Quilla'], 'Av. Francisco Bolognesi 397, Barranco', 'independiente',
         'Sala pequeña de teatro de autor y experiencias inmersivas, activa desde al menos octubre de 2025.',
         ['Joinnus'],
         ['https://puroteatro.pe/obra-teatral/barba-sangre', 'https://puroteatro.pe/obra-teatral/la-caida',
          'https://diariocorreo.pe/cultura/reset-el-espectaculo-inmersivo-protagonizado-por-patricia-barreto-que-fusiona-arte-tecnologia-y-emocion-noticia/'],
         'media', 'activa',
         'Tres obras en cartel entre fines de octubre y noviembre de 2026. Sin web ni redes verificadas; la difusión llega por Puro Teatro y Joinnus.'),
    sala('Teatro Esencia', ['Espacio Teatro Esencia', 'Esencia de Barranco', 'Teatro Esencia de Barranco'],
         'Av. Almirante Miguel Grau 069-A, Barranco', 'independiente',
         'Teatro de bolsillo ligado a la Escuela de Teatro Musical Esencia (ETME); presenta musicales, teatro infantil y montajes íntimos.',
         ['Joinnus', 'Passline'],
         ['https://puroteatro.pe/obra-teatral/hansel-y-gretel-donde-cantan-los-recuerdos',
          'https://larepublica.pe/cultural/2024/01/09/la-cita-perfecta-un-paseo-por-nuestros-anhelos-inseguridades-y-deseos-carolyn-tolentino-kay-productora-etme-escuela-de-teatro-musical-esencia-teatro-esencia-433863',
          'https://peru21.pe/cultura/obra-de-teatro-fe-de-ratas-se-estrena-en-esencia-de-barranco/', OSM],
         'media', 'activa',
         'Aforo de 38 personas según La República (2024). Instagram citado en esa nota: @etmesencia (de la escuela). OpenStreetMap usa el número 071. '
         'Peru21 reseñó "Fe de ratas" (feb. 2026) vendida por Passline; no se pudo abrir la nota para verificarlo.',
         instagram='https://www.instagram.com/etmesencia/', coordenadas=(-12.1518507, -77.0200353), aforo=38),
    sala('PayaCasa', [], 'Av. Francisco Bolognesi 920, Barranco', 'independiente',
         'Espacio pequeño que presenta comedia de clown; en noviembre de 2026 programa la segunda temporada de "Entre clases".',
         ['WhatsApp'],
         ['https://puroteatro.pe/obra-teatral/entre-clases-segunda-temporada'],
         'baja', 'activa',
         'Solo una fuente (Puro Teatro). No se confirmó si es una sala permanente o una casa que alquila su espacio. Sin web ni redes verificadas.'),
    sala('La Posada del Mirador', ['Posada del Mirador', 'LA POSADA DEL MIRADOR - BARRANCO - LIMA'], 'Calle La Ermita 104, Barranco', 'bar/club',
         'Bar junto al Puente de los Suspiros donde se hacen noches de stand-up y han debutado varios comediantes jóvenes.',
         ['Teleticket'],
         ['https://teleticket.com.pe/evento/2pa2-sin-censura-la-posada-del-mirador',
          'https://teleticket.com.pe/evento/la-historia-que-no-se-sube-show-de-comedia-diego-gupioc-la-posada-del-mirador',
          'https://www.escenaliberada.com/diego-gupioc-presenta-fuera-de-control/', OSM],
         'media', 'incierto',
         'Shows de stand-up en Teleticket hasta febrero de 2026 (consumo mínimo S/ 35-40). No se hallaron funciones en sep-nov 2026, por eso '
         'estado "incierto" para la programación escénica.',
         coordenadas=(-12.1495453, -77.0234137)),
    sala('Peña Don Porfirio', ['Don Porfirio'], 'Jr. Manuel Segura 115, Barranco', 'bar/club',
         'Peña criolla familiar que abre los viernes por la noche con música en vivo; en fechas como el Día de la Canción Criolla abre también otros días.',
         ['reserva directa'],
         ['https://elcomercio.pe/somos/dia-del-padre-regalos-ideas-celebra-el-dia-de-papa-en-una-pena-con-esta-ruta-noticia/',
          'https://gestion.pe/tendencias/estilos/con-guitarra-y-cajon-propuestas-de-penas-limenas-en-el-dia-de-la-cancion-criolla-musica-peruana-estilos-danzas-marinera-noticia/'],
         'media', 'activa',
         'Viernes desde las 8:30 p. m. (Somos, jun. 2026). Reservas con pago adelantado, que suelen agotarse con días de anticipación. '
         'No publica cartelera: difunde por Instagram.', instagram='https://www.instagram.com/donporfirio.oficial/'),
    sala('Peña La Oficina', ['La Oficina de Barranco', 'La Oficina'], 'Calle Enrique Barrón 441, Barranco', 'bar/club',
         'Peña criolla y afroperuana con noches de música y baile los fines de semana; de día funciona como restaurante.',
         ['reserva directa'],
         ['https://elcomercio.pe/somos/dia-del-padre-regalos-ideas-celebra-el-dia-de-papa-en-una-pena-con-esta-ruta-noticia/',
          'https://gestion.pe/tendencias/estilos/con-guitarra-y-cajon-propuestas-de-penas-limenas-en-el-dia-de-la-cancion-criolla-musica-peruana-estilos-danzas-marinera-noticia/'],
         'media', 'activa',
         'Noches de peña vie y sáb 9:30 p. m.-1:30 a. m. (Somos, jun. 2026). Aforo cercano a 80 personas según Gestión (2024). No publica cartelera: difunde por Instagram.',
         instagram='https://www.instagram.com/laoficinadebarranco/', aforo=80),
    sala('La Peña del Carajo', ['Del Carajo', 'Peña del Carajo'], 'Calle Catalino Miranda 158, Barranco', 'bar/club',
         'Peña con más de 25 años dedicada a la música criolla, con jaranas de fin de semana por la tarde.',
         ['reserva directa'],
         ['https://elcomercio.pe/somos/dia-del-padre-regalos-ideas-celebra-el-dia-de-papa-en-una-pena-con-esta-ruta-noticia/'],
         'media', 'activa',
         'Sáb y dom de 1 a 6 p. m. (Somos, jun. 2026). No publica cartelera: difunde por Instagram.',
         instagram='https://www.instagram.com/delcarajoperu/'),
]


def main():
    salas_json = json.load(open(RAIZ / 'data' / 'salas.json'))
    en_salas = {s['nombre'] for s in salas_json}
    for s in SALAS:
        if s['nombre'] in en_salas:
            assert 'Completado' in s['notas'] or 'completado' in s['notas'].lower(), s['nombre']
    out = RAIZ / 'data' / 'salas_barranco.json'
    json.dump(SALAS, open(out, 'w'), ensure_ascii=False, indent=1)
    print(len(SALAS), 'espacios ->', out, '| ya en salas.json:', sum(s['nombre'] in en_salas for s in SALAS))


if __name__ == '__main__':
    main()
