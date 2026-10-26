// «Google арқылы кіру»: Supabase толығымен жасанды сервермен ауыстырылған (нақты желіге шықпайды).
const { chromium } = require('playwright');
const nodeCrypto = require('crypto');
const ok = (c, m) => console.log((c ? 'PASS' : 'FAIL') + '  ' + m);
const SB = 'https://test.supabase.co', KEY = 'test-anon-key-0123456789abcdef';
const CORS = { 'access-control-allow-origin': '*', 'access-control-allow-headers': '*', 'access-control-allow-methods': '*' };
const EMPTY_CFG = '<script id="account-config" type="application/json">{}</script>';
const sleep = ms => new Promise(r => setTimeout(r, ms));
const until = async (fn, ms = 6000) => { const t0 = Date.now(); while (Date.now() - t0 < ms) { if (await fn()) return true; await sleep(100); } return false; };

(async () => {
  const url = process.argv[2], base = new URL(url);
  const b = await chromium.launch();
  const errs = [], outside = [];

  /** A fresh browser context: the page with (or without) the account config, a fake Supabase and some local data. */
  async function open(o) {
    const be = { row: o.row || null, calls: [] };
    const ctx = await b.newContext({ viewport: o.viewport || { width: 1280, height: 860 } });
    const seed = Object.assign({ 'kobem-talday:help-seen': '1', 'kobem-talday:cover-hidden': '1' }, o.seed || {});
    await ctx.addInitScript(s => { try { if (!sessionStorage.getItem('__seeded')) { sessionStorage.setItem('__seeded', '1'); for (const k in s) localStorage.setItem(k, s[k]); } } catch (e) {} }, seed);
    await ctx.route(u => u.origin + u.pathname === base.origin + base.pathname, async route => {
      const r = await route.fetch();
      const body = (await r.text()).replace(EMPTY_CFG, o.noConfig ? EMPTY_CFG
        : '<script id="account-config" type="application/json">' + JSON.stringify({ supabaseUrl: SB, supabaseAnonKey: KEY }) + '</script>');
      await route.fulfill({ response: r, body });
    });
    await ctx.route(SB + '/**', async route => {
      const req = route.request(), u = new URL(req.url());
      if (req.method() === 'OPTIONS') return route.fulfill({ status: 204, headers: CORS });
      be.calls.push({ method: req.method(), path: u.pathname, search: u.search, params: u.searchParams, headers: req.headers(), body: req.postData() });
      const json = (status, data) => route.fulfill({ status, headers: Object.assign({ 'content-type': 'application/json' }, CORS), body: data === undefined ? '' : JSON.stringify(data) });
      if (u.pathname === '/auth/v1/authorize') {
        const back = u.searchParams.get('redirect_to');
        // A page that sends the browser back (a redirect answer is not routed again by Playwright).
        return route.fulfill({ status: 200, contentType: 'text/html', body: '<script>location.replace(' + JSON.stringify(back + (o.denied ? '?error=access_denied' : '?code=abc123')) + ')</script>' });
      }
      if (u.pathname === '/auth/v1/token') {
        return json(200, { access_token: 'at-1', refresh_token: 'rt-1', expires_in: 3600, expires_at: Math.floor(Date.now() / 1000) + 3600,
          user: { id: 'u-1', email: 'sara@gmail.com', user_metadata: { full_name: 'Сара Бекжанова' } } });
      }
      if (u.pathname === '/auth/v1/logout') return route.fulfill({ status: 204, headers: CORS });
      if (u.pathname === '/rest/v1/user_data') {
        if (req.method() === 'GET') return json(200, be.row ? [be.row] : []);
        if (req.method() === 'POST') { be.row = { data: JSON.parse(req.postData()).data, updated_at: new Date().toISOString() }; return route.fulfill({ status: 201, headers: CORS }); }
        if (req.method() === 'DELETE') { be.row = null; return route.fulfill({ status: 204, headers: CORS }); }
      }
      return json(404, {});
    });
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(e.message));
    p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    p.on('request', r => { const h = new URL(r.url()); if (!/^(file|data|blob):/.test(r.url()) && h.origin !== base.origin && h.origin !== SB) outside.push(r.url()); });
    p.on('dialog', d => d.accept());
    await p.goto(url);
    return { ctx, p, be };
  }
  const posts = be => be.calls.filter(c => c.method === 'POST' && c.path === '/rest/v1/user_data');
  const banner = p => p.locator('#banner-slot .banner').first().textContent().catch(() => '');
  const signIn = async p => { await p.click('#account-box'); await p.waitForSelector('details#account-box'); };

  // 1. Without a config the site is as before: no button, no requests
  {
    const { ctx, p, be } = await open({ noConfig: true });
    ok(await p.locator('#account-box').count() === 0, 'no config → no sign-in button');
    ok(await p.evaluate(() => acc.cfg) === null, 'no config → account module is off');
    await sleep(500);
    ok(be.calls.length === 0, 'no config → no request to the service');
    await ctx.close();
  }

  // 2. Sign in with Google (PKCE), first time: the local work goes to the cloud
  {
    const seed = { 'kobem-talday:test-work': 'uni', 'kobem-talday:test-flag': '1' };
    const { ctx, p, be } = await open({ seed });
    const btn = p.locator('#account-box');
    ok(await btn.count() === 1 && (await btn.textContent()).includes('Google арқылы кіру') && await btn.locator('svg').count() === 1, 'sign-in button «Google арқылы кіру» with the Google mark');
    ok(await p.locator('#account-box').evaluate(e => e.getBoundingClientRect().height) >= 42, 'button is a comfortable target');
    await signIn(p);
    const auth = be.calls.find(c => c.path === '/auth/v1/authorize');
    ok(auth && auth.params.get('provider') === 'google', 'goes to the Google provider');
    ok(auth && auth.params.get('code_challenge_method') === 's256' && /^[A-Za-z0-9_-]{43}$/.test(auth.params.get('code_challenge')), 'PKCE challenge (S256)');
    ok(auth && auth.params.get('redirect_to') === base.origin + base.pathname, 'comes back to the site itself');
    const tok = be.calls.find(c => c.path === '/auth/v1/token');
    const tb = tok && JSON.parse(tok.body);
    ok(tok && tok.params.get('grant_type') === 'pkce' && tb.auth_code === 'abc123', 'the code is exchanged for a session');
    ok(tb && nodeCrypto.createHash('sha256').update(tb.code_verifier).digest('base64url') === auth.params.get('code_challenge'), 'the verifier matches the challenge');
    ok(tok && tok.headers.apikey === KEY, 'public key sent');
    ok(new URL(p.url()).search === '', 'the code is removed from the address');
    ok((await banner(p)).includes('Сіз Google арқылы кірдіңіз'), 'welcome message');
    ok((await p.locator('.acc-avatar').textContent()) === 'СБ' && (await p.locator('.acc-name').textContent()) === 'Сара', 'initials and first name in the header (no outside picture)');
    ok(await until(() => be.row), 'local work is uploaded when the cloud is empty');
    const post = posts(be)[0];
    ok(post && post.headers.authorization === 'Bearer at-1' && JSON.parse(post.body).user_id === 'u-1', 'upload is signed with the user token');
    const data = be.row && be.row.data;
    ok(data && data['kobem-talday:test-work'] === 'uni' && data['kobem-talday:test-flag'] === '1', 'work keys are uploaded');
    ok(data && !('kobem-talday:help-seen' in data) && !('kobem-talday:cover-hidden' in data), 'interface flags stay on the device');
    ok(data && !Object.keys(data).some(k => k.indexOf('kt-account') === 0), 'the session never goes to the cloud');
    await p.click('#account-box summary');
    ok((await p.locator('#acc-sync').textContent()).includes('бұлтқа сақталды'), 'menu says it is saved');
    ok((await p.locator('.acc-who').textContent()).includes('sara@gmail.com'), 'menu shows the e-mail');
    await p.keyboard.press('Escape');
    // a change on this device is sent
    const n = posts(be).length;
    await p.evaluate(() => { localStorage.setItem('kobem-talday:test-work', 'school'); return accTick(true); });
    ok(await until(() => posts(be).length > n) && be.row.data['kobem-talday:test-work'] === 'school', 'a later change is sent');
    // reload: the session stays, nothing is asked again
    await p.reload();
    ok(await p.locator('details#account-box').count() === 1 && await p.locator('.dlg').count() === 0, 'signed in after a reload, no question');
    // sign out
    await p.click('#account-box summary'); await p.click('text=Шығу');
    ok(await until(async () => await p.locator('button#account-box').count() === 1 && be.calls.some(c => c.path === '/auth/v1/logout')), 'sign out → button again');
    ok(await p.evaluate(() => localStorage.getItem('kt-account:session')) === null && await p.evaluate(() => localStorage.getItem('kobem-talday:test-work')) === 'school', 'session removed, work stays on the device');
    ok(!errs.length, 'no page errors ' + JSON.stringify(errs));
    await ctx.close();
  }

  // 3. Different work on the device and in the cloud: the user decides, nothing is lost
  {
    const { ctx, p, be } = await open({ seed: { 'kobem-talday:test-work': 'uni' }, row: { data: { 'kobem-talday:test-work': 'school', 'kobem-talday:test-note': 'plot' } } });
    await signIn(p);
    ok(await p.locator('.dlg h2').textContent() === 'Жұмыстар әртүрлі', 'a question appears when both sides differ');
    ok(posts(be).length === 0, 'nothing is overwritten before the answer');
    await p.click('.dlg >> text=Бұлттағыны алу');
    await p.waitForLoadState('load');
    ok(await until(async () => (await p.evaluate(() => localStorage.getItem('kobem-talday:test-work'))) === 'school'), 'the cloud copy is on the device');
    ok(await p.evaluate(() => localStorage.getItem('kobem-talday:test-note')) === 'plot', 'all cloud keys come over');
    ok((await p.evaluate(() => localStorage.getItem('kt-account:backup') || '')).includes('"uni"'), 'the old device copy is kept as a backup');
    await sleep(400);
    ok(await p.locator('.dlg').count() === 0 && posts(be).length === 0, 'after the reload both sides agree, nothing is sent');
    await ctx.close();
  }
  {
    const { ctx, p, be } = await open({ seed: { 'kobem-talday:test-work': 'uni' }, row: { data: { 'kobem-talday:test-work': 'school' } } });
    await signIn(p);
    await p.click('.dlg >> text=Осы құрылғыдағыны сақтау');
    ok(await until(() => be.row && be.row.data['kobem-talday:test-work'] === 'uni'), '«Осы құрылғыдағыны сақтау» replaces the cloud copy');
    await ctx.close();
  }

  // 4. A new device: nothing local, the cloud has work → it is taken without a question
  {
    const { ctx, p } = await open({ row: { data: { 'kobem-talday:test-work': 'school', 'kobem-talday:test-note': 'plot' } } });
    await signIn(p);
    await p.waitForLoadState('load');
    ok(await until(async () => (await p.evaluate(() => localStorage.getItem('kobem-talday:test-note'))) === 'plot'), 'new device: the cloud work is loaded');
    ok(await p.locator('.dlg').count() === 0, 'new device: no question');
    await ctx.close();
  }

  // 5. Delete the cloud data
  {
    const { ctx, p, be } = await open({ seed: { 'kobem-talday:test-work': 'uni' } });
    await signIn(p);
    await until(() => be.row);
    await p.click('#account-box summary'); await p.click('text=Бұлттағы деректерді өшіру');
    ok((await p.locator('.dlg p').textContent()).includes('Осы құрылғыдағы жұмыс қалады'), 'asks first, says the device copy stays');
    await p.click('.dlg .btn.primary');
    ok(await until(() => be.row === null) && be.calls.some(c => c.method === 'DELETE' && c.params.get('user_id') === 'eq.u-1'), 'the row of this user only is deleted');
    ok(await until(async () => await p.locator('button#account-box').count() === 1 && (await banner(p)).includes('өшірілді')), 'signed out with a message');
    ok(await p.evaluate(() => localStorage.getItem('kobem-talday:test-work')) === 'uni', 'the device copy stays');
    await ctx.close();
  }

  // 6. Expired token is renewed; a refused sign-in shows a calm message
  {
    const exp = JSON.stringify({ access_token: 'old', refresh_token: 'rt-0', expires_at: 1000, user: { id: 'u-1', email: 'sara@gmail.com', name: 'Сара Бекжанова' } });
    const { ctx, p, be } = await open({ seed: { 'kt-account:session': exp } });
    ok(await until(() => be.calls.some(c => c.path === '/auth/v1/token' && c.params.get('grant_type') === 'refresh_token')), 'an expired token is renewed with the refresh token');
    ok(await p.locator('details#account-box').count() === 1, 'still signed in');
    await ctx.close();
  }
  {
    const { ctx, p } = await open({ denied: true });
    await p.click('#account-box');
    await p.waitForSelector('#banner-slot .banner');
    ok((await banner(p)).includes('Кіру мүмкін болмады') && await p.locator('button#account-box').count() === 1, 'refused sign-in → message, button stays');
    await ctx.close();
  }

  // 7. Phone
  {
    const { ctx, p } = await open({ viewport: { width: 390, height: 844 } });
    const o = await p.evaluate(() => { const r = document.getElementById('account-box').getBoundingClientRect(); return { h: r.height, w: r.width, over: document.documentElement.scrollWidth - innerWidth }; });
    ok(o.h >= 44 && o.w >= 44 && o.over <= 0, 'phone: the button is a 44px target and the header does not overflow ' + JSON.stringify(o));
    await ctx.close();
  }

  ok(!outside.length, 'no request outside the site and the service ' + JSON.stringify(outside));
  ok(!errs.length, 'no errors overall ' + JSON.stringify(errs));
  await b.close();
})();
