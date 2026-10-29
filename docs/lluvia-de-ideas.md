# Lluvia de ideas

Ideas en bruto para trabajar. Nada de esto está decidido todavía.

## 1. Estrategia central: ganar por la venta, no por el catálogo

- Un catálogo abierto beneficia a todos: Google, ChatGPT o Claude lo leen y mandan a la gente a comprar donde sea. Esconder links no sirve, porque un agente los encuentra al toque.
- **El catálogo es marketing, no el negocio.** El negocio es ser el sistema con el que el productor vende sus entradas, en todas partes: su bio de Instagram, su web, WhatsApp, los agentes de IA. Si la obra vende con nosotros, el "link directo" que pasa un agente es nuestro checkout (lógica tipo Shopify, no tipo marketplace).
- Obras que venden en otro lado: se listan igual (nombre, fecha, sala, link), porque traen tráfico y alimentan los perfiles, pero sin invertir en ellas. La experiencia rica queda solo para las que venden con nosotros.
- Enfocar todo en las nuevas formas de comprar (agentes de IA, WhatsApp) desde el principio.

## 2. Punto de entrada: quien hoy no tiene tiquetera

- Muchas obras pequeñas y medianas venden por Yape, mensaje directo y validación manual de capturas. Para ellas no hay costo de cambio: les reemplazamos el caos.
- Medianos, grandes y salas consolidadas vienen después, con casos de éxito.
- **Sala piloto** de la red de contactos: una temporada "a costo" (sin nuestro margen; la pasarela se cubre igual), a cambio de ser el caso de éxito. Se le puede compensar con cosas que nos cuestan poco: promoción con IA, reportes, perfil destacado (en su perfil, nunca en el ranking general).

## 3. Beneficios para el productor (que existan solo si vende con nosotros)

- **Público nuevo, demostrado**: "45 de tus 120 entradas las compró gente que te encontró aquí".
  - Idea de tarifa: cobrar menos por las ventas que trae el propio productor y más por las que traemos nosotros. Hay que diseñarlo para que la atribución no se pueda manipular.
- **Seguidores**: la gente sigue a actores, compañías y salas, y recibe aviso de la próxima obra. El productor construye una audiencia propia que no se pierde entre temporadas.
- **Butacas de último minuto**: ofrecer las entradas que van a quedar vacías, con descuento, a quienes buscan algo para esa noche. Beneficio medible: "recuperaste S/ 600".
- **Promoción con IA**: piezas para Instagram, nota de prensa, página del espectáculo, link para la bio.
- **Liquidez rápida**, y más adelante adelantos sobre la preventa.
- **Datos de su público**, con consentimiento.
- **Para actores**: perfil/portafolio automático que puede funcionar como herramienta de casting.
- **Para salas**: calendario visible, estadísticas de ocupación, contacto con producciones que buscan sala.

## 4. Beneficios para el público (que prefiera comprar aquí)

- Una cuenta con el pago guardado: comprar en un clic.
- Todas las entradas en un solo lugar, con recordatorios.
- Seguir artistas y salas.
- Cargo por servicio transparente y menor al de las tiqueteras grandes.
- Desglose visible: cuánto va a la obra, cuánto a la pasarela, cuánto a nosotros.

## 5. Agentes de IA como canal de venta

- Solo de las obras que venden con nosotros tenemos **disponibilidad y precio en tiempo real**: el agente puede decir "quedan 12 entradas, ¿te compro 2?". De las externas solo puede decir "existe, búscala en tal sitio".
- Servidor MCP que permita **comprar dentro de la conversación**, no solo buscar.
- Revisar los protocolos de compra por agentes (OpenAI + Stripe, Google) y si funcionan con pasarelas que operan en Perú. Stripe, hasta donde sabemos, no da cuentas a comercios peruanos.

## 6. Agente de WhatsApp

