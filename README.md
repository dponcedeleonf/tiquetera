# Tiquetera (nombre provisional)

Portal de artes escénicas (teatro, stand-up, danza, música en vivo y más) que reúne obras, funciones, salas y artistas en un solo lugar, con búsqueda inteligente, buen posicionamiento en buscadores y venta de entradas a bajo costo.

Empieza en Perú y luego se extiende a otros países.

## El problema

- La oferta está repartida en muchas tiqueteras, redes sociales y espacios. Para enterarse de algo hay que saber dónde buscar.
- Los eventos no están bien indexados en buscadores y las búsquedas no entienden preguntas naturales.
- Las tiqueteras existentes cobran tarifas que dejan fuera a los espectáculos pequeños.

## Qué construimos

### 1. Cartelera y directorio (el gancho)

- Registro de **obras/espectáculos**, **funciones** (fecha, hora, sala), **salas/espacios**, **personas** (actores, directores, etc.) y **productoras/compañías**.
- Las personas y las salas son entidades propias, no texto suelto. Así se puede preguntar "¿en qué otras obras está este actor?".
- **Búsqueda con IA**: "el martes estoy en Cusco, no quiero ir a fiestas, ¿qué hay?".
- **Servidor MCP** para que asistentes de IA consulten la cartelera.
- Publicar en la cartelera es gratis, aunque el espectáculo no venda entradas con nosotros.

### 2. Perfiles automáticos (tipo Linktree / Google Business)

- Cada actor, productora y sala tiene una página generada automáticamente a partir de los datos del portal.
- El dueño puede **reclamar** su perfil, completarlo y personalizarlo.
- Cada página está optimizada para SEO (datos estructurados de schema.org: `Event`, `Person`, `Place`, `TheaterEvent`…).

### 3. Tiquetera de bajo costo (el negocio principal)

- Venta de entradas con pasarela de pago y **liquidación rápida** al organizador.
- Operación automatizada con agentes de IA para mantener el costo operativo al mínimo.
- Tarifas accesibles para espectáculos pequeños, sin cobrar por cosas que aportan poco valor y que otras tiqueteras sí cobran.

### 4. Salas (futuro)

- Inventario y disponibilidad de espacios.
- Posibles líneas de negocio: llenar salas, reservar/bloquear fechas, productos financieros (por ejemplo, adelantos sobre ventas).

## Principios

- **Variedad**: que se sienta que está todo, de lo grande a lo pequeño.
- **Fácil**: buscar, publicar y comprar sin fricción.
- **Vibra positiva**: estética limpia, sin saturar de publicidad.
- **Recomendación honesta**: nada sube en el ranking porque alguien pagó. Se muestra lo que le interesa a cada persona.
- **SEO automático**: cada obra, sala, persona y ciudad posiciona sola.

## Preguntas abiertas

- **Carga de datos**: ¿registro propio de salas/productores, carga asistida por el equipo, importación desde otras fuentes, o una mezcla?
- **Eventos de otras tiqueteras**: ¿se listan con enlace externo desde el inicio y luego se incentiva vender con nosotros, o solo se listan los que venden aquí?
- **Modelo de tarifas**: ¿tarifa pública única, tramos según tamaño, postulación a tarifa reducida, tratos individuales?
- **Pasarela de pago** en Perú, costos por transacción, medios locales (tarjetas, Yape/Plin, etc.) y tiempos de liquidación.
- **Obligaciones legales y tributarias** de vender entradas en Perú (comprobantes electrónicos, libro de reclamaciones, etc.) y su costo operativo.
- **Equilibrio** entre el objetivo de promoción (artistas, comunidad) y el de negocio.
