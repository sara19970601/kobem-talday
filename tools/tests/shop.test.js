const { chromium } = require('playwright');
const ok = (c, m) => console.log((c ? 'PASS' : 'FAIL') + '  ' + m);
const focusId = sel => { const id = sel.replace(/^#lab-/, ''); return id.startsWith('tech-') ? 'techniques' : id.split('-')[0]; };
const isLabField = sel => /^#lab-/.test(sel) && !/^#lab-(consent|type)/.test(sel);
const goF = async (p, sel) => { if (isLabField(sel)) await p.evaluate(id => labFocusField(id), focusId(sel)); else if (/^#tb-/.test(sel)) await p.evaluate(() => setWorkOpen(true)); };
const F = async (p, sel, v) => { await goF(p, sel); await p.fill(sel, v); };
const IV = async (p, sel) => { await goF(p, sel); return p.inputValue(sel); };
const SO = async (p, sel, v) => { await goF(p, sel); return p.selectOption(sel, v); };
const CHK = async (p, sel) => { await goF(p, sel); return p.isChecked(sel); };
const MSG = {
  workbook: 'Сәлеметсіз бе! “Көркем шығарманы талдау” жұмыс дәптерінің word нұсқасын сатып алғым келеді. Бағасы мен Kaspi арқылы төлем жасау жолын жіберсеңіз.',
  guide: 'Сәлеметсіз бе! “Көркем шығарманы талдау” әдістемелік нұсқаулығының PDF нұсқасын сатып алғым келеді. Бағасы мен Kaspi арқылы төлем жасау жолын жіберсеңіз.',
};
(async () => {
  const url = process.argv[2], shots = process.argv[3];
  const b = await chromium.launch();
  for (const vp of [{ width: 1280, height: 860, name: 'desk' }, { width: 1000, height: 760, name: 'tablet' }, { width: 390, height: 844, name: 'phone' }, { width: 320, height: 640, name: 'p320' }]) {
    const ctx = await b.newContext({ viewport: vp });
    await ctx.addInitScript(() => { try { localStorage.setItem('kobem-talday:help-seen', '1'); localStorage.setItem('kobem-talday:cover-hidden', '1'); } catch (e) {} });
    const p = await ctx.newPage(); const errs = [], net = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    p.on('request', r => { if (!/^(file|data|blob):/.test(r.url())) net.push(r.url()); });
    await p.goto(url);
    const bar = await p.evaluate(() => { const r = s => document.querySelector(s).getBoundingClientRect();
      return { shopTop: Math.round(r('.shop-btn').top), helpTop: Math.round(r('.help-btn').top), brandTop: Math.round(r('.brand').top), tabsTop: Math.round(r('.tabs').top), ov: document.documentElement.scrollWidth - innerWidth }; });
    ok(bar.shopTop === bar.helpTop && bar.ov <= 0, vp.name + ' shop button beside help, no overflow ' + JSON.stringify(bar));
    await p.screenshot({ path: shots + '/shop-bar-' + vp.name + '.png', clip: { x: 0, y: 0, width: vp.width, height: 130 } });
    await p.click('.shop-btn');
    ok(await p.locator('.shop-card').count() === 2, vp.name + ' two product cards');
    for (const id of ['workbook', 'guide']) {
      const a = p.locator('#shop-' + id + ' a.wa-btn');
      const href = await a.getAttribute('href');
      const u = new URL(href);
      ok(u.origin + u.pathname === 'https://wa.me/77782633831' && u.searchParams.get('text') === MSG[id] && await a.getAttribute('target') === '_blank',
        vp.name + ' ' + id + ' link opens WhatsApp with its message');
      ok((await p.textContent('#shop-' + id + ' .shop-price')).replace(/\s/g, '') === '3000теңге' && (await a.textContent()) === 'WhatsApp арқылы сатып алу', vp.name + ' ' + id + ' price and label');
    }
    ok((await p.textContent('.shop-how')).includes('Төлем расталған соң PDF нұсқасы сізге жіберіледі.'), vp.name + ' order steps text');
    ok(await p.locator('a[href$=".pdf"], a[download]').count() === 0, vp.name + ' no PDF download links');
    const dov = await p.evaluate(() => { const d = document.querySelector('.dlg'); return [d.scrollWidth - d.clientWidth, document.documentElement.scrollWidth - innerWidth]; });
    ok(dov[0] <= 0 && dov[1] <= 0, vp.name + ' dialog fits ' + dov);
    await p.screenshot({ path: shots + '/shop-' + vp.name + '.png' });
    if (vp.name === 'phone') { await p.locator('.shop-how').scrollIntoViewIfNeeded(); await p.screenshot({ path: shots + '/shop-phone-2.png' }); }
    // clicking opens a new tab to wa.me (blocked network → just check popup URL)
    if (vp.name === 'desk') {
      await ctx.route('https://wa.me/**', r => r.fulfill({ status: 200, body: 'ok' }));
      const [pop] = await Promise.all([p.waitForEvent('popup'), p.click('#shop-guide a.wa-btn')]);
      ok(pop.url().startsWith('https://wa.me/77782633831?text='), 'click opens wa.me in a new tab');
      await pop.close();
    }
    await p.keyboard.press('Escape');
    ok(await p.locator('.dlg').count() === 0, vp.name + ' Esc closes');
    // other tabs still fine
    for (const tab of ['library', 'book', 'glossary', 'kids']) await p.click('#tab-' + tab);
    ok(await p.locator('.k-card').count() === 38, vp.name + ' tabs still work');
    ok(!errs.length, vp.name + ' no errors ' + JSON.stringify(errs));
    ok(!net.filter(x => !x.startsWith('https://wa.me/')).length, vp.name + ' no network on load ' + JSON.stringify(net));
    await ctx.close();
  }
  // #duken link and cover button
  const ctx = await b.newContext({ viewport: { width: 1280, height: 860 } });
  const p = await ctx.newPage();
  await p.goto(url + '#duken');
  ok(await p.locator('.shop-card').count() === 2 && await p.locator('.cover').count() === 0, '#duken opens the shop directly');
  await p.keyboard.press('Escape');
  await p.goto(url.replace(/#.*/, '') + '?x=1');
  await p.click('.cover-actions >> text=Электронды нұсқасын сатып алу');
  ok(await p.locator('.shop-card').count() === 2, 'cover button opens the shop');
  await p.screenshot({ path: shots + '/shop-from-cover.png' });
  await b.close();
})();
