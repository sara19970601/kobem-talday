const { chromium } = require('playwright');
const ok = (c, m) => console.log((c ? 'PASS' : 'FAIL') + '  ' + m);
const focusId = sel => { const id = sel.replace(/^#lab-/, ''); return id.startsWith('tech-') ? 'techniques' : id.split('-')[0]; };
const isLabField = sel => /^#lab-/.test(sel) && !/^#lab-(consent|type)/.test(sel);
const goF = async (p, sel) => { if (isLabField(sel)) await p.evaluate(id => labFocusField(id), focusId(sel)); else if (/^#tb-/.test(sel)) await p.evaluate(() => setWorkOpen(true)); };
const F = async (p, sel, v) => { await goF(p, sel); await p.fill(sel, v); };
const IV = async (p, sel) => { await goF(p, sel); return p.inputValue(sel); };
const SO = async (p, sel, v) => { await goF(p, sel); return p.selectOption(sel, v); };
const CHK = async (p, sel) => { await goF(p, sel); return p.isChecked(sel); };
(async () => {
  const url = process.argv[2], shots = process.argv[3];
  const b = await chromium.launch();
  for (const vp of [{ width: 1280, height: 860, name: 'desk' }, { width: 375, height: 760, name: 'phone' }]) {
    const ctx = await b.newContext({ viewport: vp });
    await ctx.addInitScript(() => { try { localStorage.setItem('kobem-talday:help-seen', '1'); localStorage.setItem('kobem-talday:cover-hidden', '1'); } catch (e) {} });
    const p = await ctx.newPage(); const errs = []; const net = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    p.on('request', r => { if (!r.url().startsWith('file:') && !r.url().startsWith('data:') && !r.url().startsWith('blob:')) net.push(r.url()); });
    await p.goto(url);
    ok(await p.locator('.tab').count() === 5, vp.name + ' 5 tabs');
    await p.click('#tab-glossary');
    ok(await p.locator('.gl-item').count() === 63, vp.name + ' 63 terms shown');
    ok(await p.locator('.gl-sec').count() === 6, vp.name + ' 6 sections');
    const dramaDef = await p.locator('.gl-item').filter({ has: p.locator('dt', { hasText: /^Драма$/ }) }).locator('dd').textContent();
    ok(dramaDef.startsWith('Кең мағынада — диалог'), vp.name + ' Драма definition keeps inner dash');
    await p.evaluate(() => document.getElementById('main').scrollTop = 99999);
    const ov = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
    ok(ov <= 0, vp.name + ' no horizontal overflow (' + ov + ')');
    const tabsTrunc = await p.evaluate(() => [...document.querySelectorAll('.tab')].filter(t => t.scrollWidth > t.clientWidth).map(t => t.textContent));
    ok(!tabsTrunc.length, vp.name + ' tab labels fit: ' + JSON.stringify(tabsTrunc));
    await p.screenshot({ path: shots + '/gl-' + vp.name + '.png' });
    if (vp.name === 'phone') await p.click('.nav-toggle');
    await p.fill('#gloss-search', 'ХРОНОТОП');
    ok(await p.locator('.gl-item').count() >= 1 && await p.locator('.gl-item mark').count() >= 1, vp.name + ' case-insensitive search + highlight (' + await p.textContent('#gloss-results') + ')');
    ok(await p.evaluate(() => document.activeElement.id) === 'gloss-search', vp.name + ' search keeps focus');
    await p.fill('#gloss-search', 'бахтин');
    ok(await p.locator('.gl-item').count() === 1, vp.name + ' search in definitions');
    await p.fill('#gloss-search', 'жжжж');
    ok(await p.locator('.gl-empty').count() === 1, vp.name + ' empty result message');
    await p.fill('#gloss-search', '');
    await p.click('#gloss-nav li:nth-child(5) button');
    await p.waitForTimeout(200);
    const top = await p.evaluate(() => document.getElementById('gl-V').getBoundingClientRect().top);
    ok(top < 320, vp.name + ' section nav scrolls to V (' + Math.round(top) + ')');
    if (vp.name === 'phone') await p.screenshot({ path: shots + '/gl-phone-V.png' });
    // reload keeps the tab
    await p.waitForTimeout(800); await p.reload();
    ok(await p.getAttribute('#tab-glossary', 'aria-selected') === 'true', vp.name + ' reload stays on Сөздік');
    // print
    await p.evaluate(() => buildPrintArea(defaultPrintTarget()));
    ok(await p.locator('#print-area dt').count() === 63, vp.name + ' print area has all 63 terms');
    if (vp.name === 'desk') {
      await p.emulateMedia({ media: 'print' });
      await p.pdf({ path: shots + '/gl.pdf', format: 'A4' });
      await p.emulateMedia({ media: 'screen' });
      await p.click('.brand'); await p.waitForTimeout(300);
      ok((await p.textContent('.cover-feats')).includes('63 термин'), 'cover lists glossary');
    }
    ok(!errs.length, vp.name + ' no errors ' + JSON.stringify(errs));
    ok(!net.length, vp.name + ' no network ' + JSON.stringify(net));
    await ctx.close();
  }
  await b.close();
})();
