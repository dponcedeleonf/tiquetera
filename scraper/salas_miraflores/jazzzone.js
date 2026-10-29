// Jazz Zone: hace clic en cada día de la programación mensual y guarda el texto del modal que aparece.
// uso: node jazzzone.js > ../raw/salas_miraflores/jazzzone_modales.json
const { chromium } = require('playwright');
const espera = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1400, height: 1000 } });
  await p.route('**/*', r => /joinnus\.com|facebook\.com|instagram\.com/.test(r.request().url()) ? r.abort() : r.continue());
  await p.goto('https://www.jazzzoneperu.com/', { waitUntil: 'networkidle', timeout: 90000 });
  const base = await p.evaluate(() => document.body.innerText);
  const salida = [];
  const n = await p.locator('#programacion-mensual div[x-on\\:click]').count();
  for (let i = 0; i < n; i++) {
    const el = p.locator('#programacion-mensual div[x-on\\:click]').nth(i);
    const attr = await el.getAttribute('x-on:click');
    const f = (attr.match(/date: '([\d-]+)'/) || [])[1];
    if (!(await el.isVisible())) { const mas = p.locator('text=CARGAR MAS EVENTOS'); if (await mas.isVisible()) { await mas.click(); await espera(1500); } }
    try { await el.scrollIntoViewIfNeeded(); await el.click({ timeout: 5000 }); } catch (e) { salida.push({ fecha: f, error: String(e).slice(0, 100) }); continue; }
    await espera(2500);
    const txt = await p.evaluate(() => document.body.innerText);
    // texto nuevo respecto a la página base
    const nuevas = txt.split('\n').filter(l => l.trim() && !base.includes(l.trim()));
    salida.push({ fecha: f, texto: nuevas.join('\n').slice(0, 5000) });
    await p.keyboard.press('Escape'); await espera(600);
    const cerrar = p.locator('[x-on\\:click*="close"], button:has-text("×"), button:has-text("Cerrar")').first();
    try { if (await cerrar.isVisible()) await cerrar.click({ timeout: 2000 }); } catch (e) {}
    await espera(400);
  }
  process.stdout.write(JSON.stringify(salida, null, 1));
  await b.close();
})();
