const { chromium } = require('playwright'); const fs = require('fs');
const ok = (c, m) => console.log((c ? 'PASS' : 'FAIL') + '  ' + m);
const focusId = sel => { const id = sel.replace(/^#lab-/, ''); return id.startsWith('tech-') ? 'techniques' : id.split('-')[0]; };
const isLabField = sel => /^#lab-/.test(sel) && !/^#lab-(consent|type)/.test(sel);
const goF = async (p, sel) => { if (isLabField(sel)) await p.evaluate(id => labFocusField(id), focusId(sel)); else if (/^#tb-/.test(sel)) await p.evaluate(() => setWorkOpen(true)); };
const F = async (p, sel, v) => { await goF(p, sel); await p.fill(sel, v); };
const IV = async (p, sel) => { await goF(p, sel); return p.inputValue(sel); };
const SO = async (p, sel, v) => { await goF(p, sel); return p.selectOption(sel, v); };
const CHK = async (p, sel) => { await goF(p, sel); return p.isChecked(sel); };
(async () => {
  const url = process.argv[2];
  const b = await chromium.launch(); const ctx = await b.newContext({ acceptDownloads: true, viewport: { width: 1280, height: 860 } });  await ctx.addInitScript(() => { try { localStorage.setItem('kobem-talday:help-seen', '1'); localStorage.setItem('kobem-talday:cover-hidden', '1'); } catch (e) {} });

  let p = await ctx.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  p.on('dialog', d => { errs.push('native dialog'); d.dismiss(); });

  // A. Migration: the browser only has data from the previous version (single analysis under kobem-talday:v2)
  await ctx.addInitScript(() => {
    if (!localStorage.getItem('seeded')) {
      localStorage.setItem('seeded', '1');
      localStorage.setItem('kobem-talday:v2', JSON.stringify({ app: 'kobem-talday', version: 2,
        meta: { genre: 'folklore', title: 'Ер Төстік', author: 'Халық', grade: '5' }, answers: { 'ws-01-first-reading': { genre: 'ертегі' } },
        lessonPlan: { text: '', edited: false }, ui: { step: 'ws-04-plot', tab: 'book' } }));
    }
  });
  await p.goto(url);
  ok(await IV(p, '#tb-title') === 'Ер Төстік' && await p.evaluate(() => library.analyses.length) === 1 && await p.textContent('.ws-title') === 'Сюжет картасы',
     'A. old single analysis moved into the library, same sheet reopened');

  // B. New analysis keeps the old one
  await p.$eval('.tb-menu', d => { d.open = true; }).then(() => p.click('.tb-menu-list >> text=Жаңа талдау'));
  ok(await IV(p, '#tb-title') === '' && await p.evaluate(() => library.analyses.length) === 2, 'B. «Жаңа талдау» starts empty and keeps the previous one (' + await p.textContent('.banner.ok') + ')');
  await F(p, '#tb-title', 'Менің атым Қожа'); await SO(p, '#tb-grade', '6');
  await p.fill('#f-ws-01-first-reading-genre', 'повесть');
  // empty-new does not pile up blank entries
  await p.$eval('.tb-menu', d => { d.open = true; }).then(() => p.click('.tb-menu-list >> text=Жаңа талдау')); await p.$eval('.tb-menu', d => { d.open = true; }).then(() => p.click('.tb-menu-list >> text=Жаңа талдау'));
  ok(await p.evaluate(() => library.analyses.length) === 3, 'B2. pressing «Жаңа талдау» on an empty analysis reuses it (3 entries)');

  // C. Library tab
  await p.click('#tab-library');
  const titles = await p.locator('.lib-card h3').allTextContents();
  ok(titles.length === 3 && titles[0] === 'Менің атым Қожа' && titles.includes('Ер Төстік') && titles.includes('Менің атым Қожа'), 'C. cards: ' + titles.join(' | '));
  await p.screenshot({ path: 'lib-desk.png' });
  await p.locator('.lib-card', { hasText: 'Ер Төстік' }).locator('text=Ашу').click();
  ok(await IV(p, '#tb-title') === 'Ер Төстік' && await p.inputValue('#f-ws-01-first-reading-genre').catch(() => '?') !== 'повесть', 'C2. «Ашу» opens Ер Төстік in the Дәптер tab');
  await p.click('#tab-library');
  await p.locator('.lib-card', { hasText: 'Менің атым Қожа' }).locator('text=Көшірмесін жасау').click();
  ok((await p.locator('.lib-card h3').allTextContents()).includes('Менің атым Қожа (көшірме)'), 'C3. copy made');
  await p.locator('.lib-card', { hasText: '(атауы көрсетілмеген)' }).locator('text=Өшіру').click();
  await p.click('.dlg button:has-text("Иә, жалғастыру")');
  ok(await p.locator('.lib-card').count() === 3, 'C4. delete with in-page confirm → 3 cards');

  // D. Save all → wipe → open file brings them back
  const [dl] = await Promise.all([p.waitForEvent('download'), (async () => { await p.click('.lib-tools >> text=Барлығын файлға сақтау'); await p.click('.save-choice:has-text("Word")'); })()]);
  fs.writeFileSync('all.json', fs.readFileSync(await dl.path()));
  const allData = JSON.parse(Buffer.from(/<!--KOBEM-DATA:([^-]+)-->/.exec(fs.readFileSync('all.json', 'utf8'))[1].replace(/\s+/g, ''), 'base64').toString('utf8'));
  // a different computer: a brand-new browser profile
  const ctx2 = await b.newContext({ acceptDownloads: true, viewport: { width: 1280, height: 860 } });  await ctx2.addInitScript(() => { try { localStorage.setItem('kobem-talday:help-seen', '1'); localStorage.setItem('kobem-talday:cover-hidden', '1'); } catch (e) {} });

  const p2 = await ctx2.newPage();
  p2.on('pageerror', e => errs.push(e.message)); p2.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p2.goto(url);
  const pOld = p; p = p2;
  ok(await p.evaluate(() => library.analyses.length) === 1, 'D. fresh browser: one empty analysis');
  await p.click('#tab-library');
  const [ch] = await Promise.all([p.waitForEvent('filechooser'), p.click('.lib-tools >> text=Файлдан ашу')]);
  await ch.setFiles('all.json'); await p.waitForTimeout(200);
  ok(await p.evaluate(() => library.analyses.length) === 3 && allData.analyses.length === 3, 'D2. «Барлығын файлға сақтау» + «Файлдан ашу» restores all 3 (empty one replaced): ' + await p.textContent('.banner.ok'));

  // E. Single file and old-format files add a new analysis, nothing overwritten
  const T = require('path').join(__dirname, 'fixtures') + '/';
  for (const f of ['v2export.json', 'export.json']) {
    const before = await p.evaluate(() => library.analyses.length);
    await p.setInputFiles('#import-file', T + f); await p.waitForTimeout(200);
    ok(await p.evaluate(() => library.analyses.length) === before + 1, 'E. ' + f + ' added (' + (await p.textContent('.banner')).replace('×', '') + ')');
  }

  // F. persistence across reload, active analysis remembered
  const active = await IV(p, '#tb-title'); console.log('  before reload:', active, await p.evaluate(() => library.analyses.length), await p.evaluate(() => 'storageAvailable=' + storageAvailable + ' stored=' + (localStorage.getItem('kobem-talday:library') || '').length + ' status=' + (document.getElementById('save-status') || {}).textContent)); await p.reload(); console.log('  after reload:', await IV(p, '#tb-title'), await p.evaluate(() => library.analyses.length), await p.evaluate(() => { const r = localStorage.getItem('kobem-talday:library'); let n = -1, err = ''; try { const o = JSON.parse(r); n = o.analyses.length; o.analyses.forEach((x, i) => { try { entryToState(x); } catch (e) { err += i + ':' + e.message + ' '; } }); } catch (e) { err = 'parse ' + e.message; } return 'stored=' + (r ? r.length : 'null') + ' n=' + n + ' bad=' + err + ' keys=' + Object.keys(localStorage).join(','); }));
  ok(await IV(p, '#tb-title') === active && await p.evaluate(() => library.analyses.length) === 5, 'F. reload keeps 5 analyses and the open one ("' + active + '")');

  // G. phone layout
  await p.setViewportSize({ width: 390, height: 844 }); await p.click('#tab-library');
  ok(await p.evaluate(() => document.documentElement.scrollWidth - innerWidth) === 0, 'G. phone: no horizontal overflow');
  await p.screenshot({ path: 'lib-phone.png' });
  console.log('errors:', errs); await b.close();
})();
