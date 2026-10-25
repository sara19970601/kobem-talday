"""Build kobem-talday.html = base app + worksheets.json + guide.json + guide tab.
Usage: python3 -I assemble.py base.html worksheets.json guide.json out.html"""
import json, sys

base, wsj, gj, out = sys.argv[1:5]
s = open(base, encoding='utf8').read()
worksheets = json.load(open(wsj, encoding='utf8'))
guide = json.load(open(gj, encoding='utf8'))

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('patch anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

def script_json(obj):
    return json.dumps(obj, ensure_ascii=False, indent=1).replace('</', '<\\/')

# ---------------------------------------------------------------- data blocks
a = s.index('const WORKBOOK = ') + len('const WORKBOOK = ')
b = s.index('};\n</script>', a) + 1
s = s[:a] + json.dumps(worksheets, ensure_ascii=False, indent=2) + s[b:]

end_ws = s.index('</script>', s.index('<script id="worksheets-data">')) + len('</script>')
s = s[:end_ws] + """

<script id="guide-data">
'use strict';
/* ==============================================================================
   GUIDE — data block: the methodology guide «Көркем шығарманы талдау»,
   split into chapters (N-БӨЛІМ) and subsections (N.N) by build_guide.py from
   the PDF's text layer. Wording is unchanged; do not edit by hand — rebuild.
   level: 0 = lead-in (preface, introduction), 1 = chapter, 2 = subsection.
   Paragraphs are separated by a blank line; a paragraph with line breaks is a
   table kept as laid out in the PDF.
   ============================================================================== */
const GUIDE = """ + script_json(guide) + """;
</script>""" + s[end_ws:]

# ---------------------------------------------------------------- README
rep("""  Code sections: CONFIG, STRINGS, WORKSHEETS, STATE, RENDER, LESSON_PLAN,
  RUBRIC, PRINT, IMPORT/EXPORT, INIT.""", """  Two tabs
    - "Дәптер": the 31 worksheets, lesson plan and rubric. Each worksheet has
      "Нұсқаулық: N →" buttons for the guide sections in its "guide" field.
    - "Нұсқаулық": the methodology guide (GUIDE block), one section at a time,
      with chapter navigation and search. "Дәптерге оралу" goes back to the
      worksheet; typed answers are kept.

  Rebuilding the data blocks (only needed when the PDF or JSON changes)
      pdftotext -layout guide.pdf guide.txt
      python3 build_guide.py guide.txt guide.json      # stops if 1–16 or 2.1–2.24 are missing
      python3 assemble.py base.html worksheets.json guide.json kobem-talday.html

  Code sections: CONFIG, STRINGS, WORKSHEETS, GUIDE, STATE, RENDER, LESSON_PLAN,
  RUBRIC, GUIDE VIEW, PRINT, IMPORT/EXPORT, INIT.""")

# ---------------------------------------------------------------- CSS
rep("    --overlay: rgba(20, 24, 26, .5);\n  }", "    --overlay: rgba(20, 24, 26, .5);\n    --mark: #ffe08a;\n  }")
rep("--stage-empty: #2d3337; --overlay: rgba(0, 0, 0, .6); color-scheme: dark;",
    "--stage-empty: #2d3337; --overlay: rgba(0, 0, 0, .6); --mark: #7a5f12; color-scheme: dark;", count=2)
rep("  #print-area { display: none; }\n", """  #print-area { display: none; }

  /* Tabs */
  .tabs {
    display: inline-flex; gap: 2px; padding: 3px; align-self: center;
    border: 1px solid var(--line); border-radius: 10px; background: var(--surface-2);
  }
  .tab {
    border: 0; background: none; padding: 6px 16px; border-radius: 7px;
    cursor: pointer; font-weight: 600; color: var(--ink-2);
  }
  .tab:hover { color: var(--ink); }
  .tab[aria-selected="true"] { background: var(--accent); color: var(--accent-ink); }
  .tab:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; }

  /* Guide */
  .step-btn[aria-current="page"] { background: var(--accent-soft); border-color: var(--accent); }
  .g-search { padding: 0 4px; }
  .g-search input {
    width: 100%; border: 1px solid var(--line); border-radius: 6px;
    padding: 7px 9px; background: var(--surface);
  }
  .g-results { font-size: 12px; color: var(--ink-2); margin: 6px 8px 4px; min-height: 1.2em; }
  .g-subs { list-style: none; margin: 0 0 4px 14px; padding: 0 0 0 4px; border-left: 1px solid var(--line); }
  .g-item .step-label { flex: 1; }
  .g-item.lvl1 .step-label, .g-item.lvl0 .step-label { font-weight: 600; }
  .g-count {
    flex: none; align-self: center; font-size: 11px; font-weight: 700;
    background: var(--accent); color: var(--accent-ink); border-radius: 99px; padding: 1px 7px;
  }
  .g-body { font-size: 15.5px; line-height: 1.65; max-width: 74ch; }
  .g-body p { margin: 0 0 12px; }
  .g-sub { font-size: 16px; margin: 20px 0 8px; text-wrap: balance; }
  .g-list { margin: 0 0 12px; padding-left: 22px; }
  .g-list li { margin-bottom: 6px; }
  .g-table {
    overflow-x: auto; margin: 0 0 14px; max-width: 100%;
    border: 1px solid var(--line); border-radius: 6px; background: var(--surface);
  }
  .g-table pre {
    margin: 0; padding: 10px 12px; font-size: 12.5px; line-height: 1.45;
    font-family: ui-monospace, Consolas, "Courier New", monospace;
  }
  mark { background: var(--mark); color: var(--ink); border-radius: 2px; padding: 0 1px; }
  .g-refs { margin-top: 18px; }
""")
rep("    .print-std { font-size: 9.5pt; margin-top: 10pt; }\n", """    .print-std { font-size: 9.5pt; margin-top: 10pt; }
    .print-guide p { margin: 0 0 6pt; }
    .print-guide .g-sub { font-size: 11.5pt; margin: 10pt 0 4pt; }
    .print-guide .g-list { margin: 0 0 6pt; padding-left: 16pt; }
    .print-guide .g-table { border: 1px solid #000; border-radius: 0; overflow: visible; page-break-inside: avoid; break-inside: avoid; }
    .print-guide .g-table pre { font-size: 7.5pt; padding: 4pt; white-space: pre; }
    mark { background: none; color: inherit; }
""")

# ---------------------------------------------------------------- CONFIG / GENRES
rep("  DEFAULT_GENRE: 'folklore',", "  DEFAULT_GENRE: 'all',\n  LEGACY_STORAGE_KEYS: ['kobem-talday:v1'],   // older versions, read once if nothing newer is saved")
a = s.index('const GENRES = {'); b = s.index('};', a) + 2
s = s[:a] + """const GENRES = {
  all:      { label: 'Барлық жанр (жалпы парақтар)',  activities: 'default' },
  poetry:   { label: 'Поэзия',                        activities: 'poetry' },
  prose:    { label: 'Проза (әңгіме, повесть, роман)', activities: 'default' },
  drama:    { label: 'Драма',                         activities: 'drama' },
  children: { label: 'Балалар әдебиеті',              activities: 'default' },
  folklore: { label: 'Фольклор (ертегі, жыр-дастан)', activities: 'folklore' },
};""" + s[b:]

# ---------------------------------------------------------------- STRINGS
rep("  errOlder: 'Файл құралдың ескі нұсқасында (нұсқа {v}) жасалған, оның құрылымы басқа. Талдауды жаңа парақтарда қайта толтырыңыз.',\n", "")
rep("  probNumber: 'сан күтілді',\n", """  probNumber: 'сан күтілді',
  tabBook: 'Дәптер',
  tabGuide: 'Нұсқаулық',
  tabsLabel: 'Бөлімдер',
  guideBtn: 'Нұсқаулық: {id} →',
  backToBook: '← Дәптерге оралу: {name}',
  guideSearch: 'Нұсқаулықтан іздеу',
  guideSearchPh: 'Сөз немесе тіркес…',
  guideResults: '{n} бөлімнен табылды',
  guideNoResults: 'Ештеңе табылмады.',
  guideLeadIn: 'Алғы сөз және кіріспе',
  guideChapter: '{n}-БӨЛІМ',
  guideSheetsRef: 'Осы бөлімге сілтейтін жұмыс парақтары:',
  guidePrev: '← Алдыңғы бөлім',
  guideNext: 'Келесі бөлім →',
  guidePos: '{n} / {total} бөлім',
  sheetName: '{n}-парақ. {title}',
  importMigrated: 'Талдау құралдың алғашқы нұсқасынан жүктелді: жауаптар 1, 2, 4, 6, 7, 8, 9, 16 және 29-парақтарға көшірілді.',
""")

# ---------------------------------------------------------------- STATE
rep("    ui: { step: 'ws-01-first-reading' },\n  };\n}", "    ui: freshUi(),\n  };\n}", count=2)
rep("function genre() {", "function freshUi() {\n  return { step: 'ws-01-first-reading', tab: 'book', guideSection: GUIDE.sections[0].id, search: '' };\n}\n\nfunction genre() {")
rep("""    const raw = window.localStorage.getItem(CONFIG.STORAGE_KEY);
    if (raw) {
      const parsed = JSON.parse(raw);
      const clean = validateImport(parsed);
      clean.ui = { step: parsed.ui && typeof parsed.ui.step === 'string' ? parsed.ui.step : clean.ui.step };
      state = clean;
    }""", """    let raw = window.localStorage.getItem(CONFIG.STORAGE_KEY);
    for (const k of CONFIG.LEGACY_STORAGE_KEYS) { if (!raw) raw = window.localStorage.getItem(k); }
    if (raw) {
      const parsed = JSON.parse(raw);
      const clean = validateImport(parsed);
      const u = isObj(parsed.ui) ? parsed.ui : {};
      clean.ui = {
        step: typeof u.step === 'string' ? u.step : clean.ui.step,
        tab: u.tab === 'guide' ? 'guide' : 'book',
        guideSection: typeof u.guideSection === 'string' && GUIDE_INDEX[u.guideSection] ? u.guideSection : clean.ui.guideSection,
        search: typeof u.search === 'string' ? u.search.slice(0, 200) : '',
      };
      state = clean;
    }""")

# ---------------------------------------------------------------- RENDER dispatch
rep("""function renderSidebar() {
  const nav = document.getElementById('sidebar');""", """function renderSidebar() {
  if (state.ui.tab === 'guide') { renderGuideSidebar(); return; }
  const nav = document.getElementById('sidebar');""")
rep("""function renderFooter() {
  const foot = document.getElementById('footer');""", """function renderFooter() {
  if (state.ui.tab === 'guide') { renderGuideFooter(); return; }
  const foot = document.getElementById('footer');""")
rep("""  const box = document.getElementById('main-inner');
  const step = currentStep();
  const content = step.kind === 'plan'""", """  const box = document.getElementById('main-inner');
  if (state.ui.tab === 'guide') {
    box.replaceChildren(h('div', { id: 'banner-slot' }), renderGuideMain());
    renderBanner();
    return;
  }
  const step = currentStep();
  const content = step.kind === 'plan'""")
rep("""function goTo(key) {
  state.ui.step = key;""", """function goTo(key) {
  state.ui.step = key;
  state.ui.tab = 'book';""")
rep("""    h('div', { class: 'brand' },
      h('h1', { text: t('appTitle') }),
      h('p', { text: t('appSubtitle') })),
""", """    h('div', { class: 'brand' },
      h('h1', { text: t('appTitle') }),
      h('p', { text: t('appSubtitle') })),
    h('div', { class: 'tabs', role: 'tablist', 'aria-label': t('tabsLabel') },
      ['book', 'guide'].map(tab => h('button', {
        type: 'button', role: 'tab', class: 'tab', id: 'tab-' + tab,
        'aria-selected': state.ui.tab === tab ? 'true' : 'false',
        onclick: () => switchTab(tab),
      }, t(tab === 'book' ? 'tabBook' : 'tabGuide')))),
""")
rep("""    meta ? h('p', { class: 'ws-meta', text: meta }) : null,
    ws.note ?""", """    meta ? h('p', { class: 'ws-meta', text: meta }) : null,
    guideRefs(ws.guide).length ? h('div', { class: 'ws-tools' }, guideRefs(ws.guide).map(id => h('button', {
      class: 'btn guide-link', type: 'button', title: guideHeading(GUIDE_INDEX[id]),
      onclick: () => openGuide(id),
    }, t('guideBtn', { id: id })))) : null,
    ws.note ?""")

# ---------------------------------------------------------------- GUIDE VIEW
rep("""/* ==============================================================================
   PRINT —""", """/* ==============================================================================
   GUIDE VIEW — the "Нұсқаулық" tab, built from the real GUIDE section list.
   ============================================================================== */
const GUIDE_INDEX = {};
GUIDE.sections.forEach((sec, i) => { sec.index = i; GUIDE_INDEX[sec.id] = sec; });
const tabScroll = { book: 0, guide: 0 };   // remembered scroll position per tab

function guideHeading(sec) {
  if (sec.level === 0) return t('guideLeadIn');
  return sec.level === 1 ? t('guideChapter', { n: sec.id }) + '. ' + sec.title : sec.id + '. ' + sec.title;
}
function guideNavLabel(sec) {
  return sec.level === 0 ? t('guideLeadIn') : sec.id + (sec.level === 1 ? '. ' : ' ') + sec.title;
}

/** Section ids named in a worksheet's "guide" string ("2.8, 4.2", "3 (соңғы тармақ), 2.10"). */
function guideRefs(str) {
  const ids = String(str || '').match(/\\d+(?:\\.\\d+)?/g) || [];
  return ids.filter((id, i) => ids.indexOf(id) === i && GUIDE_INDEX[id]);
}

/** Sheets visible in the current genre whose "guide" field points at a section. */
function sheetsReferencing(id) {
  return sheetsForGenre().filter(ws => guideRefs(ws.guide).includes(id));
}

function sheetStepKey(wsId) { return wsId === CONFIG.RUBRIC_SHEET ? 'rubric' : wsId; }
function stepFullName(step) {
  return step.kind === 'sheet' ? t('sheetName', { n: step.ws.order, title: step.ws.title }) : stepLabel(step);
}

function switchTab(tab) {
  if (state.ui.tab === tab) return;
  tabScroll[state.ui.tab] = document.getElementById('main').scrollTop;
  state.ui.tab = tab;
  scheduleSave();
  render();
  document.getElementById('main').scrollTop = tabScroll[tab] || 0;
}

function openGuide(id) {
  tabScroll.book = document.getElementById('main').scrollTop;
  state.ui.tab = 'guide';
  showGuideSection(id);
}

function showGuideSection(id) {
  state.ui.guideSection = id;
  const q = (state.ui.search || '').trim();
  if (q && !countMatches(GUIDE_INDEX[id], q)) state.ui.search = '';
  scheduleSave();
  render();
  document.getElementById('main').scrollTop = 0;
  scrollToFirstMark();
}

function openSheet(wsId) {
  tabScroll.book = 0;
  state.ui.step = sheetStepKey(wsId);
  switchTab('book');
  document.getElementById('main').scrollTop = 0;
}

/* Case-insensitive matching for Kazakh/Cyrillic: lower-case each character but
   keep string length, so positions in the folded text map to the original. */
function fold(str) {
  return Array.from(String(str)).map(c => { const l = c.toLowerCase(); return l.length === c.length ? l : c; }).join('');
}
function countMatches(sec, q) {
  const f = fold(q);
  if (!f || !sec) return 0;
  const hay = fold(guideHeading(sec) + '\\n' + sec.text);
  let n = 0, i = hay.indexOf(f);
  while (i !== -1) { n++; i = hay.indexOf(f, i + f.length); }
  return n;
}
function appendHighlighted(el, text, q) {
  const f = fold(q || '');
  if (!f) { el.append(text); return; }
  const hay = fold(text);
  let i = 0, j;
  while ((j = hay.indexOf(f, i)) !== -1) {
    if (j > i) el.append(text.slice(i, j));
    el.append(h('mark', null, text.slice(j, j + f.length)));
    i = j + f.length;
  }
  if (i < text.length) el.append(text.slice(i));
}
function scrollToFirstMark() {
  const m = document.querySelector('#main-inner mark');
  if (m && m.scrollIntoView) m.scrollIntoView({ block: 'center' });
}

/** Paragraphs → DOM: bullet runs become lists, multi-line blocks are tables
    (kept as laid out), short unpunctuated lines are subheadings. */
function renderGuideText(text, q) {
  const out = [];
  let list = null;
  text.split('\\n\\n').forEach(p => {
    if (/^[•-] /.test(p)) {
      if (!list) { list = h('ul', { class: 'g-list' }); out.push(list); }
      const li = h('li');
      appendHighlighted(li, p.slice(2), q);
      list.append(li);
      return;
    }
    list = null;
    let el;
    if (p.indexOf('\\n') !== -1) {
      const pre = h('pre');
      appendHighlighted(pre, p, q);
      el = h('div', { class: 'g-table', tabindex: '0' }, pre);
    } else if (p.length < 90 && !/[.!?:;»)…,"]$/.test(p) && (!/^\\d/.test(p) || p === p.toUpperCase())) {
      el = h('h3', { class: 'g-sub' });
      appendHighlighted(el, p, q);
    } else {
      el = h('p');
      appendHighlighted(el, p, q);
    }
    out.push(el);
  });
  return out;
}

function renderGuideSidebar() {
  const nav = document.getElementById('sidebar');
  nav.replaceChildren(
    h('h2', null, h('label', { for: 'guide-search', text: t('guideSearch') })),
    h('div', { class: 'g-search' }, h('input', {
      id: 'guide-search', type: 'search', value: state.ui.search || '', maxlength: 200,
      placeholder: t('guideSearchPh'), autocomplete: 'off',
      oninput: e => { state.ui.search = e.target.value; scheduleSave(); onSearchChanged(); },
    })),
    h('p', { id: 'guide-results', class: 'g-results', 'aria-live': 'polite' }),
    h('div', { id: 'guide-nav-list' }));
  updateGuideNav();
}

function updateGuideNav() {
  const list = document.getElementById('guide-nav-list');
  if (!list) return;
  const q = (state.ui.search || '').trim();
  const counts = {};
  let hits = 0;
  GUIDE.sections.forEach(sec => { counts[sec.id] = q ? countMatches(sec, q) : 0; if (counts[sec.id]) hits++; });
  document.getElementById('guide-results').textContent =
    q ? (hits ? t('guideResults', { n: hits }) : t('guideNoResults')) : '';
  const item = sec => h('li', null, h('button', {
    type: 'button', class: 'step-btn g-item lvl' + sec.level,
    'aria-current': sec.id === state.ui.guideSection ? 'page' : null,
    onclick: () => showGuideSection(sec.id),
  }, h('span', { class: 'step-label' }, guideNavLabel(sec)),
    counts[sec.id] ? h('span', { class: 'g-count', title: String(counts[sec.id]) }, String(counts[sec.id])) : null));
  // Chapters (and the lead-in) with their subsections, from the real list.
  const groups = [];
  GUIDE.sections.forEach(sec => {
    if (sec.level < 2) groups.push({ head: sec, subs: [] });
    else groups[groups.length - 1].subs.push(sec);
  });
  const parts = [];
  groups.forEach(g => {
    const subs = q ? g.subs.filter(sec => counts[sec.id]) : g.subs;
    if (q && !counts[g.head.id] && !subs.length) return;
    parts.push(h('ul', { class: 'steps' }, item(g.head),
      subs.length ? h('li', null, h('ul', { class: 'g-subs' }, subs.map(item))) : null));
  });
  list.replaceChildren.apply(list, parts);
}

function onSearchChanged() {
  const q = (state.ui.search || '').trim();
  if (q && !countMatches(GUIDE_INDEX[state.ui.guideSection], q)) {
    const first = GUIDE.sections.find(sec => countMatches(sec, q));
    if (first) state.ui.guideSection = first.id;
  }
  updateGuideNav();
  renderMain();
  renderFooter();
  scrollToFirstMark();
}

function renderGuideMain() {
  const sec = GUIDE_INDEX[state.ui.guideSection] || GUIDE.sections[0];
  const q = (state.ui.search || '').trim();
  const chapter = sec.level === 2 ? GUIDE_INDEX[sec.id.split('.')[0]] : null;
  const title = h('h2', { class: 'ws-title' });
  appendHighlighted(title, guideHeading(sec), q);
  const refs = sheetsReferencing(sec.id);
  return h('article', { class: 'guide' },
    h('div', { class: 'ws-tools' },
      h('button', { class: 'btn primary', type: 'button', id: 'back-to-book',
        text: t('backToBook', { name: stepFullName(currentStep()) }), onclick: () => switchTab('book') })),
    h('p', { class: 'ws-kicker', text: chapter ? guideHeading(chapter) : t('tabGuide') }),
    title,
    h('div', { class: 'g-body' }, renderGuideText(sec.text, q)),
    refs.length ? h('div', { class: 'card g-refs' },
      h('span', { class: 'field-label', text: t('guideSheetsRef') }),
      h('div', { class: 'ws-tools' }, refs.map(ws => h('button', {
        class: 'btn', type: 'button', onclick: () => openSheet(ws.id),
      }, t('sheetName', { n: ws.order, title: ws.title }))))) : null);
}

function renderGuideFooter() {
  const sec = GUIDE_INDEX[state.ui.guideSection] || GUIDE.sections[0];
  const prev = GUIDE.sections[sec.index - 1], next = GUIDE.sections[sec.index + 1];
  document.getElementById('footer').replaceChildren(
    h('button', { class: 'btn', type: 'button', disabled: !prev, text: t('guidePrev'),
      onclick: () => showGuideSection(prev.id) }),
    h('div', { class: 'progress' },
      h('span', { class: 'progress-label', text: t('guidePos', { n: sec.index + 1, total: GUIDE.sections.length }) })),
    h('button', { class: 'btn primary', type: 'button', disabled: !next, text: t('guideNext'),
      onclick: () => showGuideSection(next.id) }));
}

/* ==============================================================================
   PRINT —""")

# ---------------------------------------------------------------- PRINT
rep("""function defaultPrintTarget() {
  const s = currentStep();""", """function defaultPrintTarget() {
  if (state.ui.tab === 'guide') return 'guide:' + state.ui.guideSection;
  const s = currentStep();""")
rep("""    section = h('section', { class: 'print-section' }, h('div', { class: 'print-plan', text: text }));
  } else {""", """    section = h('section', { class: 'print-section' }, h('div', { class: 'print-plan', text: text }));
  } else if (target.indexOf('guide:') === 0) {
    const sec = GUIDE_INDEX[target.slice(6)] || GUIDE.sections[0];
    section = h('section', { class: 'print-section print-guide' },
      h('h2', { text: guideHeading(sec) }), renderGuideText(sec.text, ''));
  } else {""")

# ---------------------------------------------------------------- IMPORT (older files)
rep("""  if (!isObj(data) || data.app !== CONFIG.APP_ID) fail('errWrongApp');
  if (typeof data.version !== 'number') failAt('version', 'probNumber');""", """  if (!isObj(data) || data.app !== CONFIG.APP_ID) fail('errWrongApp');
  if (typeof data.version !== 'number') failAt('version', 'probNumber');
  if (data.version === 1) data = migrateV1(data);""")
rep("  if (data.version < CONFIG.DATA_VERSION) fail('errOlder', { v: data.version });\n",
    "  if (data.version < 1) failAt('version', 'probOption');\n")
rep("""function importText(text) {""", """/** Map a first-version export (ертегі, 3 worksheets) onto the 31-sheet layout.
    Types are checked by validateImport afterwards. */
function migrateV1(d) {
  const a = isObj(d.answers) ? d.answers : {};
  const fr = isObj(a.first_reading) ? a.first_reading : {};
  const pm = isObj(a.plot_map) ? a.plot_map : {};
  const st = isObj(pm.stages) ? pm.stages : {};
  const chars = isObj(a.characters) && Array.isArray(a.characters.list) ? a.characters.list.filter(isObj) : [];
  const ROLE = { main: 'Бас кейіпкер', helper: 'Көмекші кейіпкер', antagonist: 'Қарсылас' };
  const CONFLICT = { person_person: 'тұлға–тұлға', person_nature: 'тұлға–табиғат', person_self: 'тұлға–өзі' };
  const text = v => (typeof v === 'string' ? v : '');
  const traits = c => (Array.isArray(c.traits) ? c.traits.filter(x => typeof x === 'string' && x.trim()) : []);
  const out = {};
  const put = (wsId, fieldId, v) => {
    const empty = Array.isArray(v) ? !v.some(x => (Array.isArray(x) ? x.some(Boolean) : x)) : !v;
    if (!empty) (out[wsId] = out[wsId] || {})[fieldId] = v;
  };
  put('ws-01-first-reading', 'first_impression', fr.impression);
  put('ws-01-first-reading', 'unclear', fr.studentQuestion);
  put('ws-02-theme-idea', 'theme_word', Array.isArray(fr.keywords) ? fr.keywords.filter(x => typeof x === 'string' && x.trim()).join(', ') : '');
  ['exposition', 'development', 'tension', 'climax', 'resolution'].forEach(k => put('ws-04-plot', k, st[k]));
  put('ws-06-conflict', 'conflict_type', CONFLICT[pm.conflictType] || '');
  put('ws-06-conflict', 'main_conflict', pm.conflictText);
  const main = chars.find(c => c.role === 'main') || chars[0];
  if (main) {
    put('ws-07-character', 'character', main.name);
    put('ws-07-character', 'traits', traits(main).slice(0, CONFIG.LIST_ROWS));
    put('ws-08-evolution', 'end', main.change);
  }
  put('ws-09-relations', 'characters', chars.slice(0, 4).map(c =>
    [text(c.name), [ROLE[c.role], traits(c).join(', ')].filter(Boolean).join(' — ')]));
  put('ws-16-quotes', 'quotes', chars.filter(c => text(c.quote).trim()).slice(0, CONFIG.LIST_ROWS)
    .map(c => (text(c.name) ? text(c.name) + ': ' : '') + c.quote));
  const meta = isObj(d.meta) ? d.meta : {};
  if (meta.genre === 'ertegi') put('ws-29-folklore', 'folk_genre', 'ертегі');
  return {
    app: d.app,
    version: CONFIG.DATA_VERSION,
    meta: { genre: meta.genre === 'ertegi' ? 'folklore' : 'all', title: meta.title, author: '', grade: meta.grade },
    answers: out,
    lessonPlan: isObj(d.lessonPlan) && d.lessonPlan.edited === true ? d.lessonPlan : null,
  };
}

function importText(text) {""")
rep("""    showBanner('ok', t('importOk'));
  });""", """    showBanner('ok', t(data.version === 1 ? 'importMigrated' : 'importOk'));
  });""")

open(out, 'w', encoding='utf8').write(s)
print('wrote', out, len(s.encode('utf8')) // 1024, 'KB')
