"""Focus mode (design, step 3.1): new colours and fonts for the whole site, a one-row header,
the work card («Жанр · Шығарма · Сынып ✎») with the level switch, and a three-column lab:
steps on the left, one question at a time in the middle, «Кеңес | Мысал | Дереккөз» on the right.
Fonts: Inter and Literata (OFL), Latin + Cyrillic + Cyrillic Ext subsets, embedded.
Usage: python3 -I focus.py in.html fonts_dir out.html   (run after merge.py)"""
import base64, os, re, sys

src, fdir, out = sys.argv[1:4]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('focus anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

def rep_fn(name, new):
    """Replace a whole top-level function (from `function name(` to its closing `}` line)."""
    global s
    m = re.search(r'\nfunction ' + re.escape(name) + r'\(.*?\n\}\n', s, re.S)
    if not m:
        sys.exit('focus: function %s not found' % name)
    s = s[:m.start()] + '\n' + new.strip('\n') + '\n' + s[m.end():]

# ---- Fonts ----
RANGES = {
    'latin': 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD',
    'cyrillic': 'U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116',
    'cyrillic-ext': 'U+0460-052F,U+1C80-1C8A,U+20B4,U+2DE0-2DFF,U+A640-A69F,U+FE2E-FE2F',
}
faces = []
for fam, name, wght in [('inter', 'Inter', '100 900'), ('literata', 'Literata', '200 900')]:
    for sub, rng in RANGES.items():
        path = os.path.join(fdir, 'fontsource-variable-%s-5.3.0/package/files/%s-%s-wght-normal.woff2' % (fam, fam, sub))
        data = base64.b64encode(open(path, 'rb').read()).decode('ascii')
        faces.append('  @font-face { font-family: "%s"; font-style: normal; font-display: swap; font-weight: %s;\n'
                     '    src: url(data:font/woff2;base64,%s) format("woff2"); unicode-range: %s; }' % (name, wght, data, rng))

# ---- CSS ----
rep('</style>\n</head>', """</style>
<style id="fonts">
  /* FONTS — Inter (interface) and Literata (headings), SIL Open Font License 1.1, via Fontsource. */
%s
</style>
<style id="focus">
  /* FOCUS — palette (light), fonts, one-row header, work card, three-column lab */
  :root {
    --bg: #F7F4EE; --surface: #FFFFFF; --surface-2: #FBF9F4; --ink: #17233B; --ink-2: #4A556B;
    --line: #D9D2C2; --line-strong: #C9C0AC; --accent: #234A8F; --accent-hover: #17356B; --accent-ink: #FFFFFF; --accent-soft: #E8EEF9;
    --gold: #C98B2B; --gold-ink: #8A5A12; --gold-soft: #F6ECD9; --ok: #2F5A2A; --ok-soft: #E4EEDF;
    --font: "Inter", -apple-system, "Segoe UI", Roboto, "Noto Sans", Arial, sans-serif;
    --display: "Literata", "PT Serif", Georgia, "Noto Serif", serif;
  }
  body { background: var(--bg); color: var(--ink); font-family: var(--font); }
  h1, h2, h3, .ws-title, .lab-step-title, .cover h1, .k-group-title, .gl-sec-title { font-family: var(--display); }
  .btn.primary { background: var(--accent); border-color: var(--accent); color: var(--accent-ink); }
  .btn.primary:hover { background: var(--accent-hover); border-color: var(--accent-hover); }
  .btn:focus-visible, .tab:focus-visible, select:focus-visible, input:focus-visible, textarea:focus-visible, summary:focus-visible {
    outline: 3px solid var(--gold); outline-offset: 2px; }

  /* Header: one row (brand, sections, save state, buy, help) */
  .topbar { display: block; padding: 0; }
  .hdr { display: flex; align-items: center; gap: 10px 16px; padding: 10px 20px; }
  .hdr .brand { flex: none; margin: 0; }
  .hdr .brand h1 { font-size: 19px; }
  .hdr .tabs { order: 0; flex: 0 1 auto; margin: 0; }
  .hdr-right { margin-left: auto; display: flex; align-items: center; gap: 8px; }
  .hdr .shop-btn, .hdr .help-btn { order: 0; margin: 0; }
  #save-status.save-status { position: static; order: 0; display: inline-flex; align-items: center; gap: 6px; min-width: 0;
    font-size: 13px; font-weight: 600; padding: 5px 10px; border-radius: 999px; background: var(--ok-soft); color: var(--ok); white-space: nowrap; }
  #save-status.save-status:empty { display: none; }
  #save-status.save-status.busy { background: var(--gold-soft); color: var(--gold-ink); }
  #save-status.save-status.off { background: #FBE9E7; color: #9A2B1E; }
  .topbar .more-toggle { display: none !important; }

  /* Second row: the work card, the level switch (lab), file actions */
  .ctx { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 12px; padding: 8px 20px 16px; border-top: 1px solid var(--line); }
  .work-card { position: relative; }
  .work-sum { display: inline-flex; align-items: center; gap: 10px; max-width: 100%%; min-height: 40px; padding: 7px 14px; border-radius: 10px;
    border: 1px solid var(--line-strong); background: var(--surface); color: var(--ink); font-weight: 600; text-align: left; }
  .work-sum:hover { border-color: var(--accent); }
  .work-sum-text { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .work-sum-text.empty { color: var(--ink-2); font-weight: 500; }
  .work-edit { color: var(--accent); flex: none; }
  .work-panel { position: absolute; left: 0; top: calc(100%% + 6px); z-index: 70; display: grid; grid-template-columns: repeat(2, minmax(180px, 1fr));
    gap: 10px 12px; width: min(560px, calc(100vw - 32px)); padding: 14px; background: var(--surface); border: 1px solid var(--line);
    border-radius: 14px; box-shadow: 0 12px 32px rgba(23, 35, 59, .18); }
  .work-panel[hidden] { display: none; }
  #topbar .work-panel .tb-field { display: flex; flex-direction: column; gap: 4px; max-width: none; flex: none; order: 0; }
  .work-panel .tb-field input, .work-panel .tb-field select { width: 100%%; }
  .work-panel .work-done { grid-column: 1 / -1; justify-self: end; }
  .ctx .lab-level { font-size: 14px; }
  .ctx-actions { margin-left: auto; display: flex; gap: 8px; align-items: center; }
  #topbar .ctx-actions { display: flex; }

  /* Lab: three columns (steps live in the side list) */
  .lab-focus .lab-head { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px; margin: 0 0 14px; }
  .lab-type { display: inline-flex; align-items: center; gap: 8px; font-weight: 600; color: var(--ink-2); }
  .lab-focus .lab-tool-select { display: block; width: auto; min-width: 240px; margin: 0; font-family: var(--display); font-size: 17px; font-weight: 700; color: var(--ink); }
  .lab-head-tools { margin-left: auto; display: flex; flex-wrap: wrap; align-items: center; gap: 8px 14px; }
  .lab-grid { display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 18px; align-items: start; }
  .lab-center { min-width: 0; }
  .lab-focus .lab-pos { margin: 0 0 2px; }
  .lab-focus .lab-step-title { margin: 0 0 10px; font-size: 24px; }
  .lab-q-pager { display: flex; align-items: center; gap: 8px; margin: 0 0 10px; font-size: 13px; color: var(--ink-2); font-weight: 600; }
  .lab-q-dot { width: 26px; height: 26px; border-radius: 50%%; border: 1px solid var(--line-strong); background: var(--surface); font-size: 12px; font-weight: 700; color: var(--ink-2); }
  .lab-q-dot.done { background: var(--ok-soft); border-color: var(--ok); color: var(--ok); }
  .lab-q-dot[aria-current="true"] { background: var(--accent); border-color: var(--accent); color: #fff; }
  .lab-focus .lab-center > .card { padding: 18px 20px; }
  .lab-focus .lab-center .field-label { font-family: var(--display); font-size: 18px; font-weight: 600; line-height: 1.35; margin-bottom: 10px; }
  .lab-focus .lab-center textarea { min-height: 220px; font-size: 16px; line-height: 1.6; }
  .lab-focus .lab-center .lab-excerpt textarea { min-height: 260px; }
  .lab-focus .lab-center .lab-row textarea, .lab-focus .lab-center .lab-tech textarea { min-height: 70px; font-size: 15px; }
  .lab-focus .lab-center .lab-tip { display: none; }   /* tips are in the side panel */
  .lab-focus .lab-steps { display: none; }
  .lab-panel { position: sticky; top: 0; border: 1px solid var(--line); border-radius: 14px; background: var(--surface); overflow: hidden; }
  .lab-panel-tabs { display: flex; border-bottom: 1px solid var(--line); background: var(--surface-2); }
  .lab-panel-tabs button { flex: 1; min-height: 44px; border: 0; background: none; font-weight: 600; color: var(--ink-2); border-bottom: 3px solid transparent; }
  .lab-panel-tabs button[aria-selected="true"] { color: var(--accent); border-bottom-color: var(--accent); background: var(--surface); }
  .lab-panel-body { padding: 14px 16px; font-size: 14.5px; line-height: 1.55; }
  .lab-panel-body h4 { margin: 12px 0 4px; font-size: 14px; color: var(--ink); }
  .lab-panel-body h4:first-child { margin-top: 0; }
  .lab-panel-body p { margin: 0 0 8px; }
  .lab-panel-body ul, .lab-panel-body ol { margin: 0 0 10px; padding-left: 18px; }
  .lab-panel-body li { margin-bottom: 4px; }
  .lab-sample { margin: 6px 0 10px; padding: 10px 12px; border-left: 3px solid var(--gold); background: var(--gold-soft); border-radius: 0 10px 10px 0; color: var(--ink); }
  .lab-terms { display: flex; flex-wrap: wrap; gap: 6px; margin: 4px 0 10px; }
  .lab-terms button { border: 1px solid var(--line-strong); background: var(--surface); border-radius: 999px; padding: 4px 10px; font-size: 13px; font-weight: 600; color: var(--accent); }
  .lab-src-item { padding: 8px 0; border-top: 1px solid var(--line); }
  .lab-src-item:first-of-type { border-top: 0; padding-top: 0; }
  .link-btn { min-height: 0; }
  .lab-focus .lab-consent { font-size: 14px; }

  /* Side list: done green, current blue */
  #lab-nav .step-btn.done .step-num { background: var(--ok); color: #fff; border-color: var(--ok); }
  #lab-nav .step-btn[aria-current="step"] { background: var(--accent-soft); color: var(--accent); }
  #lab-nav .step-btn[aria-current="step"] .step-num { background: var(--accent); color: #fff; border-color: var(--accent); }

  /* Footer: previous · progress · next */
  .lab-progress { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 5px; min-width: 120px; }
  .lab-progress-bar { width: min(360px, 100%%); height: 8px; border-radius: 999px; background: var(--line); overflow: hidden; }
  .lab-progress-bar span { display: block; height: 100%%; background: var(--accent); border-radius: 999px; }
  .lab-progress-label { font-size: 13px; font-weight: 600; color: var(--ink-2); }

  .sidebar h2, .gl-num { color: var(--gold-ink); }   /* gold as text: the darker shade (AA) */
  .sidebar h2 { font-family: var(--font); }
  .menu-print { display: none; }
  .lab-nav-btn .q-short { display: none; }
  @media (max-width: 1100px) { .lab-grid { grid-template-columns: minmax(0, 1fr) 260px; } }
  @media (max-width: 900px) {
    .hdr { flex-wrap: wrap; padding: 8px 12px; gap: 8px; }
    .hdr .tabs { order: 5; flex: 1 1 100%%; }
    .hdr-right { gap: 6px; }
    .ctx { padding: 8px 12px 14px; }
    .work-card, .work-sum { width: 100%%; }
    .work-panel { grid-template-columns: 1fr; }
    .ctx-actions { margin-left: 0; flex: 1 1 100%%; }
    .ctx-actions > * { flex: 1; }
    .lab-grid { grid-template-columns: minmax(0, 1fr); }
    .lab-panel { position: static; }
    .lab-focus .lab-steps { display: flex; }
    .lab-focus .lab-tool-select { width: 100%%; }
    .lab-head-tools { margin-left: 0; }
    .btn, .tab, select, input[type=text], summary.btn, .lab-q-dot, .work-sum, .lab-level-opts button, .book-modes button { min-height: 44px; }
    .lab-q-dot { min-width: 44px; }
    #topbar .tab, #topbar .btn, #main .btn, #footer .btn, #sidebar .btn, .tb-menu-item, .dlg .btn, .lab-panel-tabs button, .link-btn, #sidebar .step-btn, .k-chip, .lab-dot, .lab-terms button { min-height: 44px; }
    .link-btn { display: inline-flex; align-items: center; }
  }
  @media (max-width: 900px) {
    .hdr .brand h1 { display: none; }
    .hdr .nav-toggle { order: 0; } .hdr .brand { order: 1; } .hdr-right { order: 2; } .hdr .tabs { order: 5; }
    #topbar .ctx-actions { order: 2; flex: none; }
    .ctx .work-card { order: 1; }
    .hdr .brand .brand-mark { display: block; }
    .ctx .work-card { flex: 1 1 0; min-width: 0; width: auto; }
    .ctx .work-sum { width: 100%%; }
    .ctx-actions { flex: none; margin-left: 0; }
    .ctx-actions > .btn.primary { display: none; }
    .menu-print { display: block; }
    .ctx .lab-level { order: 3; flex: 1 1 100%%; }
    .ctx .lab-level > span:first-child { display: none; }
    .ctx .lab-level-opts { display: flex; width: 100%%; }
    .ctx .lab-level-opts button { flex: 1; }
    .lab-type > span { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
    .lab-type { flex: 1 1 100%%; }
    .lab-type select { flex: 1; }
    .lab-head-tools { flex: 1 1 100%%; justify-content: space-between; flex-wrap: nowrap; }
  }
  @media (max-width: 520px) {
    #save-status.save-status { font-size: 12px; padding: 4px 8px; }
    .lab-nav-btn .q-long { display: none; } .lab-nav-btn .q-short { display: inline; }
    .lab-focus .lab-step-title { font-size: 21px; }
  }
  @media (max-width: 380px) {
    .lab-head-tools { flex-wrap: wrap; }
    .lab-head-tools .btn { flex: 1 1 100%%; }
    #footer .lab-nav-btn { white-space: nowrap; padding-left: 10px; padding-right: 10px; font-size: 14px; }
    .lab-progress-label { white-space: nowrap; font-size: 12px; }
    .lab-progress { min-width: 70px; }
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) { --bg: #0c1118; --surface: #141b24; --surface-2: #19222d; --ink: #e8edf3; --ink-2: #a9b4c2;
      --line: #263140; --line-strong: #364253; --accent: #7aa6f0; --accent-hover: #a2c0f5; --accent-ink: #0b1a33; --accent-soft: #16294a;
      --gold: #d8b25e; --gold-ink: #e3c27d; --gold-soft: #33290f; --ok: #7cc074; --ok-soft: #1c2f1a; }
  }
  :root[data-theme="dark"] { --bg: #0c1118; --surface: #141b24; --surface-2: #19222d; --ink: #e8edf3; --ink-2: #a9b4c2;
    --line: #263140; --line-strong: #364253; --accent: #7aa6f0; --accent-hover: #a2c0f5; --accent-ink: #0b1a33; --accent-soft: #16294a;
    --gold: #d8b25e; --gold-ink: #e3c27d; --gold-soft: #33290f; --ok: #7cc074; --ok-soft: #1c2f1a; }
  @media print { .ctx, .lab-panel, .lab-q-pager, .lab-head { display: none !important; } }
</style>
</head>""" % '\n'.join(faces))

# ---- Strings ----
rep("  saved: 'Сақталды',", """  saved: 'Сақталды ✓',
  workCardLabel: 'Шығарма карточкасы',
  workCardEmpty: 'Шығарманы көрсетіңіз',
  workCardDone: 'Дайын',
  labTypeLabel: 'Талдау түрі',
  labQuestion: 'Сұрақ {n} / {total}',
  labQuestionN: '{n}-сұрақ',
  labNextQ: 'Келесі сұрақ →',
  labPrevShort: '← Алдыңғы',
  labNextShort: 'Келесі →',
  labPrevQ: '← Алдыңғы сұрақ',
  labProgress: '{n} / {total} кезең',
  labPanelTip: 'Кеңес',
  labPanelExample: 'Мысал',
  labPanelSources: 'Дереккөз',
  labPanelLabel: 'Көмекші панель',
  labExIntro: 'Жауаптың үлгі құрылымы. Ол нақты шығарма туралы емес: өз мәтініңізбен толтырыңыз.',
  labExNone: 'Бұл өріске үлгі қажет емес.',
  labSrcGuide: 'Нұсқаулықта',
  labSrcOpen: 'Нұсқаулықта ашу →',
  labSrcTerms: 'Сөздіктегі терминдер',
  labSrcTheory: 'Өз дереккөздеріңізді соңғы «Теориялық негіз / дереккөздер» кезеңіне жазыңыз.',
  labSrcTheoryGo: 'Сол кезеңге өту →',""")

# ---- Header: one row + the work card row ----
rep_fn('renderTopbar', r"""
function genreShort(id) { return String((GENRES[id] || {}).label || '').split(' (')[0]; }
/** «Қарасөз · Ер Төстік · 7-сынып»: the genre only when one is chosen. */
function workSummary() {
  const m = state.meta;
  const parts = [m.genre && m.genre !== CONFIG.DEFAULT_GENRE ? genreShort(m.genre) : '',
    filled(m.title) ? oneLine(m.title) : '', m.grade ? m.grade + t('gradeSuffix') : ''].filter(Boolean);
  return parts.join(' · ');
}
function updateWorkCard() {
  const el = document.getElementById('work-sum-text');
  if (!el) return;
  const text = workSummary();
  el.textContent = text || t('workCardEmpty');
  el.classList.toggle('empty', !text);
}
let workOpen = false;
function setWorkOpen(open) {
  workOpen = open;
  const panel = document.getElementById('work-panel'), btn = document.getElementById('work-sum');
  if (panel) panel.hidden = !open;
  if (btn) btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  if (open) { const first = panel && panel.querySelector('select, input'); if (first) first.focus(); }
}

function renderTopbar() {
  const bar = document.getElementById('topbar');
  bar.replaceChildren(
    h('div', { class: 'hdr' },
      h('button', { class: 'btn nav-toggle', type: 'button', 'aria-label': t('navOpen'),
        'aria-expanded': document.body.classList.contains('nav-open') ? 'true' : 'false',
        onclick: openNav }, h('span', { 'aria-hidden': 'true' }, '☰'), h('span', { class: 'nav-text' }, ' ' + t(['guide', 'glossary', 'kids', 'lab'].includes(state.ui.tab) ? 'navGuide' : 'navBook'))),
      h('div', { class: 'brand', role: 'button', tabindex: '0', title: t('appTitle'), style: 'cursor:pointer',
        onclick: () => showCover(true), onkeydown: e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); showCover(true); } } },
        h('span', { class: 'brand-mark', 'aria-hidden': 'true' }),
        h('div', null, h('h1', { text: t('appTitle') }))),
      h('div', { class: 'tabs', role: 'tablist', 'aria-label': t('tabsLabel') },
        ['library', 'book', 'glossary', 'kids', 'lab'].map(tab => h('button', {
          type: 'button', role: 'tab', class: 'tab', id: 'tab-' + tab,
          'aria-selected': state.ui.tab === tab || (tab === 'book' && state.ui.tab === 'guide') ? 'true' : 'false',
          onclick: () => switchTab(tab),
        }, tab === 'kids' ? [h('span', { class: 'tab-long', text: t('tabKids') }), h('span', { class: 'tab-short', text: t('tabKidsShort') })]
          : t({ library: 'tabLibrary', book: 'tabBook', guide: 'tabGuide', glossary: 'tabGlossary', lab: 'tabLab' }[tab])))),
      h('div', { class: 'hdr-right' },
        h('span', { id: 'save-status', class: 'save-status', 'aria-live': 'polite' }),
        h('button', { class: 'btn shop-btn', type: 'button', onclick: showShop, title: t('shopTitle'), 'aria-label': t('shopTitle') },
          svgIcon(CART_ICON, 'shop-ico'), h('span', { class: 'shop-label', text: t('shopBtn') })),
        h('button', { class: 'btn help-btn', type: 'button', onclick: showHelp, title: t('helpTitle'), 'aria-label': t('helpTitle') },
          h('span', { class: 'help-q', 'aria-hidden': 'true' }, '?'), h('span', { class: 'help-label', text: t('helpBtn') })))),
    h('div', { class: 'ctx' },
      h('div', { class: 'work-card' },
        h('button', { class: 'work-sum', id: 'work-sum', type: 'button', 'aria-expanded': workOpen ? 'true' : 'false', 'aria-controls': 'work-panel',
          title: t('workCardLabel'), onclick: () => setWorkOpen(!workOpen) },
          h('span', { class: 'work-sum-text', id: 'work-sum-text' }), h('span', { class: 'work-edit', 'aria-hidden': 'true' }, '✎')),
        h('div', { class: 'work-panel', id: 'work-panel', role: 'group', 'aria-label': t('workCardLabel'), hidden: !workOpen,
          onkeydown: e => { if (e.key === 'Escape') { setWorkOpen(false); document.getElementById('work-sum').focus(); } } },
          h('div', { class: 'tb-field' },
            h('label', { for: 'tb-genre', text: t('genre') }),
            h('select', {
              id: 'tb-genre', value: state.meta.genre,
              onchange: e => {
                state.meta.genre = e.target.value;
                if (!state.lessonPlan.edited) state.lessonPlan.text = '';
                onStateChanged(); render();
              },
            }, Object.keys(GENRES).map(id => h('option', { value: id }, GENRES[id].label)))),
          metaInput('tb-title', 'title', 'workTitle', 'workTitlePh', 300),
          metaInput('tb-author', 'author', 'author', 'authorPh', 200),
          h('div', { class: 'tb-field' },
            h('label', { for: 'tb-grade', text: t('grade') }),
            h('select', {
              id: 'tb-grade', value: state.meta.grade,
              onchange: e => { state.meta.grade = e.target.value; onStateChanged(); },
            }, h('option', { value: '' }, t('gradePh')),
              CONFIG.GRADES.map(g => h('option', { value: String(g) }, g + t('gradeSuffix'))))),
          h('button', { class: 'btn primary work-done', type: 'button', text: t('workCardDone'),
            onclick: () => { setWorkOpen(false); document.getElementById('work-sum').focus(); } }))),
      state.ui.tab === 'lab' ? labLevelSwitch() : null,
      h('div', { class: 'tb-actions ctx-actions' },
        h('details', { class: 'tb-menu' },
          h('summary', { class: 'btn', text: t('fileMenu') }),
          h('div', { class: 'tb-menu-list', role: 'menu' }, [[exportJson, 'exportBtn'], [openImport, 'importBtn'], [newAnalysis, 'resetBtn']].map(([run, key]) =>
            h('button', { class: 'tb-menu-item', type: 'button', role: 'menuitem', text: t(key),
              onclick: e => { e.currentTarget.closest('details').open = false; run(); } })).concat(
            h('button', { class: 'tb-menu-item menu-print', type: 'button', role: 'menuitem', text: t('printBtn'),
              onclick: e => { e.currentTarget.closest('details').open = false; printOutputs(defaultPrintTarget()); } })))),
        h('button', { class: 'btn primary', type: 'button', onclick: () => printOutputs(defaultPrintTarget()), text: t('printBtn') }))),
  );
  updateWorkCard();
  setSaveStatus();
  const openTab = bar.querySelector('.tab[aria-selected="true"]'), row = openTab && openTab.parentNode;
  if (row && row.scrollWidth > row.clientWidth) row.scrollLeft = openTab.offsetLeft - row.offsetLeft - 8;
}
""")
rep("""function onStateChanged() {
  scheduleSave();""", """function onStateChanged() {
  scheduleSave();
  updateWorkCard();""")
# Save state pill: «Сақталуда…» in gold, «Сақталды ✓» in green.
rep("""    el.textContent = text || '';
    el.className = 'save-status';""", """    el.textContent = text || '';
    el.className = 'save-status' + (text === t('saving') ? ' busy' : '');""")
# Close the work card when clicking elsewhere.
rep("document.addEventListener('click', e => { document.querySelectorAll('.tb-menu[open]')",
    "document.addEventListener('click', e => { if (workOpen && !e.target.closest('.work-card')) setWorkOpen(false); });\n"
    "document.addEventListener('click', e => { document.querySelectorAll('.tb-menu[open]')")

# ---- Lab: level switch in the card row; one question at a time; side panel ----
rep("function labFieldVisible(f) {", r"""function labLevelSwitch() {
  return h('div', { class: 'lab-level', role: 'group', 'aria-label': t('labLevel') }, h('span', { text: t('labLevel') }),
    h('span', { class: 'lab-level-opts' }, [['school', 'labLevelSchool'], ['uni', 'labLevelUni']].map(([id, key]) => h('button', {
      type: 'button', 'aria-pressed': labLevel === id ? 'true' : 'false', text: t(key), onclick: () => { if (labLevel !== id) setLabLevel(id); },
    }))));
}
function labFieldVisible(f) {""")
rep("""  try { if (labConsent) window.localStorage.setItem(LAB_LEVEL_KEY, level); } catch (e) { /* storage blocked */ }
  renderMain(); renderFooter();""", """  try { if (labConsent) window.localStorage.setItem(LAB_LEVEL_KEY, level); } catch (e) { /* storage blocked */ }
  renderTopbar(); renderMain(); renderFooter();""")
rep("""  lab.step = Math.max(0, Math.min(LAB_STEPS.length - 1, i));
  labSaveNow();""", """  lab.step = Math.max(0, Math.min(LAB_STEPS.length - 1, i));
  lab.qi = 0;
  labSaveNow();""")

rep_fn('renderLabMain', r"""
/* Focus mode: the fields of a stage are shown one at a time (the preparation step, with its
   short name fields, stays a single form). `lab.qi` is the open question of the open step. */
function labStepFields(st) { return st && st.fields ? st.fields.filter(labFieldVisible) : []; }
function labPaged(st) { return !!st && !st.summary && !st.rules && labStepFields(st).length > 1; }
function labQi() {
  const st = LAB_STEPS[lab.step], n = labStepFields(st).length;
  lab.qi = Math.max(0, Math.min(n - 1, lab.qi || 0));
  return lab.qi;
}
function labGoQ(qi) { lab.qi = qi; renderMain(); renderFooter(); const box = document.querySelector('.lab-center textarea, .lab-center input'); if (box) box.focus({ preventScroll: true }); document.getElementById('main').scrollTop = 0; }
/** Open the step and question that hold a field (used by links to a field). */
function labFocusField(id) {
  const i = LAB_STEPS.findIndex(st => labStepFields(st).some(f => f.id === id));
  if (i < 0) return false;
  if (i !== lab.step) labGo(i);
  const st = LAB_STEPS[lab.step];
  if (labPaged(st)) { lab.qi = labStepFields(st).findIndex(f => f.id === id); renderMain(); renderFooter(); }
  return true;
}
/** Back from the first question of a step: the previous step's last question. */
function labPrev() {
  const st = LAB_STEPS[lab.step];
  if (labPaged(st) && labQi() > 0) { labGoQ(lab.qi - 1); return; }
  if (lab.step === 0) return;
  labGo(lab.step - 1);
  const prev = LAB_STEPS[lab.step];
  if (labPaged(prev)) labGoQ(labStepFields(prev).length - 1);
}
function labNext() {
  const st = LAB_STEPS[lab.step];
  if (labPaged(st) && labQi() < labStepFields(st).length - 1) { labGoQ(lab.qi + 1); return; }
  if (lab.step < LAB_STEPS.length - 1) labGo(lab.step + 1);
}

let labPanel = 'tip';   // «Кеңес» | «Мысал» | «Дереккөз»
const LAB_GUIDE_REFS = { hero: ['3', '2.9', '2.10'], plot: ['2.6', '2.7', '2.8', '4.1', '4.2'], narratology: ['2.12'], symbols: ['2.16', '2.23'],
  chronotope: ['2.13', '2.14', '2.24'], mythopoetics: ['12'], comparative: ['11'], style: ['2.18', '2.19'], hermeneutics: ['2.22', '2.20'], ecocriticism: ['13'] };
const LAB_TERMS = { hero: ['Кейіпкер', 'Характер', 'Психологизм', 'Ішкі монолог'], plot: ['Сюжет', 'Фабула', 'Композиция', 'Кульминация'],
  narratology: ['Баяндаушы', 'Фокализация', 'Сана ағымы'], symbols: ['Образ', 'Көркем образ', 'Қайталау'], chronotope: ['Хронотоп', 'Көркем уақыт', 'Көркем кеңістік'],
  mythopoetics: ['Ертегі', 'Эпопея', 'Баллада'], comparative: ['Жанр', 'Тип', 'Концепция'], style: ['Пафос', 'Диалог', 'Монолог'],
  hermeneutics: ['Идея', 'Концепция', 'Авторлық позиция'], ecocriticism: ['Көркем кеңістік', 'Мекен', 'Пафос'] };

function labCurrentField() {
  const st = LAB_STEPS[lab.step], fields = labStepFields(st);
  return labPaged(st) ? fields[labQi()] : fields.length === 1 ? fields[0] : null;
}

/** «Мысал»: the shape of a good answer for this kind of field — never a made-up answer about a work. */
function labExample(f) {
  const ex = (items, sample) => [h('p', { text: t('labExIntro') }), h('ol', null, items.map(x => h('li', { text: x }))),
    sample ? h('p', { class: 'lab-sample', text: sample }) : null];
  if (!f) return [h('p', { text: t('labExNone') })];
  if (f.id === 'sources') return ex(['Автор (тегі, аты-жөнінің бас әріптері).', 'Еңбектің атауы.', 'Баспа орны, баспа, жылы.', 'Пайдаланған беті.'],
    'Тегі А.Ә. Еңбектің атауы. — Қала: Баспа, жыл. — 00–00 б.');
  if (f.id === 'uniFrame') return ex(['Сүйенетін теория немесе ұғым (кімнің еңбегі).', 'Оның негізгі қағидасы бір сөйлеммен.', 'Бұл тұрғы шығарманың қай қырын ашады.', 'Оның шегі: нені түсіндірмейді.']);
  if (f.evidenceFor) return ex(['Қысқа дәйексөз, өзгертпей, тырнақшада.', 'Беті немесе тарауы.', 'Ол қай тұжырымыңызды дәлелдейді.'],
    '«…» (… бет). Бұл дәйексөз … деген тұжырымды растайды, өйткені …');
  if (f.type === 'rows') return ex(f.columns.map(c => c + ': …'), f.columns.map(c => c + ': …').join(' | '));
  if (f.type === 'techniques') return ex(['Мәтінде бар тәсілді белгілеңіз.', 'Мысал: эпизод немесе қысқа дәйексөз.', 'Бұл тәсіл кейіпкердің ішкі әлемінің қай қырын ашады.']);
  if (f.type === 'choice' || f.type === 'text') return [h('p', { text: t('labExNone') })];
  return ex(['Тұжырым: сұраққа бір-екі сөйлеммен нақты жауап.', 'Дәлел: мәтіннен эпизод немесе қысқа дәйексөз «…» (беті).', 'Түсіндіру: бұл дәлел тұжырымды қалай растайды.', 'Қорытынды: бұл шығарманың мағынасына не қосады.'],
    'Менің ойымша, … . Мұны … эпизоды көрсетеді: «…» (… бет). Бұл … екенін байқатады, сондықтан … .');
}

function labPanelBody() {
  const st = LAB_STEPS[lab.step], tool = LAB_TOOLS[labTool], f = labCurrentField();
  if (labPanel === 'example') return labExample(f);
  if (labPanel === 'sources') {
    const refs = (LAB_GUIDE_REFS[labTool] || []).filter(id => GUIDE_INDEX[id]);
    const theoryIdx = LAB_STEPS.findIndex(x => x.id === 'theory');
    return [
      refs.length ? h('h4', { text: t('labSrcGuide') }) : null,
      refs.map(id => { const sec = GUIDE_INDEX[id]; return h('div', { class: 'lab-src-item' },
        h('p', null, h('b', { text: guideHeading(sec) })),
        sec.locked && filled(sec.text) ? h('p', { text: sec.text }) : null,
        sec.locked ? h('p', { class: 'ws-tip-pdf' }, h('span', { text: t('guideLockedTitle') }), h('button', { type: 'button', class: 'link-btn', text: t('guideLockedBuy'), onclick: showShop }))
          : h('button', { type: 'button', class: 'link-btn', text: t('labSrcOpen'), onclick: () => openGuide(id) })); }),
      h('h4', { text: t('labSrcTerms') }),
      h('div', { class: 'lab-terms' }, (LAB_TERMS[labTool] || []).map(term => h('button', { type: 'button', text: term,
        onclick: () => { glossQuery = term; switchTab('glossary'); } }))),
      theoryIdx >= 0 && theoryIdx !== lab.step ? [h('p', { text: t('labSrcTheory') }),
        h('button', { type: 'button', class: 'link-btn', text: t('labSrcTheoryGo'), onclick: () => labGo(theoryIdx) })] : null,
    ];
  }
  // «Кеңес»: the question's guiding questions, then the step's intro, note and rules.
  const hints = f ? (f.hints || []).concat(labLevel === 'uni' ? f.hintsUni || [] : f.hintsSchool || [])
    : labStepFields(st).reduce((a, x) => a.concat(x.hints || []), []);
  return [
    lab.step === 0 ? h('p', { text: toolText(tool, 'intro') }) : null,
    st.intro ? h('p', { text: st.intro }) : null,
    st.note ? h('p', { text: st.note }) : null,
    hints.length ? h('ul', null, hints.map(x => h('li', { text: x }))) : null,
    st.rules ? [h('h4', { text: t('labRulesTitle') }),
      h('ul', null, (tool.rulesList || STRINGS[tool.rules]).map(x => h('li', { text: x })))] : null,
  ];
}

function renderLabPanel() {
  const body = h('div', { class: 'lab-panel-body', id: 'lab-panel-body', role: 'tabpanel' }, labPanelBody());
  return h('aside', { class: 'lab-panel', 'aria-label': t('labPanelLabel') },
    h('div', { class: 'lab-panel-tabs', role: 'tablist' }, [['tip', 'labPanelTip'], ['example', 'labPanelExample'], ['sources', 'labPanelSources']].map(([id, key]) =>
      h('button', { type: 'button', role: 'tab', 'aria-selected': labPanel === id ? 'true' : 'false', text: t(key),
        onclick: e => {
          labPanel = id;
          e.currentTarget.parentNode.querySelectorAll('button').forEach(b => b.setAttribute('aria-selected', b === e.currentTarget ? 'true' : 'false'));
          body.replaceChildren.apply(body, [].concat(labPanelBody()).flat(Infinity).filter(Boolean));
        } }))),
    body);
}

/** One question per screen: on a claim, say when the stage's «Мәтіндік дәлел» is still empty. */
function labClaimWarn(fields, f, evWarns) {
  const ev = fields.find(x => x.evidenceFor && x.evidenceFor.includes(f.id));
  if (!ev) return null;
  const w = labEvidenceWarn(ev);
  evWarns.push(w);
  return w.el;
}

function renderLabMain() {
  const st = LAB_STEPS[lab.step];
  const consent = h('input', { type: 'checkbox', id: 'lab-consent', onchange: e => setLabConsent(e.target.checked) });
  consent.checked = labConsent;
  const evWarns = [];
  const fields = labStepFields(st), paged = labPaged(st), qi = paged ? labQi() : 0;
  return h('article', { class: 'lab lab-focus' },
    h('div', { class: 'lab-head' },
      h('label', { class: 'lab-type', for: 'lab-type' }, h('span', { text: t('labTypeLabel') }),
        h('select', { class: 'lab-tool-select', id: 'lab-type', value: labTool, onchange: e => labSwitch(e.target.value) },
          Object.keys(LAB_TOOLS).map(id => h('option', { value: id }, toolText(LAB_TOOLS[id], 'label'))))),
      h('div', { class: 'lab-head-tools' },
        h('label', { class: 'lab-consent', for: 'lab-consent', title: t(labConsent ? 'labConsentOn' : 'labConsentOff') }, consent, h('span', null, t('labConsent'))),
        h('button', { type: 'button', class: 'btn', text: t('labClear'), onclick: () => askConfirm(t('labClearAsk'), () => {
          lab = labStates[labTool] = labFresh(); labSaveNow(); render(); document.getElementById('main').scrollTop = 0; showBanner('ok', t('labCleared'));
        }) }))),
    h('nav', { class: 'lab-steps', 'aria-label': t('labSteps') }, LAB_STEPS.map((x, i) => h('button', {
      type: 'button', class: 'lab-dot' + (labStepDone(x) ? ' done' : ''), 'aria-current': i === lab.step ? 'step' : null,
      title: x.title, onclick: () => labGo(i),
    }, h('span', { class: 'n', text: labBadge(x, i) }), h('span', { text: x.title })))),
    h('div', { class: 'lab-grid' },
      h('section', { class: 'lab-center' },
        h('p', { class: 'lab-pos', text: labPosText(lab.step) }),
        h('h2', { class: 'lab-step-title', text: st.title }),
        paged ? h('div', { class: 'lab-q-pager', role: 'group', 'aria-label': t('labQuestion', { n: qi + 1, total: fields.length }) },
          h('span', { text: t('labQuestion', { n: qi + 1, total: fields.length }) }),
          fields.map((f, i) => h('button', { type: 'button', class: 'lab-q-dot' + (labFieldFilled(f) ? ' done' : ''),
            'aria-current': i === qi ? 'true' : 'false', 'aria-label': t('labQuestionN', { n: i + 1 }), text: String(i + 1), onclick: () => labGoQ(i) }))) : null,
        st.summary ? renderLabSummary() : (paged ? [fields[qi]] : fields).map(f => renderLabField(f, evWarns)),
        paged ? labClaimWarn(fields, fields[qi], evWarns) : null,
        !st.summary && !st.rules ? tutorCard(false) : null),
      renderLabPanel()));
}
""")
rep_fn('renderLabFooter', r"""
function renderLabFooter() {
  const i = lab.step, last = LAB_STEPS.length - 1, st = LAB_STEPS[i];
  const paged = labPaged(st), qi = paged ? labQi() : 0, n = labStepFields(st).length;
  const moreQ = paged && qi < n - 1, backQ = paged && qi > 0;
  const pct = Math.round((i + 1) / LAB_STEPS.length * 100);
  document.getElementById('footer').replaceChildren(
    h('button', { class: 'btn lab-nav-btn', type: 'button', disabled: i === 0 && !backQ, 'aria-label': t(backQ ? 'labPrevQ' : 'labPrev'), onclick: labPrev },
      h('span', { class: 'q-long', text: t(backQ ? 'labPrevQ' : 'labPrev') }), h('span', { class: 'q-short', text: t('labPrevShort') })),
    h('div', { class: 'lab-progress' },
      h('div', { class: 'lab-progress-bar', role: 'progressbar', 'aria-valuemin': 1, 'aria-valuemax': LAB_STEPS.length, 'aria-valuenow': i + 1,
        'aria-label': t('labProgress', { n: i + 1, total: LAB_STEPS.length }) }, h('span', { style: 'width:' + pct + '%' })),
      h('span', { class: 'lab-progress-label', text: t('labProgress', { n: i + 1, total: LAB_STEPS.length }) })),
    i < last || moreQ ? h('button', { class: 'btn primary lab-nav-btn', type: 'button', 'aria-label': t(moreQ ? 'labNextQ' : i === last - 1 ? 'labToSummary' : 'labNext'), onclick: labNext },
      h('span', { class: 'q-long', text: t(moreQ ? 'labNextQ' : i === last - 1 ? 'labToSummary' : 'labNext') }), h('span', { class: 'q-short', text: t('labNextShort') }))
      : h('button', { class: 'btn primary', type: 'button', text: t('labPrint'), onclick: () => printOutputs('lab') }));
}
""")
rep("  document.querySelectorAll('.lab-dot').forEach((d, i) => d.classList.toggle('done', labStepDone(LAB_STEPS[i])));",
    "  document.querySelectorAll('.lab-dot').forEach((d, i) => d.classList.toggle('done', labStepDone(LAB_STEPS[i])));\n"
    "  const qf = labStepFields(LAB_STEPS[lab.step]);\n"
    "  document.querySelectorAll('.lab-q-dot').forEach((d, i) => d.classList.toggle('done', !!qf[i] && labFieldFilled(qf[i])));")
# The level switch now lives in the card row; the lab bar is gone (consent and clear are in the lab head).

s = s.replace('      python3 merge.py tidy.html kobem-talday.html         # «Нұсқаулық» inside «Дәптер»',
              '      python3 merge.py tidy.html merge.html                # «Нұсқаулық» inside «Дәптер»\n'
              '      python3 focus.py merge.html fonts kobem-talday.html  # «Фокус режимі»: palette, fonts, header, three-column lab')
open(out, 'w', encoding='utf8').write(s)
print('focus -> %s (%d KB)' % (out, os.path.getsize(out) // 1024))
