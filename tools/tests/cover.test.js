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
  const url = 'file://' + process.argv[2]; const b = await chromium.launch(); const errs = [];
  for (const [name, vp] of [['desk', { width: 1280, height: 820 }], ['phone', { width: 390, height: 844 }]]) {
    const ctx = await b.newContext({ viewport: vp }); await ctx.setOffline(true); const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.goto(url);
    ok(await p.locator('.cover h1').textContent() === 'Көркем шығарманы талдау', name + ': cover opens with the site');
    ok(await p.evaluate(() => document.activeElement.textContent) === 'Бастау', name + ': «Бастау» has focus');
    await p.click('.cover >> text=Бастау');
    ok(await p.locator('.cover-overlay').count() === 0, name + ': «Бастау» closes it');
    await p.reload();
    ok(await p.locator('.cover-overlay').count() === 1, name + ': shown again on the next visit');
    await p.click('.cover >> text=Қалай қолдану керек?');
    ok(await p.locator('.dlg h2').textContent() === 'Қалай қолдану керек?' && await p.locator('.cover-overlay').count() === 0, name + ': «Қалай қолдану керек?» opens the help');
    await p.keyboard.press('Escape');
    await p.reload();
    await p.check('#cover-hide'); await p.keyboard.press('Escape');
    await p.reload();
    ok(await p.locator('.cover-overlay').count() === 0, name + ': «Келесі жолы көрсетпеу» keeps it closed');
    await p.click('.brand');
    ok(await p.locator('.cover-overlay').count() === 1, name + ': clicking the title opens it again');
    await p.click('.cover >> text=Бастау');
    await p.click('.help-btn');
    ok(await p.locator('.dlg h3').count() === 6, name + ': «?» help button still works');
    await ctx.close();
  }
  console.log('errors:', errs); await b.close();
})();
