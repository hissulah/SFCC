const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  const reportPath = `file://${path.resolve('report/index.html')}`;
  await page.goto(reportPath, { waitUntil: 'networkidle0' });

  await page.pdf({
    path: 'results/report.pdf',
    format: 'A4',
    printBackground: true
  });

  await browser.close();
})();
