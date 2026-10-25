"""Lab tool 2: «Сюжет пен композицияны талдау» inside the shared «Зертхана».
Turns the lab into a set of tools (a switcher on top); the character tool keeps its
steps, its storage key and its document exactly as before.
Usage: python3 -I plot.py in.html out.html   (run after lab.py)"""
import sys

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('plot anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

# ---- CSS ----
rep('</style>\n</head>', r"""</style>
<style id="lab-tools">
  /* LAB TOOLS — switcher between the analyses of «Зертхана» */
  .lab-tools { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 240px), 1fr)); gap: 10px; margin: 0 0 14px; }
  .lab-tool { display: flex; flex-direction: column; gap: 3px; text-align: left; padding: 12px 14px; border-radius: 14px;
    border: 1px solid var(--line-strong); background: var(--surface); color: var(--ink); }
  .lab-tool b { font-size: 15.5px; }
  .lab-tool small { color: var(--ink-2); font-size: 13px; line-height: 1.4; }
  .lab-tool:hover { border-color: var(--accent); }
  .lab-tool[aria-pressed="true"] { border-color: var(--accent); background: var(--accent-soft); box-shadow: inset 0 0 0 1px var(--accent); }
  .lab-tool[aria-pressed="true"] b { color: var(--accent); }
  .lab-doc-meta { margin: 0 0 8px; color: var(--ink-2); }
  .lab-excerpt textarea { min-height: 180px; }
  @media (max-width: 520px) {   /* phones: the two tools side by side, names only */
    .lab-tools { grid-template-columns: 1fr 1fr; gap: 8px; }
    .lab-tool { padding: 9px 10px; justify-content: center; }
    .lab-tool b { font-size: 14px; line-height: 1.3; }
    .lab-tool small { display: none; }
  }
  @media print { .print-lab .lab-doc-meta { margin: 0 0 6pt; } }
</style>
</head>""")

# ---- Strings ----
rep("  labClearAsk: 'Зертханадағы барлық жауап өшіріледі. Бұл әрекетті қайтару мүмкін емес. Жалғастырасыз ба?',",
    "  labClearAsk: 'Осы талдаудағы барлық жауап өшіріледі. Бұл әрекетті қайтару мүмкін емес. Жалғастырасыз ба?',")
rep("  labDocNote: 'Бұл — әдеби кейіпкердің талдауы, психологиялық диагноз емес.',", r"""  labDocNote: 'Бұл — әдеби кейіпкердің талдауы, психологиялық диагноз емес.',
  labToolsLabel: 'Талдау түрі',
  labToolHero: 'Кейіпкер психологиясы',
  labToolHeroHint: 'Мінез, мақсат, эмоция, қарым-қатынас, өзгеріс',
  labToolPlot: 'Сюжет пен композиция',
  labToolPlotHint: 'Сюжеттің негізі, тартыс, композиция, интерпретация',
  plotTitle: 'Сюжет пен композицияны талдау',
  plotIntro: 'Шығарманың сюжетін, тартысын және композициялық құрылымын төрт кезеңде талдаңыз. Соңында жауаптарыңыз бір құжатқа жиналады.',
  plotPrep: 'Дайындық',
  plotStagePos: '{n}-кезең / 4',
  plotSummaryPos: 'Жинақтау',
  plotRules: [
    'Талдау тек сіз енгізген үзінді мен жауаптарыңызға сүйенеді. Мәтінде жоқ эпизодты немесе дәйексөзді ойдан қоспаңыз.',
    'Әр тұжырымды үзіндіден мысалмен бекітіңіз: әр кезеңде «Мәтіндік дәлел» өрісі бар.',
    'Сюжет — оқиғалардың себеп-салдарлы тізбегі; композиция — шығарма бөліктерінің орналасу тәртібі мен өзара байланысы.',
    'Мәтінге қатысы жоқ сұрақты бос қалдыра аласыз: бос жауап нәтижеге кірмейді.',
  ],
  plotDocTitle: 'Сюжет пен композицияны талдау',
  plotDocNote: 'Бұл талдау пайдаланушы енгізген мәтін мен жауаптарға сүйенеді.',""")

# ---- Tool registry: the character tool keeps its steps and key ----
rep("const LAB_STEPS = [\n  { id: 'about', title: 'Шығарма мен кейіпкер', rules: true,",
    "const LAB_HERO_STEPS = [\n  { id: 'about', title: 'Шығарма мен кейіпкер', rules: true,")
rep("""const LAB_FIELDS = {};
LAB_STEPS.forEach(st => (st.fields || []).forEach(f => { LAB_FIELDS[f.id] = f; }));""", r"""
/* «Сюжет пен композицияны талдау»: preparation, four stages, summary. */
const plotQ = (id, label, hints) => ({ id: id, type: 'long', label: label, hints: hints || [] });
const plotEvidence = (id, of, hints) => ({ id: id, type: 'long', label: 'Мәтіндік дәлел', evidenceFor: of,
  hints: hints || ['Жауаптарыңызды бекітетін эпизодты немесе қысқа дәйексөзді үзіндіден өзгертпей көшіріп жазыңыз.', 'Мүмкін болса, беті не тарауын көрсетіңіз.'] });
const LAB_PLOT_STEPS = [
  { id: 'plotPrep', title: 'Шығарма мен үзінді', badge: '✎', pos: 'plotPrep', rules: true,
    intro: 'Талдайтын шығарманы және үзіндіні енгізіңіз. Барлық кезең осы мәтінге сүйенеді.',
    fields: [
      { id: 'plWork', type: 'text', label: 'Шығарманың атауы', hints: ['Шығарманың толық атауын жазыңыз.'] },
      { id: 'plAuthor', type: 'text', label: 'Автордың аты-жөні', hints: ['Автордың аты-жөнін толық жазыңыз.'] },
      { id: 'plExcerpt', type: 'long', label: 'Талдайтын үзінді', cls: 'lab-excerpt',
        hints: ['Талдайтын үзіндіні немесе эпизодтарды осында қойыңыз.', 'Шығарма көлемді болса, негізгі эпизодтарды өз сөзіңізбен қысқаша жазып, маңызды сөйлемдерін тырнақшаға алыңыз.'] },
    ] },
  { id: 'plotBase', title: 'Сюжеттің негізі', badge: '1', stage: 1,
    fields: [
      plotQ('b1', '1. Шығармада қандай негізгі оқиға суреттеледі?', ['Оқиғаны бір-екі сөйлеммен атаңыз.']),
      plotQ('b2', '2. Шығарма басында қандай жағдай қалыптасқан?', ['Кейіпкерлер қайда, қандай күйде? Тепе-теңдік бар ма?']),
      plotQ('b3', '3. Негізгі тартыс неден туындайды?', ['Кім мен кім (немесе не) қарама-қарсы тұр?']),
      plotQ('b4', '4. Оқиғалардың дамуына қандай себептер әсер етеді?', ['Кейіпкердің шешімі, кездейсоқтық, қоғам, табиғат т.б.']),
      plotQ('b5', '5. Қай оқиғалар сюжеттің әрі қарай өрбуіне ықпал етеді?'),
      plotEvidence('ev1', ['b1', 'b2', 'b3', 'b4', 'b5']),
    ] },
  { id: 'plotConflict', title: 'Тартыс пен оқиғалардың дамуы', badge: '2', stage: 2,
    fields: [
      plotQ('c1', '1. Басты кейіпкер қандай кедергіге кездеседі?'),
      plotQ('c2', '2. Тартыс қалай күрделене түседі?', ['Тартысқа жаңа кейіпкер, жаңа себеп не жаңа қауіп қосыла ма?']),
      plotQ('c3', '3. Қақтығыстың шиеленісуіне қандай оқиғалар әсер етеді?'),
      plotQ('c4', '4. Шығармадағы ең шешуші оқиға қайсы?'),
      plotQ('c5', '5. Шарықтау шегі қай тұста көрінеді? Жауабыңызды мәтінмен негіздеңіз.', ['Шарықтау шегін көрсететін сөйлемді төмендегі «Мәтіндік дәлел» өрісіне жазыңыз.']),
      plotEvidence('ev2', ['c1', 'c2', 'c3', 'c4', 'c5']),
    ] },
  { id: 'plotComposition', title: 'Композициялық құрылым', badge: '3', stage: 3,
    fields: [
      plotQ('k1', '1. Шығарма қалай басталады және бұл басталу оқырманды қалай дайындайды?'),
      plotQ('k2', '2. Оқиғалар хронологиялық ретпен баяндала ма?', ['Рет бұзылса, автор оны неге осылай құрды деп ойлайсыз?']),
      plotQ('k3', '3. Еске алу, шегініс немесе алдын ала ишара кездеседі ме?', ['Кездессе, қай жерде және не үшін қолданылған?']),
      plotQ('k4', '4. Қандай эпизодтар бір-бірімен мағыналық байланыс жасайды?'),
      plotQ('k5', '5. Қайталау, қарама-қарсылық немесе параллель эпизодтар бар ма?'),
      plotQ('k6', '6. Шығармадағы аяқталу тартысты қалай шешеді?', ['Шешім ашық па, жабық па? Тартыс толық шешіле ме?']),
      plotQ('k7', '7. Тақырып пен композиция арасында қандай байланыс бар?'),
      plotEvidence('ev3', ['k1', 'k2', 'k3', 'k4', 'k5', 'k6', 'k7']),
    ] },
  { id: 'plotMeaning', title: 'Интерпретация және қорытынды', badge: '4', stage: 4,
    fields: [
      plotQ('i1', '1. Қай эпизод шығарманың негізгі идеясын ашуға ерекше үлес қосады?'),
      plotQ('i2', '2. Бір эпизодты алып тастасақ, шығарманың мағынасы қалай өзгерер еді?', ['Нақты бір эпизодты атап, сол арқылы жауап беріңіз.']),
      plotQ('i3', '3. Сюжеттік құрылым оқырманның кейіпкерлерге көзқарасына қалай әсер етеді?'),
      plotQ('i4', '4. Автор оқиғалардың дәл осылай өрбуі арқылы қандай ой ұсынады?'),
      plotQ('i5', '5. Сюжет пен композицияның шығарма мағынасын қалыптастырудағы рөлі туралы қорытындыңыз қандай?'),
      plotEvidence('ev4', ['i1', 'i2', 'i3', 'i4', 'i5']),
    ] },
  { id: 'plotSummary', title: 'Талдауды жинақтау', badge: '≡', pos: 'plotSummaryPos', summary: true,
    intro: 'Жауаптарыңыз бір құрылымды құжатқа жиналды. Бос өрістер құжатқа кірмейді.' },
];

const LAB_TOOLS = {
  hero: { key: LAB_KEY, steps: LAB_HERO_STEPS, label: 'labToolHero', hint: 'labToolHeroHint', title: 'labTitle', intro: 'labIntro',
    rules: 'labRules', diagnosis: true, doc: () => labHeroDoc() },
  plot: { key: 'kobem-talday:lab-plot', steps: LAB_PLOT_STEPS, label: 'labToolPlot', hint: 'labToolPlotHint', title: 'plotTitle', intro: 'plotIntro',
    rules: 'plotRules', diagnosis: false, doc: () => labPlotDoc() },
};
Object.values(LAB_TOOLS).forEach(tool => {
  tool.fields = {};
  tool.steps.forEach(st => (st.fields || []).forEach(f => { tool.fields[f.id] = f; }));
});
const LAB_TOOL_KEY = 'kobem-talday:lab-tool';
let labTool = 'hero', LAB_STEPS = LAB_HERO_STEPS, LAB_FIELDS = LAB_TOOLS.hero.fields;""")

# State: one answer set per tool; `lab` is the open tool's.
rep("""let lab = (() => {
  if (!labConsent) return labFresh();
  try { return labClean(JSON.parse(window.localStorage.getItem(LAB_KEY) || 'null')); } catch (e) { return labFresh(); }
})();""", """const labStates = {};
let lab = null;
function labSelect(id) {
  labTool = LAB_TOOLS[id] ? id : 'hero';
  LAB_STEPS = LAB_TOOLS[labTool].steps;
  LAB_FIELDS = LAB_TOOLS[labTool].fields;
  lab = labStates[labTool];
}
Object.keys(LAB_TOOLS).forEach(id => {
  labSelect(id);
  labStates[id] = (() => {
    if (!labConsent) return labFresh();
    try { return labClean(JSON.parse(window.localStorage.getItem(LAB_TOOLS[id].key) || 'null')); } catch (e) { return labFresh(); }
  })();
});
labSelect((() => { try { return labConsent && window.localStorage.getItem(LAB_TOOL_KEY) || 'hero'; } catch (e) { return 'hero'; } })());""")

rep("""  try { window.localStorage.setItem(LAB_KEY, JSON.stringify(lab)); } catch (e) { /* storage full or blocked */ }""",
    """  try {
    window.localStorage.setItem(LAB_TOOLS[labTool].key, JSON.stringify(lab));
    window.localStorage.setItem(LAB_TOOL_KEY, labTool);
  } catch (e) { /* storage full or blocked */ }""")
rep("""    if (on) { window.localStorage.setItem(LAB_CONSENT_KEY, '1'); labSaveNow(); }
    else { window.localStorage.removeItem(LAB_CONSENT_KEY); window.localStorage.removeItem(LAB_KEY); }""",
    """    if (on) {
      window.localStorage.setItem(LAB_CONSENT_KEY, '1');
      Object.keys(LAB_TOOLS).forEach(id => window.localStorage.setItem(LAB_TOOLS[id].key, JSON.stringify(labStates[id])));
      labSaveNow();
    } else {
      window.localStorage.removeItem(LAB_CONSENT_KEY);
      window.localStorage.removeItem(LAB_TOOL_KEY);
      Object.values(LAB_TOOLS).forEach(tool => window.localStorage.removeItem(tool.key));
    }""")
rep("  if (!on && labHasContent()) showBanner('ok', t('labSavedOff'));", "  if (!on && labAnyContent()) showBanner('ok', t('labSavedOff'));")
rep("""function labFieldFilled(f) {
  const v = lab.data[f.id];""", """function labFieldFilled(f, data) {
  const v = (data || lab.data)[f.id];""")
rep("""function labHasContent() { return Object.values(LAB_FIELDS).some(labFieldFilled); }""",
    """function labHasContent() { return Object.values(LAB_FIELDS).some(f => labFieldFilled(f)); }
function labAnyContent() {
  return Object.keys(LAB_TOOLS).some(id => Object.values(LAB_TOOLS[id].fields).some(f => labFieldFilled(f, labStates[id].data)));
}
function labSwitch(id) {
  if (id === labTool) return;
  labSaveNow();
  labSelect(id);
  labSaveNow();
  closeNav();
  renderSidebar(); renderMain(); renderFooter();
  document.getElementById('main').scrollTop = 0;
}
/** Step marker: the tool's own badge, or the step number. */
function labBadge(st, i) { return st.badge || (st.summary ? '≡' : String(i + 1)); }
function labPosText(i) {
  const st = LAB_STEPS[i];
  if (st.stage) return t('plotStagePos', { n: st.stage });
  if (st.pos) return t(st.pos);
  return t('labPos', { n: i + 1, total: LAB_STEPS.length });
}""")
rep("  if (!labConsent && labHasContent()) { e.preventDefault();", "  if (!labConsent && labAnyContent()) { e.preventDefault();")
rep("labStepDone(st) ? '✓' : st.summary ? '≡' : String(i + 1)", "labStepDone(st) ? '✓' : labBadge(st, i)")
rep("done ? '✓' : LAB_STEPS[i].summary ? '≡' : String(i + 1)", "done ? '✓' : labBadge(LAB_STEPS[i], i)")
rep("h('span', { class: 'n', text: x.summary ? '≡' : String(i + 1) })", "h('span', { class: 'n', text: labBadge(x, i) })")
rep("    h('p', { class: 'lab-pos', text: t('labPos', { n: lab.step + 1, total: LAB_STEPS.length }) }),",
    "    h('p', { class: 'lab-pos', text: labPosText(lab.step) }),")
rep("    h('div', { class: 'progress' }, h('span', { class: 'progress-label', text: t('labPos', { n: i + 1, total: LAB_STEPS.length }) })),",
    "    h('div', { class: 'progress' }, h('span', { class: 'progress-label', text: labPosText(i) })),")
# Clinical-term notes only in the character tool.
rep("  const check = v => { const w = diagnosisWord(v);", "  const check = v => { const w = LAB_TOOLS[labTool].diagnosis ? diagnosisWord(v) : '';")
# Main view: tool switcher, the open tool's title, intro and rules; a field can carry a class.
rep("""    h('h2', { class: 'ws-title', text: t('labTitle') }),
    h('p', { class: 'k-intro', text: t('labIntro') }),""", """    h('div', { class: 'lab-tools', role: 'group', 'aria-label': t('labToolsLabel') }, Object.keys(LAB_TOOLS).map(id => h('button', {
      type: 'button', class: 'lab-tool', 'aria-pressed': id === labTool ? 'true' : 'false', onclick: () => labSwitch(id),
    }, h('b', { text: t(LAB_TOOLS[id].label) }), h('small', { text: t(LAB_TOOLS[id].hint) })))),
    h('h2', { class: 'ws-title', text: t(LAB_TOOLS[labTool].title) }),
    h('p', { class: 'k-intro', text: t(LAB_TOOLS[labTool].intro) }),""")
rep("      h('ul', null, STRINGS.labRules.map(x => h('li', { text: x })))) : null,",
    "      h('ul', null, STRINGS[LAB_TOOLS[labTool].rules].map(x => h('li', { text: x })))) : null,")
rep("        lab = labFresh(); labSaveNow(); render();", "        lab = labStates[labTool] = labFresh(); labSaveNow(); render();")
rep("""  return h('div', { class: 'card' }, label, labHints(f.hints),
    labTextInput(f, id, lab.data[f.id],""", """  return h('div', { class: 'card' + (f.cls ? ' ' + f.cls : '') }, label, labHints(f.hints),
    labTextInput(f, id, lab.data[f.id],""")
rep("""    h('h2', { text: t('labSteps') }),
    h('ul', { class: 'steps', id: 'lab-nav' }""", """    h('h2', { text: t(LAB_TOOLS[labTool].label) }),
    h('ul', { class: 'steps', id: 'lab-nav' }""")

# Documents: each tool builds its own; title and note come with the document.
rep("function labDoc() {\n  const d = lab.data;", "function labDoc() { return LAB_TOOLS[labTool].doc(); }\n\nfunction labHeroDoc() {\n  const d = lab.data;")
rep("  return { hero: v('hero'), sections: sections.filter(sec => sec.parts.length).map((sec, i) => Object.assign(sec, { title: (i + 1) + '. ' + sec.title })) };",
    "  return { title: t('labDocTitle') + (v('hero') ? ': ' + v('hero') : ''), note: t('labDocNote'),\n"
    "    sections: sections.filter(sec => sec.parts.length).map((sec, i) => Object.assign(sec, { title: (i + 1) + '. ' + sec.title })) };")
rep("""function labDocNodes() {
  const doc = labDoc();
  const title = t('labDocTitle') + (doc.hero ? ': ' + doc.hero : '');
  if (!doc.sections.length) return [h('h2', { class: 'lab-doc-title', text: title }), h('p', { class: 'lab-empty', text: t('labDocEmpty') })];
  return [h('h2', { class: 'lab-doc-title', text: title }),""", """function labDocNodes() {
  const doc = labDoc();
  const title = doc.title, meta = doc.meta ? h('p', { class: 'lab-doc-meta', text: doc.meta }) : null;
  if (!doc.sections.length) return [h('h2', { class: 'lab-doc-title', text: title }), meta, h('p', { class: 'lab-empty', text: t('labDocEmpty') })];
  return [h('h2', { class: 'lab-doc-title', text: title }), meta,""")
rep("""    h('p', { class: 'lab-empty', text: t('labDocNote') })];""", """    h('p', { class: 'lab-empty', text: doc.note })];""")
rep("""  const lines = [t('labDocTitle') + (doc.hero ? ': ' + doc.hero : ''), ''];""",
    """  const lines = [doc.title].concat(doc.meta ? [doc.meta] : [], '');""")
rep("""  lines.push(t('labDocNote'));
  return lines.join('\\n');""", """  lines.push(doc.note);
  return lines.join('\\n');""")

# Keep the open panel visible in the scrolling row of panels (phones).
rep("""    st.summary ? renderLabSummary() : st.fields.map(f => renderLabField(f, evWarns)));
}""", """    st.summary ? renderLabSummary() : st.fields.map(f => renderLabField(f, evWarns)));
}
function labScrollDots() {
  const dot = document.querySelector('.lab-dot[aria-current="step"]'), row = dot && dot.parentNode;
  if (row && row.scrollWidth > row.clientWidth) row.scrollLeft = dot.offsetLeft - row.offsetLeft - 8;
}""")
rep("""  renderSidebar(); renderMain(); renderFooter();
  document.getElementById('main').scrollTop = 0;
}""", """  renderSidebar(); renderMain(); renderFooter();
  labScrollDots();
  document.getElementById('main').scrollTop = 0;
}""", count=2)

rep("""function labDocNodes() {""", r"""/** «Сюжет пен композиция»: answers grouped as the five parts of the result; questions as labels. */
function labPlotDoc() {
  const d = lab.data;
  const v = x => (d[x] || '').trim();
  const qa = stage => LAB_PLOT_STEPS.find(st => st.stage === stage).fields
    .filter(f => !f.evidenceFor && filled(d[f.id])).map(f => ({ label: f.label.replace(/^\d+\.\s*/, ''), text: v(f.id) }));
  const field = (label, text) => filled(text) ? { label: label, text: text } : null;
  const work = v('plWork').replace(/^«|»$/g, '');
  const sections = [
    { title: 'Сюжеттік негіз', parts: qa(1) },
    { title: 'Тартыстың дамуы', parts: qa(2) },
    { title: 'Композициялық ерекшеліктер', parts: qa(3) },
    { title: 'Мәтіндік дәлелдер', parts: [
      field('Талданған үзінді', v('plExcerpt')),
      field('Сюжеттің негізі бойынша', v('ev1')), field('Тартыс пен оқиғалардың дамуы бойынша', v('ev2')),
      field('Композициялық құрылым бойынша', v('ev3')), field('Интерпретация бойынша', v('ev4'))].filter(Boolean) },
    { title: 'Қорытынды интерпретация', parts: qa(4) },
  ];
  return {
    title: t('plotDocTitle') + (work ? ': «' + work + '»' : ''),
    meta: v('plAuthor') ? 'Автор: ' + v('plAuthor') : '',
    note: t('plotDocNote'),
    sections: sections.filter(sec => sec.parts.length).map((sec, i) => Object.assign(sec, { title: (i + 1) + '. ' + sec.title })),
  };
}

function labDocNodes() {""")

# Help and cover: the lab now has two analyses.
rep("      '«Зертхана» қойындысында кейіпкер психологиясын кезең-кезеңімен талдап, нәтижені бір құжатқа жинайсыз. Оны көшіруге немесе PDF ретінде сақтауға болады.',",
    "      '«Зертхана» қойындысында екі талдау құралы бар: «Кейіпкер психологиясы» және «Сюжет пен композиция». Талдау түрін жоғарыдан таңдап, кезең-кезеңімен толтырасыз, нәтижені көшіруге немесе PDF ретінде сақтауға болады.',")
rep("    'Кейіпкер психологиясын талдау зертханасы: кезең-кезеңімен талдау, нәтижені көшіру және PDF',",
    "    'Зертхана: кейіпкер психологиясын және сюжет пен композицияны кезең-кезеңімен талдау, нәтижені көшіру және PDF',")

s = s.replace('      python3 lab.py shop.html kobem-talday.html           # «Зертхана» (character psychology lab)',
              '      python3 lab.py shop.html lab.html                    # «Зертхана» (character psychology lab)\n'
              '      python3 plot.py lab.html kobem-talday.html           # «Зертхана»: сюжет пен композиция')
open(out, 'w', encoding='utf8').write(s)
print('plot ->', out)
