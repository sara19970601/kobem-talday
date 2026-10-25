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
  for (const vp of [{ width: 1280, height: 860, name: 'desk' }, { width: 390, height: 844, name: 'phone' }]) {
    const ctx = await b.newContext({ viewport: vp });
    await ctx.addInitScript(() => { try { localStorage.setItem('kobem-talday:help-seen', '1'); localStorage.setItem('kobem-talday:cover-hidden', '1'); } catch (e) {} });
    const p = await ctx.newPage(); const errs = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.goto(url);
    // sheet 1 → «Нұсқаулық: 2.1 →»
    await p.click('.ws-guide-tip summary'); await p.evaluate(() => openGuide('2.1'));
    ok(await p.evaluate(() => state.ui.tab === 'guide') && (await p.textContent('.ws-title')).startsWith('2.1'), vp.name + ' sheet button opens 2.1');
    ok((await p.textContent('.g-tip')).includes('Алғашқы әсер') && await p.locator('.g-body').count() === 0, vp.name + ' 2.1 shows the short tip, no full text');
    ok((await p.textContent('.g-locked')).includes('Толық нұсқасы PDF-те'), vp.name + ' «Толық нұсқасы PDF-те» shown');
    await p.screenshot({ path: shots + '/pv-tip-' + vp.name + '.png' });
    await p.click('.g-locked button');
    ok(await p.locator('.shop-card').count() === 2, vp.name + ' «Сатып алу» opens the shop');
    await p.keyboard.press('Escape');
    await p.click('#back-to-book');
    ok(await p.getAttribute('#tab-book', 'aria-selected') === 'true' && (await p.textContent('.ws-title')) === 'Шығарманы алғашқы оқу', vp.name + ' «Дәптерге оралу» returns to the sheet');
    // free sections
    await p.evaluate(() => switchTab('guide'));
    await p.evaluate(() => showGuideSection('1'));
    ok(await p.locator('.g-body p').count() > 5 && await p.locator('.g-locked').count() === 0, vp.name + ' chapter 1 is full and open');
    await p.evaluate(() => showGuideSection('pre'));
    ok(await p.locator('.g-body p').count() > 3 && await p.locator('.g-locked').count() === 0, vp.name + ' lead-in is full and open');
    // locked without tip
    await p.evaluate(() => showGuideSection('16'));
    ok(await p.locator('.g-tip').count() === 0 && await p.locator('.g-locked').count() === 1, vp.name + ' chapter 16: lock card only');
    if (vp.name === 'desk') {
      ok(await p.locator('#guide-nav-list .g-pdf').count() === 47, 'nav marks the 47 locked sections with PDF');
      await p.screenshot({ path: shots + '/pv-nav.png' });
      await p.fill('#guide-search', 'хронотоп');
      ok((await p.textContent('#guide-results')).length > 0 && await p.locator('#main mark').count() > 0, 'search still works: ' + await p.textContent('#guide-results'));
      await p.fill('#guide-search', '');
      await p.evaluate(() => showGuideSection('2.8'));
      await p.evaluate(() => buildPrintArea(defaultPrintTarget()));
      ok((await p.textContent('#print-area')).includes('PDF нұсқасында'), 'printing a locked section adds the PDF note');
    }
    ok(!errs.length, vp.name + ' no errors ' + JSON.stringify(errs));
    await ctx.close();
  }
  await b.close();
})();
