// node render.js URL [espera_ms] -> HTML renderizado por stdout
const { chromium } = require('playwright');
(async () => {
  const [url, espera] = [process.argv[2], parseInt(process.argv[3] || '4000')];
  const b = await chromium.launch();
  const p = await b.newPage({ userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36' });
  await p.route('**/*', r => { const u = r.request().url(); if (/joinnus\.com|entradas\.laplaza\.com\.pe|facebook\.com|instagram\.com/.test(u)) return r.abort(); return r.continue(); });
  try { await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 }); } catch (e) {}
  await p.waitForTimeout(espera);
  process.stdout.write(await p.content());
  await b.close();
})();
