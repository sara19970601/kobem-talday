"""«Менің талдауларым» layer: several analyses kept in one browser.
Usage: python3 -I library.py in.html out.html   (run after theme.py)"""
import sys

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('library anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

# ---------------------------------------------------------------- CSS
rep("  /* ---------- PRINT (A4) ---------- */", """  /* ==========================================================================
     LIBRARY — «Менің талдауларым»
     ========================================================================== */
  .lib-tools { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
  .lib-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; }
  .lib-card {
    display: flex; flex-direction: column; gap: 8px; min-width: 0;
    background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 14px 16px;
  }
  .lib-card.active { border-color: var(--accent); }
  .lib-card h3 { margin: 0; font-family: var(--display); font-size: 18px; line-height: 1.3; overflow-wrap: anywhere; }
  .lib-meta { margin: 0; color: var(--ink-2); font-size: 13px; }
  .lib-badge {
    align-self: flex-start; font-size: 11px; font-weight: 700; letter-spacing: .03em;
    background: var(--accent-soft); color: var(--accent); border-radius: 99px; padding: 2px 9px;
  }
  .lib-progress { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--ink-2); font-variant-numeric: tabular-nums; }
  .lib-progress .progress-track { flex: 1; height: 6px; }
  .lib-actions { display: flex; flex-wrap: wrap; gap: 6px; margin-top: auto; padding-top: 4px; }
  .btn.small { padding: 5px 10px; font-size: 13px; }
  .lib-note { margin-top: 18px; font-size: 13px; color: var(--ink-2); }
  .lib-help { margin: 0 8px 10px; padding-left: 18px; font-size: 13px; color: var(--ink-2); }
  .lib-help li { margin-bottom: 6px; }

  /* ---------- PRINT (A4) ---------- */""")

# ---------------------------------------------------------------- STRINGS
rep("  tabBook: 'Дәптер',", """  tabLibrary: 'Талдауларым',
  libTitle: 'Менің талдауларым',
  libIntro: 'Осы браузерде сақталған барлық талдауыңыз. Біреуін ашып жалғастырыңыз немесе жаңа шығарманы бастаңыз.',
  libNew: '+ Жаңа талдау',
  libImport: 'Файлдан ашу',
  libExportAll: 'Барлығын файлға сақтау',
  libOpen: 'Ашу',
  libContinue: 'Жалғастыру',
  libDuplicate: 'Көшірмесін жасау',
  libExportOne: 'Файлға сақтау',
  libDelete: 'Өшіру',
  libActive: 'ҚАЗІР АШЫҚ',
  libUpdated: 'Өзгертілген: {date}',
  libProgress: '{done} / {total} парақ',
  libCopySuffix: ' (көшірме)',
  libDeleteConfirm: '«{name}» талдауы осы браузерден біржола өшіріледі. Керек болса, алдымен «Файлға сақтау» арқылы сақтап алыңыз. Өшіресіз бе?',
  libDeleted: 'Талдау өшірілді.',
  libNewDone: 'Жаңа талдау басталды. Алдыңғы талдауыңыз «Талдауларым» бөлімінде сақтаулы тұр.',
  libDuplicated: 'Көшірмесі жасалды. Ол тізімнің басында тұр.',
  libImported: 'Файлдан {n} талдау «Талдауларым» тізіміне қосылды.',
  libImportedOne: 'Талдау файлдан ашылды және «Талдауларым» тізіміне қосылды.',
  libNote: 'Талдаулар тек осы браузерде сақталады, ешқайда жіберілмейді. Басқа компьютерге көшіру немесе сақтық көшірме жасау үшін «Барлығын файлға сақтау» басыңыз.',
  libCount: '{n} талдау сақталған',
  libGoBook: 'Дәптерге өту →',
  libAllFile: 'барлық-талдаулар',
  libHelp1: '«Жаңа талдау» алдыңғы жұмысты өшірмейді: ол осы тізімде қалады.',
  libHelp2: '«Көшірмесін жасау» бір шығарманың талдауын басқа сыныпқа бейімдеуге ыңғайлы.',
  libHelp3: '«Барлығын файлға сақтау» барлық талдауды бір файлға жазады. Бұл толық сақтық көшірме.',
  tabBook: 'Дәптер',""")
rep("  resetConfirm: 'Барлық жауап өшіріліп, жаңа талдау басталады. Керек болса, алдымен «Файлға сақтау» арқылы сақтап алыңыз. Жалғастырасыз ба?',\n", "")

# ---------------------------------------------------------------- top bar
rep("['book', 'guide'].map(tab => h('button', {", "['library', 'book', 'guide'].map(tab => h('button', {")
rep("}, t(tab === 'book' ? 'tabBook' : 'tabGuide')))),", "}, t({ library: 'tabLibrary', book: 'tabBook', guide: 'tabGuide' }[tab])))),")
rep("h('button', { class: 'btn danger', type: 'button', onclick: resetAll, text: t('resetBtn') }),",
    "h('button', { class: 'btn', type: 'button', onclick: newAnalysis, text: t('resetBtn') }),")

# ---------------------------------------------------------------- render dispatch
rep("  if (state.ui.tab === 'guide') { renderGuideSidebar(); return; }",
    "  if (state.ui.tab === 'guide') { renderGuideSidebar(); return; }\n  if (state.ui.tab === 'library') { renderLibrarySidebar(); return; }")
rep("  if (state.ui.tab === 'guide') { renderGuideFooter(); return; }",
    "  if (state.ui.tab === 'guide') { renderGuideFooter(); return; }\n  if (state.ui.tab === 'library') { renderLibraryFooter(); return; }")
rep("""  if (state.ui.tab === 'guide') {
    box.replaceChildren(h('div', { id: 'banner-slot' }), renderGuideMain());
    renderBanner();
    return;
  }""", """  if (state.ui.tab === 'guide' || state.ui.tab === 'library') {
    box.replaceChildren(h('div', { id: 'banner-slot' }), state.ui.tab === 'guide' ? renderGuideMain() : renderLibraryMain());
    renderBanner();
    return;
  }""")

# ---------------------------------------------------------------- storage
rep("function loadState() {\n  try {\n    let raw", "/** Single-analysis storage of earlier versions (read once, then kept as is). */\nfunction loadSingleState() {\n  try {\n    let raw")
rep("        tab: u.tab === 'guide' ? 'guide' : 'book',", "        tab: ['guide', 'library'].includes(u.tab) ? u.tab : 'book',")
rep("""function saveStateNow() {
  if (!storageAvailable) return;
  try {
    window.localStorage.setItem(CONFIG.STORAGE_KEY, JSON.stringify(state));
    setSaveStatus(t('saved'));""", """function saveStateNow() {
  if (!storageAvailable || !library) return;
  try {
    const entry = activeEntry();
    const data = JSON.stringify(analysisData(state));
    if (entry && JSON.stringify(entry.data) !== data) {
      entry.data = JSON.parse(data);
      entry.updatedAt = new Date().toISOString();
    }
    window.localStorage.setItem(LIBRARY_KEY, JSON.stringify({
      version: 1, activeId: library.activeId, analyses: library.analyses, ui: state.ui,
    }));
    setSaveStatus(t('saved'));""")

# ---------------------------------------------------------------- files
rep("""function downloadJson(json) {
  const blob = new Blob([json], { type: 'application/json' });
  const slug = (state.meta.title || 'talday')""", """function downloadJson(json, name) {
  const blob = new Blob([json], { type: 'application/json' });
  const slug = ((name != null ? name : state.meta.title) || 'talday')""")
rep("""function exportJson() {
  const json = JSON.stringify(exportData(), null, 2);
  if (!EMBEDDED) { downloadJson(json); showBanner('ok', t('exportDone')); return; }""",
"""function exportJson() {
  offerFile(JSON.stringify(exportData(), null, 2), state.meta.title);
}

/** Download a file; where downloads are blocked, show the text to copy. */
function offerFile(json, name) {
  if (!EMBEDDED) { downloadJson(json, name); showBanner('ok', t('exportDone')); return; }""")

# Import adds analyses to the library instead of replacing the open one.
# The old doc comment sits above migrateV1(); the function itself starts at importText.
rep('/** Parse + validate; on success ask before replacing the current analysis. */\n', '')
a = s.index('function importText(text) {')
b = s.index('function resetAll() {')
s = s[:a] + """/** Parse + validate; the file's analyses are added to «Менің талдауларым». */
function importText(text) {
  if (text.length > CONFIG.MAX_IMPORT_BYTES) { showBanner('error', t('errTooLarge')); return; }
  let data;
  try { data = JSON.parse(text.replace(/^\\uFEFF/, '')); }
  catch (e) { showBanner('error', t('errNotJson')); return; }
  let found;
  try {
    if (isObj(data) && data.kind === 'library') {
      if (data.app !== CONFIG.APP_ID) fail('errWrongApp');
      if (!Array.isArray(data.analyses)) failAt('analyses', 'probArray');
      found = data.analyses.map(x => validateImport(Object.assign({ app: data.app, version: data.version }, x)));
    } else {
      found = [validateImport(data)];
    }
  } catch (e) {
    showBanner('error', e instanceof ImportError ? e.message : t('errRead'));
    return;
  }
  if (!found.length) { showBanner('error', t('errNotJson')); return; }
  saveStateNow();
  const blankId = isBlank(state) ? library.activeId : null;   // an empty analysis is replaced, not kept
  const entries = found.map(x => addEntry(x));
  if (blankId) library.analyses = library.analyses.filter(x => x.id !== blankId);
  const ui = state.ui;
  library.activeId = entries[0].id;
  state = entryToState(entries[0]);
  state.ui = Object.assign(freshUi(), { tab: found.length > 1 ? 'library' : 'book', guideSection: ui.guideSection });
  banner = null;
  saveStateNow();
  render();
  showBanner('ok', found.length > 1 ? t('libImported', { n: found.length })
    : t(data.version === 1 ? 'importMigrated' : 'libImportedOne'));
}

""" + s[b:]

# Replace resetAll with the library section.
a = s.index('function resetAll() {')
b = s.index('/* ==============================================================================\n   INIT')
s = s[:a] + """/* ==============================================================================
   LIBRARY — «Менің талдауларым»: several analyses kept in this browser.
   One localStorage entry holds them all; `state` is always the open one.
   ============================================================================== */
const LIBRARY_KEY = 'kobem-talday:library';
let library = null;   // { activeId, analyses: [{ id, createdAt, updatedAt, data }] }

function newId() { return Date.now().toString(36) + Math.random().toString(36).slice(2, 8); }
function analysisData(st) { return { meta: st.meta, answers: st.answers, lessonPlan: st.lessonPlan }; }
function isBlank(st) { return !filled(st.meta.title) && !filled(st.meta.author) && !Object.keys(st.answers).length; }
function activeEntry() { return library.analyses.find(x => x.id === library.activeId); }
function entryById(id) { return library.analyses.find(x => x.id === id); }

/** Clean state from a stored entry: the same checks as for a file. */
function entryToState(entry) {
  return validateImport(Object.assign({ app: CONFIG.APP_ID, version: CONFIG.DATA_VERSION }, entry.data));
}

function addEntry(st) {
  const now = new Date().toISOString();
  const entry = { id: newId(), createdAt: now, updatedAt: now, data: JSON.parse(JSON.stringify(analysisData(st))) };
  library.analyses.push(entry);
  return entry;
}

function sortedEntries() {
  return library.analyses.slice().sort((x, y) => String(y.updatedAt).localeCompare(String(x.updatedAt)));
}

function cleanUi(u) {
  u = isObj(u) ? u : {};
  return {
    step: typeof u.step === 'string' ? u.step : freshUi().step,
    tab: ['guide', 'library'].includes(u.tab) ? u.tab : 'book',
    guideSection: typeof u.guideSection === 'string' && GUIDE_INDEX[u.guideSection] ? u.guideSection : freshUi().guideSection,
    search: typeof u.search === 'string' ? u.search.slice(0, 200) : '',
  };
}

function loadState() {
  let stored = null;
  try { stored = JSON.parse(window.localStorage.getItem(LIBRARY_KEY) || 'null'); } catch (e) { stored = null; }
  library = { activeId: null, analyses: [] };
  if (isObj(stored) && Array.isArray(stored.analyses)) {
    stored.analyses.forEach(x => {
      if (!isObj(x) || !isObj(x.data)) return;
      try { entryToState(x); } catch (e) { return; }   // skip a damaged entry
      library.analyses.push({ id: typeof x.id === 'string' ? x.id : newId(), createdAt: String(x.createdAt || ''),
        updatedAt: String(x.updatedAt || ''), data: x.data });
    });
    library.activeId = stored.activeId;
  }
  loadSingleState();   // also checks that storage works
  const ui = isObj(stored) && isObj(stored.ui) ? cleanUi(stored.ui) : cleanUi(state.ui);
  // First run with the library: the analysis saved by the earlier version becomes its first entry.
  if (!library.analyses.length) library.activeId = addEntry(state).id;
  if (!activeEntry()) library.activeId = sortedEntries()[0].id;
  state = entryToState(activeEntry());
  state.ui = ui;
}

function openAnalysis(id) {
  if (id === library.activeId) { switchTab('book'); return; }
  saveStateNow();
  const entry = entryById(id);
  if (!entry) return;
  const ui = state.ui;
  library.activeId = id;
  state = entryToState(entry);
  state.ui = Object.assign(freshUi(), { tab: 'book', guideSection: ui.guideSection });
  banner = null;
  saveStateNow();
  render();
  document.getElementById('main').scrollTop = 0;
}

function newAnalysis() {
  saveStateNow();
  const ui = state.ui;
  const fresh = freshState();
  if (!isBlank(state)) library.activeId = addEntry(fresh).id;   // an empty open analysis is reused
  state = fresh;
  state.ui = Object.assign(freshUi(), { guideSection: ui.guideSection });
  banner = null;
  saveStateNow();
  render();
  document.getElementById('main').scrollTop = 0;
  showBanner('ok', t('libNewDone'));
}

function duplicateAnalysis(id) {
  saveStateNow();
  const copy = entryToState(entryById(id));
  if (filled(copy.meta.title)) copy.meta.title = copy.meta.title + t('libCopySuffix');
  addEntry(copy);
  saveStateNow();
  render();
  showBanner('ok', t('libDuplicated'));
}

function deleteAnalysis(id) {
  const entry = entryById(id);
  if (!entry) return;
  const name = filled(entry.data.meta && entry.data.meta.title) ? entry.data.meta.title : t('untitled');
  askConfirm(t('libDeleteConfirm', { name: name }), () => {
    library.analyses = library.analyses.filter(x => x.id !== id);
    if (id === library.activeId) {
      const ui = state.ui;
      if (!library.analyses.length) { state = freshState(); library.activeId = addEntry(state).id; }
      else { library.activeId = sortedEntries()[0].id; state = entryToState(activeEntry()); }
      state.ui = ui;
    }
    saveStateNow();
    render();
    showBanner('ok', t('libDeleted'));
  });
}

function exportAnalysis(id) {
  saveStateNow();
  const entry = entryById(id);
  const data = Object.assign({ app: CONFIG.APP_ID, version: CONFIG.DATA_VERSION, exportedAt: new Date().toISOString() }, entry.data);
  offerFile(JSON.stringify(data, null, 2), entry.data.meta && entry.data.meta.title);
}

function exportAll() {
  saveStateNow();
  const data = {
    app: CONFIG.APP_ID, version: CONFIG.DATA_VERSION, kind: 'library', exportedAt: new Date().toISOString(),
    analyses: sortedEntries().map(x => x.data),
  };
  offerFile(JSON.stringify(data, null, 2), t('libAllFile'));
}

function openImport() {
  if (EMBEDDED) importDialog(); else document.getElementById('import-file').click();
}

/** Progress of a stored analysis, computed with the usual completion rules. */
function progressFor(entry) {
  if (entry.id === library.activeId) {
    const ws = fillableSheets();
    return { done: ws.filter(isSheetComplete).length, total: ws.length };
  }
  const saved = state;
  try {
    state = entryToState(entry);
    const ws = fillableSheets();
    return { done: ws.filter(isSheetComplete).length, total: ws.length };
  } catch (e) {
    return { done: 0, total: 0 };
  } finally {
    state = saved;
  }
}

function formatDate(iso) {
  const d = new Date(iso);
  if (isNaN(d.getTime())) return '';
  const p = n => String(n).padStart(2, '0');
  return p(d.getDate()) + '.' + p(d.getMonth() + 1) + '.' + d.getFullYear() + ', ' + p(d.getHours()) + ':' + p(d.getMinutes());
}

function renderLibraryMain() {
  saveStateNow();   // the open analysis' card shows its latest text
  const cards = sortedEntries().map(entry => {
    const active = entry.id === library.activeId;
    const meta = active ? state.meta : (entry.data.meta || {});
    const pr = progressFor(entry);
    const pct = pr.total ? Math.round(pr.done / pr.total * 100) : 0;
    const details = [meta.author, meta.grade ? meta.grade + t('gradeSuffix') : '', (GENRES[meta.genre] || {}).label]
      .filter(filled).join(' · ');
    return h('article', { class: 'lib-card' + (active ? ' active' : '') },
      active ? h('span', { class: 'lib-badge', text: t('libActive') }) : null,
      h('h3', { text: filled(meta.title) ? meta.title : t('untitled') }),
      details ? h('p', { class: 'lib-meta', text: details }) : null,
      h('div', { class: 'lib-progress' },
        h('div', { class: 'progress-track', role: 'progressbar', 'aria-valuemin': 0, 'aria-valuemax': 100, 'aria-valuenow': pct },
          h('div', { class: 'progress-fill', style: 'width:' + pct + '%' })),
        h('span', { text: t('libProgress', pr) })),
      entry.updatedAt ? h('p', { class: 'lib-meta', text: t('libUpdated', { date: formatDate(entry.updatedAt) }) }) : null,
      h('div', { class: 'lib-actions' },
        h('button', { class: 'btn small primary', type: 'button', text: t(active ? 'libContinue' : 'libOpen'), onclick: () => openAnalysis(entry.id) }),
        h('button', { class: 'btn small', type: 'button', text: t('libDuplicate'), onclick: () => duplicateAnalysis(entry.id) }),
        h('button', { class: 'btn small', type: 'button', text: t('libExportOne'), onclick: () => exportAnalysis(entry.id) }),
        h('button', { class: 'btn small danger', type: 'button', text: t('libDelete'), onclick: () => deleteAnalysis(entry.id) })));
  });
  return h('section', null,
    h('p', { class: 'ws-kicker', text: t('tabLibrary') }),
    h('h2', { class: 'ws-title', text: t('libTitle') }),
    h('p', { class: 'ws-intro', text: t('libIntro') }),
    h('div', { class: 'lib-tools' },
      h('button', { class: 'btn primary', type: 'button', text: t('libNew'), onclick: newAnalysis }),
      h('button', { class: 'btn', type: 'button', text: t('libImport'), onclick: openImport }),
      h('button', { class: 'btn', type: 'button', text: t('libExportAll'), onclick: exportAll })),
    h('div', { class: 'lib-grid' }, cards),
    h('p', { class: 'lib-note', text: t('libNote') }));
}

function renderLibrarySidebar() {
  document.getElementById('sidebar').replaceChildren(
    h('h2', { text: t('libTitle') }),
    h('ul', { class: 'lib-help' }, h('li', { text: t('libHelp1') }), h('li', { text: t('libHelp2') }), h('li', { text: t('libHelp3') })),
    h('p', { class: 'privacy', text: t('privacy') }));
}

function renderLibraryFooter() {
  document.getElementById('footer').replaceChildren(
    h('div', { class: 'progress' }, h('span', { class: 'progress-label', text: t('libCount', { n: library.analyses.length }) })),
    h('button', { class: 'btn primary', type: 'button', text: t('libGoBook'), onclick: () => switchTab('book') }));
}

""" + s[b:]

# Import button in the top bar uses the same helper.
rep("onclick: () => (EMBEDDED ? importDialog() : document.getElementById('import-file').click()), text: t('importBtn')",
    "onclick: openImport, text: t('importBtn')")

# README
rep("  Two tabs\n", "  Tabs\n    - \"Талдауларым\": every analysis saved in this browser (open, copy, save to\n      a file, delete, back up all). Stored under one localStorage key.\n")
rep("      python3 theme.py app.html kobem-talday.html       # ornament theme + phone/tablet layout",
    "      python3 theme.py app.html themed.html             # ornament theme + phone/tablet layout\n"
    "      python3 library.py themed.html kobem-talday.html  # «Менің талдауларым»")

open(out, 'w', encoding='utf8').write(s)
print('wrote', out, len(s.encode('utf8')) // 1024, 'KB')
