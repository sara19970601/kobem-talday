"""Glossary: «Сөздік» tab with the literary terms dictionary (glossary.txt).
Usage: python3 -I glossary.py in.html glossary.txt out.html   (run after photos.py)"""
import json, re, sys

src, gfile, out = sys.argv[1:4]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('glossary anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

# glossary.txt: "I. Section title" lines, then "Term — definition" lines (split at the first dash).
sections = []
for line in open(gfile, encoding='utf8'):
    line = line.strip()
    if not line:
        continue
    m = re.match(r'^([IVX]+)\.\s+(.+)$', line)
    if m:
        sections.append({'id': m[1], 'title': m[2], 'terms': []})
        continue
    if ' — ' not in line or not sections:
        sys.exit('glossary: unexpected line %r' % line)
    term, definition = line.split(' — ', 1)
    sections[-1]['terms'].append({'term': term, 'def': definition})
total = sum(len(x['terms']) for x in sections)
data = json.dumps({'sections': sections}, ensure_ascii=False, indent=1).replace('</', '<\\/')

# ---- CSS ----
rep('</head>', """<style id="glossary">
  /* GLOSSARY — «Сөздік» tab */
  .gl-intro { margin: 0 0 18px; color: var(--ink-2); }
  .gl-sec { margin: 0 0 26px; scroll-margin-top: 12px; }
  .gl-sec-title { display: flex; gap: 10px; align-items: baseline; margin: 0 0 10px; padding-bottom: 6px;
    border-bottom: 2px solid var(--line); font-family: var(--display); font-size: 18px; }
  .gl-num { flex: none; color: var(--gold, var(--accent)); font-weight: 700; }
  .gl-list { margin: 0; display: grid; gap: 8px; }
  .gl-item { margin: 0; padding: 12px 14px; background: var(--surface); border: 1px solid var(--line);
    border-radius: 12px; box-shadow: var(--shadow-sm); }
  .gl-item dt { font-weight: 700; color: var(--accent); margin: 0 0 3px; font-size: 16px; }
  .gl-item dd { margin: 0; line-height: 1.55; }
  .gl-empty { padding: 18px; text-align: center; color: var(--ink-2); }
  .gl-nav .step-btn { align-items: baseline; }
  .gl-nav .step-num { font-size: 12px; }
  @media (max-width: 520px) {   /* four tabs: size to their labels instead of equal widths */
    .tabs .tab { flex: 1 1 auto; padding: 7px 5px; font-size: 13px; text-overflow: clip; }
  }
  @media (max-width: 370px) { .tabs .tab { padding: 7px 2px; font-size: 12px; } }
  /* Narrow phones: long button labels wrap instead of pushing past the screen edge. */
  @media (max-width: 420px) {
    .footer .btn, #back-to-book { white-space: normal; min-width: 0; max-width: 100%; text-align: center; }
    .footer .progress:has(> .progress-label:only-child) { display: none; }
  }
  @media print {
    .print-gloss h3 { margin: 12pt 0 4pt; font-size: 12.5pt; break-after: avoid; }
    .print-gloss dl { margin: 0; }
    .print-gloss dt { font-weight: 700; margin-top: 5pt; break-after: avoid; }
    .print-gloss dd { margin: 0 0 2pt; }
  }
</style>
</head>""")

# ---- Strings ----
rep("  tabLibrary: 'Талдауларым',", """  tabLibrary: 'Талдауларым',
  tabGlossary: 'Сөздік',
  glTitle: 'Әдеби терминдер сөздігі',
  glIntro: 'Шығарманы талдауда жиі қолданылатын %d терминнің қысқаша анықтамасы. Терминді табу үшін «Сөздіктен іздеу» жолағына сөзді жазыңыз (телефонда ол ☰ батырмасының ішінде).',
  glSearch: 'Сөздіктен іздеу',
  glSearchPh: 'Термин немесе сөз…',
  glSections: 'Бөлімдер',
  glFound: 'Табылды: {n} термин',
  glNone: 'Ештеңе табылмады. Басқа сөзбен іздеп көріңіз.',
  glCount: '{n} термин',
  glBack: '← Дәптерге оралу',""" % total)
rep("      'Әр парақтағы «Нұсқаулық: 2.8 →» сияқты батырма әдістемелік түсініктемені ашады. «Дәптерге оралу» сізді сол параққа қайтарады, жазғаныңыз өшпейді.',",
    "      'Әр парақтағы «Нұсқаулық: 2.8 →» сияқты батырма әдістемелік түсініктемені ашады. «Дәптерге оралу» сізді сол параққа қайтарады, жазғаныңыз өшпейді.',\n"
    "      '«Сөздік» қойындысында әдеби терминдердің (тақырып, идея, сюжет, хронотоп т.б.) анықтамасы бар. Іздеу жолағына сөзді жазсаңыз, керек термин бірден шығады.',")
rep("    'Әдістемелік нұсқаулық: 16 бөлім, әр параққа сілтеме, ішінен іздеу',",
    "    'Әдістемелік нұсқаулық: 16 бөлім, әр параққа сілтеме, ішінен іздеу',\n"
    "    'Әдеби терминдер сөздігі: %d термин, 6 бөлім, іздеу',""" % total)

# ---- Brand: the name only, «Көркем шығарманы талдау» (no subtitle line) ----
rep("      h('h1', { text: t('appTitle') }),\n      h('p', { text: t('appSubtitle') }))),",
    "      h('h1', { text: t('appTitle') }))),")
rep("  appSubtitle: 'Мұғалімге арналған жұмыс дәптері',\n", "")

# ---- Tabs and dispatch ----
rep("['library', 'book', 'guide'].map(tab", "['library', 'book', 'guide', 'glossary'].map(tab")
rep("t({ library: 'tabLibrary', book: 'tabBook', guide: 'tabGuide' }[tab])",
    "t({ library: 'tabLibrary', book: 'tabBook', guide: 'tabGuide', glossary: 'tabGlossary' }[tab])")
rep("t(state.ui.tab === 'guide' ? 'navGuide' : 'navBook')",
    "t(state.ui.tab === 'guide' || state.ui.tab === 'glossary' ? 'navGuide' : 'navBook')")
rep("tab: ['guide', 'library'].includes(u.tab) ? u.tab : 'book',",
    "tab: ['guide', 'library', 'glossary'].includes(u.tab) ? u.tab : 'book',", count=2)
rep("  if (state.ui.tab === 'library') { renderLibrarySidebar(); return; }",
    "  if (state.ui.tab === 'library') { renderLibrarySidebar(); return; }\n"
    "  if (state.ui.tab === 'glossary') { renderGlossarySidebar(); return; }")
rep("  if (state.ui.tab === 'library') { renderLibraryFooter(); return; }",
    "  if (state.ui.tab === 'library') { renderLibraryFooter(); return; }\n"
    "  if (state.ui.tab === 'glossary') { renderGlossaryFooter(); return; }")
rep("""  if (state.ui.tab === 'guide' || state.ui.tab === 'library') {
    box.replaceChildren(h('div', { id: 'banner-slot' }), state.ui.tab === 'guide' ? renderGuideMain() : renderLibraryMain());""",
    """  if (state.ui.tab === 'guide' || state.ui.tab === 'library' || state.ui.tab === 'glossary') {
    box.replaceChildren(h('div', { id: 'banner-slot' }), state.ui.tab === 'guide' ? renderGuideMain()
      : state.ui.tab === 'glossary' ? renderGlossaryMain() : renderLibraryMain());""")
rep("  if (state.ui.tab === 'guide') return 'guide:' + state.ui.guideSection;",
    "  if (state.ui.tab === 'guide') return 'guide:' + state.ui.guideSection;\n"
    "  if (state.ui.tab === 'glossary') return 'glossary';")
rep("""  } else if (target.indexOf('guide:') === 0) {""",
    """  } else if (target === 'glossary') {
    section = h('section', { class: 'print-section print-gloss' }, h('h2', { text: t('glTitle') }),
      GLOSSARY.sections.map(sec => [h('h3', { text: sec.id + '. ' + sec.title }),
        h('dl', null, sec.terms.map(x => [h('dt', { text: x.term }), h('dd', { text: x.def })]))]));
  } else if (target.indexOf('guide:') === 0) {""")

# ---- Data + rendering ----
rep("""/* ==============================================================================
   PRINT — fills #print-area""", """/* ==============================================================================
   GLOSSARY — «Әдеби терминдер сөздігі» (data from glossary.txt)
   ============================================================================== */
const GLOSSARY = %s;
let glossQuery = '';   // not saved: the dictionary opens unfiltered

function glossMatches(sec, q) {
  const f = fold(q);
  return f ? sec.terms.filter(x => fold(x.term + '\\n' + x.def).indexOf(f) !== -1) : sec.terms;
}

function renderGlossarySidebar() {
  const nav = document.getElementById('sidebar');
  nav.replaceChildren(
    h('h2', null, h('label', { for: 'gloss-search', text: t('glSearch') })),
    h('div', { class: 'g-search' }, h('input', {
      id: 'gloss-search', type: 'search', value: glossQuery, maxlength: 100,
      placeholder: t('glSearchPh'), autocomplete: 'off',
      oninput: e => { glossQuery = e.target.value; updateGlossaryNav(); renderMain(); renderFooter(); },
    })),
    h('p', { id: 'gloss-results', class: 'g-results', 'aria-live': 'polite' }),
    h('h2', { text: t('glSections') }),
    h('ul', { id: 'gloss-nav', class: 'steps gl-nav' }));
  updateGlossaryNav();
}

function updateGlossaryNav() {
  const q = glossQuery.trim();
  const counts = GLOSSARY.sections.map(sec => glossMatches(sec, q).length);
  const hits = counts.reduce((a, b) => a + b, 0);
  document.getElementById('gloss-results').textContent = q ? (hits ? t('glFound', { n: hits }) : t('glNone')) : '';
  document.getElementById('gloss-nav').replaceChildren.apply(document.getElementById('gloss-nav'),
    GLOSSARY.sections.map((sec, i) => q && !counts[i] ? null : h('li', null, h('button', {
      type: 'button', class: 'step-btn',
      onclick: () => {
        closeNav();
        const el = document.getElementById('gl-' + sec.id);
        if (el) el.scrollIntoView({ block: 'start' });
      },
    }, h('span', { class: 'step-num', 'aria-hidden': 'true' }, sec.id),
      h('span', { class: 'step-label' }, sec.title),
      q ? h('span', { class: 'g-count' }, String(counts[i])) : null))).filter(Boolean));
}

function renderGlossaryMain() {
  const q = glossQuery.trim();
  const secs = GLOSSARY.sections.map(sec => ({ sec: sec, terms: glossMatches(sec, q) })).filter(x => x.terms.length);
  return h('article', { class: 'glossary' },
    photoBanner('plan'),
    h('p', { class: 'ws-kicker', text: t('tabGlossary') }),
    h('h2', { class: 'ws-title', text: t('glTitle') }),
    h('p', { class: 'gl-intro', text: t('glIntro') }),
    secs.length ? secs.map(x => h('section', { class: 'gl-sec', id: 'gl-' + x.sec.id },
      h('h3', { class: 'gl-sec-title' }, h('span', { class: 'gl-num' }, x.sec.id + '.'), h('span', null, x.sec.title)),
      h('dl', { class: 'gl-list' }, x.terms.map(term => {
        const dt = h('dt'), dd = h('dd');
        appendHighlighted(dt, term.term, q);
        appendHighlighted(dd, term.def, q);
        return h('div', { class: 'gl-item' }, dt, dd);
      }))))
      : h('p', { class: 'card gl-empty', text: t('glNone') }));
}

function renderGlossaryFooter() {
  const q = glossQuery.trim();
  const n = GLOSSARY.sections.reduce((a, sec) => a + glossMatches(sec, q).length, 0);
  document.getElementById('footer').replaceChildren(
    h('button', { class: 'btn', type: 'button', text: t('glBack'),
      onclick: () => switchTab('book') }),
    h('div', { class: 'progress' }, h('span', { class: 'progress-label', text: t('glCount', { n: n }) })),
    h('button', { class: 'btn primary', type: 'button', text: t('printBtn'), onclick: () => printOutputs('glossary') }));
}

/* ==============================================================================
   PRINT — fills #print-area""" % data)

# README pipeline
if 'python3 photos.py modern.html photos kobem-talday.html' in s:
    s = s.replace('python3 photos.py modern.html photos kobem-talday.html',
                  'python3 photos.py modern.html photos photos.html\n      python3 glossary.py photos.html glossary.txt kobem-talday.html')

open(out, 'w', encoding='utf8').write(s)
print('glossary: %d sections, %d terms -> %s' % (len(sections), total, out))
