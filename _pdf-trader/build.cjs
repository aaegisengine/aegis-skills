const { chromium } = require('D:/Aegis/Aegis/node_modules/playwright');
const path = require('path');
const fs = require('fs');

const SRC = path.join(__dirname, 'guia.html');
const OUT_PDF = path.join(__dirname, 'AEGIS-SKILLS-Trader-30-Prompts.pdf');
const SHOTS = path.join(__dirname, '_preview');
fs.mkdirSync(SHOTS, { recursive: true });

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 816, height: 1056 }, deviceScaleFactor: 2 });
  await page.goto('file:///' + SRC.replace(/\\/g, '/'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);

  const pages = await page.$$('.page');
  console.log('paginas:', pages.length);
  for (let i = 0; i < pages.length; i++) {
    await pages[i].screenshot({ path: path.join(SHOTS, `pg-${String(i + 1).padStart(2, '0')}.png`) });
  }

  await page.pdf({
    path: OUT_PDF,
    width: '816px',
    height: '1056px',
    printBackground: true,
    margin: { top: 0, bottom: 0, left: 0, right: 0 },
  });
  await browser.close();
  const kb = (fs.statSync(OUT_PDF).size / 1024 / 1024).toFixed(1);
  console.log('pdf:', OUT_PDF, kb + 'mb');
})().catch((e) => { console.error(e); process.exit(1); });
