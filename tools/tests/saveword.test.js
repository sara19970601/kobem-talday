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
  const url = process.argv[2], out = process.argv[3];
  const b = await chromium.launch();
  const ctx = await b.newContext({ acceptDownloads: true, viewport: { width: 1280, height: 860 } });
  await ctx.addInitScript(() => { try { localStorage.setItem('kobem-talday:help-seen', '1'); localStorage.setItem('kobem-talday:cover-hidden', '1'); } catch (e) {} });
  const p = await ctx.newPage(); const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto(url);
  await SO(p, '#tb-genre', 'folklore');
  await F(p, '#tb-title', 'Ер Төстік'); await F(p, '#tb-author', 'Халық ауыз әдебиеті'); await SO(p, '#tb-grade', '5');
  await p.fill('#f-ws-01-first-reading-genre', 'қиял-ғажайып ертегі');
  const firstLong = p.locator('#main textarea').first(); await firstLong.fill('Көңілді, қызықты.\nЕкінші жол.');
  await p.waitForTimeout(600);
  // Word
  await p.$eval('.tb-menu', d => { d.open = true; }).then(() => p.click('.tb-menu-list >> text=Файлға сақтау'));
  ok(await p.locator('.save-choice').count() === 2, 'dialog offers Word and PDF');
  await p.screenshot({ path: out + '/save-dialog.png' });
  const [dl] = await Promise.all([p.waitForEvent('download'), p.click('.save-choice:has-text("Word")')]);
  const name = dl.suggestedFilename(); const path = out + '/' + name; await dl.saveAs(path);
  ok(true, 'file name (headless shows «download» for non-Latin names) ' + name);
  const doc = fs.readFileSync(path, 'utf8');
  ok(doc.includes('«Ер Төстік»') && doc.includes('қиял-ғажайып ертегі') && doc.includes('Екінші жол') && doc.includes('Сабақ жоспары'), 'Word doc has title, answers and lesson plan');
  ok(doc.includes('<!--KOBEM-DATA:') && !doc.includes('"answers"'), 'data kept only in the hidden note');
  ok((await p.textContent('.banner.ok')).includes('Word'), 'banner: ' + await p.textContent('.banner.ok'));
  // PDF
  await p.evaluate(() => { window.__printed = 0; window.print = () => { window.__printed++; }; });
  await p.$eval('.tb-menu', d => { d.open = true; }).then(() => p.click('.tb-menu-list >> text=Файлға сақтау'));
  await p.click('.save-choice:has-text("PDF")');
  ok(await p.evaluate(() => window.__printed) === 1 && await p.locator('#print-area .doc-analysis h1').textContent() === '«Ер Төстік»', 'PDF opens print with the filled analysis');
  await p.emulateMedia({ media: 'print' }); await p.pdf({ path: out + '/analysis.pdf', format: 'A4' }); await p.emulateMedia({ media: 'screen' });
  await p.evaluate(() => window.dispatchEvent(new Event('afterprint')));
  // Re-open the Word file: new analysis
  const before = await p.evaluate(() => library.analyses.length);
  await p.setInputFiles('#import-file', path);
  await p.waitForTimeout(300);
  ok(await p.evaluate(() => library.analyses.length) === before + 1 && await IV(p, '#tb-title') === 'Ер Төстік' && await p.inputValue('#f-ws-01-first-reading-genre') === 'қиял-ғажайып ертегі', 'Word file reopens through «Файлдан ашу»');
  // Word-edited file (note removed) → clear error
  fs.writeFileSync(out + '/edited.doc', doc.replace(/<!--KOBEM-DATA:[\s\S]*?-->/, ''));
  await p.setInputFiles('#import-file', out + '/edited.doc'); await p.waitForTimeout(300);
  ok((await p.textContent('.banner.error')).includes('түпнұсқа'), 'edited Word file: ' + await p.textContent('.banner.error'));
  // Old JSON still opens
  fs.writeFileSync(out + '/old.json', JSON.stringify({ app: 'kobem-talday', version: 2, meta: { genre: 'prose', title: 'Көксерек', author: 'М. Әуезов', grade: '7' }, answers: {}, lessonPlan: { text: '', edited: false } }));
  await p.setInputFiles('#import-file', out + '/old.json'); await p.waitForTimeout(300);
  ok(await IV(p, '#tb-title') === 'Көксерек', 'old .json file still opens');
  // Library: save all
  await p.click('#tab-library');
  const [dl2] = await Promise.all([p.waitForEvent('download'), (async () => { await p.click('button:text-is("Барлығын файлға сақтау")'); await p.click('.save-choice:has-text("Word")'); })()]);
  const p2 = out + '/' + dl2.suggestedFilename(); await dl2.saveAs(p2);
  const all = fs.readFileSync(p2, 'utf8');
  ok(all.includes('«Ер Төстік»') && all.includes('«Көксерек»'), 'all analyses in one Word file: ' + dl2.suggestedFilename());
  const n = await p.evaluate(() => library.analyses.length);
  await p.setInputFiles('#import-file', p2); await p.waitForTimeout(300);
  ok(await p.evaluate(() => library.analyses.length) > n, 'library Word file reopens (' + n + ' → ' + await p.evaluate(() => library.analyses.length) + ')');
  ok(!errs.length, 'no errors ' + JSON.stringify(errs));
  await b.close();
})();
