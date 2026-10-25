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
  for (const vp of [{ width: 1280, height: 860, name: 'desk' }, { width: 390, height: 844, name: 'phone' }, { width: 320, height: 640, name: 'p320' }]) {
    const ctx = await b.newContext({ viewport: vp, permissions: ['clipboard-read', 'clipboard-write'] });
    await ctx.addInitScript(() => { try { localStorage.setItem('kobem-talday:help-seen', '1'); localStorage.setItem('kobem-talday:cover-hidden', '1'); } catch (e) {} });
    const p = await ctx.newPage(); const errs = [], ext = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    p.on('request', r => { if (!/^(file|data|blob):|^http:\/\/localhost/.test(r.url())) ext.push(r.url()); });
    p.on('dialog', d => d.accept());
    await p.goto(url);
    await p.click('#tab-lab');
    ok(await p.locator('#lab-type option').count() === 10 && await p.inputValue('#lab-type') === 'hero', vp.name + ' ten tools, character tool open by default');
    // keep some character answers to prove they survive
    await F(p, '#lab-hero', 'Құрмаш');
    await p.evaluate(() => labSwitch('plot'));
    ok(await p.inputValue('#lab-type') === 'plot' && await p.locator('.lab-dot').count() === 7, vp.name + ' plot tool: own title, 6 panels (preparation, 4 stages, summary)');
    ok(JSON.stringify(await p.locator('.lab-dot .n').allTextContents()) === JSON.stringify(['✎', '1', '2', '3', '4', 'Т', '≡']), vp.name + ' panel badges ✎ 1 2 3 4 ≡');
    ok(await p.textContent('.lab-pos') === 'Дайындық' && await p.locator('#lab-plWork').count() === 1 && await p.locator('#lab-plExcerpt').count() === 1, vp.name + ' preparation: work, author, excerpt');
    ok(await p.locator('.lab-panel-body h4 + ul li').count() === 4, vp.name + ' plot rules shown');
    await p.screenshot({ path: shots + '/plot-prep-' + vp.name + '.png' });
    const ov = async label => { await p.evaluate(() => document.getElementById('main').scrollTop = 1e6); const o = await p.evaluate(() => document.documentElement.scrollWidth - innerWidth); if (o > 0) ok(false, vp.name + ' overflow ' + label + ': ' + o); };
    await ov('prep');
    // Question counts per stage
    const counts = [];
    for (let i = 1; i <= 4; i++) { await p.evaluate(i => labGo(i), i); await ov('stage ' + i); counts.push(await p.evaluate(() => labStepFields(LAB_STEPS[lab.step]).length)); }
    ok(JSON.stringify(counts) === JSON.stringify([6, 6, 8, 6]), vp.name + ' stage fields (questions + evidence): ' + counts.join(','));
    await p.evaluate(() => labGo(2));
    ok(await p.textContent('.lab-pos') === '2-кезең / 4' && await p.textContent('.lab-step-title') === 'Тартыс пен оқиғалардың дамуы', vp.name + ' stage 2 position and title');
    if (vp.name !== 'desk') {
      await p.screenshot({ path: shots + '/plot-stage-' + vp.name + '.png' });
      await p.evaluate(() => labGo(6)); await ov('summary');
      ok(!errs.length, vp.name + ' no errors ' + JSON.stringify(errs));
      await ctx.close(); continue;
    }
    // Fill: preparation
    await p.evaluate(() => labGo(0));
    await F(p, '#lab-plWork', 'Қараш-Қараш оқиғасы'); await F(p, '#lab-plAuthor', 'Мұхтар Әуезов');
    await F(p, '#lab-plExcerpt', 'Үзінді мәтіні: «Бақтығұл ...»');
    await p.evaluate(() => labGo(lab.step + 1));
    ok(await p.textContent('.lab-pos') === '1-кезең / 4', 'next → stage 1');
    await F(p, '#lab-b1', 'Бақтығұлдың кек алуы');
    ok((await p.locator('.lab-warn').last().textContent()).includes('дәлел'), 'answer without evidence → gentle note');
    await F(p, '#lab-ev1', '«Бақтығұл ...» (1-тарау)');
    ok((await p.locator('.lab-warn').last().textContent()) === '', 'evidence clears the note');
    await F(p, '#lab-b3', 'Әлеуметтік әділетсіздік');
    // stage 2 climax
    await p.evaluate(() => labGo(lab.step + 1));
    await F(p, '#lab-c5', 'Бақтығұлдың Қараш асуындағы шешімі');
    await F(p, '#lab-ev2', '«...» деген сөйлем');
    // back to stage 1 and change an answer
    await p.evaluate(() => labGo(lab.step - 1));
    ok(await IV(p, '#lab-b1') === 'Бақтығұлдың кек алуы', 'going back keeps answers');
    await F(p, '#lab-b1', 'Бақтығұлдың кек алуы және оның салдары');
    // stage 3 and 4
    await p.evaluate(() => labGo(3)); await F(p, '#lab-k2', 'Жоқ, шегініс бар');
    await p.evaluate(() => labGo(4)); await F(p, '#lab-i5', 'Сюжет кейіпкердің ішкі өзгерісін ашады');
    // tool switch keeps both
    await p.evaluate(() => labSwitch('hero'));
    ok(await IV(p, '#lab-hero') === 'Құрмаш', 'character tool answers kept after switching');
    await p.evaluate(() => labSwitch('plot'));
    ok(await IV(p, '#lab-i5') === 'Сюжет кейіпкердің ішкі өзгерісін ашады', 'plot answers and stage kept after switching back');
    // other tab and back
    await p.click('#tab-book'); await p.click('#tab-lab');
    ok(await p.inputValue('#lab-type') === 'plot', 'lab tab reopens the same tool');
    // summary
    await p.evaluate(() => labGo(6));
    const secs = await p.locator('.lab-doc h3').allTextContents();
    ok(JSON.stringify(secs) === JSON.stringify(['1. Сюжеттік негіз', '2. Тартыстың дамуы', '3. Композициялық ерекшеліктер', '4. Мәтіндік дәлелдер', '5. Қорытынды интерпретация']), 'result structure: ' + secs.join(' | '));
    const doc = await p.textContent('.lab-doc');
    ok(doc.includes('Сюжет пен композицияны талдау: «Қараш-Қараш оқиғасы»') && doc.includes('Автор: Мұхтар Әуезов') && doc.includes('Бақтығұлдың кек алуы және оның салдары') && doc.includes('Талданған үзінді'), 'document uses the entered answers');
    ok(!doc.includes('Басты кейіпкер қандай кедергіге') && !doc.includes('Шығарма қалай басталады'), 'unanswered questions are left out');
    ok(!doc.includes('Құрмаш') && !doc.includes('диагноз'), 'character answers do not leak into the plot document');
    await p.screenshot({ path: shots + '/plot-summary.png', fullPage: false });
    await p.click('text=Талдауды көшіру'); await p.waitForTimeout(200);
    const clip = await p.evaluate(() => navigator.clipboard.readText());
    ok(clip.startsWith('Сюжет пен композицияны талдау: «Қараш-Қараш оқиғасы»\nАвтор: Мұхтар Әуезов') && clip.includes('4. МӘТІНДІК ДӘЛЕЛДЕР'), 'copy gives the structured text');
    await p.evaluate(() => { window.__printed = 0; window.print = () => { window.__printed++; }; });
    await p.click('.lab-actions >> text=Басып шығару / PDF сақтау');
    ok(await p.evaluate(() => window.__printed) === 1 && (await p.textContent('#print-area')).includes('Қорытынды интерпретация'), 'print fills the print area');
    await p.emulateMedia({ media: 'print' }); await p.pdf({ path: shots + '/plot.pdf', format: 'A4' }); await p.emulateMedia({ media: 'screen' });
    await p.evaluate(() => window.dispatchEvent(new Event('afterprint')));
    // clearing one tool leaves the other
    await p.click('text=Жауаптарды тазарту'); await p.click('.dlg .btn.primary');
    await p.evaluate(() => labGo(1));
    ok(await IV(p, '#lab-b1') === '' , 'clear empties the plot tool');
    await p.evaluate(() => labSwitch('hero'));
    ok(await IV(p, '#lab-hero') === 'Құрмаш', 'clear does not touch the character tool');
    // consent: both tools stored, tool remembered
    await p.evaluate(() => labSwitch('plot'));
    await p.evaluate(() => labGo(0)); await F(p, '#lab-plWork', 'Абай жолы');
    await p.check('#lab-consent'); await p.waitForTimeout(500);
    const keys = await p.evaluate(() => [localStorage.getItem('kobem-talday:lab'), localStorage.getItem('kobem-talday:lab-plot'), localStorage.getItem('kobem-talday:lab-tool')]);
    ok(JSON.parse(keys[0]).data.hero === 'Құрмаш' && JSON.parse(keys[1]).data.plWork === 'Абай жолы' && keys[2] === 'plot', 'consent stores both tools under their own keys (character key unchanged)');
    await p.reload(); await p.click('#tab-lab');
    ok(await p.inputValue('#lab-type') === 'plot' && await IV(p, '#lab-plWork') === 'Абай жолы', 'after reload: same tool and answers');
    await p.uncheck('#lab-consent');
    ok(await p.evaluate(() => ['kobem-talday:lab', 'kobem-talday:lab-plot', 'kobem-talday:lab-tool'].every(k => localStorage.getItem(k) === null)), 'unticking removes all stored lab answers');
    // other parts unaffected
    await p.click('#tab-kids'); ok(await p.locator('.k-card').count() === 38, 'kids tab still works');
    ok(!errs.length, 'no errors ' + JSON.stringify(errs));
    ok(!ext.length, 'no outside requests ' + JSON.stringify(ext));
    await ctx.close();
  }
  // old saved character answers (from the previous version) still load
  const ctx = await b.newContext();
  await ctx.addInitScript(() => { if (!sessionStorage.getItem('x')) { sessionStorage.setItem('x', 1); localStorage.setItem('kobem-talday:help-seen', '1'); localStorage.setItem('kobem-talday:cover-hidden', '1'); localStorage.setItem('kobem-talday:lab-consent', '1'); localStorage.setItem('kobem-talday:lab', JSON.stringify({ version: 1, step: 2, data: { hero: 'Абай', goal: 'Білім' } })); } });
  const p = await ctx.newPage(); await p.goto(url); await p.click('#tab-lab');
  ok(await p.inputValue('#lab-type') === 'hero' && await IV(p, '#lab-goal') === 'Білім', 'answers saved by the previous version open in the character tool');
  await b.close();
})();
