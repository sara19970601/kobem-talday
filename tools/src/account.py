"""Google арқылы кіру (тек Google) + жұмыстарды бұлтқа сақтау.
Сервис — Supabase (Auth + Postgres). Сыртқы кітапхана жоқ: бәрі fetch арқылы, PKCE ағынымен.
Баптау өшірулі болса (supabaseUrl бос), сайт бұрынғыдай жұмыс істейді: кіру түймесі де, сұраныстар да жоқ.

Usage: python3 -I account.py in.html auth.json out.html   (run before seo.py)
  auth.json: {"supabaseUrl": "https://xxxx.supabase.co", "supabaseAnonKey": "…"}  (файл болмаса да болады)
Баптау қадамдары: tools/ACCOUNT.md."""
import json, os, re, sys

src, cfg_path, out = sys.argv[1:4]
s = open(src, encoding='utf8').read()


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('account anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)


# ---- Config (public by design: the anon key is protected by row-level security) ----
cfg = {}
if os.path.exists(cfg_path):
    try:
        raw = json.load(open(cfg_path, encoding='utf8'))
        url = str(raw.get('supabaseUrl', '')).strip().rstrip('/')
        key = str(raw.get('supabaseAnonKey', '')).strip()
        if re.fullmatch(r'https://[a-z0-9-]+(\.[a-z0-9-]+)+', url) and len(key) >= 20:
            cfg = {'supabaseUrl': url, 'supabaseAnonKey': key}
    except (ValueError, OSError):
        cfg = {}
cfg_json = json.dumps(cfg, ensure_ascii=False).replace('<', '\\u003c')

CSS = r"""
  /* ACCOUNT — «Google арқылы кіру» and the account menu */
  .acc-signin { gap: 10px; }
  .acc-signin svg { flex: none; }
  .acc-chip { display: inline-flex; align-items: center; gap: 8px; padding-left: 6px; }
  .acc-avatar { width: 28px; height: 28px; border-radius: 50%; background: var(--accent); color: var(--accent-ink); font-size: 12px; font-weight: 700;
    display: inline-flex; align-items: center; justify-content: center; flex: none; }
  .acc-name { max-width: 120px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .acc-menu .tb-menu-list { left: auto; right: 0; min-width: 270px; }
  .acc-who { display: grid; gap: 2px; padding: 8px 12px 10px; border-bottom: 1px solid var(--line); margin-bottom: 4px; }
  .acc-who span { font-size: 13px; color: var(--ink-2); overflow-wrap: anywhere; }
  .acc-sync { padding: 6px 12px 8px; font-size: 13px; color: var(--ink-2); }
  .acc-sync.ok { color: var(--ok, #2F5A2A); }
  .acc-sync.err { color: var(--danger, #a3271f); }
  .acc-note { padding: 0 12px 8px; font-size: 12.5px; color: var(--ink-2); }
  @media (max-width: 900px) {
    .acc-label, .acc-name { display: none; }
    .acc-signin { padding-left: 12px; padding-right: 12px; }
    .acc-chip { padding-right: 8px; }
  }
"""

# Runs before the page reads its storage: puts the cloud copy (left in sessionStorage by accApply) on the device.
EARLY = r"""(function () {
  try {
    var raw = sessionStorage.getItem('kt-account:apply');
    if (!raw) return;
    sessionStorage.removeItem('kt-account:apply');
    var d = JSON.parse(raw), skip = ['kobem-talday:help-seen', 'kobem-talday:cover-hidden'], old = [], i, k;
    for (i = 0; i < localStorage.length; i++) { k = localStorage.key(i); if (k && k.indexOf('kobem-talday:') === 0 && skip.indexOf(k) < 0) old.push(k); }
    old.forEach(function (x) { localStorage.removeItem(x); });
    Object.keys(d).forEach(function (x) { if (x.indexOf('kobem-talday:') === 0 && skip.indexOf(x) < 0 && typeof d[x] === 'string') localStorage.setItem(x, d[x]); });
  } catch (e) { /* storage blocked: the page opens as it was */ }
})();"""

rep('</style>\n</head>', '</style>\n<style id="account-css">' + CSS + '</style>\n'
    '<script id="account-config" type="application/json">' + cfg_json + '</script>\n'
    '<script id="account-apply">' + EARLY + '</script>\n</head>')

# ---- Strings ----
rep("  saved: 'Сақталды ✓',", """  saved: 'Сақталды ✓',
  accSignIn: 'Google арқылы кіру',
  accMenu: 'Аккаунт мәзірі',
  accSignInErr: 'Кіру мүмкін болмады. Қайтадан көріңіз.',
  accSignedIn: 'Сіз Google арқылы кірдіңіз.',
  accSignedOut: 'Аккаунттан шықтыңыз. Жұмыстарыңыз осы құрылғыда қалды.',
  accSyncIdle: 'Бұлтқа сақтау күтіп тұр',
  accSyncSaving: 'Бұлтқа сақталуда…',
  accSyncOk: 'Жұмыстарыңыз бұлтқа сақталды',
  accSyncErr: 'Бұлтқа сақтау мүмкін болмады. Жұмысыңыз осы құрылғыда сақталған.',
  accSyncPaused: 'Бұлтқа сақтау тоқтатылды',
  accSyncNow: 'Қазір бұлтқа сақтау',
  accTooBig: 'Жұмыс көлемі бұлтқа сыймайды. Оны «Файл» мәзірінен файлға жүктеп алыңыз.',
  accPrivacy: 'Бұлттағы деректерді тек сіз көре аласыз.',
  accDeleteCloud: 'Бұлттағы деректерді өшіру',
  accDeleteAsk: 'Бұлттағы барлық жұмысыңыз өшеді. Осы құрылғыдағы жұмыс қалады. Жалғастырасыз ба?',
  accDeleted: 'Бұлттағы деректер өшірілді.',
  accSignOut: 'Шығу',
  accConflictTitle: 'Жұмыстар әртүрлі',
  accConflictText: 'Бұлтта сақталған жұмыс пен осы құрылғыдағы жұмыс бір-біріне ұқсамайды. Қайсысын қалдырамыз?',
  accConflictNote: 'Бұлттағыны алсаңыз, осы құрылғыдағы жұмыс резервте сақталады.',
  accUseCloud: 'Бұлттағыны алу',
  accUseDevice: 'Осы құрылғыдағыны сақтау',
  accLater: 'Кейін шешемін',""")

# ---- Module: before the topbar ----
JS = r"""
/* ===== Google арқылы кіру (Supabase Auth, PKCE) + бұлттық көшірме. Баптау: tools/ACCOUNT.md ===== */
const ACC_SESSION_KEY = 'kt-account:session';
const ACC_VERIFIER_KEY = 'kt-account:verifier';
const ACC_TAB_KEY = 'kt-account:tab';
const ACC_SYNC_KEY = 'kt-account:sync';
const ACC_BACKUP_KEY = 'kt-account:backup';
const ACC_PREFIX = 'kobem-talday:';
const ACC_SKIP = ['kobem-talday:help-seen', 'kobem-talday:cover-hidden'];
const ACC_MAX = 900000;
const ACC_GOOGLE_G = '<svg viewBox="0 0 48 48" width="18" height="18" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>';
const acc = { cfg: null, session: null, busy: false, sync: 'idle', paused: false, syncing: false, timer: null };

function accGet(k) { try { return window.localStorage.getItem(k); } catch (e) { return null; } }
function accSet(k, v) { try { window.localStorage.setItem(k, v); return true; } catch (e) { return false; } }
function accDel(k) { try { window.localStorage.removeItem(k); } catch (e) { /* storage blocked */ } }

function accReadConfig() {
  const el = document.getElementById('account-config');
  if (!el) return null;
  try {
    const c = JSON.parse(el.textContent || '{}');
    if (c && /^https:\/\//.test(c.supabaseUrl || '') && String(c.supabaseAnonKey || '').length >= 20) return { url: c.supabaseUrl.replace(/\/+$/, ''), key: c.supabaseAnonKey };
  } catch (e) { /* no config */ }
  return null;
}

function accApi(path, o) {
  o = o || {};
  const headers = Object.assign({ apikey: acc.cfg.key, 'Content-Type': 'application/json' }, o.headers || {});
  if (o.auth && acc.session) headers.Authorization = 'Bearer ' + acc.session.access_token;
  return fetch(acc.cfg.url + path, { method: o.method || 'GET', headers: headers, body: o.body ? JSON.stringify(o.body) : undefined });
}

function accStoreSession(d) {
  const u = d.user || {}, m = u.user_metadata || {};
  acc.session = {
    access_token: d.access_token, refresh_token: d.refresh_token,
    expires_at: d.expires_at || Math.floor(Date.now() / 1000) + (d.expires_in || 3600),
    user: { id: u.id, email: u.email || '', name: m.full_name || m.name || u.email || '' },
  };
  accSet(ACC_SESSION_KEY, JSON.stringify(acc.session));
}
function accClearSession() { acc.session = null; accDel(ACC_SESSION_KEY); clearInterval(acc.timer); acc.timer = null; }

/** A fresh access token; false when it cannot be had (offline: the session is kept; rejected: the session is dropped). */
async function accFresh() {
  const s = acc.session;
  if (!s) return false;
  if (s.expires_at * 1000 - Date.now() > 60000) return true;
  let r;
  try { r = await accApi('/auth/v1/token?grant_type=refresh_token', { method: 'POST', body: { refresh_token: s.refresh_token } }); } catch (e) { return false; }
  if (!r.ok) { accClearSession(); renderAccount(); return false; }
  accStoreSession(await r.json());
  return true;
}

function accRandom(n) { const a = new Uint8Array(n); crypto.getRandomValues(a); return Array.from(a, b => ('0' + b.toString(16)).slice(-2)).join(''); }
async function accChallenge(v) {
  const d = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(v));
  return btoa(String.fromCharCode.apply(null, new Uint8Array(d))).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

async function accSignIn() {
  if (!acc.cfg || acc.busy) return;
  acc.busy = true; renderAccount();
  try {
    const verifier = accRandom(48);
    window.sessionStorage.setItem(ACC_VERIFIER_KEY, verifier);
    window.sessionStorage.setItem(ACC_TAB_KEY, state.ui.tab || '');
    const challenge = await accChallenge(verifier);
    const back = location.origin + location.pathname;
    location.assign(acc.cfg.url + '/auth/v1/authorize?provider=google&redirect_to=' + encodeURIComponent(back)
      + '&code_challenge=' + challenge + '&code_challenge_method=s256');
  } catch (e) { acc.busy = false; renderAccount(); showBanner('error', t('accSignInErr')); }
}

async function accSignOut(silent) {
  if (acc.session) { try { await accApi('/auth/v1/logout', { method: 'POST', auth: true }); } catch (e) { /* offline: just forget the session */ } }
  accClearSession(); acc.sync = 'idle'; acc.paused = false;
  renderAccount();
  if (!silent) showBanner('ok', t('accSignedOut'));
}

function accCanon(o) { return JSON.stringify(Object.keys(o).sort().map(k => [k, o[k]])); }
function accHash(str) { let x = 5381; for (let i = 0; i < str.length; i++) x = ((x << 5) + x + str.charCodeAt(i)) | 0; return String(x); }
function accSnapshot() {
  const data = {};
  try {
    for (let i = 0; i < window.localStorage.length; i++) {
      const k = window.localStorage.key(i);
      if (k && k.indexOf(ACC_PREFIX) === 0 && ACC_SKIP.indexOf(k) < 0) data[k] = window.localStorage.getItem(k);
    }
  } catch (e) { /* storage blocked */ }
  return data;
}
function accMarkSynced(data) { accSet(ACC_SYNC_KEY, JSON.stringify({ uid: acc.session.user.id, hash: accHash(accCanon(data)) })); }
function accLastSync() { try { return JSON.parse(accGet(ACC_SYNC_KEY) || 'null'); } catch (e) { return null; } }

async function accPull() {
  const r = await accApi('/rest/v1/user_data?select=data,updated_at&user_id=eq.' + encodeURIComponent(acc.session.user.id), { auth: true });
  if (!r.ok) throw new Error('pull ' + r.status);
  const rows = await r.json();
  return rows[0] || null;
}
async function accPush(data) {
  const r = await accApi('/rest/v1/user_data?on_conflict=user_id', { method: 'POST', auth: true, headers: { Prefer: 'resolution=merge-duplicates,return=minimal' },
    body: { user_id: acc.session.user.id, data: data, updated_at: new Date().toISOString() } });
  if (!r.ok) throw new Error('push ' + r.status);
}

/** Put the cloud copy on this device: the old local copy goes to a backup key; the page reloads and a small script
    in <head> (#account-apply) writes the cloud copy before the page reads its storage, so nothing in memory can overwrite it. */
function accApply(data) {
  accSet(ACC_BACKUP_KEY, JSON.stringify({ at: new Date().toISOString(), data: accSnapshot() }));
  try { window.sessionStorage.setItem('kt-account:apply', JSON.stringify(data)); } catch (e) { showBanner('error', t('accSyncErr')); return; }
  location.reload();
}

/** No real work: only settings, or the empty analysis the page creates on a first visit. */
const ACC_SETTINGS = ['kobem-talday:lab-tool', 'kobem-talday:lab-level', 'kobem-talday:lab-consent'];
function accIsBlank(snap) {
  return Object.keys(snap).every(k => {
    if (ACC_SETTINGS.indexOf(k) >= 0) return true;
    if (k !== 'kobem-talday:library') return false;
    try {
      return (JSON.parse(snap[k]).analyses || []).every(a => {
        const d = a.data || {}, m = d.meta || {};
        return !m.title && !m.author && !Object.keys(d.answers || {}).length && !(d.lessonPlan && d.lessonPlan.text);
      });
    } catch (e) { return false; }
  });
}

async function accReconcile() {
  const local = accSnapshot();
  const row = await accPull();
  const remote = row && row.data && typeof row.data === 'object' ? row.data : {};
  const localC = accCanon(local), remoteC = accCanon(remote);
  if (localC === remoteC) { accMarkSynced(local); acc.sync = 'ok'; return; }
  if (accIsBlank(remote)) { await accPush(local); accMarkSynced(local); acc.sync = 'ok'; return; }   // the cloud has no work yet
  if (accIsBlank(local)) { accApply(remote); return; }                                              // a new device
  const last = accLastSync();
  if (last && last.uid === acc.session.user.id) {
    if (last.hash === accHash(remoteC)) { await accPush(local); accMarkSynced(local); acc.sync = 'ok'; return; }   // only this device changed
    if (last.hash === accHash(localC)) { accApply(remote); return; }                                                 // only the cloud changed
  }
  acc.paused = true; acc.sync = 'paused';
  openDialog(t('accConflictTitle'), h('div', null, h('p', { text: t('accConflictText') }), h('p', { class: 'note', text: t('accConflictNote') })), [
    { label: t('accLater') },
    { label: t('accUseDevice'), onclick: () => { acc.paused = false; accTick(true); } },
    { label: t('accUseCloud'), primary: true, onclick: () => { accApply(remote); } },
  ]);
}

async function accTick(force) {
  if (!acc.session || !acc.cfg || acc.paused || acc.syncing) return;
  const snap = accSnapshot(), canon = accCanon(snap), last = accLastSync();
  if (last && last.uid === acc.session.user.id && last.hash === accHash(canon)) { if (acc.sync !== 'ok') { acc.sync = 'ok'; accUpdateSync(); } return; }
  if (canon.length > ACC_MAX) { if (acc.sync !== 'error') showBanner('error', t('accTooBig')); acc.sync = 'error'; accUpdateSync(); return; }
  acc.syncing = true; acc.sync = 'saving'; accUpdateSync();
  try {
    if (!(await accFresh())) throw new Error('no token');
    await accPush(snap);
    accMarkSynced(snap); acc.sync = 'ok';
  } catch (e) { acc.sync = 'error'; }
  acc.syncing = false; accUpdateSync();
}

async function accDeleteCloud() {
  try {
    if (!(await accFresh())) throw new Error('no token');
    const r = await accApi('/rest/v1/user_data?user_id=eq.' + encodeURIComponent(acc.session.user.id), { method: 'DELETE', auth: true, headers: { Prefer: 'return=minimal' } });
    if (!r.ok) throw new Error('delete ' + r.status);
    accDel(ACC_SYNC_KEY);
    await accSignOut(true);
    showBanner('ok', t('accDeleted'));
  } catch (e) { showBanner('error', t('accSyncErr')); }
}

function accSyncText() {
  return t({ idle: 'accSyncIdle', saving: 'accSyncSaving', ok: 'accSyncOk', error: 'accSyncErr', paused: 'accSyncPaused' }[acc.sync] || 'accSyncIdle');
}
function accUpdateSync() {
  const el = document.getElementById('acc-sync');
  if (!el) return;
  el.textContent = accSyncText();
  el.className = 'acc-sync' + (acc.sync === 'ok' ? ' ok' : acc.sync === 'error' ? ' err' : '');
}
function accInitials(name) {
  const w = String(name || '').trim().split(/\s+/).filter(Boolean);
  return (w.length ? (w[0][0] + (w.length > 1 ? w[1][0] : '')) : '?').toUpperCase();
}

function renderAccount() {
  const old = document.getElementById('account-box');
  if (old) old.remove();
  const right = document.querySelector('#topbar .hdr-right');
  if (!right || !acc.cfg) return;
  let box;
  if (!acc.session) {
    const g = h('span', { 'aria-hidden': 'true' });
    g.innerHTML = ACC_GOOGLE_G;   // a constant SVG, no user text
    box = h('button', { class: 'btn acc-signin', id: 'account-box', type: 'button', disabled: acc.busy, title: t('accSignIn'), 'aria-label': t('accSignIn'), onclick: accSignIn },
      g, h('span', { class: 'acc-label', text: t('accSignIn') }));
  } else {
    const u = acc.session.user, first = String(u.name || u.email).trim().split(/\s+/)[0];
    box = h('details', { class: 'tb-menu acc-menu', id: 'account-box' },
      h('summary', { class: 'btn acc-chip', 'aria-label': t('accMenu') + ': ' + (u.name || u.email), title: u.email },
        h('span', { class: 'acc-avatar', 'aria-hidden': 'true', text: accInitials(u.name || u.email) }), h('span', { class: 'acc-name', text: first })),
      h('div', { class: 'tb-menu-list', role: 'menu' },
        h('div', { class: 'acc-who' }, h('b', { text: u.name || u.email }), h('span', { text: u.email })),
        h('div', { class: 'acc-sync', id: 'acc-sync', role: 'status', text: accSyncText() }),
        h('div', { class: 'acc-note', text: t('accPrivacy') }),
        h('button', { class: 'tb-menu-item', type: 'button', role: 'menuitem', text: t('accSyncNow'),
          onclick: e => { e.currentTarget.closest('details').open = false; acc.paused = false; accTick(true); } }),
        h('button', { class: 'tb-menu-item', type: 'button', role: 'menuitem', text: t('accDeleteCloud'),
          onclick: e => { e.currentTarget.closest('details').open = false; askConfirm(t('accDeleteAsk'), accDeleteCloud); } }),
        h('button', { class: 'tb-menu-item', type: 'button', role: 'menuitem', text: t('accSignOut'),
          onclick: e => { e.currentTarget.closest('details').open = false; accSignOut(); } })));
    accUpdateSync();
  }
  right.insertBefore(box, right.querySelector('.shop-btn'));
}

async function accountBoot() {
  acc.cfg = accReadConfig();
  if (!acc.cfg) return;
  const q = new URLSearchParams(location.search);
  const code = q.get('code'), err = q.get('error');
  let verifier = null, tab = '';
  try { verifier = window.sessionStorage.getItem(ACC_VERIFIER_KEY); tab = window.sessionStorage.getItem(ACC_TAB_KEY) || ''; } catch (e) { /* storage blocked */ }
  if ((code && verifier) || err) {
    ['code', 'error', 'error_code', 'error_description'].forEach(k => q.delete(k));
    history.replaceState(null, '', location.pathname + (q.toString() ? '?' + q.toString() : '') + location.hash);
  }
  try { window.sessionStorage.removeItem(ACC_VERIFIER_KEY); window.sessionStorage.removeItem(ACC_TAB_KEY); } catch (e) { /* storage blocked */ }
  if (code && verifier) {
    try {
      const r = await accApi('/auth/v1/token?grant_type=pkce', { method: 'POST', body: { auth_code: code, code_verifier: verifier } });
      if (!r.ok) throw new Error('token ' + r.status);
      accStoreSession(await r.json());
      const cover = document.querySelector('.cover-overlay');
      if (cover) cover.remove();
      if (['library', 'book', 'glossary', 'kids', 'lab'].indexOf(tab) >= 0 && tab !== state.ui.tab) switchTab(tab);
      showBanner('ok', t('accSignedIn'));
    } catch (e) { showBanner('error', t('accSignInErr')); }
  } else if (err) {
    showBanner('error', t('accSignInErr'));
  }
  if (!acc.session) { try { acc.session = JSON.parse(accGet(ACC_SESSION_KEY) || 'null'); } catch (e) { acc.session = null; } }
  if (acc.session && !(acc.session.user && acc.session.user.id && acc.session.access_token)) acc.session = null;
  renderAccount();
  if (!acc.session) return;
  try {
    if (await accFresh()) { acc.sync = 'saving'; accUpdateSync(); await accReconcile(); }
    else acc.sync = 'error';
  } catch (e) { acc.sync = 'error'; }
  accUpdateSync();
  if (acc.session) {
    acc.timer = setInterval(() => { if (!document.hidden) accTick(); }, 5000);
    document.addEventListener('visibilitychange', () => { if (document.hidden) accTick(); });
  }
}
setTimeout(accountBoot, 0);

function renderTopbar() {"""
rep('function renderTopbar() {', JS.lstrip('\n'))

# ---- The chip is added to the header each time the header is drawn ----
rep("  updateWorkCard();\n  setSaveStatus();\n  const openTab",
    "  updateWorkCard();\n  setSaveStatus();\n  renderAccount();\n  const openTab")

open(out, 'w', encoding='utf8').write(s)
print('account -> %s (%d KB, %s)' % (out, os.path.getsize(out) // 1024, 'on' if cfg else 'off: no config'))
