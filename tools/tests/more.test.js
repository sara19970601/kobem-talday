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
    const ids = await p.evaluate(() => Object.keys(LAB_TOOLS));
    ok(ids.length === 10, vp.name + ' 10 tools: ' + ids.join(','));
    ok(await p.locator('#lab-type').isVisible() && await p.locator('.lab-tool').count() === 0, vp.name + ': one «Талдау түрі» list, no chips');
    // every tool, every step, both levels: renders, fits, has theory step and summary
    for (const id of ids) {
      await p.selectOption('#lab-type', id);
      const n = await p.evaluate(() => LAB_STEPS.length);
      const names = await p.evaluate(() => LAB_STEPS.map(s => s.id));
      ok(names.includes('theory') && names[names.length - 1].toLowerCase().includes('summary'), vp.name + ' ' + id + ': ' + n + ' steps incl. theory + summary');
      for (const lvl of ['school', 'uni']) {
        await p.evaluate(l => setLabLevel(l), lvl);
        for (let i = 0; i < n; i++) {
          await p.evaluate(i => labGo(i), i);
          const o = await p.evaluate(() => { document.getElementById('main').scrollTop = 1e6; return document.documentElement.scrollWidth - innerWidth; });
          if (o > 0) ok(false, vp.name + ' ' + id + ' ' + lvl + ' step ' + i + ' overflow ' + o);
        }
      }
      await p.evaluate(() => setLabLevel('school'));
    }
    // level switch: university questions appear
    await p.evaluate(() => labSwitch('narratology'));
    await p.evaluate(() => labGo(1));
    ok(await p.evaluate(() => !labStepFields(LAB_STEPS[lab.step]).some(f => f.id === 'nar1q4')), vp.name + ' school level: university question hidden');
    await p.click('.lab-level-opts button:has-text("Университет")');
    ok(await p.evaluate(() => labStepFields(LAB_STEPS[lab.step]).some(f => f.id === 'nar1q4')) && (await p.evaluate(() => { labFocusField('nar1q4'); return !!document.querySelector('.lab-uni-tag'); })), vp.name + ' university level: extra question shown with a tag');
    if (vp.name === 'desk') await p.screenshot({ path: shots + '/more-uni.png' });
    else await p.screenshot({ path: shots + '/more-phone.png' });
    // fill and get the tutor prompt
    await p.evaluate(() => labGo(0));
    await F(p, '#lab-work', 'Абай жолы'); await F(p, '#lab-author', 'Мұхтар Әуезов'); await F(p, '#lab-excerpt', 'Үзінді.');
    await p.evaluate(() => labGo(1));
    await F(p, '#lab-nar1q1', 'Үшінші жақтан баяндалады'); await F(p, '#lab-nar1q4', 'Автор мен баяндаушы жақын');
    await p.click('.tutor-row button');
    const pr = await p.inputValue('.tutor-dlg textarea');
    ok(pr.includes('ДЕҢГЕЙ: университет') && pr.includes('нарратология: баяндаушы, фокализация') && pr.includes('Баяндаушы мен автордың көзқарасы') && pr.includes('Үзінді.'), vp.name + ' tutor prompt: university level, narratology focus, uni question, excerpt');
    await p.keyboard.press('Escape');
    // theory step
    const theoryIdx = await p.evaluate(() => LAB_STEPS.findIndex(s => s.id === 'theory'));
    await p.evaluate(i => labGo(i), theoryIdx);
    ok(await p.evaluate(() => labStepFields(LAB_STEPS[lab.step]).some(f => f.id === 'uniFrame')) && (await p.evaluate(() => { labFocusField('sources'); return document.querySelector('.lab-panel-body').textContent; })).includes('Университет деңгейінде кемінде бір-екі ғылыми дереккөзге'), vp.name + ' theory step (university): frame question + stricter hint');
    await F(p, '#lab-sources', 'Ж. Женетт. Повествовательный дискурс.');
    await p.click('.lab-level-opts button:has-text("Мектеп")');
    ok(await p.evaluate(() => !labStepFields(LAB_STEPS[lab.step]).some(f => f.id === 'uniFrame')) && (await p.textContent('.lab-panel-body')).includes('міндетті емес'), vp.name + ' theory step (school): optional hint, no frame question');
    // summary document
    await p.evaluate(() => labGo(LAB_STEPS.length - 1));
    const secs = await p.locator('.lab-doc h3').allTextContents();
    ok(secs[0] === '1. Баяндаушы' && secs.includes('2. Мәтіндік дәлелдер') && secs.includes('3. Теориялық негіз және дереккөздер'), vp.name + ' narratology document: ' + secs.join(' | '));
    ok((await p.textContent('.lab-doc')).includes('Нарратологиялық талдау: «Абай жолы»') && (await p.textContent('.lab-doc')).includes('Женетт'), vp.name + ' document title and sources');
    // comparative
    await p.evaluate(() => labSwitch('comparative'));
    await p.evaluate(() => labGo(0));
    await F(p, '#lab-work', 'Көксерек'); await F(p, '#lab-author', 'М. Әуезов'); await F(p, '#lab-work2', 'Ақ азу'); await F(p, '#lab-author2', 'Дж. Лондон');
    await F(p, '#lab-excerpt', 'Бірінші үзінді'); await F(p, '#lab-excerpt2', 'Екінші үзінді');
    await p.evaluate(() => labGo(2)); await F(p, '#lab-com2q1', 'Адам мен қасқыр');
    await p.click('.tutor-row button');
    const pc = await p.inputValue('.tutor-dlg textarea');
    ok(pc.includes('1-шығарма: «Көксерек»') && pc.includes('2-шығарма: «Ақ азу»') && pc.includes('Екінші үзінді') && pc.includes('салыстырмалы талдау'), vp.name + ' comparative prompt: both works and excerpts');
    await p.keyboard.press('Escape');
    await p.evaluate(() => labGo(LAB_STEPS.length - 1));
    ok((await p.textContent('.lab-doc-meta')).includes('«Көксерек» (М. Әуезов) · «Ақ азу» (Дж. Лондон)'), vp.name + ' comparative document names both works');
    // hero and plot still have their own steps (plus theory)
    await p.evaluate(() => labSwitch('hero'));
    ok(await p.evaluate(() => LAB_STEPS.map(s => s.id).join(',')) === 'about,traits,goals,emotions,relations,techniques,quotes,dynamics,interpretation,theory,summary', vp.name + ' character tool steps kept, theory added');
    // consent stores all tools and the level
    await p.evaluate(() => setLabLevel('uni'));
    await p.check('#lab-consent'); await p.waitForTimeout(300);
    const st = await p.evaluate(() => ({ nar: localStorage.getItem('kobem-talday:lab-narratology'), com: localStorage.getItem('kobem-talday:lab-comparative'), lvl: localStorage.getItem('kobem-talday:lab-level') }));
    ok(JSON.parse(st.nar).data.work === 'Абай жолы' && JSON.parse(st.com).data.work2 === 'Ақ азу' && st.lvl === 'uni', vp.name + ' consent stores every tool and the level');
    await p.reload(); await p.click('#tab-lab');
    ok(await p.locator('.lab-level-opts button[aria-pressed="true"]').textContent() === 'Университет', vp.name + ' level remembered after reload');
    await p.uncheck('#lab-consent');
    ok(await p.evaluate(() => Object.keys(localStorage).filter(k => k.startsWith('kobem-talday:lab')).length) === 0, vp.name + ' unticking removes all lab keys');
    ok(!errs.length, vp.name + ' no errors ' + JSON.stringify(errs.slice(0, 3)));
    ok(!ext.length, vp.name + ' no outside requests ' + JSON.stringify(ext));
    await ctx.close();
  }
  await b.close();
})();
