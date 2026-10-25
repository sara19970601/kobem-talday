"""Design layer: national ornament theme + phone/tablet layout.
Usage: python3 -I theme.py in.html out.html   (run after assemble.py)"""
import sys
from urllib.parse import quote

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('theme anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

def svg_url(svg):
    return "url(\"data:image/svg+xml," + quote(svg, safe=" =:/,.-") + "\")"

# Қошқар мүйіз (ram's horn) band and a single motif; шаңырақ mark.
def band(gold):
    return svg_url(
        '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="14" viewBox="0 0 40 14">'
        '<g fill="none" stroke="%s" stroke-width="1.4" stroke-linecap="round">'
        '<path d="M0 13H40"/>'
        '<path d="M20 13C20 7 25 3.5 29.5 5C33.5 6.5 33 11 29.8 11C27.6 11 27 8.6 29 8"/>'
        '<path d="M20 13C20 7 15 3.5 10.5 5C6.5 6.5 7 11 10.2 11C12.4 11 13 8.6 11 8"/>'
        '</g></svg>' % gold)

def motif(gold):
    return svg_url(
        '<svg xmlns="http://www.w3.org/2000/svg" width="26" height="14" viewBox="7 2 26 12">'
        '<g fill="none" stroke="%s" stroke-width="1.6" stroke-linecap="round">'
        '<path d="M20 13C20 7 25 3.5 29.5 5C33.5 6.5 33 11 29.8 11C27.6 11 27 8.6 29 8"/>'
        '<path d="M20 13C20 7 15 3.5 10.5 5C6.5 6.5 7 11 10.2 11C12.4 11 13 8.6 11 8"/>'
        '</g></svg>' % gold)

def shanyrak(blue, gold):
    return svg_url(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
        '<g fill="none" stroke="%s" stroke-width="1.7" stroke-linecap="round">'
        '<circle cx="16" cy="16" r="9.5"/>'
        '<path d="M12.6 7.2C11.4 13 11.4 19 12.6 24.8M19.4 7.2C20.6 13 20.6 19 19.4 24.8'
        'M7.2 12.6C13 11.4 19 11.4 24.8 12.6M7.2 19.4C13 20.6 19 20.6 24.8 19.4"/></g>'
        '<g stroke="%s" stroke-width="1.7" stroke-linecap="round">'
        '<path d="M16 2.5V5M16 27V29.5M2.5 16H5M27 16H29.5M6.5 6.5L8.3 8.3M23.7 23.7L25.5 25.5'
        'M25.5 6.5L23.7 8.3M8.3 23.7L6.5 25.5"/></g></svg>' % (blue, gold))

LIGHT = dict(blue='#0f5c8c', gold='#b8892a')
DARK = dict(blue='#6cb4e4', gold='#d6ad55')

theme_css = """
  /* ==========================================================================
     THEME — ұлттық нақыш: көк (sky) and алтын (gold), қошқар мүйіз band,
     шаңырақ mark. Layout: sidebar becomes a drawer below 900px.
     ========================================================================== */
  :root {
    --bg: #f5f3ec; --surface: #ffffff; --surface-2: #f9f7f1; --ink: #18222e; --ink-2: #4f5b69;
    --line: #ddd5c3; --accent: #0f5c8c; --accent-ink: #ffffff; --accent-soft: #e2edf6;
    --gold: #b8892a; --gold-soft: #f5ead0; --stage-empty: #e6e0d2; --mark: #f8dd8a;
    --display: "PT Serif", Cambria, "Noto Serif", "DejaVu Serif", Georgia, serif;
    --orn-band: %(band_l)s; --orn-motif: %(motif_l)s; --brand-mark: %(mark_l)s;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #101820; --surface: #18222d; --surface-2: #141d27; --ink: #e8ecef; --ink-2: #a5b0bb;
      --line: #2f3c49; --accent: #6cb4e4; --accent-ink: #08223a; --accent-soft: #16324a;
      --gold: #d6ad55; --gold-soft: #3a2f16; --stage-empty: #283442; --mark: #7a5f12;
      --orn-band: %(band_d)s; --orn-motif: %(motif_d)s; --brand-mark: %(mark_d)s; color-scheme: dark;
    }
  }
  :root[data-theme="dark"] {
    --bg: #101820; --surface: #18222d; --surface-2: #141d27; --ink: #e8ecef; --ink-2: #a5b0bb;
    --line: #2f3c49; --accent: #6cb4e4; --accent-ink: #08223a; --accent-soft: #16324a;
    --gold: #d6ad55; --gold-soft: #3a2f16; --stage-empty: #283442; --mark: #7a5f12;
    --orn-band: %(band_d)s; --orn-motif: %(motif_d)s; --brand-mark: %(mark_d)s; color-scheme: dark;
  }

  .topbar { position: relative; padding-bottom: 16px; }
  .topbar::after {
    content: ""; position: absolute; left: 0; right: 0; bottom: 0; height: 9px;
    background: var(--orn-band) repeat-x left bottom / 30px 9px; opacity: .85; pointer-events: none;
  }
  .brand { display: flex; align-items: center; gap: 10px; }
  .brand-mark { flex: none; width: 38px; height: 38px; background: var(--brand-mark) center / contain no-repeat; }
  .brand h1 { font-family: var(--display); font-size: 20px; letter-spacing: .01em; }
  .ws-title, .g-sub { font-family: var(--display); }
  .ws-title { font-size: 25px; line-height: 1.25; text-wrap: balance; }
  .ws-kicker { color: var(--gold); letter-spacing: .08em; display: flex; align-items: center; gap: 8px; }
  .ws-kicker::before {
    content: ""; flex: none; width: 24px; height: 12px; background: var(--orn-motif) center / contain no-repeat;
  }
  .sidebar h2 { color: var(--gold); letter-spacing: .08em; }
  .tab[aria-selected="true"] { box-shadow: inset 0 -2px 0 var(--gold); }
  .btn.primary:hover { filter: brightness(1.08); }
  .progress-fill { background: linear-gradient(90deg, var(--accent), var(--gold)); }
  .step-btn.done .step-num { background: var(--accent); border-color: var(--accent); }
  .card { overflow-x: auto; }
  .guide .ws-title { margin-bottom: 14px; }
  .g-count { background: var(--gold); color: #1b1407; }

  /* Hidden on wide screens; shown by the small-screen rules below. */
  .nav-toggle, .more-toggle { display: none; }
  .nav-scrim { display: none; }

  @media (max-width: 900px) {
    .app {
      grid-template-columns: 1fr;
      grid-template-rows: auto minmax(0, 1fr) auto;
      grid-template-areas: "top" "main" "foot";
    }
    .sidebar {
      position: fixed; z-index: 40; top: 0; bottom: 0; left: 0;
      width: min(86vw, 340px); max-height: none;
      padding: calc(14px + env(safe-area-inset-top, 0px)) 10px calc(14px + env(safe-area-inset-bottom, 0px)) max(10px, env(safe-area-inset-left, 0px));
      border-right: 1px solid var(--line); border-bottom: 0;
      transform: translateX(-105%%); transition: transform .22s ease; box-shadow: 0 0 40px rgba(0, 0, 0, .25);
      visibility: hidden;
    }
    body.nav-open .sidebar { transform: none; visibility: visible; }
    body.nav-open .nav-scrim { display: block; position: fixed; inset: 0; z-index: 35; background: var(--overlay); }
    .sidebar h2, .privacy { display: block; }
    .steps { display: block; overflow: visible; }
    .step-btn { white-space: normal; width: 100%%; }

    .topbar { align-items: center; gap: 8px 10px; padding-left: max(12px, env(safe-area-inset-left, 0px)); padding-right: max(12px, env(safe-area-inset-right, 0px)); }
    .nav-toggle, .more-toggle { display: inline-flex; align-items: center; gap: 6px; min-height: 42px; }
    .nav-toggle { order: 0; }
    .brand { order: 1; flex: 1 1 0; min-width: 0; margin-right: 0; }
    .brand > div { min-width: 0; }
    .brand h1 { font-size: 17px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .brand p { display: none; }
    .brand-mark { width: 30px; height: 30px; }
    .more-toggle { order: 2; }
    .tabs { order: 3; flex: 1 1 100%%; }
    .tabs .tab { flex: 1; min-height: 40px; }
    .tb-field { order: 4; flex: 1 1 calc(50%% - 10px); min-width: 0; }
    .tb-field input { width: 100%%; }
    .tb-actions { order: 5; flex: 1 1 100%%; display: none; }
    .topbar.more-open .tb-actions { display: flex; }
    .tb-actions .btn { flex: 1 1 calc(50%% - 6px); min-height: 42px; }
    .save-status { flex-basis: 100%%; }
    .main { padding: 16px max(16px, env(safe-area-inset-right, 0px)) 28px max(16px, env(safe-area-inset-left, 0px)); }
    .footer { padding: 8px max(12px, env(safe-area-inset-right, 0px)) calc(8px + env(safe-area-inset-bottom, 0px)) max(12px, env(safe-area-inset-left, 0px)); gap: 10px; }
    .footer .btn { min-height: 42px; }
  }
  @media (max-width: 600px) {
    .tb-field { display: none; }
    .topbar.more-open .tb-field { display: flex; flex-basis: 100%%; }
    .ws-title { font-size: 21px; }
    input[type=text], input[type=search], select, textarea { font-size: 16px; }   /* no iOS zoom on focus */
    .ws-table:has(th:nth-child(4)) { min-width: 560px; }
    .footer .btn { padding: 7px 10px; }
    .progress-label { font-size: 11px; }
    .stage-names span { font-size: 10.5px; }
  }
  @media (pointer: coarse) {
    .step-btn { min-height: 44px; align-items: center; }
    .chip { padding: 8px 14px; }
  }
  @media (prefers-reduced-motion: reduce) {
    .sidebar { transition: none; }
  }
""" % dict(band_l=band(LIGHT['gold']), motif_l=motif(LIGHT['gold']), mark_l=shanyrak(LIGHT['blue'], LIGHT['gold']),
           band_d=band(DARK['gold']), motif_d=motif(DARK['gold']), mark_d=shanyrak(DARK['blue'], DARK['gold']))

# Theme CSS goes last in the screen styles, before the print block.
rep("  /* ---------- PRINT (A4) ---------- */", theme_css + "\n  /* ---------- PRINT (A4) ---------- */")

# Strings
rep("  tabBook: 'Дәптер',", """  navBook: 'Парақтар',
  navGuide: 'Бөлімдер',
  navOpen: 'Тізімді ашу',
  moreToggle: 'Шығарма және әрекеттер',
  tabBook: 'Дәптер',""")

# Top bar: drawer toggle + brand mark + "more" toggle
rep("""  bar.replaceChildren(
    h('div', { class: 'brand' },
      h('h1', { text: t('appTitle') }),""", """  bar.classList.toggle('more-open', moreOpen);
  bar.replaceChildren(
    h('button', { class: 'btn nav-toggle', type: 'button', 'aria-label': t('navOpen'),
      'aria-expanded': document.body.classList.contains('nav-open') ? 'true' : 'false',
      onclick: openNav }, '☰ ', t(state.ui.tab === 'guide' ? 'navGuide' : 'navBook')),
    h('div', { class: 'brand' },
      h('span', { class: 'brand-mark', 'aria-hidden': 'true' }),
      h('div', null,
      h('h1', { text: t('appTitle') }),""")
rep("""      h('p', { text: t('appSubtitle') })),
    h('div', { class: 'tabs',""", """      h('p', { text: t('appSubtitle') }))),
    h('button', { class: 'btn more-toggle', type: 'button', 'aria-label': t('moreToggle'), title: t('moreToggle'),
      'aria-expanded': moreOpen ? 'true' : 'false',
      onclick: e => {
        moreOpen = !moreOpen;
        bar.classList.toggle('more-open', moreOpen);
        e.currentTarget.setAttribute('aria-expanded', moreOpen ? 'true' : 'false');
      } }, '⚙'),
    h('div', { class: 'tabs',""")

# Drawer helpers (before goTo) and closing it on navigation.
rep("""function goTo(key) {
  state.ui.step = key;""", """/* ---- Small screens: sidebar drawer + collapsible top bar ---- */
let moreOpen = false;
function openNav() {
  document.body.classList.add('nav-open');
  const cur = document.querySelector('#sidebar [aria-current]');
  const first = cur || document.querySelector('#sidebar button, #sidebar input');
  if (first) first.focus();
}
function closeNav() { document.body.classList.remove('nav-open'); }

function goTo(key) {
  closeNav();
  state.ui.step = key;""")
rep("""function showGuideSection(id) {
  state.ui.guideSection = id;""", """function showGuideSection(id) {
  closeNav();
  state.ui.guideSection = id;""")
rep("""document.getElementById('import-file').addEventListener('change', e => {""", """document.body.append(h('div', { class: 'nav-scrim', onclick: closeNav }));
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeNav(); });

document.getElementById('import-file').addEventListener('change', e => {""")

# README pipeline line
rep("      python3 assemble.py base.html worksheets.json guide.json kobem-talday.html",
    "      python3 assemble.py base.html worksheets.json guide.json app.html\n"
    "      python3 theme.py app.html kobem-talday.html       # ornament theme + phone/tablet layout")

open(out, 'w', encoding='utf8').write(s)
print('wrote', out, len(s.encode('utf8')) // 1024, 'KB')
