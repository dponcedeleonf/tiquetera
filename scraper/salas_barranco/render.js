// Renderiza páginas que arman su contenido con JavaScript y guarda HTML + texto visible.
// Uso: node render.js <url> <salida_sin_extension> [espera_ms]
// Respeta 1 petición/segundo por sitio desde el script que lo llama (se usa de a una URL).
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const [url, out, waitMs] = process.argv.slice(2);
  const proxy = process.env.HTTPS_PROXY ? { server: process.env.HTTPS_PROXY } : undefined;
  const browser = await chromium.launch({ proxy });
  const ctx = await browser.newContext({ ignoreHTTPSErrors: false, locale: 'es-PE' });
  const page = await ctx.newPage();
  const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(parseInt(waitMs || '5000', 10));
  // scroll para cargar contenido perezoso
  for (let i = 0; i < 6; i++) {
    await page.mouse.wheel(0, 3000);
    await page.waitForTimeout(500);
  }
  const html = await page.content();
  const text = await page.evaluate(() => document.body.innerText);
  const links = await page.evaluate(() =>
    Array.from(document.querySelectorAll('a[href]')).map(a => [a.innerText.trim().slice(0, 80), a.href])
  );
  fs.writeFileSync(out + '.html', html);
  fs.writeFileSync(out + '.txt', text);
  fs.writeFileSync(out + '.links.json', JSON.stringify(links, null, 1));
  console.log(resp ? resp.status() : 'sin respuesta', url, text.length, 'chars');
  await browser.close();
})().catch(e => { console.error('ERROR', e.message); process.exit(1); });
