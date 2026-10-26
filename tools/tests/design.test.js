// «Жарық» design: palette tokens, no ornament band, text contrast ≥ 4.5:1 (light and dark),
// phone buttons ≥ 44px, no horizontal scroll, lab steps with a line, segmented tabs, bottom dock.
// Usage: node design.test.js <url of index.html>
const { chromium } = require('playwright');
const ok = (c, m) => console.log((c ? 'PASS' : 'FAIL') + '  ' + m);

// Every visible text node: its colour against the first opaque background behind it (alpha blended).
const contrastScan = () => {
  const parse = c => { const m = c.match(/[\d.]+/g); return m ? m.map(Number).concat(m.length === 3 ? [1] : []) : [0, 0, 0, 0]; };
  const lum = ([r, g, b]) => { const f = v => (v /= 255) <= .03928 ? v / 12.92 : Math.pow((v + .055) / 1.055, 2.4); return .2126 * f(r) + .7152 * f(g) + .0722 * f(b); };
  const mix = (top, under) => { const a = top[3]; return [0, 1, 2].map(i => top[i] * a + under[i] * (1 - a)).concat([1]); };
  const bgOf = el => {
    const layers = [];
    for (let e = el; e; e = e.parentElement) {
      const cs = getComputedStyle(e);
      if (cs.backgroundImage !== 'none' && !/gradient/.test(cs.backgroundImage)) return null;   // text over a photo: skip
      const c = parse(cs.backgroundColor);
      if (c[3] > 0) { layers.push(c); if (c[3] >= 1) break; }
    }
    let base = [255, 255, 255, 1];
    if (!layers.length || layers[layers.length - 1][3] < 1) base = parse(getComputedStyle(document.body).backgroundColor);
    return layers.reverse().reduce((acc, l) => mix(l, acc), base);
  };
  const bad = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let n; (n = walker.nextNode());) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement; if (!el) continue;
    const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || +cs.opacity === 0 || el.closest('[hidden],[aria-hidden="true"],.sr-only,button:disabled,.btn:disabled')) continue;
    if (el.closest('svg, option, .wl-photo, .ph, [class*="photo"]')) continue;
    const bg = bgOf(el); if (!bg) continue;
    const fg = mix(parse(cs.color), bg);
    const [a, b] = [lum(fg), lum(bg)].sort((x, y) => y - x);
    const ratio = (a + .05) / (b + .05);
    const big = parseFloat(cs.fontSize) >= 24 || (parseFloat(cs.fontSize) >= 18.66 && +cs.fontWeight >= 700);
    if (ratio < (big ? 3 : 4.5)) bad.push(n.textContent.trim().slice(0, 30) + ' ' + ratio.toFixed(2) + ' ' + cs.color + ' on rgb(' + bg.slice(0, 3).map(Math.round) + ')');
  }
  return [...new Set(bad)];
};

