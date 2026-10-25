"""Modern look (system fonts, clean surfaces) + opening cover.
Usage: python3 -I modern.py in.html out.html   (run after help.py)"""
import sys
from urllib.parse import quote

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('modern anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

def svg_url(svg):
    return "url(\"data:image/svg+xml," + quote(svg, safe=" =:/,.-") + "\")"

HORN = ('<path d="M20 13C20 7 25 3.5 29.5 5C33.5 6.5 33 11 29.8 11C27.6 11 27 8.6 29 8"/>'
        '<path d="M20 13C20 7 15 3.5 10.5 5C6.5 6.5 7 11 10.2 11C12.4 11 13 8.6 11 8"/>')
# Cover pattern: rows of ram's-horn motifs, offset every other row.
pattern = svg_url('<svg xmlns="http://www.w3.org/2000/svg" width="80" height="40" viewBox="0 0 80 40">'
                  '<g fill="none" stroke="#e2b85c" stroke-width="1.3" stroke-linecap="round" opacity=".5">'
                  '<g transform="translate(0 2)">%s</g><g transform="translate(40 2)">%s</g>'
                  '<g transform="translate(20 22)">%s</g><g transform="translate(60 22)">%s</g>'
                  '<g transform="translate(-20 22)">%s</g></g></svg>' % ((HORN,) * 5))
big_mark = svg_url('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">'
                   '<g fill="none" stroke="#ffffff" stroke-width="1.5" stroke-linecap="round">'
                   '<circle cx="16" cy="16" r="9.5"/>'
                   '<path d="M12.6 7.2C11.4 13 11.4 19 12.6 24.8M19.4 7.2C20.6 13 20.6 19 19.4 24.8'
                   'M7.2 12.6C13 11.4 19 11.4 24.8 12.6M7.2 19.4C13 20.6 19 20.6 24.8 19.4"/></g>'
                   '<g stroke="#e2b85c" stroke-width="1.5" stroke-linecap="round">'
                   '<path d="M16 2.5V5M16 27V29.5M2.5 16H5M27 16H29.5M6.5 6.5L8.3 8.3M23.7 23.7L25.5 25.5'
                   'M25.5 6.5L23.7 8.3M8.3 23.7L6.5 25.5"/></g></svg>')

css = """
  /* ==========================================================================
     MODERN — system fonts, clean surfaces, soft shadows; ornament kept subtle.
     Layout: top bar in two rows (brand · tabs · help · actions / work fields).
     ========================================================================== */
  :root {
    --bg: #f3f5f8; --surface: #ffffff; --surface-2: #f6f8fb; --ink: #111827; --ink-2: #586374;
    --line: #e3e8ef; --line-strong: #cfd7e2; --accent: #0b66b0; --accent-ink: #ffffff; --accent-soft: #e7f1fa;
    --gold: #c08a22; --gold-soft: #f8eed6; --ok: #16a34a; --stage-empty: #e6ebf1; --mark: #ffe08a;
    --overlay: rgba(15, 23, 42, .45);
    --font: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Segoe UI Variable Text", "Segoe UI", Roboto, "Noto Sans", Arial, sans-serif;
    --display: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI Variable Display", "Segoe UI", Roboto, "Noto Sans", Arial, sans-serif;
    --radius: 14px;
    --shadow-sm: 0 1px 2px rgba(16, 24, 40, .05);
    --shadow: 0 1px 3px rgba(16, 24, 40, .06), 0 10px 28px rgba(16, 24, 40, .07);
    --cover-pattern: %(pattern)s; --cover-mark: %(big_mark)s;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #0c1118; --surface: #141b24; --surface-2: #19222d; --ink: #e8edf3; --ink-2: #9ca8b6;
      --line: #263140; --line-strong: #364253; --accent: #5aaaf0; --accent-ink: #061f36; --accent-soft: #14304b;
      --gold: #d8b25e; --gold-soft: #33290f; --ok: #3fb97a; --stage-empty: #222c38; --mark: #7a5f12;
      --overlay: rgba(0, 0, 0, .6); --shadow-sm: none; --shadow: 0 0 0 1px rgba(255, 255, 255, .04); color-scheme: dark;
    }
  }
  :root[data-theme="dark"] {
    --bg: #0c1118; --surface: #141b24; --surface-2: #19222d; --ink: #e8edf3; --ink-2: #9ca8b6;
    --line: #263140; --line-strong: #364253; --accent: #5aaaf0; --accent-ink: #061f36; --accent-soft: #14304b;
    --gold: #d8b25e; --gold-soft: #33290f; --ok: #3fb97a; --stage-empty: #222c38; --mark: #7a5f12;
    --overlay: rgba(0, 0, 0, .6); --shadow-sm: none; --shadow: 0 0 0 1px rgba(255, 255, 255, .04); color-scheme: dark;
  }
  body { -webkit-font-smoothing: antialiased; }

  /* Top bar */
  .topbar { background: var(--surface); border-bottom: 1px solid var(--line); box-shadow: var(--shadow-sm); padding: 12px 20px 16px; gap: 10px 14px; }
  .topbar::after { height: 6px; opacity: .45; background-size: 24px 6px; }
  .brand { margin-right: 6px; gap: 10px; }
  .brand-mark { width: 34px; height: 34px; }
  .brand h1 { font-family: var(--display); font-size: 18px; font-weight: 700; letter-spacing: -.01em; }
  .brand p { font-size: 12px; }
  .tb-field label { font-size: 12px; font-weight: 600; color: var(--ink-2); }
  .tabs { background: var(--surface-2); border: 1px solid var(--line); border-radius: 12px; padding: 4px; gap: 2px; }
  .tab { border-radius: 9px; padding: 7px 16px; color: var(--ink-2); font-weight: 600; transition: background .15s, color .15s; }
  .tab:hover { color: var(--ink); }
  .tab[aria-selected="true"] { background: var(--surface); color: var(--accent); box-shadow: var(--shadow-sm), 0 0 0 1px var(--line); }
  /* Row 1: brand · tabs · help (right). Row 2: work fields · actions (right). */
  @media (min-width: 901px) {
    .topbar::before { content: ""; order: 5; flex-basis: 100%%; height: 0; }   /* line break */
    .brand { order: 0; }
    .tabs { order: 1; }
    .help-btn { order: 2; margin-left: auto; }
    .tb-field { order: 6; flex: 1 1 170px; max-width: 260px; min-width: 0; }
    .tb-field:has(#tb-grade) { flex: 0 0 110px; }
    .tb-field input, .tb-field select { width: 100%%; }
    .tb-actions { order: 7; margin-left: auto; align-self: flex-end; gap: 6px; }
    .tb-actions .btn { padding: 8px 12px; font-size: 14px; }
    .save-status { order: 3; min-width: 0; }
  }
  @media (max-width: 900px) {
    .app { grid-template-columns: minmax(0, 1fr); }
    .tab { padding: 7px 8px; min-width: 0; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .save-status { order: 8; flex-basis: 100%%; }
    .save-status:not(.off) { display: none; }   /* phones: only the "not saved" warning */
  }
  @media (max-width: 520px) {
    .nav-text { display: none; }
    .nav-toggle, .more-toggle, .help-btn { padding: 8px 11px; }
    .brand h1 { font-size: 15.5px; }
    .tabs { padding: 3px; }
    .tab { padding: 7px 4px; font-size: 13.5px; }
  }
  @media (max-width: 420px) { .brand-mark { display: none; } }

  /* Controls */
  .btn {
    border-radius: 10px; border: 1px solid var(--line-strong); background: var(--surface);
    padding: 8px 14px; font-weight: 500; transition: background .15s, border-color .15s, box-shadow .15s, filter .15s;
  }
  .btn:hover { background: var(--surface-2); border-color: var(--line-strong); }
  .btn.primary { background: var(--accent); border-color: var(--accent); color: var(--accent-ink); box-shadow: 0 1px 2px rgba(11, 102, 176, .25); }
  .btn.primary:hover { background: var(--accent); filter: brightness(1.07); }
  .btn.danger { color: var(--danger); }
  input[type=text], input[type=search], select, textarea {
    border-radius: 10px; border: 1px solid var(--line-strong); padding: 9px 12px; background: var(--surface);
    transition: border-color .15s, box-shadow .15s;
  }
  input:focus, select:focus, textarea:focus { outline: none; border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
  .help-btn .help-q { background: var(--gold); }

  /* Sidebar */
  .sidebar { background: var(--surface); border-right: 1px solid var(--line); padding: 16px 12px; }
  .sidebar h2 { color: var(--ink-2); font-size: 11px; letter-spacing: .09em; }
  .step-btn { border-radius: 10px; padding: 7px 10px; border-color: transparent; }
  .step-btn:hover { background: var(--surface-2); border-color: transparent; }
  .step-btn[aria-current="step"], .step-btn[aria-current="page"] { background: var(--accent-soft); border-color: transparent; color: var(--accent); }
  .step-btn[aria-current] .step-label { font-weight: 600; }
  .step-num { border: 0; background: var(--surface-2); color: var(--ink-2); box-shadow: inset 0 0 0 1px var(--line); }
  .step-btn.done .step-num { background: var(--ok); color: #fff; box-shadow: none; }

  /* Content */
  .main { padding: 28px 36px 44px; }
  .main-inner { max-width: 920px; }
  .ws-kicker { color: var(--accent); letter-spacing: .07em; font-size: 12px; }
  .ws-kicker::before { display: none; }
  .ws-title { font-family: var(--display); font-size: 28px; font-weight: 750; letter-spacing: -.02em; line-height: 1.2; margin-bottom: 6px; }
  .ws-meta, .ws-intro { color: var(--ink-2); }
  .card { border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow-sm); padding: 18px 20px; margin-bottom: 14px; }
  .field-label { font-weight: 600; font-size: 15px; }
  .banner { border-radius: 12px; }
  .stage-bar { border-radius: 8px 8px 0 0; }
  .lib-card { border-radius: var(--radius); box-shadow: var(--shadow-sm); transition: box-shadow .15s; }
  .lib-card:hover { box-shadow: var(--shadow); }
  .lib-card.active { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
  .g-body { font-size: 16px; line-height: 1.7; }
  .g-sub, .lib-card h3, .help-body h3 { font-family: var(--display); font-weight: 700; letter-spacing: -.01em; }
  .footer { background: var(--surface); border-top: 1px solid var(--line); padding: 12px 24px; }
  .progress-track { height: 8px; }
  .dlg { border-radius: 18px; padding: 22px 24px; box-shadow: 0 24px 64px rgba(0, 0, 0, .25); }
  .dlg h2 { font-family: var(--display); font-weight: 700; letter-spacing: -.01em; }
  @media (max-width: 900px) {
    .main { padding: 18px max(16px, env(safe-area-inset-right, 0px)) 30px max(16px, env(safe-area-inset-left, 0px)); }
    .ws-title { font-size: 23px; }
  }

  /* COVER — shown when the site opens */
  .cover-overlay {
    position: fixed; inset: 0; z-index: 60; display: flex; align-items: center; justify-content: center;
    padding: 16px; background: rgba(8, 20, 36, .55); -webkit-backdrop-filter: blur(6px); backdrop-filter: blur(6px);
    animation: coverFade .25s ease;
  }
  .cover {
    width: 100%%; max-width: 860px; max-height: 94%%; overflow: auto; display: grid; grid-template-columns: 290px minmax(0, 1fr);
    background: var(--surface); color: var(--ink); border-radius: 22px; box-shadow: 0 30px 90px rgba(0, 0, 0, .35);
    animation: coverIn .3s ease;
  }
  .cover-art {
    position: relative; overflow: hidden; display: flex; flex-direction: column; justify-content: space-between; gap: 20px;
    min-height: 380px; padding: 28px 26px; color: #fff;
    background: linear-gradient(160deg, #0d5a97 0%%, #0a3d68 55%%, #072a4a 100%%);
  }
  .cover-art::before { content: ""; position: absolute; inset: 0; background: var(--cover-pattern) 0 0 / 80px 40px; opacity: .55; }
  .cover-art > * { position: relative; }
  .cover-mark { width: 96px; height: 96px; background: var(--cover-mark) center / contain no-repeat; }
  .cover-art-title { font-family: var(--display); font-size: 15px; font-weight: 600; letter-spacing: .04em; line-height: 1.4; opacity: .95; }
  .cover-art-foot { font-size: 13px; opacity: .85; }
  .cover-body { display: flex; flex-direction: column; gap: 14px; padding: 30px 30px 24px; min-width: 0; }
  .cover-kicker { margin: 0; font-size: 12px; font-weight: 700; letter-spacing: .08em; color: var(--accent); }
  .cover-body h1 { margin: 0; font-family: var(--display); font-size: 32px; font-weight: 800; letter-spacing: -.02em; line-height: 1.12; text-wrap: balance; }
  .cover-lead { display: grid; gap: 8px; color: var(--ink-2); font-size: 15px; line-height: 1.6; }
  .cover-lead p { margin: 0; }
  .cover-lead p:first-child { color: var(--ink); font-weight: 600; }
  .cover-feats-title {
    margin: 6px 0 0; padding-top: 14px; border-top: 1px solid var(--line);
    font-family: var(--display); font-size: 13px; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; color: var(--accent);
  }
  .cover-feats { list-style: none; margin: 2px 0; padding: 0; display: grid; gap: 8px; }
  .cover-feats li { display: flex; gap: 10px; align-items: flex-start; font-size: 14.5px; line-height: 1.45; }
  .cover-feats li::before {
    content: "✓"; flex: none; display: inline-flex; align-items: center; justify-content: center;
    width: 22px; height: 22px; border-radius: 50%%; background: var(--accent-soft); color: var(--accent); font-size: 13px; font-weight: 700;
  }
  .cover-author { margin: 0; font-size: 13px; color: var(--ink-2); }
  .cover-actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 4px; }
  .cover-actions .btn { padding: 11px 20px; font-size: 15px; font-weight: 600; }
  .cover-hide { display: flex; align-items: center; gap: 8px; font-size: 13px; color: var(--ink-2); cursor: pointer; }
  .cover-hide input { width: 16px; height: 16px; accent-color: var(--accent); }
  @keyframes coverFade { from { opacity: 0; } to { opacity: 1; } }
  @keyframes coverIn { from { opacity: 0; transform: translateY(14px) scale(.98); } to { opacity: 1; transform: none; } }
  @media (max-width: 680px) {
    .cover { grid-template-columns: 1fr; border-radius: 18px; }
    .cover-art { min-height: 0; flex-direction: row; align-items: center; padding: 18px 20px; gap: 14px; }
    .cover-mark { width: 56px; height: 56px; flex: none; }
    .cover-art-foot { display: none; }
    .cover-body { padding: 20px 20px 18px; gap: 12px; }
    .cover-body h1 { font-size: 26px; }
    .cover-actions .btn { flex: 1 1 auto; }
  }
  @media (prefers-reduced-motion: reduce) {
    .cover-overlay, .cover { animation: none; }
    .btn, .tab, .lib-card, input, select, textarea { transition: none; }
  }
""" % dict(pattern=pattern, big_mark=big_mark)

rep("  /* ---------- PRINT (A4) ---------- */", css + "\n  /* ---------- PRINT (A4) ---------- */")
# «Сақталды» moves out of the actions group into row 1 (next to «Көмек»).
rep(",\n      h('span', { id: 'save-status', class: 'save-status', 'aria-live': 'polite' })),\n  );",
    "),\n    h('span', { id: 'save-status', class: 'save-status', 'aria-live': 'polite' }),\n  );")
# Phones: the drawer button shows only «☰» so the title has room.
rep("onclick: openNav }, '☰ ', t(state.ui.tab === 'guide' ? 'navGuide' : 'navBook')),",
    "onclick: openNav }, h('span', { 'aria-hidden': 'true' }, '☰'), h('span', { class: 'nav-text' }, ' ' + t(state.ui.tab === 'guide' ? 'navGuide' : 'navBook'))),")
rep("    #print-area { display: block; }", "    #print-area { display: block; }\n    .cover-overlay, .dlg-overlay { display: none !important; }")

rep("  helpBtn: 'Көмек',", """  coverKicker: 'ӘДІСТЕМЕЛІК ҚҰРАЛ',
  coverArtTitle: 'Көркем шығарманы талдауға арналған тегін платформа',
  coverLead: [
    'Жасанды интеллект кез келген мәтінді бір сәтте мазмұндап беретін заманда көркем әдебиетті оқытудың мәні ақпарат алумен шектелмейді.',
    'Көркем шығарманы талдау оқушыға өзіндік пікір қалыптастыруға үйретеді. Шығарма талдау арқылы оқырман сұрақ қоюға, мәтіннен дәлел іздеуге, тұжырымын тексеруге бейімделеді. Көркем шығарма эмпатияны, сыни ойлауды және өз бетінше ой түюді дамытады.',
    'Бұл құрал мұғалімдер мен жалпы оқырман қауымға осы жолда көмекші болмақ.',
  ],
  coverFeatsTitle: 'Мүмкіндіктері',
  coverFeats: [
    'Шығарманы жанрына қарай кезең-кезеңімен талдау',
    'Әдістемелік нұсқаулық: 16 бөлім, әр параққа сілтеме, ішінен іздеу',
    '45 минуттық сабақ жоспары мен бағалау рубрикасы жауаптарыңыздан өзі құрылады',
    'Талдаулар осы браузерде сақталады, интернетсіз де жұмыс істейді, оқушы деректері жиналмайды',
  ],
  coverAuthor: 'Құрастырған: Бекжанова Сара · Алматы, 2026',
  coverStart: 'Бастау',
  coverHelp: 'Қалай қолдану керек?',
  coverHide: 'Келесі жолы көрсетпеу',
  helpBtn: 'Көмек',""")

# Cover replaces the first-visit help.
a = s.index('function showHelpOnFirstVisit() {')
b = s.index('/* ==============================================================================\n   INIT')
s = s[:a] + """/* ---- COVER — the opening window (until «Келесі жолы көрсетпеу» is ticked) ---- */
const COVER_HIDDEN_KEY = 'kobem-talday:cover-hidden';

function showCover(force) {
  let hidden = false;
  try { hidden = !!window.localStorage.getItem(COVER_HIDDEN_KEY); } catch (e) { hidden = false; }
  if (hidden && !force) return;
  const prev = document.activeElement;
  const hide = h('input', { type: 'checkbox', id: 'cover-hide' });
  hide.checked = hidden;
  const overlay = h('div', { class: 'cover-overlay' });
  const close = then => {
    try {
      if (hide.checked) window.localStorage.setItem(COVER_HIDDEN_KEY, '1');
      else window.localStorage.removeItem(COVER_HIDDEN_KEY);
    } catch (e) { /* storage blocked */ }
    overlay.remove();
    if (then) then(); else if (prev && prev.focus) prev.focus();
  };
  const start = h('button', { class: 'btn primary', type: 'button', text: t('coverStart'), onclick: () => close() });
  overlay.append(h('div', { class: 'cover', role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'cover-title' },
    h('div', { class: 'cover-art', 'aria-hidden': 'true' },
      h('div', { class: 'cover-mark' }),
      h('div', { class: 'cover-art-title', text: t('coverArtTitle') }),
      h('div', { class: 'cover-art-foot', text: 'korkemtaldau.com' })),
    h('div', { class: 'cover-body' },
      h('p', { class: 'cover-kicker', text: t('coverKicker') }),
      h('h1', { id: 'cover-title', text: t('appTitle') }),
      h('div', { class: 'cover-lead' }, STRINGS.coverLead.map(x => h('p', { text: x }))),
      h('h2', { class: 'cover-feats-title', text: t('coverFeatsTitle') }),
      h('ul', { class: 'cover-feats' }, STRINGS.coverFeats.map(x => h('li', { text: x }))),
      h('p', { class: 'cover-author', text: t('coverAuthor') }),
      h('div', { class: 'cover-actions' },
        start,
        h('button', { class: 'btn', type: 'button', text: t('coverHelp'), onclick: () => close(showHelp) })),
      h('label', { class: 'cover-hide', for: 'cover-hide' }, hide, t('coverHide')))));
  overlay.addEventListener('click', e => { if (e.target === overlay) close(); });
  overlay.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  document.body.append(overlay);
  start.focus({ preventScroll: true });   // keep the cover scrolled to its top on small screens
  overlay.firstChild.scrollTop = 0;
}

""" + s[b:]
rep("showHelpOnFirstVisit();", "showCover();")
# The brand opens the cover again (also after «Келесі жолы көрсетпеу»).
rep("    h('div', { class: 'brand' },\n      h('span', { class: 'brand-mark', 'aria-hidden': 'true' }),",
    "    h('div', { class: 'brand', role: 'button', tabindex: '0', title: t('appTitle'), style: 'cursor:pointer',\n"
    "      onclick: () => showCover(true), onkeydown: e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); showCover(true); } } },\n"
    "      h('span', { class: 'brand-mark', 'aria-hidden': 'true' }),")

rep("      python3 help.py library.html kobem-talday.html    # «Қалай қолдану керек?»",
    "      python3 help.py library.html helped.html          # «Қалай қолдану керек?»\n"
    "      python3 modern.py helped.html kobem-talday.html   # modern look + opening cover")

open(out, 'w', encoding='utf8').write(s)
print('wrote', out, len(s.encode('utf8')) // 1024, 'KB')