- Comprar sin entrar a la página: buscar, elegir función, pagar y recibir la entrada en el chat.
- **Pago dentro de WhatsApp**: hasta donde se pudo averiguar, no está disponible en Perú (solo India y Brasil). Alternativa: el agente manda un link de pago y la entrada llega al chat apenas se confirma.
- **Costos** (a confirmar con la tabla oficial de Meta; las fuentes no coinciden):
  - Meta cobra por mensaje según el país del cliente. Para Perú, las fuentes dan ~USD 0,02–0,03 por mensaje de utilidad (por ejemplo, el envío de la entrada) y ~USD 0,045–0,07 por mensaje de marketing.
  - Las respuestas dentro de una conversación que inicia el cliente eran gratis desde noviembre de 2024, pero una fuente dice que se empiezan a cobrar desde el 1 de octubre de 2026. Hay que confirmarlo, porque cambia mucho el costo de un agente conversacional.
  - Si se usa un proveedor intermediario (BSP), suma un recargo y una cuota mensual. Conectarse directo a la API de Meta lo evita.
  - Más el costo del modelo de IA por conversación.
  - Objetivo: estimar el costo por venta completa por WhatsApp y que quepa dentro del cargo por transacción.
- No usar mensajes de marketing masivos, para mantener costo bajo y vibra no invasiva.

## 7. Sombrero virtual

- Al pagar: "¿Quieres dejar algo para la producción? S/ 2 · S/ 5 · otro monto", como la propina en Rappi.
- Va en la misma transacción: no suma el cargo fijo de la pasarela, solo el porcentaje.
- También para funciones gratuitas o "a la gorra": QR o link de sombrero aunque no vendan entradas.
- Puede repartirse automáticamente entre elenco y técnicos.
- Es la capa solidaria del proyecto. Revisar tratamiento tributario para quien lo recibe.

## 8. Las salas como canal de distribución

- Las salas alquilan su espacio a muchas producciones. Si la sala recomienda o exige nuestra tiquetera, cada producción que entra a la sala entra a la plataforma.
- Incentivos para la sala:
  - Una pequeña comisión por cada producción que da de alta.
  - **Resolverle un problema administrativo crítico**, como el borderó (ver abajo).
  - Que el dinero le llegue rápido.
- Alta de una producción en minutos, iniciada por la sala.

## 9. Problemas colaterales que podemos resolver (más allá de las entradas)

> Prioridad baja: guardadas, pero con poca fe por ahora. Observaciones:
> - Quien recibe la plata quiere control financiero y no repartirla en el momento. Alternativa: calcular el borderó y entregar el reporte, sin repartir el dinero.
> - Facturación: verificar que la boleta se emita al instante de la compra y quién es el emisor (si nosotros vendemos por cuenta propia, podríamos cargar con el IGV de toda la entrada; ver con un contador).

Para salas:

- **Borderó automático**: el reparto de taquilla entre sala y compañía (por ejemplo, 60/40) calculado y pagado solo, con pagos divididos para que cada uno reciba su parte directo.
- **Calendario y alquiler de sala**: disponibilidad, reservas, contratos de alquiler.
- **Venta de consumos** en el mismo pedido (bebida, snack para el intermedio). Ingreso extra para la sala.
- **Control de acceso** con el celular.

Para productores:

- **Comprobantes electrónicos**: muchos productores pequeños son informales y no pueden emitir boletas. Explorar si podemos resolverlo (implicancias tributarias a evaluar con un contador).
- **Trámites**: calificación del espectáculo como cultural ante el Ministerio de Cultura (puede incidir en impuestos municipales), derechos de autor de música, permisos municipales. Asistidos por IA. A verificar qué aplica a cada caso.
- **Pago a elenco y técnicos**: repartir automáticamente lo recaudado.
- **Prensa**: kit de prensa, invitaciones a críticos y medios, gestión de cortesías.
- **Convocatorias y fondos**: avisos de fondos concursables y estímulos económicos, con ayuda de IA para postular. Encaja con la visión solidaria.
- **Encuestas y reseñas** después de la función.
- **Reporte de ventas** listo para la contabilidad.

## 10. Costos y tarifas