(async () => {
  const [url] = process.argv.slice(2);
  const b = await chromium.launch();
  const errs = [];
  const views = ['Талдауларым', 'Дәптер', 'Сөздік', 'Кітаптар', 'Зертхана'];
  async function open(vp, scheme) {
    const ctx = await b.newContext({ viewport: vp, colorScheme: scheme });
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(e.message));
    p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await p.goto(url); await p.waitForTimeout(500);
    return { ctx, p };
  }
  const go = (p, name) => p.evaluate(n => { const t = [...document.querySelectorAll('#topbar .tab')].find(x => x.textContent.trim() === n); t && t.click(); }, name);

  // Tokens, logo, theme-color, no ornament band.
  {
    const { ctx, p } = await open({ width: 1280, height: 860 }, 'light');
    const v = await p.evaluate(() => { const cs = getComputedStyle(document.documentElement); return ['--bg', '--surface', '--accent', '--accent-ink', '--ok'].map(k => cs.getPropertyValue(k).trim()); });
    ok(JSON.stringify(v) === JSON.stringify(['#F5F6FA', '#FFFFFF', '#3A56E4', '#2A3FB8', '#17673A']), 'light tokens ' + v.join(' '));
    ok(await p.evaluate(() => document.querySelector('meta[name="theme-color"]').content) === '#3A56E4', 'theme-color is the new accent');
    ok(await p.evaluate(() => getComputedStyle(document.querySelector('.wl-top'), '::after').content) === 'none', 'welcome: no ornament band');
    await p.click('.cover >> text=Бастау');
    ok(await p.evaluate(() => getComputedStyle(document.querySelector('.topbar'), '::after').content) === 'none', 'header: no ornament band');
    ok(await p.evaluate(() => getComputedStyle(document.querySelector('.brand-mark')).backgroundImage.includes('3A56E4')), 'new logo mark');

    // Lab: steps joined by a line, segmented tabs, answer focus ring, bottom dock with the progress bar.
    await go(p, 'Зертхана'); await p.waitForTimeout(300);
    ok(await p.evaluate(() => getComputedStyle(document.querySelector('#lab-nav li'), '::before').width) === '2px', 'lab steps: connecting line');
    ok(await p.evaluate(() => { const r = [...document.querySelectorAll('#lab-nav .step-btn')].map(x => x.getBoundingClientRect()); return r.length > 5 && r.every((x, i) => !i || x.top > r[i - 1].top); }), 'lab steps: vertical');
    const seg = await p.evaluate(() => { const t = document.querySelector('.lab-panel-tabs'), s = t.querySelector('[aria-selected="true"]'); return [getComputedStyle(t).borderRadius, getComputedStyle(s).backgroundColor]; });
    ok(seg[0] === '12px' && seg[1] === 'rgb(255, 255, 255)', 'segmented «Кеңес / Мысал / Дереккөз» ' + seg);
    await p.focus('.lab-center .card textarea, .lab-center .card input');
    await p.waitForTimeout(400);   // the ring fades in
    ok(await p.evaluate(() => getComputedStyle(document.activeElement.closest('.card')).boxShadow.includes('233, 237, 255')), 'answer card: focus ring');
    const dock = await p.evaluate(() => { const f = document.querySelector('#footer'), r = f.getBoundingClientRect(); return { radius: getComputedStyle(f).borderRadius, gap: innerHeight - r.bottom, bar: !!f.querySelector('.lab-progress-bar[role=progressbar] span') }; });
    ok(dock.radius === '16px' && dock.gap >= 8 && dock.bar, 'bottom dock with the progress bar ' + JSON.stringify(dock));
    await ctx.close();
  }

  // Contrast in light and dark, on the first page and in every section; phone size: 44px, no overflow.
  for (const scheme of ['light', 'dark']) {
    for (const vp of [{ width: 1280, height: 860 }, { width: 375, height: 760 }]) {
      const { ctx, p } = await open(vp, scheme);
      const tag = scheme + ' ' + vp.width + 'px';
      let bad = await p.evaluate(contrastScan);
      ok(!bad.length, tag + ' first page: contrast ≥ 4.5:1 ' + JSON.stringify(bad.slice(0, 3)));
      await p.click('.cover >> text=Бастау');
      for (const v of views) {
        await go(p, v); await p.waitForTimeout(250);
        bad = await p.evaluate(contrastScan);
        ok(!bad.length, tag + ' ' + v + ': contrast ≥ 4.5:1 ' + JSON.stringify(bad.slice(0, 3)));
        ok(await p.evaluate(() => document.documentElement.scrollWidth - innerWidth) <= 0, tag + ' ' + v + ': no horizontal scroll');
        if (vp.width < 900) {
          const small = await p.evaluate(() => [...document.querySelectorAll('#topbar button, #main button, #footer button, #topbar select, #main select')]
            .filter(e => { const r = e.getBoundingClientRect(); return r.width && r.height && r.height < 44 && !e.closest('[hidden], .lab-panel-body, .g-body, .k-text'); })
            .map(e => (e.textContent.trim() || e.className).slice(0, 24) + ' ' + Math.round(e.getBoundingClientRect().height)));
          ok(!small.length, tag + ' ' + v + ': buttons ≥ 44px ' + JSON.stringify(small.slice(0, 4)));
        }
      }
      await ctx.close();
    }
  }
  ok(!errs.length, 'no page errors ' + JSON.stringify(errs.slice(0, 3)));
  await b.close();
})();
