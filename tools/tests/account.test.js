// «Google арқылы кіру»: sign-in (PKCE), 5-second sync, new device, conflicts, delete, sign-out,
// token refresh — against an in-memory Supabase mock (auth + PostgREST), no real network.
// Usage: node account.test.js <url of index.html> <dir that holds index.html>
const { chromium } = require('playwright');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const ok = (c, m) => console.log((c ? 'PASS' : 'FAIL') + '  ' + m);
const sleep = ms => new Promise(r => setTimeout(r, ms));
async function waitFor(fn, ms = 12000, step = 200) {
  const end = Date.now() + ms;
  while (Date.now() < end) { try { if (await fn()) return true; } catch (e) { /* not yet */ } await sleep(step); }
  return false;
}

const SB = 'https://test-proj.supabase.co';
const KEY = 'anon-test-key';
const USER = { id: 'u-123', email: 'sara@example.com', user_metadata: { full_name: 'Сара Бекжанова', avatar_url: 'https://lh3.googleusercontent.com/a/photo.jpg' } };

// In-memory Supabase. jsonb returns keys in its own order: imitate that (shorter keys first).
const db = { rows: {}, challenges: {}, access: {}, refresh: {}, log: [], offline: {}, n: 0 };
const jsonbOrder = v => Array.isArray(v) ? v.map(jsonbOrder)
  : v && typeof v === 'object' ? Object.fromEntries(Object.keys(v).sort((a, b) => a.length - b.length || (a < b ? -1 : 1)).map(k => [k, jsonbOrder(v[k])])) : v;
function issue() {
  const k = ++db.n, at = 'at-' + k, rt = 'rt-' + k;
  db.access[at] = USER.id; db.refresh[rt] = true;
  return { access_token: at, refresh_token: rt, expires_in: 3600, token_type: 'bearer', user: USER };
}
async function mock(route, device) {
  const req = route.request(), u = new URL(req.url()), method = req.method();
  db.log.push({ device, method, path: u.pathname, search: u.search });
  if (db.offline[device]) return route.abort('internetdisconnected');
  // The browser opens /authorize itself (no apikey header), as with the real Supabase.
  if (u.pathname !== '/auth/v1/authorize' && req.headers()['apikey'] !== KEY) return route.fulfill({ status: 401, body: '{"msg":"no apikey"}' });
  const json = (status, body) => route.fulfill({ status, contentType: 'application/json', body: body === undefined ? '' : JSON.stringify(body) });
  if (u.pathname === '/auth/v1/authorize') {
    const q = u.searchParams;
    if (q.get('provider') !== 'google' || q.get('code_challenge_method') !== 's256' || !q.get('code_challenge')) return json(400, { error: 'bad authorize' });
    const code = 'code-' + (++db.n);
    db.challenges[code] = q.get('code_challenge');
    return route.fulfill({ status: 302, headers: { location: q.get('redirect_to') + '?code=' + code } });
  }
  if (u.pathname === '/auth/v1/token') {
    const body = JSON.parse(req.postData() || '{}'), grant = u.searchParams.get('grant_type');
    if (grant === 'pkce') {
      const ch = crypto.createHash('sha256').update(body.code_verifier || '').digest('base64url');
      if (!db.challenges[body.auth_code] || db.challenges[body.auth_code] !== ch) return json(400, { error: 'invalid_grant' });
      delete db.challenges[body.auth_code];
      return json(200, issue());
    }
    if (grant === 'refresh_token') {
      if (!db.refresh[body.refresh_token]) return json(400, { error: 'invalid_grant' });
      delete db.refresh[body.refresh_token];
      return json(200, issue());
    }
    return json(400, { error: 'unsupported_grant_type' });
  }
  if (u.pathname === '/auth/v1/logout') return route.fulfill({ status: 204 });
  if (u.pathname === '/rest/v1/user_data') {
    const auth = (req.headers()['authorization'] || '').replace(/^Bearer /, '');
    const uid = db.access[auth];
    if (!uid) return json(401, { message: 'JWT expired' });
    const owner = (u.searchParams.get('user_id') || '').replace(/^eq\./, '');
    if (method === 'GET') {
      if (owner !== uid) return json(200, []);
      return json(200, db.rows[uid] ? [{ data: jsonbOrder(db.rows[uid].data), updated_at: db.rows[uid].updated_at }] : []);
    }
    if (method === 'POST') {
      const body = JSON.parse(req.postData() || '{}');
      if (body.user_id !== uid) return json(403, { message: 'row-level security' });
      if (JSON.stringify(body.data).length >= 1000000) return json(400, { message: 'check constraint' });
      db.rows[uid] = { data: body.data, updated_at: body.updated_at };
      return route.fulfill({ status: 201 });
    }
    if (method === 'DELETE') { if (owner === uid) delete db.rows[uid]; return route.fulfill({ status: 204 }); }
  }
  return json(404, { error: 'not mocked: ' + u.pathname });
}
const cloudTitles = () => ((db.rows[USER.id] || {}).data || { library: { analyses: [] } }).library.analyses.map(a => a.data.meta.title);

