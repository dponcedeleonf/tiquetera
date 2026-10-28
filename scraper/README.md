# Recolección de datos para el prototipo

Datos reales de cartelera para el demo privado. No publicar estos datos ni las imágenes de terceros.

Fuentes:
- **Teleticket**: listado `/todos` y páginas de evento (funciones, precios, descripción).
- **Ticketmaster Perú**: páginas de evento (JSON-LD `Event` + texto).
- **Joinnus**: no se usa. Su `robots.txt` bloquea explícitamente a los bots de IA.

Pasos:
1. `python3 parse_tt_listing.py raw/tt_todos.html > raw/tt_listing.json` (con `raw/tt_todos.html` descargado de https://teleticket.com.pe/todos)
2. `python3 fetch_tt.py` y `python3 fetch_tm.py`: descargan las páginas, 1 petición por segundo.
3. `python3 parse_tt.py` y `python3 parse_tm.py` → `data/teleticket.json`, `data/ticketmaster.json`
4. `python3 armar_lotes.py` → `data/lotes/`, entrada para la extracción con IA (elenco, ficha, género, sinopsis).

`data/salas.json`: salas principales de Lima, Cusco, Arequipa y Trujillo, investigadas a mano con IA.