- El cargo al comprador es **por transacción**, no por entrada.
- **Esquema propuesto:** el comprador paga un cargo fijo por pedido (≈ S/ 1–1,50) que cubre el monto fijo de la pasarela y nuestro margen; un sol por transacción no le molesta a nadie. El productor paga solo un porcentaje bajo (pasarela + margen chico). Así, para elegir pasarela importan el porcentaje (sobre todo en Yape/Plin), el plazo de abono, los pagos divididos y el respaldo antifraude, no el monto fijo.
- Izipay (fuentes no oficiales): tarjeta peruana 3,44% + IGV, extranjera 3,95% + IGV, Yape/Plin ~1,5% (por confirmar). Yape Empresas cobra 2,95% desde abril de 2024. Pedir cotización formal a Izipay, Culqi y Niubiz.
- La única cosa que no desaparece es la pasarela. Mercado Pago, según fuentes no oficiales: ~3,49% + S/ 1,00 + IGV con cobro inmediato, ~3,29% + S/ 1,00 + IGV a 14 días. Confirmar en su panel y cotizar Culqi, Izipay, Niubiz.
- Yape/Plin no es gratis: sin validación automática es trabajo manual y riesgo; con validación, cuesta parecido a la tarjeta.
- Fraude y contracargos: estándar de mercado, no se ahorra ahí.
- Componentes del costo por pedido: pasarela, IGV sobre la comisión, comprobante electrónico, servidores e IA, reserva para fraude, devoluciones (la pasarela muchas veces no devuelve su comisión), margen propio (ej. S/ 0,50 + un % chico).
- Si el cargo lo paga el comprador, la pasarela también cobra sobre el cargo: hay que calcularlo "hacia arriba".
- Lo que no hace falta cargar: adelantos y devoluciones de comisión para ganar exclusividades, puntos de venta físicos, infraestructura para megaconciertos.
- Pendiente: calculadora de costos por transacción comparando pasarelas y plazos.

## 11. Por qué tienen éxito algunas tiqueteras

- **Joinnus (Perú)**: ganó la venta de un partido de la selección después de que Teleticket colapsara en el repechaje (servidor caído, colas, crisis en redes). Lección: la confiabilidad en el momento de mayor demanda es reputación; una caída mata la marca.
- **Eventbrite, Sympla (Brasil), Passline (Chile)**: autoservicio para cualquier organizador y gratis para eventos gratuitos. Cada asistente ve la marca y luego organiza su propio evento con ella. Crecen por la cola larga.
- **DICE (Reino Unido)**: empezó como guía de conciertos (descubrimiento) y después vendió entradas. Precio final sin sorpresas, entradas solo en la app (anti-reventa), descubrimiento personalizado. Su público fiel es lo que convence a las salas. Crítica: el organizador no se queda con los datos de su público.
- **Fever**: usa los datos de lo que la gente busca para crear y programar experiencias propias (como los conciertos Candlelight) en espacios poco usados. Compró DICE en 2025. Analogía directa con "llenar salas".
- **Tiqueteras grandes (Teleticket, Ticketmaster)**: exclusivas con grandes promotores y alianzas con bancos y marcas (preventas para clientes de un banco).

Ideas que salen de esto:

- Infraestructura que no se caiga, sobre todo en preventas.
- Gratis para eventos gratuitos y "a la gorra": crecimiento por la cola larga y la capa solidaria.
- Precio final transparente desde el primer vistazo.
- A diferencia de DICE, el productor sí se queda con los datos de su público (diferenciador).
- **Datos de demanda como producto**: lo que la gente busca y no encuentra ("martes en Cusco, algo tranquilo") le dice a salas y productores qué programar y dónde. Base para el negocio futuro de llenar salas.
- **Alianzas con marcas y bancos** que financien descuentos o preventas: plata para el productor que hoy no tiene acceso a eso.

## 12. Pendientes

- Entender mejor a productores y salas: conversaciones con 5 a 10 de la red de contactos.
- Prototipo para convencer a la socia, enfocado en el productor: publicar en 2 minutos pegando el afiche, compra en un clic, ventas en tiempo real, aviso a seguidores, sombrero virtual.
- Definir stack (propuesta: Next.js + PostgreSQL + Claude).
