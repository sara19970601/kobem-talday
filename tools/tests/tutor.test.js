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
    const ctx = await b.newContext({ viewport: vp, permissions: ['clipboard-read', 'clipboard-write'] });
    await ctx.addInitScript(() => { try { localStorage.setItem('kobem-talday:help-seen', '1'); localStorage.setItem('kobem-talday:cover-hidden', '1'); } catch (e) {} });
    const p = await ctx.newPage(); const errs = [], ext = [];
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    p.on('request', r => { if (!/^(file|data|blob):|^http:\/\/localhost/.test(r.url())) ext.push(r.url()); });
    await p.goto(url);
    await p.click('#tab-lab');
    ok(await p.locator('.tutor-row').count() === 0, vp.name + ' no tutor card on the first (names) step');
    await F(p, '#lab-work', 'Көксерек'); await F(p, '#lab-author', 'Мұхтар Әуезов'); await F(p, '#lab-hero', 'Құрмаш');
    await p.evaluate(() => labGo(1));
    ok(await p.locator('.tutor-row').count() === 1, vp.name + ' tutor card under a stage');
    await F(p, '#lab-traits-0-0', 'Мейірімді');
    await p.click('.tutor-row button');
    ok(await p.locator('.tutor-dlg').count() === 1 && await p.isDisabled('input[value="revision"]'), vp.name + ' dialog opens; revision disabled before a first copy');
    const prompt1 = await p.inputValue('.tutor-dlg textarea');
    ok(prompt1.includes('ЖИ тәлімгері') && prompt1.includes('Кезең: Мінез ерекшеліктері') && prompt1.includes('Мінез белгісі: Мейірімді') && prompt1.includes('Мәтіндегі дәлел (эпизод немесе дәйексөз): —'), vp.name + ' prompt holds stage, answers and missing evidence');
    ok(prompt1.includes('1. Сәтті шыққан тұсы') && prompt1.includes('5. Қайта өңдеу') && prompt1.includes('орнына дайын') && prompt1.includes('ойдан жасама') && prompt1.includes('клиникалық диагноз'), vp.name + ' prompt has the 5-part structure, rules and character focus');
    ok(prompt1.includes('Шығарма: «Көксерек»') && prompt1.includes('Шығарманың мәтіні берілмеген'), vp.name + ' context: work, and no-text caution');
    await p.screenshot({ path: shots + '/tutor-dlg-' + vp.name + '.png' });
    await p.click('.tutor-dlg .btn.primary'); await p.waitForTimeout(150);
    const clip = await p.evaluate(() => navigator.clipboard.readText());
    ok(clip === prompt1, vp.name + ' copy puts the prompt on the clipboard');
    await p.keyboard.press('Escape');
    // revise
    await F(p, '#lab-traits-0-1', 'Бөлтірікті асырап алады');
    await p.click('.tutor-row button');
    ok(!(await p.isDisabled('input[value="revision"]')) && await p.isChecked('input[value="revision"]'), vp.name + ' after editing: revision mode offered and chosen');
    const prompt2 = await p.inputValue('.tutor-dlg textarea');
    ok(prompt2.includes('БҰРЫНҒЫ НҰСҚА') && prompt2.includes('ЖАҢА (ҚАЙТА ӨҢДЕЛГЕН) НҰСҚА') && prompt2.includes('Бөлтірікті асырап алады') && prompt2.includes('«Өзгерістер»'), vp.name + ' revision prompt compares old and new');
    await p.check('input[value="first"]');
    ok(!(await p.inputValue('.tutor-dlg textarea')).includes('БҰРЫНҒЫ НҰСҚА'), vp.name + ' switching back to a plain request');
    await p.keyboard.press('Escape');
    // plot tool: focus and excerpt
    await p.evaluate(() => labSwitch('plot'));
    await F(p, '#lab-plExcerpt', 'Үзінді мәтіні осында.');
    await p.evaluate(() => labGo(2)); await F(p, '#lab-c5', 'Шарықтау шегі');
    await p.click('.tutor-row button');
    const pp = await p.inputValue('.tutor-dlg textarea');
    ok(pp.includes('сюжет пен композиция: оқиғалар байланысы') && pp.includes('Үзінді мәтіні осында.') && pp.includes('5. Шарықтау шегі қай тұста көрінеді?') && pp.includes('Шарықтау шегі') && !pp.includes('клиникалық диагноз'), vp.name + ' plot prompt: own focus, excerpt, its questions');
    await p.keyboard.press('Escape');
    // final
    await p.evaluate(() => labGo(6));
    ok(await p.locator('.tutor-row').count() === 1, vp.name + ' tutor card on the summary');
    await p.click('.tutor-row button');
    const pf = await p.inputValue('.tutor-dlg textarea');
    ok(pf.includes('(бүкіл талдау)') && pf.includes('Ең сәтті үш байқау') && pf.includes('бір қорытынды сұрақ') && pf.includes('## Сюжеттің негізі') && pf.includes('## Интерпретация және қорытынды') && pf.includes('Сандық балл қойма'), vp.name + ' final prompt: whole analysis + final structure');
    ok(await p.locator('.tutor-links a').count() === 3, vp.name + ' links to ChatGPT, Claude, Gemini');
    const ov = await p.evaluate(() => { const d = document.querySelector('.dlg'); return [d.scrollWidth - d.clientWidth, document.documentElement.scrollWidth - innerWidth]; });
    ok(ov[0] <= 0 && ov[1] <= 0, vp.name + ' dialog fits ' + ov);
    await p.keyboard.press('Escape');
    // printing the summary does not include the card
    await p.evaluate(() => buildPrintArea('lab'));
    ok(!(await p.textContent('#print-area')).includes('ЖИ тәлімгері'), vp.name + ' printed document has no tutor card');
    ok(!errs.length, vp.name + ' no errors ' + JSON.stringify(errs));
    ok(!ext.length, vp.name + ' no outside requests ' + JSON.stringify(ext));
    await ctx.close();
  }
  await b.close();
})();
