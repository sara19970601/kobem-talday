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
  for (const vp of [{ width: 1280, height: 860, name: 'desk' }, { width: 1000, height: 760, name: 'tablet' }, { width: 375, height: 760, name: 'phone' }, { width: 320, height: 640, name: 'p320' }]) {
    const ctx = await b.newContext({ viewport: vp });
    await ctx.addInitScript(() => { try { localStorage.setItem('kobem-talday:help-seen', '1'); localStorage.setItem('kobem-talday:cover-hidden', '1'); } catch (e) {} });
    const p = await ctx.newPage(); const errs = []; const net = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    p.on('request', r => { if (!/^(file|data|blob):/.test(r.url())) net.push(r.url()); });
    await p.goto(url);
    ok(await p.locator('.tab').count() === 5, vp.name + ' 5 tabs');
    const tabsRow = await p.evaluate(() => { const ts = [...document.querySelectorAll('.tab')]; const tb = document.querySelector('.tabs'); return { tops: new Set(ts.map(t => Math.round(t.getBoundingClientRect().top))).size, clip: ts.filter(t => t.scrollWidth > t.clientWidth).length, scroll: tb.scrollWidth - tb.clientWidth, help: Math.round(document.querySelector('.help-btn').getBoundingClientRect().top), brand: Math.round(document.querySelector('.brand').getBoundingClientRect().top) }; });
    ok(tabsRow.tops === 1 && tabsRow.clip === 0, vp.name + ' tabs on one row, labels whole ' + JSON.stringify(tabsRow));
    await p.click('#tab-kids');
    ok(await p.locator('.k-card').count() === 38, vp.name + ' 38 books');
    ok(await p.locator('.k-group').count() === 4, vp.name + ' 4 age groups');
    for (const tab of ['library', 'book', 'glossary', 'kids']) {
      await p.click('#tab-' + tab);
      await p.evaluate(() => document.getElementById('main').scrollTop = 1e6);
      const ov = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth);
      if (ov > 0) ok(false, vp.name + ' overflow on ' + tab + ': ' + ov);
    }
    await p.evaluate(() => document.getElementById('main').scrollTop = 0);
    await p.screenshot({ path: shots + '/k-' + vp.name + '.png' });
    await p.click('.k-chip:has-text("11–13 жас")');
    ok(await p.locator('.k-card').count() === 10 && await p.locator('.k-group').count() === 1, vp.name + ' age chip filters');
    await p.click('.k-chip:has-text("Барлығы")');
    await p.evaluate(() => { const i = document.getElementById('kids-search'); i.value = 'ДОСТЫҚ'; i.dispatchEvent(new Event('input')); });
    const n = await p.locator('.k-card').count();
    ok(n > 1 && n < 38 && await p.locator('.k-card mark').count() >= n, vp.name + ' search «достық»: ' + n + ' (' + await p.textContent('#kids-results') + ')');
    ok(await p.textContent('.footer .progress-label').catch(() => '') !== null, vp.name + ' footer');
    await p.evaluate(() => buildPrintArea('kids'));
    ok(await p.locator('#print-area .pk').count() === n, vp.name + ' print follows the filter');
    await p.evaluate(() => { const i = document.getElementById('kids-search'); i.value = ''; i.dispatchEvent(new Event('input')); });
    if (vp.name === 'desk') {
      await p.evaluate(() => buildPrintArea('kids'));
      await p.emulateMedia({ media: 'print' }); await p.pdf({ path: shots + '/kids.pdf', format: 'A4' }); await p.emulateMedia({ media: 'screen' });
      const before = await p.evaluate(() => library.analyses.length);
      await p.locator('.k-card', { hasText: 'Әлканың күміс тұмары' }).locator('button').click();
      ok(await p.getAttribute('#tab-book', 'aria-selected') === 'true' && await IV(p, '#tb-title') === 'Әлканың күміс тұмары'
        && await IV(p, '#tb-author') === 'Нұрайна Сәтбаева' && await IV(p, '#tb-genre') === 'children', 'analyze button fills a new analysis');
      ok(await p.evaluate(() => library.analyses.length) === before, 'blank analysis reused (' + before + ')');
      await p.click('#tab-kids');
      await p.locator('.k-card', { hasText: 'Перси Жәксон' }).locator('button').click();
      ok(await IV(p, '#tb-title') === 'Перси Жәксон мен Олимп тұрғындары. Найзағай ұрлаушы' && await p.evaluate(() => library.analyses.length) === before + 1,
        'second book: new entry, title cleaned: ' + await IV(p, '#tb-title'));
      await p.screenshot({ path: shots + '/k-analyze.png' });
      await p.click('#tab-kids'); await p.waitForTimeout(700); await p.reload();
      ok(await p.getAttribute('#tab-kids', 'aria-selected') === 'true', 'reload stays on kids tab');
      await p.click('.brand'); await p.waitForTimeout(300);
      ok((await p.textContent('.wl-cards')).includes('38 кітап'), 'cover lists the books');
    }
    ok(!errs.length, vp.name + ' no errors ' + JSON.stringify(errs));
    ok(!net.length, vp.name + ' no network ' + JSON.stringify(net));
    await ctx.close();
  }
  await b.close();
})();