(async () => {
  const [url, dir] = process.argv.slice(2);
  const page0 = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
  const marker = '<script id="account-config" type="application/json">{}</script>';
  ok(page0.includes(marker), 'built page has an empty account config');
  fs.writeFileSync(path.join(dir, 'account.html'), page0.replace(marker,
    '<script id="account-config" type="application/json">' + JSON.stringify({ supabaseUrl: SB, supabaseAnonKey: KEY }) + '</script>'));
  const accUrl = url.replace(/index\.html$/, 'account.html');
  const b = await chromium.launch();
  const errs = [], outside = [];

  async function device(name, vp) {
    const ctx = await b.newContext({ viewport: vp || { width: 1280, height: 860 } });
    await ctx.addInitScript(() => { try { localStorage.setItem('kobem-talday:help-seen', '1'); localStorage.setItem('kobem-talday:cover-hidden', '1'); } catch (e) {} });
    await ctx.route(SB + '/**', r => mock(r, name));
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(name + ': ' + e.message));
    p.on('console', m => { if (m.type() === 'error' && !/internetdisconnected|ERR_INTERNET_DISCONNECTED|Failed to load resource/.test(m.text())) errs.push(name + ': ' + m.text()); });
    p.on('request', r => { const x = r.url(); if (!/^(data|blob):|^http:\/\/localhost/.test(x) && !x.startsWith(SB)) outside.push(x); });
    return { ctx, p };
  }
  const title = p => p.evaluate(() => state.meta.title);
  async function setTitle(p, v) {
    await p.evaluate(() => setWorkOpen(true));
    await p.fill('#tb-title', v);
    await p.evaluate(() => setWorkOpen(false));
  }
  async function signIn(p) {
    await p.click('#acc-btn');
    await p.click('.dlg .btn.primary');   // «Google арқылы кіру»
    return waitFor(() => p.locator('.acc-avatar').first().isVisible().catch(() => false), 15000);
  }

  // 1. Empty config (the page as published): no button, no request to Supabase.
  {
    const ctx = await b.newContext();
    const p = await ctx.newPage(); const reqs = [], pe = [];
    p.on('request', r => { if (!/^http:\/\/localhost|^(data|blob):/.test(r.url())) reqs.push(r.url()); });
    p.on('pageerror', e => pe.push(e.message));
    await p.goto(url); await sleep(800);
    await p.click('.cover >> text=Бастау');
    ok(await p.locator('#acc-btn').count() === 0, '1. empty config: no sign-in button');
    ok(!reqs.length && !pe.length, '1. empty config: no outside request, no error ' + JSON.stringify(reqs.concat(pe)));
    await ctx.close();
  }

  // 2. Sign in on device A: PKCE round trip, initials avatar, clean address, first upload.
  const A = await device('A');
  await A.p.goto(accUrl);
  ok(await A.p.locator('.acc-login').isVisible(), '2. sign-in button shows when configured');
  await setTitle(A.p, 'Абай жолы');
  await A.p.waitForTimeout(500);
  ok(await signIn(A.p), '2. back from Google: avatar shows');
  ok((await A.p.textContent('.acc-avatar')).trim() === 'СБ', '2. avatar shows initials «СБ»');
  ok(!A.p.url().includes('code='), '2. ?code= removed from the address');
  ok(await waitFor(() => cloudTitles()[0] === 'Абай жолы', 8000), '2. local work uploaded to the cloud');
  const sess = await A.p.evaluate(() => localStorage.getItem('kt-account:session'));
  ok(sess && !sess.includes('googleusercontent') && !sess.includes('avatar'), '2. no profile picture stored');
  ok(await A.p.getAttribute('#acc-btn', 'data-state') === 'synced', '2. state «synced»');

  // 3. Changes reach the cloud within ~5 seconds.
  await setTitle(A.p, 'Абай жолы 2');
  ok(await waitFor(() => cloudTitles()[0] === 'Абай жолы 2', 9000), '3. change synced within 5 s');

  // 4. New device, nothing local, work in the cloud → loaded without asking.
  const B = await device('B');
  await B.p.goto(accUrl);
  ok(await signIn(B.p), '4. device B signed in');
  ok(await waitFor(async () => (await title(B.p)) === 'Абай жолы 2', 15000), '4. cloud work loaded on the new device');
  ok(await B.p.locator('.dlg').count() === 0, '4. no question asked');
  ok((await B.p.textContent('#banner-slot')).includes('Бұлттағы жұмысыңыз'), '4. banner says the cloud copy was loaded');
  ok(await waitFor(async () => (await B.p.getAttribute('#acc-btn', 'data-state')) === 'synced', 8000), '4. device B synced after loading');
  ok(await B.p.evaluate(() => !sessionStorage.getItem('kt-account:apply') && !sessionStorage.getItem('kt-account:applied')), '4. hand-over keys cleaned up');

  // 5a. Both changed (A offline) → A asks; «Бұлттағыны алу».
  db.offline.A = true;
  await setTitle(A.p, 'A нұсқасы');
  await setTitle(B.p, 'B нұсқасы');
  ok(await waitFor(() => cloudTitles()[0] === 'B нұсқасы', 9000), '5. device B uploaded its change');
  db.offline.A = false;
  ok(await waitFor(() => A.p.locator('.dlg h2:has-text("Екі түрлі нұсқа бар")').isVisible(), 9000), '5a. device A asks which copy to keep');
  await A.p.click('.dlg >> text=Бұлттағыны алу');
  ok(await waitFor(async () => (await title(A.p)) === 'B нұсқасы', 12000), '5a. «Бұлттағыны алу» loads the cloud copy');

  // 5b. Both changed again → A keeps its own copy.
  await sleep(1500);
  db.offline.A = true;
  await setTitle(A.p, 'A қалсын');
  await setTitle(B.p, 'B тағы');
  ok(await waitFor(() => cloudTitles()[0] === 'B тағы', 9000), '5b. device B uploaded again');
  db.offline.A = false;
  ok(await waitFor(() => A.p.locator('.dlg h2:has-text("Екі түрлі нұсқа бар")').isVisible(), 9000), '5b. device A asks again');
  await A.p.click('.dlg >> text=Осы құрылғыдағыны сақтау');
  ok(await waitFor(() => cloudTitles()[0] === 'A қалсын', 9000), '5b. «Осы құрылғыдағыны сақтау» overwrites the cloud');

  // 6. Expired token → refreshed on the next load.
  await B.p.evaluate(() => { const s = JSON.parse(localStorage.getItem('kt-account:session')); s.expires_at = 10; localStorage.setItem('kt-account:session', JSON.stringify(s)); });
  const before = db.log.filter(x => x.device === 'B' && x.search.includes('grant_type=refresh_token')).length;
  await B.p.reload();
  ok(await waitFor(() => db.log.filter(x => x.device === 'B' && x.search.includes('grant_type=refresh_token')).length > before, 9000), '6. expired token refreshed');
  ok(await waitFor(async () => (await title(B.p)) === 'A қалсын', 15000), '6. device B picks up A\'s copy (B unchanged since sync)');

  // 7. Sign out on B: local work stays, session gone, sign-in button back.
  await B.p.click('#acc-btn'); await B.p.click('.dlg >> text=Шығу');
  ok(await waitFor(() => B.p.locator('.acc-login').isVisible(), 5000), '7. sign-out: sign-in button back');
  ok(await B.p.evaluate(() => localStorage.getItem('kt-account:session')) === null && (await title(B.p)) === 'A қалсын', '7. session removed, local work kept');
  ok(db.log.some(x => x.device === 'B' && x.path === '/auth/v1/logout'), '7. logout endpoint called');

  // 8. Delete the cloud copy from A (asks first); A is signed out, local work kept.
  await A.p.click('#acc-btn'); await A.p.click('.dlg >> text=Бұлттағы деректерді өшіру');
  ok(await A.p.locator('.dlg >> text=Бұлттағы барлық талдауыңыз өшеді').isVisible() && !!db.rows[USER.id], '8. asks before deleting (nothing deleted yet)');
  await A.p.click('.dlg .btn.primary');   // «Иә»
  ok(await waitFor(() => !db.rows[USER.id], 6000), '8. cloud row deleted');
  ok(await waitFor(() => A.p.locator('.acc-login').isVisible(), 5000) && (await title(A.p)) === 'A қалсын', '8. signed out, local work kept');

  // 9. Phone: the sign-in button is at least 44px and nothing overflows.
  const P = await device('P', { width: 375, height: 760 });
  await P.p.goto(accUrl);
  const box = await P.p.locator('#acc-btn').boundingBox();
  ok(box && box.height >= 44, '9. phone: sign-in button ' + (box && Math.round(box.height)) + 'px');
  ok(await P.p.evaluate(() => document.documentElement.scrollWidth - innerWidth) <= 0, '9. phone: no horizontal scroll');

  ok(!errs.length, 'no page errors ' + JSON.stringify(errs.slice(0, 4)));
  ok(!outside.length, 'no request outside the site and the Supabase mock ' + JSON.stringify(outside.slice(0, 4)));
  await b.close();
})();
