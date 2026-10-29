"""Arma data/extraido/salas_barranco.json con la cartelera de Barranco (desde el 17-09-2026, 6 semanas antes
del 29-10-2026, hasta lo anunciado a futuro). Los datos salen de las páginas guardadas en raw/barranco/
(Puro Teatro, Teleticket, Passline vía buscador, Conciertos Perú, Lima Times, Diario Correo, El Comercio,
Diario UNO, Gato Encerrado). Las sinopsis están escritas a mano, sin copiar el texto de las fuentes.
Los enlaces de Joinnus solo se anotan como url_compra: no se abrieron.

Uso: python3 obras_barranco.py  (valida contra catalogo.json y escribe el JSON)
"""
import json, re, unicodedata, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'data' / 'extraido' / 'salas_barranco.json'

PT = 'https://puroteatro.pe/obra-teatral/'
CP = 'https://conciertosperu.com.pe/'
TT = 'https://teleticket.com.pe/evento/'
PL_TB = 'https://www.passline.com/productora/teatro-barranco-755463861'
JN = 'https://www.joinnus.com/events/'


def slug(s):
    s = unicodedata.normalize('NFKD', s.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def P(nombres):
    return [{'nombre': n, 'personaje': None} for n in nombres]


def F(*pares):
    return [{'nombre': n, 'rol': r} for n, r in pares]


OBRAS = []


def obra(sala, titulo, tipo, generos, sinopsis, fuente, url, url_compra, horario, inicio, fin,
         precio=None, edad=None, dur=None, elenco=(), ficha=(), artistas=(), productora=None, incluir=True):
    OBRAS.append({
        'id': f'brc-{slug(sala)}-{slug(titulo)}'[:120],
        'fuente': fuente, 'url': url, 'url_compra': url_compra, 'incluir': incluir,
        'titulo': titulo, 'tipo': tipo, 'generos': list(generos)[:3], 'sinopsis': sinopsis,
        'elenco': list(elenco), 'ficha': list(ficha), 'artistas': list(artistas), 'productora': productora,
        'sala': sala, 'distrito': 'Barranco', 'ciudad': 'Lima',
        'duracion_min': dur, 'edad_minima': edad, 'horario_texto': horario,
        'temporada': {'inicio': inicio, 'fin': fin}, 'precio_desde': precio, 'imagen': None,
    })


# ---------------------------------------------------------------- Teatro Barranco (Av. Grau 701)
S = 'Teatro Barranco'
obra(S, 'El ritmo del dolor', 'teatro', ['drama'],
     'Un montaje que parte de los dolores que cargamos sin que se noten y busca transformarlos en arte sobre el escenario.',
     'prensa', PT + 'el-ritmo-del-dolor', JN + 'theater/lima-el-ritmo-del-dolor-79711',
     'Sáb 8 p. m. (7, 14, 21 y 28 de noviembre)', '2026-11-07', '2026-11-28')
obra(S, 'Los chismes de las mujeres', 'comedia', ['comedia', 'clásico'],
     'La comedia de Goldoni sobre un vecindario donde los rumores y los celos se enredan hasta que nadie queda a salvo, en versión de Alumbra Producciones.',
     'prensa', 'https://diariouno.pe/2026/10/24/obra-dirigida-por-martin-velasquez-marvelat-vuelve-al-teatro-barranco/',
     JN + 'theater/lima-los-chismes-de-las-mujeres-80012',
     'Dom 8 p. m. (15, 22 y 29 de noviembre; 6 y 13 de diciembre)', '2026-11-15', '2026-12-13',
     elenco=P(['Pau Simons', 'Angie Orihuela', 'Marcelo Prado', 'Hugo Menéndez', 'Violeta Dueñas', 'José Leonardo',
               'Sophia García', 'Yaneth Gutiérrez', 'Walter Gil', 'Petronik', 'Carlos Thornton', 'Katherina Sánchez']),
     ficha=F(('Carlo Goldoni', 'dramaturgia'), ('Martín Velásquez Marvelat', 'dirección'), ('Loreley Vidal', 'producción')),
     productora='Alumbra Producciones')
obra(S, 'Mamma Mia: la fiesta', 'musical', ['musical', 'familiar'],
     'Un elenco de jóvenes cantantes repasa en vivo las canciones de ABBA en un espectáculo pensado para ver en familia.',
     'prensa', PT + 'mamma-mia-la-fiesta', JN + 'theater/lima-mamma-mia-la-fiesta-76837',
     'Dom 20 de diciembre, 5 p. m.', '2026-12-20', '2026-12-20')
obra(S, 'Mesa tomada 2.0', 'comedia', ['comedia', 'romance'],
     'En una trattoria imaginaria se cruzan parejas en crisis, citas fallidas y amores que recién empiezan, y cada mesa termina afectando a la de al lado.',
     'prensa', 'https://diariocorreo.pe/cultura/mesa-tomada-20-llega-al-teatro-barranco-con-amores-rupturas-y-enredos-noticia/',
     PL_TB, 'Vie 8 p. m. (4, 11, 18 y 25 de septiembre; función promocional el 2 de octubre)', '2026-09-04', '2026-10-02',
     precio=40, edad=16,
     elenco=P(['Fernando Cáceres', 'Luisito Fernández', 'Pepe Murray', 'Andrea Chuiman', 'Christian Alden', 'Quini Gómez']),
     ficha=F(('Christian Ávalos', 'dirección'), ('Christian Ávalos', 'dramaturgia'), ('Luisito Fernández', 'dramaturgia'),
             ('Christian Ávalos', 'adaptación')),
     productora='Krakens Producciones y La Intensa Producción')
obra(S, 'Kortas: octubre', 'teatro', ['teatro breve'],
     'Edición de octubre de Kortas, el ciclo de la sala que junta varias obras cortas de creadores emergentes en una misma noche.',
     'passline', PL_TB, PL_TB, 'Mar 6 y mié 7 de octubre, 8 p. m.', '2026-10-06', '2026-10-07', precio=25)
obra(S, 'Rodeados de amor', 'comedia', ['comedia', 'romance', 'lgbtiq+'],
     'Comedia romántica de temática queer para público mayor de 16 años.',
     'passline', 'https://www.passline.com/sitio-evento/rodeados-de-amor-568357',
     'https://www.passline.com/sitio-evento/rodeados-de-amor-568357',
     'Jue 5 y jue 12 de noviembre, 8 p. m.', '2026-11-05', '2026-11-12', precio=40, edad=16)
# Funciones que solo aparecen en el listado de Passline de la productora, sin descripción: se anotan con incluir=false.
for t, tipo, h, d, p in [('Polinecios', 'otro', 'Sáb 3 de octubre, 4 p. m.', '2026-10-03', 30),
                         ('Cuando pienses en volver', 'musical', 'Jue 8 de octubre', '2026-10-08', 40),
                         ('Acto de magia', 'otro', 'Sáb 24 de octubre, 8 p. m.', '2026-10-24', 35),
                         ('EPIC: edición Halloween', 'otro', 'Sáb 31 de octubre, 2 p. m.', '2026-10-31', 40),
                         ('Canto como niña', 'otro', 'Jue 5 de noviembre, 8 p. m.', '2026-11-05', 44)]:
    obra(S, t, tipo, [], 'Función programada en el Teatro Barranco; el listado público de Passline no trae descripción ni ficha.',
         'passline', PL_TB, PL_TB, h, d, d, precio=p, incluir=False)

# ---------------------------------------------------------------- Teatro Juanita Tarnawiecki (ex Mocha Graña)
S = 'Teatro Juanita Tarnawiecki (ex Mocha Graña)'
obra(S, 'La noche de los asesinos', 'teatro', ['drama'],
     'Vuelve este montaje en el que tres hermanos ensayan una y otra vez la muerte de sus padres, un juego que se va pareciendo cada vez más a un juicio.',
     'prensa', PT + 'la-noche-de-los-asesinos', JN + 'theater/lima-la-noche-de-los-asesinos-77646',
     'Vie y sáb 8 p. m. (30 y 31 de octubre; 6 y 7 de noviembre)', '2026-10-30', '2026-11-07')
obra(S, 'El engranaje', 'teatro', ['teatro', 'danza'],
     'Con teatro y danza, una joven conversa con el público sobre su vocación mientras un sistema, test vocacional de por medio, intenta convertirla en una pieza productiva más.',
     'prensa', 'https://limatimes.pe/agenda-cultural/2026/10/08/barranco-colectivo-auredia-presenta-obra-de-teatro-y-danza-el-engranaje/',
     None, 'Vie 9, sáb 10 y vie 16 de octubre, 8 p. m.', '2026-10-09', '2026-10-16', precio=30,
     elenco=P(['Sol Yucra Sereno', 'Natalia López', 'Suleira Antoanee', 'María Angulo']),
     ficha=F(('Emilio Napan Cerro', 'dramaturgia'), ('Emilio Napan Cerro', 'dirección')),
     productora='Auredia Colectivo Teatral')

# ---------------------------------------------------------------- Teatro Racional
S = 'Teatro Racional'
obra(S, 'Sofía y el daño que habitamos', 'teatro', ['drama', 'psicológico'],
     'Drama psicológico contado sin orden cronológico, que se mete con los límites de la moral familiar y el deseo.',
     'prensa', PT + 'sofia-y-el-dano-que-habitamos', JN + 'theater/lima-sofia-y-el-dano-que-habitamos-79726',
     'Vie y sáb 8 p. m. (20, 21, 27 y 28 de noviembre)', '2026-11-20', '2026-11-28')

# ---------------------------------------------------------------- Sala Quilla (Av. Bolognesi 397)
S = 'Sala Quilla'
obra(S, 'Barba Sangre', 'teatro', ['terror', 'cuentos', 'música'],
     'Una sesión de cuentos de terror narrados con música, pensada para que la palabra hablada vuelva a dar escalofríos.',
     'prensa', PT + 'barba-sangre', JN + 'theater/lima-barba-sangre-79144',
     'Vie a dom (30 y 31 de octubre; 1, 6, 7 y 8 de noviembre); función del 30 a las 8:30 p. m.', '2026-10-30', '2026-11-08')
obra(S, 'La caída', 'teatro', ['drama'],
     'Un recorrido simbólico guiado por el espíritu de un ave extinta, que se pregunta por el tiempo que vivimos y por otras formas posibles de convivir.',
     'prensa', PT + 'la-caida', JN + 'theater/lima-la-caida-79927',
     'Mié 4 de noviembre, 8 p. m.', '2026-11-04', '2026-11-04')
obra(S, 'Los tres cantos del gallo', 'teatro', ['drama', 'teatro físico'],
     'Toma la figura del gallo, ave domesticada que aun así anuncia el amanecer, para poner en cuerpo y voz la pérdida de dignidad del ser humano.',
     'prensa', PT + 'los-tres-cantos-del-gallo', JN + 'theater/lima-los-tres-cantos-del-gallo-79942',
     'Jue 5 de noviembre, 8 p. m.', '2026-11-05', '2026-11-05')

# ---------------------------------------------------------------- Teatro Esencia (Av. Grau 069-A)
obra('Teatro Esencia', 'Hansel y Gretel: donde cantan los recuerdos', 'infantil', ['familiar', 'musical', 'cuentos'],
     'Versión musical del cuento de los hermanos perdidos en el bosque, con canciones y humor, que pone el acento en el cariño, la imaginación y el perdón.',
     'prensa', PT + 'hansel-y-gretel-donde-cantan-los-recuerdos', JN + 'theater/lima-hansel-y-gretel-donde-cantan-los-recuerdos-79375',
     'Dom 5 p. m. (1, 8 y 15 de noviembre)', '2026-11-01', '2026-11-15')

# ---------------------------------------------------------------- El Dragón de Barranco (Nicolás de Piérola 168)
S = 'El Dragón de Barranco'
obra(S, '(Con ketchup) Antes de parir', 'comedia', ['comedia', 'metateatro'],
     'A dos días de un estreno, una actriz que no logra entrar en su personaje intenta salvar el ensayo general mientras su hijo pequeño tiene hambre y quiere irse a casa.',
     'prensa', PT + 'con-ketchup-antes-de-parir', 'https://wa.me/996503431',
     'Mar 3 de noviembre, 8 p. m.', '2026-11-03', '2026-11-03',
     elenco=P(['Vane De la Torre', 'Ilda Polo', 'Paulo César Polo Chávez']),
     ficha=F(('Paulo César Polo Chávez', 'dramaturgia'), ('Paulo César Polo Chávez', 'dirección'),
             ('Fátima Producciones', 'producción'), ('Luis Peche Alvarado', 'otro')),
     productora='LSPC Creación Escénica Sensorial')
obra(S, 'Space Cake', 'concierto', ['jazz', 'electrónica'],
     'El trío de Diego Rodríguez Arnaiz, Andrés Landavere y Cristóbal Mujica tocó su electro jazz en una fecha del ciclo Escena Dragón.',
     'prensa', CP + 'space-cake-en-el-dragon-de-barranco-2026/', None,
     'Mié 14 de octubre', '2026-10-14', '2026-10-14', precio=40,
     artistas=['Space Cake'], productora='Escena Dragón')

# ---------------------------------------------------------------- PayaCasa (Av. Bolognesi 920)
obra('PayaCasa', 'Entre clases (segunda temporada)', 'comedia', ['clown', 'comedia'],
     'Monina, una clown muy refinada que nunca salió de su burbuja, sueña con ser profesora y descubre que en el aula tiene más que aprender que enseñar.',
     'prensa', PT + 'entre-clases-segunda-temporada', 'https://wa.me/991842602',
     'Sáb y dom (7, 8, 14 y 15 de noviembre); función del 7 a las 8 p. m.', '2026-11-07', '2026-11-15')

# ---------------------------------------------------------------- Casa Bulbo (Av. Bolognesi 660)
obra('Casa Bulbo', 'Miedo a volar', 'comedia', ['comedia', 'romance'],
     'Una tormenta deja atrapados en un aeropuerto a dos desconocidos que no se soportan y que, entre discusiones, terminan hablando de lo que más les asusta.',
     'prensa', 'https://limatimes.pe/agenda-cultural/2026/10/08/esta-semana-estrenan-la-obra-miedo-a-volar-en-casa-bulbo-de-barranco/',
     None, 'Jue 9 p. m. (del 8 al 29 de octubre)', '2026-10-08', '2026-10-29',
     elenco=P(['Juan Carlos Díaz', 'Silvana Picco']),
     ficha=F(('Federico Abrill', 'dramaturgia'), ('Joamoc', 'dirección')))

# ---------------------------------------------------------------- La Casa Roja (Av. Bolognesi 296)
S = 'La Casa Roja'
obra(S, 'Perú oculto: un viaje ancestral hacia lo desconocido', 'teatro', ['terror', 'inmersivo', 'leyendas'],
     'Experiencia inmersiva de terror en la que un guía lleva al público por tres espacios inspirados en las brujas de Cachiche, el Tunche y la Jarjacha.',
     'prensa', 'https://limatimes.pe/agenda-cultural/2026/10/26/teatro-en-barranco-peru-oculto-un-viaje-ancestral-hacia-lo-desconocido/',
     JN + 'theater/lima-peru-oculto-un-viaje-ancentral-hacia-lo-desconocido-79775',
     'Jue 8 y 10 p. m.; sáb 7 y 9 p. m. (del 5 al 21 de noviembre)', '2026-11-05', '2026-11-21',
     ficha=F(('Mario Gaviria', 'dirección'), ('Mario Gaviria', 'dramaturgia'), ('José Leonardo', 'producción'),
             ('Melanie Malpartida', 'producción'), ('Valeria Ramos', 'otro')),
     productora='Ukupacha Producciones')
obra(S, 'Oney1', 'concierto', ['urbano'],
     'Primera visita a Lima del artista argentino, que llegó tras sus shows en salas de Buenos Aires.',
     'prensa', CP + 'oney1-en-lima-2026/', JN + 'concerts/lima-oney1-en-lima-peru-77851',
     'Sáb 19 de septiembre', '2026-09-19', '2026-09-19', precio=75, artistas=['Oney1'])
obra(S, 'El Perro y la Banda Sutil', 'concierto', ['rock', 'independiente'],
     'Juan Carlos «El Perro» Calderón volvió al escenario con su Banda Sutil, en una noche compartida con La Máquina Camaleón y Cementerio Inocentes.',
     'prensa', CP + 'el-perro-y-la-banda-sutil/', None, 'Vie 9 de octubre', '2026-10-09', '2026-10-09', edad=18,
     artistas=['Juan Carlos Calderón', 'La Banda Sutil', 'La Máquina Camaleón', 'Cementerio Inocentes'],
     productora='Vichama Conciertos')
obra(S, 'BQestia Soundsystem: 10 años', 'concierto', ['electrónica', 'club'],
     'El colectivo celebra una década con una noche de club music, techno y bass a cargo de varios DJ invitados.',
     'prensa', CP + 'bqestia-soundsystem-10-anos/', None, 'Sáb 7 de noviembre', '2026-11-07', '2026-11-07', precio=20,
     artistas=['Jah Chata', 'Jesperino', 'King Cholo', 'N3T4', 'Trilce', 'Yozty'])
obra(S, 'Diana Salas', 'concierto', ['pop'],
     'Concierto especial en el que la cantante revelará cuál de dos temas inéditos, elegido por votación de su público, será su próximo sencillo.',
     'prensa', CP + 'diana-salas-en-lima-2026/', None, 'Sáb 14 de noviembre', '2026-11-14', '2026-11-14', precio=55, edad=18,
     artistas=['Diana Salas'])

# ---------------------------------------------------------------- Aforo Barranco (Av. Grau 264)
S = 'Aforo Barranco'
obra(S, 'Terapia Blanquiazvl', 'teatro', ['inmersivo', 'música en vivo'],
     'Montaje inmersivo sobre la identidad y el sentido de pertenencia de los hinchas de Alianza Lima, con música en vivo y cierre de fiesta temática.',
     'prensa', 'https://www.gatoencerrado.net/el-1-de-octubre-se-estrena-terapia-blanquiazvl-en-barranco/', None,
     'Jue 8 p. m. (1, 8, 15, 22 y 29 de octubre)', '2026-10-01', '2026-10-29',
     elenco=P(['Luis José Ocampo', 'Alain Salinas']),
     ficha=F(('Herbert Corimanya', 'dramaturgia'), ('Herbert Corimanya', 'dirección')))
obra(S, 'Giru Mad Fleiva: Mad Fleiva Tour', 'concierto', ['urbano'],
     'Cierre en Lima de la gira de Giru Mad Fleiva, con un repaso de sus temas más conocidos y artistas invitados.',
     'prensa', CP + 'giru-mad-fleiva-en-lima-2026/', 'https://www.passline.com/eventos/mad-fleiva-tour-07-oct',
     'Mié 7 de octubre', '2026-10-07', '2026-10-07', precio=35, edad=18, artistas=['Giru Mad Fleiva'])
obra(S, 'Dimitri y las Brujas', 'concierto', ['pop', 'rock'],
     'Debut en Lima de Dimitri y las Brujas, con un recorrido por toda su discografía y teloneros locales.',
     'prensa', CP + 'dimitri-y-las-brujas-en-lima-2026/', None, 'Vie 16 de octubre', '2026-10-16', '2026-10-16', precio=100,
     artistas=['Dimitri y las Brujas', 'Manuel Valdez', 'Daniela de Izcue'])

# ---------------------------------------------------------------- Centro de Convenciones Bianca (Av. Grau 135)
S = 'Centro de Convenciones Bianca'
obra(S, 'Se busca marido cama afuera', 'comedia', ['comedia', 'música en vivo'],
     'Johanna San Miguel volvió con una edición especial de su comedia sobre reinventarse después de una caída, con anécdotas y música en vivo.',
     'teleticket', 'https://teleticket.com.pe/sebuscamaridocamaafuera-bianca2026', 'https://teleticket.com.pe/sebuscamaridocamaafuera-bianca2026',
     'Jue 8 p. m. (del 6 de agosto al 24 de septiembre)', '2026-08-06', '2026-09-24', precio=51, edad=18, dur=90,
     elenco=P(['Johanna San Miguel']), productora='DEA Promotora S.A.')
obra(S, 'Los Vílchez en Santo Problema', 'show', ['comedia', 'música'],
     'Un show sin guion ni director en el que la familia Vílchez cuenta su vida en escena, con música de antaño y trivias con el público.',
     'teleticket', TT + 'los-vilchez-en-santo-problema-cc-bianca', TT + 'los-vilchez-en-santo-problema-cc-bianca',
     'Funciones a las 8:30 p. m. entre el 7 de mayo y el 23 de septiembre', '2026-05-07', '2026-09-23', edad=18, dur=60,
     productora='Danger Producciones')
obra(S, 'Noche de emociones', 'concierto', ['balada', 'música romántica'],
     'Tres voces, César Mancilla, Susan Ochoa y Jeremy Gómez, compartieron escenario en una noche de canciones para corear.',
     'teleticket', TT + 'noche-de-emociones-cesar-mancilla-susan-ochoa-jeremy-gomez-centro-de-convenciones-bianca',
     TT + 'noche-de-emociones-cesar-mancilla-susan-ochoa-jeremy-gomez-centro-de-convenciones-bianca',
     'Vie 18 de septiembre, 10:30 p. m.', '2026-09-18', '2026-09-18', edad=14, dur=120,
     artistas=['César Mancilla', 'Susan Ochoa', 'Jeremy Gómez'], productora='Showmusic E.I.R.L.')
obra(S, 'Jayro Tafur: más romántico que nunca', 'concierto', ['balada', 'música romántica'],
     'El cantante romántico presentó sus éxitos con banda en vivo y artistas invitados.',
     'teleticket', TT + 'jayro-tafur-mas-romantico-que-nunca-cc-bianca', TT + 'jayro-tafur-mas-romantico-que-nunca-cc-bianca',
     'Sáb 10 de octubre, 10:30 p. m.', '2026-10-10', '2026-10-10', edad=18, dur=180,
     artistas=['Jayro Tafur'], productora='Family Productions EIRL')
obra(S, 'Tunantadas de amor', 'folklore', ['música andina', 'almuerzo show'],
     'Almuerzo show de Gustavo Ratto, «el arriero de la tunantada», con danzantes, banda en vivo y la agrupación Entre Manos.',
     'prensa', 'https://diariocorreo.pe/espectaculos/gustavo-ratto-lleva-tunantadas-de-amor-a-barranco-fecha-lugar-y-entradas-noticia/',
     None, 'Dom 18 de octubre, desde la 1 p. m.', '2026-10-18', '2026-10-18', artistas=['Gustavo Ratto', 'Entre Manos'])
obra(S, 'Ricky Santos: Amor y cumbia', 'concierto', ['cumbia'],
     'Ricky Santos presentó su show de cumbia con orquesta en vivo y artistas invitados.',
     'prensa', CP + 'ricky-santos-en-lima-2026/', None, 'Jue 22 de octubre', '2026-10-22', '2026-10-22', precio=45,
     artistas=['Ricky Santos'], productora='Emiam Producciones Perú')
obra(S, 'Ellas en concierto en Bianca', 'concierto', ['tributo', 'pop latino'],
     'Cuatro ganadoras de concursos de imitación rindieron homenaje a Alejandra Guzmán, Mon Laferte, Yuri y Olga Tañón.',
     'teleticket', TT + 'ellas-en-concierto-en-bianca-cc-bianca', TT + 'ellas-en-concierto-en-bianca-cc-bianca',
     'Vie 23 de octubre, 10 p. m.', '2026-10-23', '2026-10-23', edad=14, dur=240,
     artistas=['Melissa Ángeles', 'Oriana Montero', 'Noelia Calle', 'Luna Mendoza'], productora='TYS Eventos Perú E.I.R.L.')
obra(S, 'Cero migajeros', 'comedia', ['comedia', 'romance'],
     'Laura Huarcayo y Carlos Vílchez debutan juntos en el teatro con una comedia sobre amores complicados y lo que pasa cuando uno acepta menos de lo que merece.',
     'prensa', 'https://elcomercio.pe/luces/teatro/laura-huarcayo-y-carlos-vilchez-debutan-en-el-teatro-con-la-comedia-cero-migajeros-ultimas-noticia/',
     None, 'Mié 8 p. m. (18 y 25 de noviembre; 2 y 9 de diciembre)', '2026-11-18', '2026-12-09', precio=50,
     elenco=P(['Laura Huarcayo', 'Carlos Vílchez']))
obra(S, 'Barranqueando a nuestro modo', 'folklore', ['música andina', 'huayno'],
     'Diosdado Gaitán Castro ofrece una noche de huaynos, carnavales y caporales junto al Dúo Ayacucho y el Grupo Ocobamba.',
     'prensa', 'https://limatimes.pe/agenda-cultural/2026/10/29/diosdado-gaitan-llega-con-su-canto-andino-a-barranco/',
     JN + 'concerts/lima-barranqueando-a-nuestro-modo-79475', 'Vie 20 de noviembre, 9:30 p. m.', '2026-11-20', '2026-11-20',
     artistas=['Diosdado Gaitán Castro', 'Dúo Ayacucho', 'Grupo Ocobamba'])

# ---------------------------------------------------------------- La Estación de Barranco (Av. Pedro de Osma 112)
S = 'La Estación de Barranco'
obra(S, 'Migajera nunca más', 'comedia', ['comedia', 'humor'],
     'Un show de humor que mezcla historias reales para recordarle al público que nadie debería conformarse con migajas en el amor.',
     'teleticket', TT + 'migajera-nunca-mas-la-estacion-de-barranco', TT + 'migajera-nunca-mas-la-estacion-de-barranco',
     'Mar 8:30 p. m. (del 1 de septiembre al 27 de octubre)', '2026-09-01', '2026-10-27', edad=14,
     productora='AMU Agencia de Mentes Únicas SAC')
obra(S, 'Tributo a Cristian Castro por Daniel Rioja', 'concierto', ['tributo', 'balada'],
     'Daniel Rioja y banda en vivo repasaron las baladas más conocidas de Cristian Castro, con artistas invitados.',
     'teleticket', TT + 'tributo-a-cristian-castro-por-daniel-rioja-la-estacion-de-barranco',
     TT + 'tributo-a-cristian-castro-por-daniel-rioja-la-estacion-de-barranco',
     'Sáb 24 de octubre, 10:30 p. m.', '2026-10-24', '2026-10-24', edad=18, dur=120, artistas=['Daniel Rioja'])

# ---------------------------------------------------------------- Capital Restobar (Av. Grau 680)
obra('Capital Restobar', 'Electro Showck: la comedia de alto voltaje', 'comedia', ['comedia', 'musical'],
     'Comedia musical sobre el regreso de un cantante a los escenarios que se desbarata cuando el único técnico del show se emborracha y pierde el control de luces y sonido.',
     'teleticket', TT + 'electro-showck-%E2%80%93-la-comedia-de-alto-voltaje-capital-restobar',
     TT + 'electro-showck-%E2%80%93-la-comedia-de-alto-voltaje-capital-restobar',
     'Funciones a las 8 p. m. entre el 11 de septiembre y el 23 de octubre', '2026-09-11', '2026-10-23', dur=120,
     productora='La X Productora S.A.C.')

# ---------------------------------------------------------------- Roble de Barranco (Psje. Sánchez Carrión 147)
obra('Roble de Barranco', 'Feliz Día de la Canción Criolla con Los Kipus', 'concierto', ['música criolla', 'almuerzo show'],
     'Almuerzo show por el Día de la Canción Criolla con Los Kipus y, como invitados, Manuel Donayre y Dayron Aranguren.',
     'teleticket', TT + 'feliz-dia-de-la-cancion-criolla-con-los-kipus-el-roble-de-barranco',
     TT + 'feliz-dia-de-la-cancion-criolla-con-los-kipus-el-roble-de-barranco',
     'Sáb 31 de octubre, 1 p. m.', '2026-10-31', '2026-10-31', dur=120,
     artistas=['Los Kipus', 'Manuel Donayre', 'Dayron Aranguren'], productora='Arte.pe E.I.R.L.')

# ---------------------------------------------------------------- Centro de Convenciones Barranco (Av. República de Panamá 220)
S = 'Centro de Convenciones Barranco'
obra(S, 'Kidd Voodoo: Euforia World Tour', 'concierto', ['urbano', 'trap'],
     'El chileno Kidd Voodoo trajo la gira de su disco Euforia, entre el trap y el pop alternativo.',
     'teleticket', 'https://teleticket.com.pe/kidd-voodoo', 'https://teleticket.com.pe/kidd-voodoo',
     'Vie 16 de octubre, 8 p. m.', '2026-10-16', '2026-10-16', precio=115, dur=120,
     artistas=['Kidd Voodoo'], productora='Bizarro Entertainment y Servicios Perú S.A.C.')
for (t, g, sin, url, compra, h, d, d2, p, e, art, prod) in [
    ('Tipling Rock: América Latina Tour 2026', ['indie pop'], 'Primera fecha en el Perú de la banda de indie pop Tipling Rock.',
     'tipling-rock-en-lima-2026/', 'https://www.passline.com/eventos/tipling-rock-en-lima', 'Mié 14 de octubre', '2026-10-14', '2026-10-14', None, None, ['Tipling Rock'], None),
    ('Six Sex: ULTRA', ['electrónica', 'urbano'], 'Debut en Lima de Six Sex, que presenta su álbum ULTRA.',
     'six-sex-en-lima-2026/', None, 'Mié 21 de octubre', '2026-10-21', '2026-10-21', 164, 18, ['Six Sex'], 'Veltrac Music'),
    ('Rock N’ Love Vol. 3', ['rock', 'balada'], 'Tercera edición de esta noche de baladas del rock peruano, con Mar de Copas y Pelo Madueño a la cabeza.',
     'rock-n-love-vol-3-2026/', 'https://www.digitalticket.pe/event/rock-n-love-vol-3', 'Vie 23 de octubre', '2026-10-23', '2026-10-23', 99, None,
     ['Mar de Copas', 'Pelo Madueño', 'Los Trece Baladas', 'Toño Jáuregui', 'Gaia', 'Percy Behr', 'Fantasmaas'], None),
    ('Jaze: QNEPT Tour II', ['rap', 'urbano'], 'Dos noches de Jaze con un show que alterna momentos intensos, pasajes acústicos y freestyle.',
     'jaze-en-lima-2026/', JN + 'concerts/lima-jaze-lima-29-de-octubre-76657', 'Mié 28 y jue 29 de octubre', '2026-10-28', '2026-10-29', 72.5, None, ['Jaze'], None),
    ('Saramalacara: Mataderos World Tour', ['rap', 'urbano'], 'Primera visita a Lima de la rapera argentina, que presenta su álbum Mataderos.',
     'saramalacara-en-lima-2026/', None, 'Mar 3 de noviembre', '2026-11-03', '2026-11-03', 164, 12, ['Saramalacara'], None),
    ('Coti', ['pop', 'rock'], 'El cantautor argentino repasa las canciones que marcaron su carrera.',
     'coti-en-lima-2026/', None, 'Vie 6 de noviembre', '2026-11-06', '2026-11-06', 179, None, ['Coti'], None),
    ('TIMØ', ['pop'], 'La agrupación colombiana vuelve a Lima con un show apto para menores acompañados.',
     'timo-en-lima-2026-2/', JN + 'concerts/lima-tim-en-lima-76127', 'Dom 8 de noviembre', '2026-11-08', '2026-11-08', 155, 6, ['TIMØ'], None),
    ('The Lemon Twigs', ['rock'], 'Primera presentación en Lima de la banda estadounidense, dentro del ciclo Indiegentes 2026.',
     'the-lemon-twigs-en-lima-2026/', None, 'Mié 11 de noviembre', '2026-11-11', '2026-11-11', 172, 18, ['The Lemon Twigs'], None),
    ('Lagos: Tour 2026', ['pop'], 'El dúo venezolano de productores y compositores trae su gira a Lima.',
     'lagos-en-lima-2026/', None, 'Jue 10 de diciembre', '2026-12-10', '2026-12-10', 155, 16, ['Lagos'], None),
    ('Galneryus', ['heavy metal', 'power metal'], 'Primera visita a Lima de la banda japonesa de power metal.',
     'galneryus-en-lima-2027/', None, 'Vie 12 de febrero de 2027', '2027-02-12', '2027-02-12', 249, 18, ['Galneryus'], None),
]:
    obra(S, t, 'concierto', g, sin, 'prensa', CP + url, compra, h, d, d2, precio=p, edad=e, artistas=art, productora=prod)

# ---------------------------------------------------------------- Barranco Bar (Plaza Butters 291)
obra('Barranco Bar', 'Gian Marco: Bajo la manga', 'concierto', ['salsa'],
     'Gian Marco presenta su disco de salsa en una noche compartida con la Orquesta Bembé, María Grazia, Zaperoko y César Vega.',
     'prensa', CP + 'gian-marco-en-barranco-bar-2026/', None, 'Dom 8 de noviembre', '2026-11-08', '2026-11-08', precio=35,
     artistas=['Gian Marco', 'Orquesta Bembé', 'María Grazia', 'Zaperoko', 'César Vega'])

# ---------------------------------------------------------------- La Noche de Barranco (Psje. Sánchez Carrión 199)
S = 'La Noche de Barranco'
for (t, g, sin, url, compra, h, d, d2, p, e, art, prod) in [
    ('Perros & Friends', ['rock'], 'Perros Santos reversionó su repertorio con varios invitados en una formación armada solo para esa noche.',
     'perros-friends-perros-santos-2026/', None, 'Jue 17 de septiembre', '2026-09-17', '2026-09-17', None, None,
     ['Perros Santos', 'Andrea Martínez', 'Draco', 'Ciané', 'Casimismo', 'Nero Lvigi', 'Lateral', 'Phat Buddha', 'Santos de Noche'], None),
    ('Campo de Almas: Un adiós', ['rock'], 'Una de las fechas de despedida de Campo de Almas tras más de tres décadas en los escenarios.',
     'campo-de-almas-un-adios-la-noche-de-barranco-setiembre-2026/', JN + 'concerts/lima-un-adios-campo-de-almas-ultimos-conciertos-76336',
     'Sáb 19 de septiembre', '2026-09-19', '2026-09-19', 100, 18, ['Campo de Almas'], None),
    ('Sueño Púrpura: Aniversario Souvenir', ['rock', 'independiente'], 'La banda tocó completo y por única vez su primer disco, Souvenir.',
     'sueno-purpura-aniversario-souvenir/', None, 'Jue 24 de septiembre', '2026-09-24', '2026-09-24', 15, None,
     ['Sueño Púrpura', 'Mauricio Moquillaza'], None),
    ('Laguna Pai: Noche de visiones', ['reggae'], 'Laguna Pai adelantó canciones de su próxima producción, con invitados.',
     'laguna-pai-noche-de-visiones/', 'https://www.passline.com/eventos/laguna-pai-presenta-noche-de-visiones',
     'Vie 25 de septiembre', '2026-09-25', '2026-09-25', 69, 18, ['Laguna Pai'], None),
    ('Gala Brie: Última parada', ['pop', 'independiente'], 'Cierre de la gira nacional de Gala Brie, que presentó su álbum Podría besar tu sombra con banda completa.',
     'gala-brie-la-noche-de-barranco-2026/', JN + 'concerts/lima-gala-brie-en-la-noche-de-barranco-ultima-parada-79259',
     'Jue 1 de octubre', '2026-10-01', '2026-10-01', 35, None, ['Gala Brie', 'Arantxa', 'Yo Soy Tú'], None),
    ('Autobús: Perdón x explotar', ['rock', 'pop'], 'Autobús estrenó en vivo un tema nuevo y repasó más de quince años de canciones con invitados.',
     'autobus-en-la-noche-de-barranco-2026/', None, 'Vie 2 de octubre', '2026-10-02', '2026-10-02', 50, 18, ['Autobús'], 'Pepa Entertainment'),
    ('Hyper Foco', ['pop'], 'Noche de pop con Geri The Boy, Negra Valencia y Any Uno.',
     'hyper-foco-en-lima-2026/', None, 'Mar 6 de octubre', '2026-10-06', '2026-10-06', 15, None, ['Geri The Boy', 'Negra Valencia', 'Any Uno'], None),
    ('Bareto', ['cumbia', 'fusión'], 'Show íntimo de Bareto con nuevo vocalista y estreno de canción.',
     'bareto-en-la-noche-de-barranco-2026/', None, 'Mié 7 de octubre', '2026-10-07', '2026-10-07', 70, 18, ['Bareto'], 'Inti Producciones'),
    ('San Hümi II', ['independiente'], 'Segunda edición de este encuentro de bandas emergentes.',
     'san-humi-ii-san-german-homi-homi-umi-murasaki/', None, 'Jue 8 de octubre', '2026-10-08', '2026-10-08', 10, 18,
     ['San Germán', 'Hömi Hömi', 'Umi Murasaki'], None),
    ('Amén: trío acústico', ['rock', 'acústico'], 'La banda Amén en formato de trío acústico, en dos fechas.',
     'amen-trio-acustico-en-barranco-2026/', None, 'Vie 9 de octubre y vie 13 de noviembre', '2026-10-09', '2026-11-13', None, None, ['Amén'], None),
    ('Loncheras de Perro y Santino Amigo', ['rock', 'independiente'], 'Debut en el local de Loncheras de Perro, banda de la nueva escena de Lima Norte, junto a Santino Amigo.',
     'loncheras-de-perro-en-la-noche-de-barranco-2026/', None, 'Jue 15 de octubre', '2026-10-15', '2026-10-15', 20, 18,
     ['Loncheras de Perro', 'Santino Amigo'], 'Festival Bizarro'),
    ('Zen', ['rock'], 'Zen repasó sus clásicos y adelantó temas de su nuevo disco.',
     'zen-en-la-noche-de-barranco-octubre-2026/', None, 'Vie 16 de octubre', '2026-10-16', '2026-10-16', 89, 18, ['Zen', 'Santos de Noche'], 'Tres Estrellas Booking'),
    ('Pelo Madueño', ['rock'], 'Una nueva fecha de Pelo Madueño y su banda, entre clásicos solistas, temas de La Liga del Sueño y canciones nuevas.',
     'pelo-madueno-en-la-noche-de-barranco-octubre-2026/', None, 'Sáb 17 de octubre', '2026-10-17', '2026-10-17', 75, 18, ['Pelo Madueño'], None),
    ('Daniel F: acústico', ['rock', 'acústico'], 'Concierto en formato acústico de Daniel F.',
     'daniel-f-en-la-noche-de-barranco-octubre-2026/', None, 'Vie 23 de octubre', '2026-10-23', '2026-10-23', None, None, ['Daniel F'], None),
    ('Que viva la criollada', ['rock', 'música criolla'], 'Julio Pérez y Más Poder presentaron un nuevo videoclip en una noche criolla con invitados.',
     'que-viva-la-criollada-2026/', JN + 'concerts/lima-que-viva-la-criollada-78995', 'Sáb 24 de octubre', '2026-10-24', '2026-10-24', 30, 18,
     ['Julio Pérez', 'Más Poder'], None),
    ('Cris en la Noche', ['pop', 'independiente'], 'Cristina Luyo se despidió en vivo de su primer disco, Histeria, y mostró material nuevo.',
     'cris-en-la-noche-cristina-luyo-2026/', None, 'Mar 27 de octubre', '2026-10-27', '2026-10-27', 39, 18, ['Cristina Luyo'], None),
    ('Greccia: Fiesta en el Castillo Greal', ['pop'], 'Greccia y su banda repasan sus canciones de debut y adelantan temas de su próximo disco.',
     'greccia-fiesta-en-el-castillo-greal/', None, 'Jue 29 de octubre', '2026-10-29', '2026-10-29', None, None, ['Greccia'], None),
    ('Gaia: La noche del hombre lobo', ['rock', 'música criolla'], 'Fecha de Halloween de Gaia, entre rock, música criolla y disfraces.',
     'gaia-la-noche-del-hombre-lobo/', None, 'Sáb 31 de octubre', '2026-10-31', '2026-10-31', 60, 18, ['Gaia'], None),
    ('Cecimonster vs Donka: Adult Violence', ['punk', 'independiente'], 'Presentación del nuevo EP del dúo, editado en vinilo, con bandas invitadas.',
     'cecimonster-vs-donka-adult-violence/', None, 'Vie 6 de noviembre', '2026-11-06', '2026-11-06', 25, None,
     ['Cecimonster vs Donka', 'Juan Gris', 'Novio', 'Sparx'], None),
    ('Elisa Tokeshi', ['pop', 'cantautor'], 'Último concierto del año de la cantautora, con canciones nuevas y temas que nunca tocó en vivo con banda.',
     'elisa-tokeshi-en-la-noche-2026/', None, 'Jue 12 de noviembre', '2026-11-12', '2026-11-12', 42, 18, ['Elisa Tokeshi', 'Lucy Pérez'], None),
    ('Alex Ferreira', ['pop', 'cantautor'], 'El cantautor dominicano llega a Lima con su gira 2026.',
     'alex-ferreira-en-lima-2026/', None, 'Mié 25 de noviembre', '2026-11-25', '2026-11-25', None, None, ['Alex Ferreira'], None),
]:
    obra(S, t, 'concierto', g, sin, 'prensa', CP + url, compra, h, d, d2, precio=p, edad=e, artistas=art, productora=prod)
obra(S, 'Cyclo: Fisherman Latam Tour 2026', 'concierto', ['electrónica'],
     'Fecha de la gira latinoamericana de Cyclo en el local de Barranco.',
     'passline', 'https://www.passline.com/venue/la-noche-de-barranco', 'https://www.passline.com/venue/la-noche-de-barranco',
     'Jue 19 de noviembre, 10 p. m.', '2026-11-19', '2026-11-19', artistas=['Cyclo'])

# ---------------------------------------------------------------- Sala Osma (Av. Pedro de Osma 203)
S = 'Sala Osma'
for (t, g, sin, url, compra, h, d, p, e, art, prod) in [
    ('Frágil: Serranío', ['rock progresivo'], 'Frágil tocó completo su álbum Serranío por un nuevo aniversario del disco.',
     'fragil-en-sala-osma-2026/', None, 'Jue 17 de septiembre', '2026-09-17', 65, None, ['Frágil'], None),
    ('Marzenit: RABIA', ['rock'], 'Presentación en vivo del disco debut de Marzenit, con un single nuevo e invitados.',
     'marzenit-rabia-sala-osma-2026/', JN + 'concerts/lima-marzenit-en-vivo-presenta-rabia-79318', 'Jue 8 de octubre', '2026-10-08', 0, 18, ['Marzenit'], None),
    ('WAN', ['indie rock'], 'Noche de indie rock con WAN y Mercury Toys como invitados.',
     'wan-en-sala-osma-2026/', None, 'Jue 15 de octubre', '2026-10-15', 25, 18, ['WAN', 'Mercury Toys'], 'We Represent Music'),
    ('Daniela De Izcue: Mi momento', ['pop', 'cantautor'], 'Lanzamiento en vivo del primer álbum de Daniela De Izcue, con banda completa y estreno del corto del disco.',
     'daniela-de-izcue-mi-momento-2026/', None, 'Jue 22 de octubre', '2026-10-22', None, None, ['Daniela De Izcue'], None),
    ('Gente Maravillosa', ['independiente'], 'Show gratuito de Gente Maravillosa con ¿Quién Ácido?, Oscar DLC y Gala Brie.',
     'gente-maravillosa-en-sala-osma-2026/', None, 'Jue 29 de octubre', '2026-10-29', 0, None,
     ['Gente Maravillosa', '¿Quién Ácido?', 'Oscar DLC', 'Gala Brie'], None),
]:
    obra(S, t, 'concierto', g, sin, 'prensa', CP + url, compra, h, d, d, precio=p, edad=e, artistas=art, productora=prod)

# ---------------------------------------------------------------- Sargento Pimienta (Av. Bolognesi 757)
S = 'Sargento Pimienta'
obra(S, 'Onda Vaga: Amuletos de cristal', 'concierto', ['rock', 'folk'],
     'La banda argentina presentó en Lima su nuevo disco junto a sus clásicos.',
     'prensa', CP + 'onda-vaga-amuletos-de-cristal-lima-2026/', JN + 'concerts/lima-onda-vaga-presenta-amuletos-de-cristal-en-lima-78389',
     'Jue 24 de septiembre', '2026-09-24', '2026-09-24', precio=80, artistas=['Onda Vaga'])
obra(S, 'El Plan de la Mariposa', 'concierto', ['rock'],
     'Regreso a Lima de la banda argentina con un recorrido por sus canciones más conocidas.',
     'prensa', CP + 'el-plan-de-la-mariposa-en-lima-2026/', JN + 'concerts/lima-el-plan-de-la-mariposa-en-lima-26-de-septiembre-77169',
     'Sáb 26 de septiembre', '2026-09-26', '2026-09-26', precio=129, edad=18, artistas=['El Plan de la Mariposa'])


# ---------------------------------------------------------------- validación y salida
def norm_titulo(t):
    t = unicodedata.normalize('NFKD', t.lower())
    t = ''.join(c for c in t if not unicodedata.combining(c))
    t = re.split(r'[:\-–(]', t)[0]
    return re.sub(r'[^a-z0-9]+', ' ', t).strip()


def main():
    cat = json.load(open(RAIZ / 'data' / 'catalogo.json'))
    salas_cat = {s['slug']: s['nombre'] for s in cat['salas']}
    existentes = {}
    # unir.py ya lee data/extraido/salas_barranco.json: se ignoran las obras del catálogo cuyas fuentes
    # salen todas de este mismo archivo (si no, la comparación se encontraría a sí misma).
    propias = {o['url'] for o in OBRAS}
    for o in cat['obras']:
        if all(f.get('url') in propias for f in o.get('fuentes', [])):
            continue
        for s in o.get('salas') or [o['sala']]:
            existentes.setdefault(salas_cat.get(s, s).lower(), set()).add(norm_titulo(o['titulo']))
    # "Roble de Barranco" y "El Roble De Barranco" son el mismo local en el catálogo
    roble = existentes.get('roble de barranco', set()) | existentes.get('el roble de barranco', set())
    existentes['roble de barranco'] = roble
    ids, salida = set(), []
    for o in OBRAS:
        assert o['id'] not in ids, o['id']
        ids.add(o['id'])
        if norm_titulo(o['titulo']) in existentes.get(o['sala'].lower(), set()):
            print('YA EN CATÁLOGO, se omite:', o['sala'], '|', o['titulo'])
            continue
        assert o['tipo'] in {'teatro', 'comedia', 'stand-up', 'musical', 'danza', 'opera', 'concierto', 'circo',
                             'infantil', 'folklore', 'show', 'otro'}, o['tipo']
        assert o['fuente'] in {'web de la sala', 'municipalidad', 'ministerio de cultura', 'prensa', 'teleticket',
                               'ticketmaster', 'passline'}
        assert o['temporada']['inicio'] <= o['temporada']['fin']
        assert o['temporada']['fin'] >= '2026-09-17', o['titulo']
        salida.append(o)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    json.dump(salida, open(SALIDA, 'w'), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(salida), 'obras ->', SALIDA)
    for s, n in Counter(o['sala'] for o in salida).most_common():
        print(f'  {n:3d}  {s}')


if __name__ == '__main__':
    main()
