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
  for (const vp of [{ width: 1280, height: 860, name: 'desk' }, { width: 1000, height: 760, name: 'tablet' }, { width: 390, height: 844, name: 'phone' }, { width: 320, height: 640, name: 'p320' }]) {
    const ctx = await b.newContext({ viewport: vp });
    await ctx.addInitScript(() => { try { localStorage.setItem('kobem-talday:help-seen', '1'); localStorage.setItem('kobem-talday:cover-hidden', '1'); } catch (e) {} });
    const p = await ctx.newPage(); const errs = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.goto(url);
    const tabs = await p.locator('.tab').allTextContents();
    ok(tabs.length === 5 && !tabs.some(x => x.includes('Нұсқаулық')), vp.name + ' five tabs, no separate guide tab: ' + tabs.join(' | '));
    const fit = await p.evaluate(() => [...document.querySelectorAll('.tab')].filter(t => t.scrollWidth > t.clientWidth).length + '/' + (document.documentElement.scrollWidth - innerWidth));
    ok(fit === '0/0', vp.name + ' tab labels whole, no overflow (' + fit + ')');
    // inline tip on sheet 1
    ok(await p.locator('.ws-guide-tip').count() === 1 && await p.locator('button:has-text("Нұсқаулық: 2.1")').count() === 0, vp.name + ' sheet shows «Әдістемелік кеңес», no jump button');
    await p.click('.ws-guide-tip summary');
    ok((await p.textContent('.ws-guide-tip')).includes('Алғашқы әсер') && (await p.textContent('.ws-guide-tip')).includes('Толық нұсқасы PDF-те'), vp.name + ' tip opens inline with the PDF line');
    await p.screenshot({ path: shots + '/mg-sheet-' + vp.name + '.png' });
    await p.click('.ws-guide-tip .link-btn');
    ok(await p.locator('.shop-card').count() === 3, vp.name + ' «Сатып алу» opens the shop'); await p.keyboard.press('Escape');
    ok(await p.getAttribute('#tab-book', 'aria-selected') === 'true', vp.name + ' still on the sheet');
    // switch to guide mode
    if (vp.width <= 900) await p.click('.nav-toggle');
    await p.click('.book-modes button:has-text("Нұсқаулық")');
    ok(await p.getAttribute('#tab-book', 'aria-selected') === 'true' && await p.evaluate(() => state.ui.tab) === 'guide' && await p.locator('.g-body, .g-locked').count() > 0, vp.name + ' guide mode inside «Дәптер»');
    await p.screenshot({ path: shots + '/mg-guide-' + vp.name + '.png' });
    if (vp.width <= 900) await p.click('.nav-toggle');
    ok(await p.getAttribute('.book-modes button:has-text("Нұсқаулық")', 'aria-pressed') === 'true', vp.name + ' switch shows «Нұсқаулық»');
    await p.click('.book-modes button:has-text("Парақтар")');
    ok(await p.evaluate(() => state.ui.tab) === 'book' && (await p.textContent('.ws-title')) === 'Шығарманы алғашқы оқу', vp.name + ' back to the same sheet');
    // chapter-level tip (free chapter 1) offers reading in the guide
    await p.evaluate(() => goTo('ws-16-quotes'));
    if (await p.locator('.ws-guide-tip').count()) {
      await p.click('.ws-guide-tip summary');
      const readBtn = p.locator('.ws-guide-tip button:has-text("Нұсқаулықта оқу")');
      if (await readBtn.count()) { await readBtn.first().click(); ok(await p.evaluate(() => state.ui.tab) === 'guide', vp.name + ' «Нұсқаулықта оқу» opens the guide section'); }
    }
    // reload in guide mode
    await p.evaluate(() => switchTab('guide')); await p.waitForTimeout(700); await p.reload();
    ok(await p.evaluate(() => state.ui.tab) === 'guide' && await p.getAttribute('#tab-book', 'aria-selected') === 'true', vp.name + ' reload keeps guide mode under «Дәптер»');
    ok(!errs.length, vp.name + ' no errors ' + JSON.stringify(errs));
    await ctx.close();
  }
  await b.close();
})();
