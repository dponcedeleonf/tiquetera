// Renderiza una lista de URLs (una por línea en un archivo) con un solo navegador.
// Uso: node render_lote.js <archivo_urls> <dir_salida> [espera_ms]
// Guarda <slug>.txt y <slug>.links.json. Pausa >= 1,5 s entre peticiones (máx. 1 req/s por sitio).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const slugify = u => u.replace(/^https?:\/\//, '').replace(/[^a-zA-Z0-9]+/g, '_').slice(0, 150);

(async () => {
  const [listFile, outDir, waitMs] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const urls = fs.readFileSync(listFile, 'utf8').split('\n').map(s => s.trim()).filter(Boolean);
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy });
  const ctx = await browser.newContext({ locale: 'es-PE' });
  const page = await ctx.newPage();
  for (const url of urls) {
    const out = path.join(outDir, slugify(url));
    if (fs.existsSync(out + '.txt')) { console.log('ya existe', url); continue; }
    try {
      const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(parseInt(waitMs || '4000', 10));
      for (let i = 0; i < 4; i++) { await page.mouse.wheel(0, 3000); await page.waitForTimeout(400); }
      const text = await page.evaluate(() => document.body.innerText);
      const links = await page.evaluate(() =>
        Array.from(document.querySelectorAll('a[href]')).map(a => [a.innerText.trim().slice(0, 80), a.href]));
      const meta = await page.evaluate(() => {
        const m = {};
        document.querySelectorAll('meta[property^="og:"], meta[name="description"]').forEach(e => {
          m[e.getAttribute('property') || e.getAttribute('name')] = e.getAttribute('content');
        });
        m.jsonld = Array.from(document.querySelectorAll('script[type="application/ld+json"]')).map(s => s.textContent);
        return m;
      });
      fs.writeFileSync(out + '.txt', url + '\n\n' + text);
      fs.writeFileSync(out + '.links.json', JSON.stringify({ url, meta, links }, null, 1));
      console.log(resp ? resp.status() : '-', url, text.length);
    } catch (e) {
      console.log('ERROR', url, e.message.split('\n')[0]);
    }
    await page.waitForTimeout(1500);
  }
  await browser.close();
})();
