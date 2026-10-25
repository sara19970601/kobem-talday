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
    const ctx = await b.newContext({ viewport: vp, permissions: ['clipboard-read', 'clipboard-write'] });
    await ctx.addInitScript(() => { try { localStorage.setItem('kobem-talday:help-seen', '1'); localStorage.setItem('kobem-talday:cover-hidden', '1'); } catch (e) {} });
    const p = await ctx.newPage(); const errs = [], net = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    p.on('request', r => { if (!/^(file|data|blob):/.test(r.url())) net.push(r.url()); });
    p.on('dialog', d => d.accept());
    await p.goto(url);
    const bar = await p.evaluate(() => { const ts = [...document.querySelectorAll('.tab')]; return { n: ts.length, rows: new Set(ts.map(t => Math.round(t.getBoundingClientRect().top))).size, clip: ts.filter(t => t.scrollWidth > t.clientWidth).length, ov: document.documentElement.scrollWidth - innerWidth, help: Math.round(document.querySelector('.help-btn').getBoundingClientRect().top), tabs: Math.round(document.querySelector('.tabs').getBoundingClientRect().top) }; });
    ok(bar.n === 5 && bar.rows === 1 && bar.clip === 0 && bar.ov <= 0, vp.name + ' 6 tabs in one row, whole labels ' + JSON.stringify(bar));
    await p.click('#tab-lab');
    ok(await p.locator('.lab-dot').count() === 11 && (await p.textContent('.lab-pos')).includes('1-кезең / 11'), vp.name + ' 11 steps, position shown');
    ok(await p.locator('.lab-panel-body h4 + ul li').count() === 5, vp.name + ' rules card on step 1');
    await p.screenshot({ path: shots + '/lab-1-' + vp.name + '.png' });
    if (vp.name !== 'desk') {
      for (const tab of ['library', 'book', 'glossary', 'kids', 'lab']) { await p.click('#tab-' + tab); await p.evaluate(() => document.getElementById('main').scrollTop = 1e6); const o = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth); if (o > 0) ok(false, vp.name + ' overflow ' + tab + ' ' + o); }
      for (let i = 0; i < 10; i++) { await p.evaluate(i => labGo(i), i); const o = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth); if (o > 0) ok(false, vp.name + ' overflow step ' + (i + 1) + ': ' + o); }
      await p.evaluate(() => labGo(1)); await p.screenshot({ path: shots + '/lab-2-' + vp.name + '.png' });
      ok(!errs.length, vp.name + ' no errors ' + JSON.stringify(errs));
      await ctx.close(); continue;
    }
    // Fill step 1
    await F(p, '#lab-work', 'Көксерек'); await F(p, '#lab-author', 'Мұхтар Әуезов'); await F(p, '#lab-hero', 'Құрмаш');
    ok(await p.locator('#lab-nav .step-btn.done').count() === 1, 'step 1 marked done while typing');
    ok(await p.evaluate(() => document.activeElement.id) === 'lab-hero', 'focus kept while typing');
    // Step 2 traits via footer next
    await p.evaluate(() => labGo(lab.step + 1));
    ok((await p.textContent('.lab-step-title')) === 'Мінез ерекшеліктері', 'next goes to step 2');
    await F(p, '#lab-traits-0-0', 'Мейірімді');
    ok((await p.textContent('.lab-row .lab-warn')).includes('дәлел'), 'trait without evidence → gentle warning');
    await F(p, '#lab-traits-0-1', 'Бөлтірікті асырап алады'); await F(p, '#lab-traits-0-2', '1-тарау');
    ok((await p.textContent('.lab-row .lab-warn')) === '', 'warning clears with evidence');
    await p.click('text=+ Жол қосу');
    ok(await p.locator('.lab-row').count() === 2 && await p.evaluate(() => document.activeElement.id) === 'lab-traits-1-0', 'add row focuses the new row');
    await F(p, '#lab-traits-1-0', 'депрессиясы бар');
    ok((await p.locator('.lab-row').nth(1).locator('.lab-warn').textContent()).includes('клиникалық термин'), 'clinical term → warning (not blocked)');
    await F(p, '#lab-traits-1-0', 'Сенгіш');
    // Step 3 goals: evidence warning
    await p.evaluate(i => labGo(i), 3 - 1);
    await F(p, '#lab-goal', 'Бөлтірікті өзімен бірге ұстау');
    ok((await p.locator('.lab-warn').last().textContent()).includes('дәлел'), 'goal without evidence → warning');
    await F(p, '#lab-motive', 'Аңға деген қызығушылығы');
    await F(p, '#lab-goalEvidence', '«…» деген сөзі');
    ok((await p.locator('.lab-warn').last().textContent()) === '', 'evidence clears warning');
    // Step 6 techniques
    await p.evaluate(i => labGo(i), 6 - 1);
    await F(p, '#lab-tech-action', 'Бөлтірікті жасырып қояды');
    ok(await CHK(p, '#lab-tech-action-on'), 'writing an example ticks the technique');
    // Step 8 dynamics: unchanged option
    await p.evaluate(i => labGo(i), 8 - 1);
    await SO(p, '#lab-change', 'Өзгермеді');
    // Tab switch keeps answers (no consent)
    await p.click('#tab-book'); await p.click('#tab-lab');
    ok((await p.textContent('.lab-step-title')) === 'Кейіпкердің даму динамикасы' && await IV(p, '#lab-change') === 'Өзгермеді', 'switching tabs keeps step and answers');
    ok(await p.evaluate(() => localStorage.getItem('kobem-talday:lab')) === null, 'without consent nothing is stored');
    // Summary
    await p.evaluate(i => labGo(i), 11 - 1);
    const doc = await p.textContent('.lab-doc');
    ok(doc.includes('Кейіпкер психологиясын талдау: Құрмаш') && doc.includes('«Көксерек»') && doc.includes('Мейірімді — Бөлтірікті асырап алады (1-тарау)') && doc.includes('Өзгермеді'), 'summary has the answers');
    const secs = await p.locator('.lab-doc h3').allTextContents();
    ok(JSON.stringify(secs) === JSON.stringify(['1. Шығарма мен кейіпкер туралы мәлімет', '2. Кейіпкердің психологиялық портреті', '3. Мақсаттары мен ішкі қайшылықтары', '4. Кейіпкердің даму динамикасы']), 'empty sections are left out: ' + secs.join(' | '));
    ok(!doc.includes('Ішкі қажеттілігі') && !doc.includes('Қарым-қатынас'), 'empty fields not shown');
    await p.screenshot({ path: shots + '/lab-summary.png' });
    await p.click('text=Талдауды көшіру');
    await p.waitForTimeout(200);
    const clip = await p.evaluate(() => navigator.clipboard.readText());
    ok(clip.startsWith('Кейіпкер психологиясын талдау: Құрмаш') && clip.includes('• Мейірімді') && clip.includes('4. КЕЙІПКЕРДІҢ ДАМУ ДИНАМИКАСЫ'), 'copy puts the document text on the clipboard');
    await p.evaluate(() => { window.__printed = 0; window.print = () => { window.__printed++; }; });
    await p.click('.lab-actions >> text=Басып шығару / PDF сақтау');
    ok(await p.evaluate(() => window.__printed) === 1 && (await p.textContent('#print-area')).includes('Мейірімді'), 'print button fills print area and opens print');
    await p.emulateMedia({ media: 'print' }); await p.pdf({ path: shots + '/lab.pdf', format: 'A4' }); await p.emulateMedia({ media: 'screen' });
    await p.evaluate(() => window.dispatchEvent(new Event('afterprint')));
    // Reload without consent → gone (browser asks first: dialog handler accepts)
    await p.reload();
    await p.click('#tab-lab');
    ok(await p.evaluate(() => labHasContent()) === false, 'without consent answers are not kept after reload');
    // With consent
    await p.check('#lab-consent');
    await F(p, '#lab-hero', 'Абай');
    await p.waitForTimeout(600);
    ok(JSON.parse(await p.evaluate(() => localStorage.getItem('kobem-talday:lab'))).data.hero === 'Абай', 'with consent answers are stored locally');
    await p.reload(); await p.click('#tab-lab');
    ok(await IV(p, '#lab-hero') === 'Абай' && await p.isChecked('#lab-consent'), 'with consent answers survive reload');
    await p.uncheck('#lab-consent');
    ok(await p.evaluate(() => localStorage.getItem('kobem-talday:lab')) === null && await IV(p, '#lab-hero') === 'Абай', 'unticking deletes stored copy, keeps the open answers');
    // Clear with confirmation
    await p.click('text=Жауаптарды тазарту');
    ok(await p.locator('.dlg').count() === 1, 'clear asks for confirmation');
    await p.click('.dlg >> text=Бас тарту');
    ok(await IV(p, '#lab-hero') === 'Абай', 'cancel keeps answers');
    await p.click('text=Жауаптарды тазарту'); await p.click('.dlg .btn.primary');
    ok(await IV(p, '#lab-hero') === '' && (await p.textContent('.banner.ok')).includes('тазартылды'), 'confirm clears answers');
    // Other parts still work
    await p.click('#tab-kids'); ok(await p.locator('.k-card').count() === 38, 'kids tab still works');
    await p.click('.shop-btn'); ok(await p.locator('.shop-card').count() === 2, 'shop still works'); await p.keyboard.press('Escape');
    ok(!errs.length, 'no errors ' + JSON.stringify(errs));
    ok(!net.length, 'no network ' + JSON.stringify(net));
    await ctx.close();
  }
  await b.close();
})();
