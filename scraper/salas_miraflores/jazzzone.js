// Jazz Zone: para cada fecha de la programación mensual dispara el evento 'open-modal-events'
// (lo mismo que hace el clic) y lee el texto del modal EventsModal que carga Livewire.
// uso: node jazzzone.js > ../raw/salas_miraflores/jazzzone_modales.json
const { chromium } = require('playwright');
const espera = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  await p.route('**/*', r => /joinnus\.com|facebook\.com|instagram\.com/.test(r.request().url()) ? r.abort() : r.continue());
  await p.goto('https://www.jazzzoneperu.com/', { waitUntil: 'networkidle', timeout: 90000 });
  const fechas = await p.$$eval('#programacion-mensual div[x-on\\:click]', els => [...new Set(els.map(e => (e.getAttribute('x-on:click').match(/date: '([\d-]+)'/) || [])[1]).filter(Boolean))]);
  const extra = (process.argv[2] || '').split(',').filter(Boolean);
  for (const e of extra) if (!fechas.includes(e)) fechas.push(e);
  const salida = [];
  let previo = '';
  for (const f of fechas) {
    await p.evaluate(d => window.dispatchEvent(new CustomEvent('open-modal-events', { detail: { date: d } })), f);
    let txt = '';
    for (let k = 0; k < 12; k++) {          // espera hasta que el contenido cambie (máx ~6 s)
      await espera(500);
      txt = await p.evaluate(() => { const m = document.querySelector('[x-data="EventsModal"]'); return m ? m.innerText + '\n@@LINKS ' + [...m.querySelectorAll('a')].map(a => a.href).join(' ') : ''; });
      if (txt && txt !== previo) break;
    }
    previo = txt;
    salida.push({ fecha: f, texto: txt.slice(0, 6000) });
    await espera(1200);                      // ritmo pausado hacia el servidor
  }
  process.stdout.write(JSON.stringify(salida, null, 1));
  await b.close();
})();
