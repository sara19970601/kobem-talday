"""Account: sign in with Google only (Supabase Auth, OAuth PKCE, plain fetch — no SDK),
keep the work in the cloud (table user_data, one row per user), sync every 5 seconds.

- Config: tools/data/auth.json → <script id="account-config" type="application/json">.
  Empty values give {} and the feature is off: no button, no request.
- Reconcile on sign-in / page load: cloud only or nothing local → take the cloud copy without
  asking; local unchanged since the last sync → take the cloud copy; cloud unchanged → upload;
  both changed → ask which copy to keep.
- Taking the cloud copy: the data goes to sessionStorage and the page reloads; a small head
  script (#account-apply) writes it to localStorage before the app starts, so the app's own
  save-on-unload cannot overwrite it.
- Never stores the Google profile picture; the avatar shows initials.
Usage: python3 -I account.py in.html auth.json out.html   (run after welcome.py)"""
import base64, json, sys

src, cfg_path, out = sys.argv[1:4]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('account anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

# ---- Config (refuse a service_role key: it must never reach the page) ----
raw = json.load(open(cfg_path, encoding='utf8'))
url, key = (raw.get('supabaseUrl') or '').strip(), (raw.get('supabaseAnonKey') or '').strip()
if key:
    try:
        payload = json.loads(base64.urlsafe_b64decode(key.split('.')[1] + '=='))
    except Exception:
        payload = {}
    if payload.get('role') == 'service_role' or key.startswith('sb_secret_'):
        sys.exit('account: auth.json holds a secret (service_role) key. Use the anon / publishable key only.')
cfg = {'supabaseUrl': url.rstrip('/'), 'supabaseAnonKey': key} if url and key else {}
cfg_json = json.dumps(cfg, ensure_ascii=False).replace('</', '<\\/')

# ---- Head: config + the script that applies a cloud copy before the app reads storage ----
rep('</style>\n</head>', r"""</style>
<script id="account-config" type="application/json">%s</script>
<script id="account-apply">
/* Runs before the app: moves a cloud copy chosen on the previous page into localStorage. */
(function () {
  try {
    var raw = sessionStorage.getItem('kt-account:apply');
    if (!raw) return;
    sessionStorage.removeItem('kt-account:apply');
    var d = JSON.parse(raw), ls = window.localStorage, cur = null;
    try { cur = JSON.parse(ls.getItem('kobem-talday:library') || 'null'); } catch (e) { cur = null; }
    if (d.library && Array.isArray(d.library.analyses)) {
      ls.setItem('kobem-talday:library', JSON.stringify({ version: 1, activeId: d.library.activeId,
        analyses: d.library.analyses, ui: cur && cur.ui ? cur.ui : undefined }));
    }
    var keep = { 'kobem-talday:lab-tool': 1, 'kobem-talday:lab-level': 1 };
    for (var i = ls.length - 1; i >= 0; i--) {
      var k = ls.key(i);
      if (/^kobem-talday:lab(-|$)/.test(k) && !keep[k]) ls.removeItem(k);
    }
    Object.keys(d.lab || {}).forEach(function (k) {
      if (/^kobem-talday:lab(-|$)/.test(k)) ls.setItem(k, typeof d.lab[k] === 'string' ? d.lab[k] : JSON.stringify(d.lab[k]));
    });
    sessionStorage.setItem('kt-account:applied', '1');
  } catch (e) { /* storage blocked: the app starts with what it has */ }
})();
</script>
<style id="account">
  /* ACCOUNT — sign-in button, initials avatar, account window */
  .acc-login { display: inline-flex; align-items: center; gap: 8px; font-weight: 600; }
  .acc-g { display: inline-flex; align-items: center; justify-content: center; width: 22px; height: 22px; border-radius: 50%%;
    background: #fff; border: 1px solid var(--line); color: #4285F4; font-weight: 800; font-size: 13px; font-family: Arial, sans-serif; }
  .acc-avatar { position: relative; display: inline-flex; align-items: center; justify-content: center; width: 40px; height: 40px; padding: 0;
    border-radius: 50%%; border: 1px solid var(--line); background: var(--accent); color: #fff; font-weight: 700; font-size: 14px; letter-spacing: .02em; }
  .acc-dot { position: absolute; right: -1px; bottom: -1px; width: 12px; height: 12px; border-radius: 50%%; border: 2px solid var(--surface); background: var(--ok); }
  .acc-avatar[data-state="syncing"] .acc-dot { background: var(--accent-soft); border-color: var(--accent); }
  .acc-avatar[data-state="error"] .acc-dot, .acc-avatar[data-state="conflict"] .acc-dot, .acc-avatar[data-state="toobig"] .acc-dot { background: #C0392B; }
  .acc-who { display: flex; align-items: center; gap: 12px; margin: 0 0 12px; }
  .acc-who .acc-avatar { width: 48px; height: 48px; font-size: 17px; flex: none; }
  .acc-who b { display: block; font-size: 16px; }
  .acc-who span { color: var(--ink-2); font-size: 14px; word-break: break-all; }
  .acc-status { margin: 0 0 12px; padding: 10px 12px; border-radius: 10px; background: var(--surface-2); font-size: 14px; }
  .acc-note { margin: 0 0 10px; font-size: 14px; line-height: 1.55; color: var(--ink-2); }
  .acc-list { margin: 0 0 12px; padding-left: 18px; font-size: 14px; line-height: 1.55; }
  .acc-danger { color: #9A2B1E; border-color: #E8B4AC; }
  @media (max-width: 600px) { .acc-login .acc-label { display: none; } .acc-login { padding: 0 10px; } }
</style>
</head>""" % cfg_json)

# ---- Strings ----
rep("  coverHide: 'Келесі жолы көрсетпеу',", """  coverHide: 'Келесі жолы көрсетпеу',
  accLogin: 'Google арқылы кіру',
  accLoginTitle: 'Google арқылы кіру',
  accLoginText: 'Кірсеңіз, талдауларыңыз бұлтта сақталады. Оларды басқа құрылғыда да аша аласыз.',
  accLoginStored: 'Бұлтта не сақталады:',
  accLoginItems: ['Google аккаунтыңыздың email-і мен аты-жөні', 'Сайттағы талдауларыңыз мен Зертхана жауаптары'],
  accLoginNote: 'Оқушылардың аты-жөнін және басқа жеке деректерін жазбаңыз. Профиль суреті сақталмайды.',
  accLoginGo: 'Google арқылы кіру',
  accCancel: 'Бас тарту',
  accMenuTitle: 'Аккаунт',
  accLogout: 'Шығу',
  accDelete: 'Бұлттағы деректерді өшіру',
  accDeleteAsk: 'Бұлттағы барлық талдауыңыз өшеді. Осы құрылғыдағы жұмыс қалады. Жалғастырасыз ба?',
  accDeleted: 'Бұлттағы деректер өшірілді. Сіз аккаунттан шықтыңыз. Осы құрылғыдағы жұмыс сақталды.',
  accSignedIn: 'Сіз кірдіңіз: {name}.',
  accSignedOut: 'Сіз аккаунттан шықтыңыз. Осы құрылғыдағы жұмыс сақталды.',
  accExpired: 'Кіру мерзімі бітті. Қайта кіріңіз.',
  accLoginFailed: 'Кіру сәтсіз аяқталды. Қайталап көріңіз.',
  accApplied: 'Бұлттағы жұмысыңыз осы құрылғыға жүктелді.',
  accStateSyncing: 'Бұлтқа сақталуда…',
  accStateSynced: 'Бұлтта сақталды ✓ {time}',
  accStateError: 'Бұлтқа сақталмады. Біраздан кейін өзі қайталайды.',
  accStateTooBig: 'Деректер тым көп: бұлтқа сақтау мүмкін емес.',
  accStateConflict: 'Қай нұсқаны сақтау керегін таңдаңыз.',
  accStateIdle: 'Бұлтпен байланысуда…',
  accConflictTitle: 'Екі түрлі нұсқа бар',
  accConflictText: 'Осы құрылғыдағы жұмыс пен бұлттағы жұмыс әртүрлі. Қайсысын сақтайсыз? Екіншісі ауыстырылады.',
  accConflictLocal: 'Осы құрылғыда: {n} талдау',
  accConflictCloud: 'Бұлтта: {n} талдау, {time} сақталған',
  accKeepLocal: 'Осы құрылғыдағыны сақтау',
  accKeepCloud: 'Бұлттағыны алу',
  accChoose: 'Нұсқаны таңдау',""")

# ---- Header: sign-in button or avatar ----
rep("""        h('span', { id: 'save-status', class: 'save-status', 'aria-live': 'polite' }),
        h('button', { class: 'btn shop-btn', type: 'button', onclick: showShop,""",
    """        h('span', { id: 'save-status', class: 'save-status', 'aria-live': 'polite' }),
        accHeaderButton(),
        h('button', { class: 'btn shop-btn', type: 'button', onclick: showShop,""")

# ---- Logic ----
rep("""/* ==============================================================================
   INIT
   ============================================================================== */""", r"""/* ==============================================================================
   ACCOUNT — «Google арқылы кіру» (Supabase Auth, OAuth PKCE; REST calls with fetch).
   The cloud keeps one row per user in user_data: { library, lab } as on this device.
   ============================================================================== */
const ACC_CFG = (() => {
  try {
    const c = JSON.parse(document.getElementById('account-config').textContent || '{}');
    return c && c.supabaseUrl && c.supabaseAnonKey ? { url: String(c.supabaseUrl).replace(/\/+$/, ''), key: String(c.supabaseAnonKey) } : null;
  } catch (e) { return null; }
})();
const ACC_SESSION_KEY = 'kt-account:session';
const ACC_VERIFIER_KEY = 'kt-account:pkce';
const ACC_APPLY_KEY = 'kt-account:apply';
const ACC_APPLIED_KEY = 'kt-account:applied';
const ACC_BASE_PREFIX = 'kt-account:base:';   // hash of the copy last agreed with the cloud
const ACC_SYNC_MS = 5000;
const ACC_MAX = 1000000;
let accSession = null, accState = 'idle', accLastSync = null, accBusy = false, accTimer = null, accJustApplied = false;

const accLs = { get: k => { try { return window.localStorage.getItem(k); } catch (e) { return null; } },
  set: (k, v) => { try { window.localStorage.setItem(k, v); } catch (e) { /* blocked */ } },
  del: k => { try { window.localStorage.removeItem(k); } catch (e) { /* blocked */ } } };
const accSs = { get: k => { try { return window.sessionStorage.getItem(k); } catch (e) { return null; } },
  set: (k, v) => { try { window.sessionStorage.setItem(k, v); } catch (e) { /* blocked */ } },
  del: k => { try { window.sessionStorage.removeItem(k); } catch (e) { /* blocked */ } } };

/** Leaving the page on the way back from Google (or right after taking the cloud copy): no cover. */
function accSkipCover() {
  if (!ACC_CFG) return false;
  const q = new URLSearchParams(location.search);
  return q.has('code') || q.has('error') || !!accSs.get(ACC_APPLIED_KEY);
}

/** JSON with sorted keys: the cloud (jsonb) reorders keys, so hashes compare content only. */
function accCanon(v) {
  if (Array.isArray(v)) return '[' + v.map(accCanon).join(',') + ']';
  if (v && typeof v === 'object') return '{' + Object.keys(v).filter(k => v[k] !== undefined).sort().map(k => JSON.stringify(k) + ':' + accCanon(v[k])).join(',') + '}';
  return JSON.stringify(v === undefined ? null : v);
}
function accHash(str) {
  let h = 0x811c9dc5;
  for (let i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 0x01000193) >>> 0; }
  return h.toString(16) + ':' + str.length;
}

/** What this device holds: analyses (without view settings) and lab answers (without the open step). */
function accSnapshot() {
  const out = { v: 1, library: null, lab: {} };
  try {
    const lib = JSON.parse(accLs.get(LIBRARY_KEY) || 'null');
    if (lib && Array.isArray(lib.analyses)) out.library = { activeId: lib.activeId || null, analyses: lib.analyses };
    const keys = [];
    for (let i = 0; i < window.localStorage.length; i++) keys.push(window.localStorage.key(i));
    keys.filter(k => /^kobem-talday:lab(-|$)/.test(k) && k !== 'kobem-talday:lab-tool' && k !== 'kobem-talday:lab-level').forEach(k => {
      let v = accLs.get(k);
      try { v = JSON.parse(v); } catch (e) { /* keep the string */ }
      if (v && typeof v === 'object') { v = Object.assign({}, v); delete v.step; delete v.qi; }
      out.lab[k] = v;
    });
  } catch (e) { /* storage blocked */ }
  return out;
}
function accFilledAny(v) {
  if (typeof v === 'string') return v.trim() !== '';
  if (Array.isArray(v)) return v.some(accFilledAny);
  if (v && typeof v === 'object') return Object.values(v).some(accFilledAny);
  return v === true;
}
function accHasContent(snap) {
  const analyses = snap && snap.library && Array.isArray(snap.library.analyses) ? snap.library.analyses : [];
  if (analyses.some(a => a && a.data && (accFilledAny(a.data.meta && a.data.meta.title) || accFilledAny(a.data.meta && a.data.meta.author) || accFilledAny(a.data.answers)))) return true;
  return Object.keys((snap && snap.lab) || {}).some(k => k !== 'kobem-talday:lab-consent' && snap.lab[k] && typeof snap.lab[k] === 'object' && accFilledAny(snap.lab[k].data));
}
function accCount(snap) { return snap && snap.library && Array.isArray(snap.library.analyses) ? snap.library.analyses.length : 0; }

async function accFetch(path, opts) {
  opts = opts || {};
  const headers = Object.assign({ apikey: ACC_CFG.key }, opts.headers || {});
  if (opts.auth !== false && accSession) headers.Authorization = 'Bearer ' + accSession.access_token;
  let body = opts.body;
  if (body !== undefined && typeof body !== 'string') { headers['Content-Type'] = 'application/json'; body = JSON.stringify(body); }
  return fetch(ACC_CFG.url + path, { method: opts.method || 'GET', headers: headers, body: body });
}

function accB64url(bytes) {
  let s = '';
  bytes.forEach(b => { s += String.fromCharCode(b); });
  return btoa(s).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}
async function accSignIn() {
  const verifier = accB64url(crypto.getRandomValues(new Uint8Array(48)));
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(verifier));
  const challenge = accB64url(new Uint8Array(digest));
  accSs.set(ACC_VERIFIER_KEY, verifier);
  saveStateNow();
  const back = location.origin + location.pathname;
  location.assign(ACC_CFG.url + '/auth/v1/authorize?provider=google&redirect_to=' + encodeURIComponent(back)
    + '&code_challenge=' + challenge + '&code_challenge_method=s256');
}
function accSetSession(data, user) {
  const u = data.user || user || {};
  const meta = u.user_metadata || {};
  accSession = {
    access_token: data.access_token, refresh_token: data.refresh_token,
    expires_at: data.expires_at || Math.floor(Date.now() / 1000) + (data.expires_in || 3600),
    user: { id: u.id, email: u.email || '', name: meta.full_name || meta.name || u.name || '' },
  };
  accLs.set(ACC_SESSION_KEY, JSON.stringify(accSession));
}
function accLoadSession() {
  try {
    const sv = JSON.parse(accLs.get(ACC_SESSION_KEY) || 'null');
    accSession = sv && sv.access_token && sv.refresh_token && sv.user && sv.user.id ? sv : null;
  } catch (e) { accSession = null; }
}
/** Back from Google with ?code=…: exchange it (with the saved verifier) for a session. */
async function accHandleReturn() {
  const q = new URLSearchParams(location.search);
  const code = q.get('code'), err = q.get('error_description') || q.get('error');
  if (!code && !err) return false;
  history.replaceState(null, '', location.pathname + location.hash);
  const verifier = accSs.get(ACC_VERIFIER_KEY);
  accSs.del(ACC_VERIFIER_KEY);
  if (err || !verifier) { showBanner('error', t('accLoginFailed')); return true; }
  try {
    const r = await accFetch('/auth/v1/token?grant_type=pkce', { method: 'POST', auth: false, body: { auth_code: code, code_verifier: verifier } });
    if (!r.ok) throw new Error('token ' + r.status);
    accSetSession(await r.json());
    showBanner('ok', t('accSignedIn', { name: accSession.user.name || accSession.user.email }));
  } catch (e) {
    accSession = null;
    showBanner('error', t('accLoginFailed'));
  }
  return true;
}
async function accEnsureToken() {
  if (!accSession) return false;
  if (accSession.expires_at - 60 > Date.now() / 1000) return true;
  try {
    const r = await accFetch('/auth/v1/token?grant_type=refresh_token', { method: 'POST', auth: false, body: { refresh_token: accSession.refresh_token } });
    if (!r.ok) throw new Error('refresh ' + r.status);
    accSetSession(await r.json(), accSession.user);
    return true;
  } catch (e) {
    accSignedOut(t('accExpired'));
    return false;
  }
}
function accSignedOut(message) {
  accSession = null;
  accLs.del(ACC_SESSION_KEY);
  clearInterval(accTimer); accTimer = null;
  accState = 'idle';
  renderTopbar();
  if (message) showBanner('ok', message);
}
async function accSignOut() {
  const token = accSession && accSession.access_token;
  accSignedOut(t('accSignedOut'));
  if (token) { try { await fetch(ACC_CFG.url + '/auth/v1/logout', { method: 'POST', headers: { apikey: ACC_CFG.key, Authorization: 'Bearer ' + token } }); } catch (e) { /* offline: the token expires */ } }
}

function accBaseKey() { return ACC_BASE_PREFIX + accSession.user.id; }
async function accCloudGet() {
  const r = await accFetch('/rest/v1/user_data?select=data,updated_at&user_id=eq.' + encodeURIComponent(accSession.user.id));
  if (!r.ok) throw new Error('get ' + r.status);
  const rows = await r.json();
  return Array.isArray(rows) && rows[0] ? rows[0] : null;
}
function accSetState(st) {
  accState = st;
  if (st === 'synced') accLastSync = new Date();
  const btn = document.getElementById('acc-btn');
  if (btn) { btn.dataset.state = st; btn.title = accStateText(); }
  const el = document.getElementById('acc-status');
  if (el) el.textContent = accStateText();
}
function accStateText() {
  const p = n => String(n).padStart(2, '0');
  if (accState === 'synced') return t('accStateSynced', { time: accLastSync ? p(accLastSync.getHours()) + ':' + p(accLastSync.getMinutes()) : '' });
  return t({ syncing: 'accStateSyncing', error: 'accStateError', toobig: 'accStateTooBig', conflict: 'accStateConflict' }[accState] || 'accStateIdle');
}

/** Upload this device's copy. With `check`, first make sure nobody else changed the cloud. */
async function accUpload(snap, check) {
  accBusy = true;
  accSetState('syncing');
  try {
    if (!(await accEnsureToken())) return;
    const json = accCanon(snap), h = accHash(json);
    if (json.length > ACC_MAX) { accSetState('toobig'); return; }
    if (check) {
      const row = await accCloudGet();
      if (row) {
        const ch = accHash(accCanon(row.data)), base = accLs.get(accBaseKey());
        if (ch !== base && ch !== h) { accConflict(snap, row); return; }
      }
    }
    const r = await accFetch('/rest/v1/user_data?on_conflict=user_id', { method: 'POST',
      headers: { Prefer: 'resolution=merge-duplicates,return=minimal' },
      body: { user_id: accSession.user.id, data: JSON.parse(json), updated_at: new Date().toISOString() } });
    if (!r.ok) throw new Error('put ' + r.status);
    accLs.set(accBaseKey(), h);
    accSetState('synced');
  } catch (e) {
    accSetState('error');
  } finally {
    accBusy = false;
  }
}
/** Take the cloud copy: hand it to the head script through a reload. */
function accApply(cloud) {
  accSs.set(ACC_APPLY_KEY, JSON.stringify(cloud));
  accLs.set(accBaseKey(), accHash(accCanon(cloud)));
  clearInterval(accTimer); accTimer = null;
  location.reload();
}
function accConflict(local, row) {
  accSetState('conflict');
  const d = new Date(row.updated_at || Date.now());
  const p = n => String(n).padStart(2, '0');
  const when = isNaN(d) ? '' : p(d.getDate()) + '.' + p(d.getMonth() + 1) + '.' + d.getFullYear() + ', ' + p(d.getHours()) + ':' + p(d.getMinutes());
  openDialog(t('accConflictTitle'), [
    h('p', { class: 'acc-note', text: t('accConflictText') }),
    h('ul', { class: 'acc-list' },
      h('li', { text: t('accConflictLocal', { n: accCount(local) }) }),
      h('li', { text: t('accConflictCloud', { n: accCount(row.data), time: when }) })),
  ], [
    { label: t('accKeepCloud'), onclick: () => accApply(row.data) },
    { label: t('accKeepLocal'), primary: true, onclick: () => { accUpload(accSnapshot(), false); } },
  ]);
}
/** Sign-in or page load: decide between this device and the cloud. */
async function accReconcile() {
  if (accBusy || !(await accEnsureToken())) return;
  accBusy = true;
  accSetState('syncing');
  let row;
  try { row = await accCloudGet(); } catch (e) { accBusy = false; accSetState('error'); return; }
  accBusy = false;
  const local = accSnapshot(), lh = accHash(accCanon(local));
  const base = accLs.get(accBaseKey());
  if (!row) {
    if (accHasContent(local)) await accUpload(local, false);
    else { accLs.set(accBaseKey(), lh); accSetState('synced'); }
    return;
  }
  const ch = accHash(accCanon(row.data));
  if (ch === lh) { accLs.set(accBaseKey(), lh); accSetState('synced'); return; }
  if (accJustApplied) { await accUpload(local, false); return; }   // never reload twice in a row
  if (!accHasContent(local) || base === lh) { accApply(row.data); return; }
  if (base === ch) { await accUpload(local, false); return; }
  accConflict(local, row);
}
/** Every 5 seconds: upload when this device's copy changed since the last sync. */
async function accTick() {
  if (!accSession || accBusy || accState === 'conflict') return;
  const snap = accSnapshot(), h = accHash(accCanon(snap));
  if (h === accLs.get(accBaseKey())) { if (accState === 'syncing' || accState === 'idle') accSetState('synced'); return; }
  await accUpload(snap, true);
}
function accStartSync() {
  clearInterval(accTimer);
  accTimer = setInterval(accTick, ACC_SYNC_MS);
}

function accInitials() {
  const u = accSession.user;
  const words = (u.name || '').trim().split(/\s+/).filter(Boolean);
  const s = words.length ? words.slice(0, 2).map(w => Array.from(w)[0]).join('') : Array.from(u.email || '?')[0];
  return s.toLocaleUpperCase('kk');
}
function accHeaderButton() {
  if (!ACC_CFG) return null;
  if (!accSession) {
    return h('button', { class: 'btn acc-login', type: 'button', id: 'acc-btn', 'aria-label': t('accLogin'), onclick: accShowLogin },
      h('span', { class: 'acc-g', 'aria-hidden': 'true' }, 'G'), h('span', { class: 'acc-label', text: t('accLogin') }));
  }
  return h('button', { class: 'acc-avatar', type: 'button', id: 'acc-btn', 'data-state': accState, title: accStateText(),
    'aria-label': t('accMenuTitle') + ': ' + (accSession.user.name || accSession.user.email), onclick: accShowMenu },
    h('span', { 'aria-hidden': 'true', text: accInitials() }), h('span', { class: 'acc-dot', 'aria-hidden': 'true' }));
}
function accShowLogin() {
  openDialog(t('accLoginTitle'), [
    h('p', { class: 'acc-note', text: t('accLoginText') }),
    h('p', { class: 'acc-note', text: t('accLoginStored') }),
    h('ul', { class: 'acc-list' }, STRINGS.accLoginItems.map(x => h('li', { text: x }))),
    h('p', { class: 'acc-note', text: t('accLoginNote') }),
  ], [{ label: t('accCancel') }, { label: t('accLoginGo'), primary: true, onclick: () => { accSignIn(); } }]);
}
function accShowMenu() {
  const u = accSession.user;
  openDialog(t('accMenuTitle'), [
    h('div', { class: 'acc-who' },
      h('span', { class: 'acc-avatar', 'aria-hidden': 'true' }, accInitials()),
      h('div', null, h('b', { text: u.name || u.email }), u.name ? h('span', { text: u.email }) : null)),
    h('p', { class: 'acc-status', id: 'acc-status', role: 'status', text: accStateText() }),
  ], [
    accState === 'conflict' ? { label: t('accChoose'), onclick: () => { accReconcile(); } } : null,
    { label: t('accDelete'), onclick: () => { askConfirm(t('accDeleteAsk'), accDeleteCloud); } },
    { label: t('accLogout'), primary: true, onclick: () => { accSignOut(); } },
  ].filter(Boolean));
}
async function accDeleteCloud() {
  try {
    if (!(await accEnsureToken())) return;
    const r = await accFetch('/rest/v1/user_data?user_id=eq.' + encodeURIComponent(accSession.user.id), { method: 'DELETE' });
    if (!r.ok) throw new Error('delete ' + r.status);
    accLs.del(accBaseKey());
    await accSignOut();
    showBanner('ok', t('accDeleted'));
  } catch (e) {
    accSetState('error');
  }
}
async function accInit() {
  if (!ACC_CFG) return;
  accLoadSession();
  await accHandleReturn();
  if (accSs.get(ACC_APPLIED_KEY)) { accSs.del(ACC_APPLIED_KEY); accJustApplied = true; showBanner('ok', t('accApplied')); }
  renderTopbar();
  if (!accSession) return;
  await accReconcile();
  accStartSync();
}

/* ==============================================================================
   INIT
   ============================================================================== */""")
rep("if (location.hash === SHOP_HASH) showShop(); else showCover();",
    "if (location.hash === SHOP_HASH) showShop(); else if (!accSkipCover()) showCover();\naccInit();")

s = s.replace('      python3 welcome.py', '      python3 welcome.py')
open(out, 'w', encoding='utf8').write(s)
print('account -> %s (%s)' % (out, 'on' if cfg else 'off: empty config'))
