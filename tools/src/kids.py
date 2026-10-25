"""Children's literature: «Балалар әдебиеті» tab with the book list by age (kids.json).
Usage: python3 -I kids.py in.html kids.json out.html   (run after glossary.py)"""
import json, sys

src, kfile, out = sys.argv[1:4]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('kids anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

kids = json.load(open(kfile, encoding='utf8'))
groups = [{'id': 'k%d' % i, 'title': g['title'], 'intro': g['intro'], 'books': g['books']}
          for i, g in enumerate(kids['groups'], 1)]
total = sum(len(g['books']) for g in groups)
data = json.dumps({'groups': groups}, ensure_ascii=False, indent=1).replace('</', '<\\/')

# ---- CSS ----
rep('</head>', """<style id="kids">
  /* KIDS — «Балалар әдебиеті» tab */
  .tab-short { display: none; }
  .k-intro { margin: 0 0 14px; color: var(--ink-2); }
  .k-chips { display: flex; flex-wrap: wrap; gap: 6px; margin: 0 0 20px; }
  .k-chip { border: 1px solid var(--line-strong); background: var(--surface); color: var(--ink-2);
    border-radius: 999px; padding: 6px 14px; font-weight: 600; font-size: 14px; }
  .k-chip[aria-pressed="true"] { background: var(--accent); border-color: var(--accent); color: var(--accent-ink, #fff); }
  .k-group { margin: 0 0 28px; scroll-margin-top: 12px; }
  .k-group-title { margin: 0 0 4px; font-family: var(--display); font-size: 20px; }
  .k-group-intro { margin: 0 0 12px; color: var(--ink-2); font-size: 15px; }
  .k-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr)); gap: 12px; }
  .k-card { display: flex; flex-direction: column; gap: 6px; padding: 14px 16px; background: var(--surface);
    border: 1px solid var(--line); border-radius: 14px; box-shadow: var(--shadow-sm); }
  .k-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; }
  .k-num { color: var(--ink-2); font-size: 13px; font-weight: 600; }
  .k-age { flex: none; max-width: 70%; text-align: right; font-size: 12.5px; font-weight: 700; color: var(--accent);
    background: var(--accent-soft); border-radius: 8px; padding: 2px 8px; }
  .k-age.unknown { color: var(--ink-2); background: var(--surface-2); font-weight: 600; }
  .k-title { margin: 0; font-size: 17px; line-height: 1.3; }
  .k-author { margin: 0; font-weight: 600; }
  .k-edition { margin: 0; font-size: 13px; color: var(--ink-2); }
  .k-desc { margin: 2px 0 0; line-height: 1.55; }
  .k-topics { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 2px; }
  .k-topic { font-size: 12.5px; background: var(--surface-2); border: 1px solid var(--line); border-radius: 999px; padding: 2px 9px; }
  .k-source { margin: 0; font-size: 12px; color: var(--ink-2); }
  .k-card .btn { align-self: flex-start; margin-top: auto; font-size: 14px; padding: 7px 12px; }
  .k-actions { margin-top: auto; padding-top: 6px; }
  @media (max-width: 1180px) and (min-width: 901px) { .tab-long { display: none; } .tab-short { display: inline; } }
  @media (max-width: 520px) {
    .tab-long { display: none; } .tab-short { display: inline; }
    .tabs { overflow-x: auto; scrollbar-width: none; }
    .tabs .tab { flex: 1 0 auto; }
  }
  @media print {
    .print-kids h3 { margin: 12pt 0 4pt; font-size: 13pt; break-after: avoid; }
    .print-kids .pk { margin: 0 0 6pt; break-inside: avoid; }
    .print-kids .pk b { font-size: 11pt; }
    .print-kids .pk div { font-size: 10pt; }
  }
</style>
</head>""")

# ---- Strings ----
rep("  tabGlossary: 'Сөздік',", """  tabGlossary: 'Сөздік',
  tabKids: 'Балалар әдебиеті',
  tabKidsShort: 'Кітаптар',
  kTitle: 'Балалар әдебиеті',
  kIntro: [
    'Әр баланың қабылдауы, қызығушылығы мен ойлау ерекшелігі жасына қарай өзгереді. Сондықтан баланың жасына сай кітап таңдау оның оқиға желісін түсінуіне, кейіпкерлермен бірге сезінуіне, қиялын дамытуына және кітап оқуға деген қызығушылығын арттыруға көмектеседі.',
    'Бұл бөлімде әр жас кезеңіне лайықталған кітаптарды таба аласыз. Балаңыздың жасына, қызығушылығына және оқу дағдысына сәйкес шығарманы таңдап, кітап әлеміне бірге саяхат жасаңыз.',
  ],
  kAll: 'Барлығы',
  kAges: 'Жас санаттары',
  kSearch: 'Кітаптан іздеу',
  kSearchPh: 'Кітап, автор немесе тақырып…',
  kFound: 'Табылды: {n} кітап',
  kNone: 'Ештеңе табылмады. Басқа сөзбен іздеп көріңіз.',
  kCount: '{n} кітап',
  kAuthor: 'Автор',
  kTopics: 'Тақырып',
  kSource: 'Дереккөз',
  kAnalyze: 'Осы кітапты талдау →',
  kAnalyzeDone: '«{title}» үшін жаңа талдау ашылды. Жанр: Балалар әдебиеті.',""")
rep("      '«Сөздік» қойындысында әдеби терминдердің",
    "      '«Балалар әдебиеті» қойындысында жасқа қарай іріктелген %d кітап бар. «Осы кітапты талдау» батырмасы сол кітапқа жаңа талдау ашады.',\n"
    "      '«Сөздік» қойындысында әдеби терминдердің" % total)
rep("    'Әдеби терминдер сөздігі: ",
    "    'Балалар әдебиеті: жас санатына қарай іріктелген %d кітап',\n    'Әдеби терминдер сөздігі: " % total)

# ---- Tabs and dispatch ----
rep("['library', 'book', 'guide', 'glossary'].map(tab", "['library', 'book', 'guide', 'glossary', 'kids'].map(tab")
rep("      }, t({ library: 'tabLibrary', book: 'tabBook', guide: 'tabGuide', glossary: 'tabGlossary' }[tab])))),",
    "      }, tab === 'kids' ? [h('span', { class: 'tab-long', text: t('tabKids') }), h('span', { class: 'tab-short', text: t('tabKidsShort') })]\n"
    "        : t({ library: 'tabLibrary', book: 'tabBook', guide: 'tabGuide', glossary: 'tabGlossary' }[tab])))),")
rep("t(state.ui.tab === 'guide' || state.ui.tab === 'glossary' ? 'navGuide' : 'navBook')",
    "t(['guide', 'glossary', 'kids'].includes(state.ui.tab) ? 'navGuide' : 'navBook')")
rep("tab: ['guide', 'library', 'glossary'].includes(u.tab) ? u.tab : 'book',",
    "tab: ['guide', 'library', 'glossary', 'kids'].includes(u.tab) ? u.tab : 'book',", count=2)
rep("  if (state.ui.tab === 'glossary') { renderGlossarySidebar(); return; }",
    "  if (state.ui.tab === 'glossary') { renderGlossarySidebar(); return; }\n"
    "  if (state.ui.tab === 'kids') { renderKidsSidebar(); return; }")
rep("  if (state.ui.tab === 'glossary') { renderGlossaryFooter(); return; }",
    "  if (state.ui.tab === 'glossary') { renderGlossaryFooter(); return; }\n"
    "  if (state.ui.tab === 'kids') { renderKidsFooter(); return; }")
rep("""  if (state.ui.tab === 'guide' || state.ui.tab === 'library' || state.ui.tab === 'glossary') {
    box.replaceChildren(h('div', { id: 'banner-slot' }), state.ui.tab === 'guide' ? renderGuideMain()
      : state.ui.tab === 'glossary' ? renderGlossaryMain() : renderLibraryMain());""",
    """  if (state.ui.tab !== 'book') {
    box.replaceChildren(h('div', { id: 'banner-slot' }), state.ui.tab === 'guide' ? renderGuideMain()
      : state.ui.tab === 'glossary' ? renderGlossaryMain() : state.ui.tab === 'kids' ? renderKidsMain() : renderLibraryMain());""")
rep("  if (state.ui.tab === 'glossary') return 'glossary';",
    "  if (state.ui.tab === 'glossary') return 'glossary';\n"
    "  if (state.ui.tab === 'kids') return 'kids';")
rep("""  } else if (target === 'glossary') {""",
    """  } else if (target === 'kids') {
    section = h('section', { class: 'print-section print-kids' }, h('h2', { text: t('kTitle') }),
      kidsShown().map(x => [h('h3', { text: x.group.title }), x.books.map(b => h('div', { class: 'pk' },
        h('b', { text: b.n + '. ' + b.title }),
        h('div', { text: t('kAuthor') + ': ' + b.author + ' · ' + b.age }),
        h('div', { text: b.desc }),
        h('div', { text: t('kTopics') + ': ' + b.topics.join(', ') })))]));
  } else if (target === 'glossary') {""")

# Phones: the tab row can scroll sideways, so keep the open tab in view.
rep("""    h('span', { id: 'save-status', class: 'save-status', 'aria-live': 'polite' }),
  );
  setSaveStatus();""", """    h('span', { id: 'save-status', class: 'save-status', 'aria-live': 'polite' }),
  );
  setSaveStatus();
  const openTab = bar.querySelector('.tab[aria-selected="true"]'), row = openTab && openTab.parentNode;
  if (row && row.scrollWidth > row.clientWidth) row.scrollLeft = openTab.offsetLeft - row.offsetLeft - 8;""")

# ---- Data + rendering ----
rep("""/* ==============================================================================
   PRINT — fills #print-area""", """/* ==============================================================================
   KIDS — «Балалар әдебиеті»: books by age group (data from kids.json)
   ============================================================================== */
const KIDS = %s;
let kidsQuery = '', kidsAge = '';   // not saved: the list opens unfiltered

function kidsMatch(b, f) {
  return !f || fold([b.title, b.author, b.edition, b.age, b.desc, b.topics.join(', ')].join('\\n')).indexOf(f) !== -1;
}
/** Groups and books that pass the age filter and the search. */
function kidsShown() {
  const f = fold(kidsQuery.trim());
  return KIDS.groups.filter(g => !kidsAge || g.id === kidsAge)
    .map(g => ({ group: g, books: g.books.filter(b => kidsMatch(b, f)) })).filter(x => x.books.length);
}
function kidsTotal() { return kidsShown().reduce((a, x) => a + x.books.length, 0); }
function kidsUpdate() { updateKidsNav(); renderMain(); renderFooter(); }
function setKidsAge(id) { kidsAge = id; closeNav(); kidsUpdate(); document.getElementById('main').scrollTop = 0; }

function renderKidsSidebar() {
  const nav = document.getElementById('sidebar');
  nav.replaceChildren(
    h('h2', null, h('label', { for: 'kids-search', text: t('kSearch') })),
    h('div', { class: 'g-search' }, h('input', {
      id: 'kids-search', type: 'search', value: kidsQuery, maxlength: 100,
      placeholder: t('kSearchPh'), autocomplete: 'off',
      oninput: e => { kidsQuery = e.target.value; kidsUpdate(); },
    })),
    h('p', { id: 'kids-results', class: 'g-results', 'aria-live': 'polite' }),
    h('h2', { text: t('kAges') }),
    h('ul', { id: 'kids-nav', class: 'steps gl-nav' }));
  updateKidsNav();
}

function updateKidsNav() {
  const f = fold(kidsQuery.trim());
  const count = g => g.books.filter(b => kidsMatch(b, f)).length;
  const all = KIDS.groups.reduce((a, g) => a + count(g), 0);
  document.getElementById('kids-results').textContent = f ? (all ? t('kFound', { n: all }) : t('kNone')) : '';
  const item = (id, label, n) => h('li', null, h('button', {
    type: 'button', class: 'step-btn', 'aria-current': kidsAge === id ? 'page' : null, onclick: () => setKidsAge(id),
  }, h('span', { class: 'step-label' }, label), h('span', { class: 'g-count' }, String(n))));
  const list = document.getElementById('kids-nav');
  list.replaceChildren.apply(list, [item('', t('kAll'), all)].concat(KIDS.groups.map(g => item(g.id, g.title, count(g)))));
}

/** «Әлканың күміс тұмары» (ертегі) → Әлканың күміс тұмары: the form's title field adds the quotes itself. */
function kidsWorkTitle(title) {
  let s = title.trim();
  while (/\\s*\\([^()]*\\)$/.test(s)) s = s.replace(/\\s*\\([^()]*\\)$/, '');
  return s.replace(/^«(.*)»$/, '$1');
}

function analyzeBook(b) {
  newAnalysis();
  state.meta.title = kidsWorkTitle(b.title);
  state.meta.author = b.author;
  state.meta.genre = 'children';
  state.lessonPlan.text = '';
  saveStateNow();
  state.ui.tab = 'book';
  render();
  document.getElementById('main').scrollTop = 0;
  showBanner('ok', t('kAnalyzeDone', { title: state.meta.title }));
}

function renderKidsMain() {
  const q = kidsQuery.trim();
  const shown = kidsShown();
  const hl = (tag, cls, text) => { const el = h(tag, { class: cls }); appendHighlighted(el, text, q); return el; };
  return h('article', { class: 'kids' },
    photoBanner('kids'),
    h('p', { class: 'ws-kicker', text: t('tabKids') }),
    h('h2', { class: 'ws-title', text: t('kTitle') }),
    STRINGS.kIntro.map(text => h('p', { class: 'k-intro', text: text })),
    h('div', { class: 'k-chips', role: 'group', 'aria-label': t('kAges') },
      [['', t('kAll')]].concat(KIDS.groups.map(g => [g.id, g.title])).map(([id, label]) => h('button', {
        type: 'button', class: 'k-chip', 'aria-pressed': kidsAge === id ? 'true' : 'false', onclick: () => setKidsAge(id),
      }, label))),
    shown.length ? shown.map(x => h('section', { class: 'k-group', id: 'kg-' + x.group.id },
      h('h3', { class: 'k-group-title', text: x.group.title }),
      h('p', { class: 'k-group-intro', text: x.group.intro }),
      h('div', { class: 'k-grid' }, x.books.map(b => h('div', { class: 'k-card' },
        h('div', { class: 'k-top' }, h('span', { class: 'k-num', text: x.group.title + ' · ' + b.n }),
          hl('span', 'k-age' + (/^\\d/.test(b.age) ? '' : ' unknown'), b.age)),
        hl('h4', 'k-title', b.title),
        hl('p', 'k-author', b.author),
        hl('p', 'k-edition', b.edition),
        h('div', { class: 'k-desc' }, b.desc.split('\\n\\n').map(p => hl('p', 'k-p', p))),
        h('div', { class: 'k-topics', 'aria-label': t('kTopics') }, b.topics.map(tp => hl('span', 'k-topic', tp))),
        h('p', { class: 'k-source', text: t('kSource') + ': ' + b.source }),
        h('div', { class: 'k-actions' }, h('button', { class: 'btn', type: 'button', text: t('kAnalyze'), onclick: () => analyzeBook(b) })))))))
      : h('p', { class: 'card gl-empty', text: t('kNone') }));
}

function renderKidsFooter() {
  document.getElementById('footer').replaceChildren(
    h('button', { class: 'btn', type: 'button', text: t('glBack'), onclick: () => switchTab('book') }),
    h('div', { class: 'progress' }, h('span', { class: 'progress-label', text: t('kCount', { n: kidsTotal() }) })),
    h('button', { class: 'btn primary', type: 'button', text: t('printBtn'), onclick: () => printOutputs('kids') }));
}

/* ==============================================================================
   PRINT — fills #print-area""" % data, count=1)

s = s.replace('      python3 glossary.py photos.html glossary.txt kobem-talday.html',
              '      python3 glossary.py photos.html glossary.txt gloss.html\n'
              '      python3 kids_extract.py kids.docx kids.json        # «Балалар әдебиеті» list\n'
              '      python3 kids.py gloss.html kids.json kobem-talday.html')

open(out, 'w', encoding='utf8').write(s)
print('kids: %d groups, %d books -> %s' % (len(groups), total, out))
