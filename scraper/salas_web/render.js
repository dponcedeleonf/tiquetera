// Uso: node render.js <url> [espera_ms]  -> imprime el HTML renderizado
const { chromium } = require('playwright');
(async () => {
  const url = process.argv[2];
  if (/joinnus\.com|entradas\.laplaza\.com\.pe/i.test(url)) { console.error('joinnus prohibido'); process.exit(2); }
  const espera = parseInt(process.argv[3] || '3000', 10);
  const browser = await chromium.launch();
  const page = await browser.newPage({ userAgent: 'Mozilla/5.0 (prototipo tiquetera; recoleccion lenta de cartelera)' });
  // No dejar que la página pida nada a joinnus
  await page.route(/joinnus\.com|entradas\.laplaza\.com\.pe/i, r => r.abort());
  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(espera);
    process.stdout.write(await page.content());
  } catch (e) { console.error(String(e)); process.exitCode = 1; }
  await browser.close();
})();
