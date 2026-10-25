"""Save as Word or PDF instead of a data file.
«Файлға сақтау» offers a Word document (.doc: the filled analysis to read and print, with the
analysis data kept in a hidden note so «Файлдан ашу» can reopen it) or a PDF (the same
document through the browser's print dialog). Older .json files still open.
Usage: python3 -I save.py in.html out.html   (run after kids.py)"""
import sys

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('save anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

# ---- CSS: save dialog choices + the printed (PDF) analysis ----
rep('</head>', """<style id="save-doc">
  /* SAVE — Word / PDF choice and the analysis document */
  .save-choices { display: grid; gap: 10px; margin: 4px 0 2px; }
  .save-choice { display: flex; gap: 12px; align-items: center; text-align: left; width: 100%;
    padding: 12px 14px; border-radius: 12px; border: 1px solid var(--line-strong); background: var(--surface); }
  .save-choice:hover { border-color: var(--accent); background: var(--accent-soft); }
  .save-ico { flex: none; width: 40px; height: 40px; border-radius: 10px; display: inline-flex; align-items: center;
    justify-content: center; font-weight: 800; font-size: 13px; color: #fff; }
  .save-ico.word { background: #2b579a; }
  .save-ico.pdf { background: #c0392b; }
  .save-choice b { display: block; font-size: 15.5px; }
  .save-choice small { display: block; color: var(--ink-2); font-size: 13px; line-height: 1.4; margin-top: 2px; }
  .save-note { margin: 10px 0 0; font-size: 13px; color: var(--ink-2); }
  @media print {
    .doc-analysis h1 { font-size: 16pt; margin: 0 0 4pt; }
    .doc-analysis .doc-meta { margin: 0 0 10pt; font-size: 10.5pt; }
    .doc-analysis h2 { font-size: 13pt; margin: 14pt 0 5pt; border-bottom: 1px solid #000; padding-bottom: 2pt; break-after: avoid; }
    .doc-analysis h3 { font-size: 11pt; margin: 7pt 0 2pt; break-after: avoid; }
    .doc-analysis p { margin: 0 0 4pt; white-space: pre-wrap; }
    .doc-analysis ol { margin: 0 0 4pt; padding-left: 18pt; }
    .doc-analysis table { width: 100%; border-collapse: collapse; margin: 2pt 0 6pt; }
    .doc-analysis th, .doc-analysis td { border: 1px solid #000; padding: 3pt 5pt; font-size: 10pt; text-align: left; vertical-align: top; }
    .doc-analysis th { background: #eee; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
    .doc-analysis .doc-plan { white-space: pre-wrap; line-height: 1.4; }
  }
</style>
</head>""")

# ---- Strings ----
rep("  exportTitle: 'Талдаудың сақтық көшірмесі',", """  exportTitle: 'Талдаудың сақтық көшірмесі',
  saveTitle: 'Талдауды сақтау',
  saveAllTitle: 'Барлық талдауды сақтау',
  saveWord: 'Word құжаты',
  saveWordHint: 'Word-та, Google Docs-та ашылады. Кейін осы файлды «Файлдан ашу» арқылы сайтқа қайта жүктеп, жұмысты жалғастыра аласыз.',
  savePdf: 'PDF',
  savePdfHint: 'Басып шығару терезесі ашылады. «Принтер» орнына «PDF ретінде сақтау» (Save as PDF) таңдаңыз.',
  saveNote: 'Ескерту: файлды Word-та өзгертіп қайта сақтасаңыз, сайт оны аша алмайды. Жұмысты жалғастыру үшін сайттан жүктелген түпнұсқа файлды сақтап қойыңыз.',
  saveWordDone: 'Талдау Word құжаты ретінде сақталды. Ол компьютердің «Жүктелгендер» қалтасында тұр. Басқа компьютерде «Файлдан ашу» арқылы осы файлдан жалғастыра аласыз.',
  docTitle: 'Көркем шығарманы талдау',
  docUntitled: 'Атауы жазылмаған шығарма',
  docGenre: 'Жанры',
  docGrade: 'Сынып',
  docDate: 'Сақталған күні',
  docEmpty: 'Әзірге бірде-бір парақ толтырылмаған.',
  docPlan: 'Сабақ жоспары (45 мин)',
  docSaved: 'Бұл құжат korkemtaldau.com сайтында жасалды.',
  errNoData: 'Бұл файлда талдау деректері жоқ. Мүмкін, ол Word-та өзгертіліп сақталған шығар. Сайттан жүктелген түпнұсқа файлды таңдаңыз.',""")
rep("  errTooLarge: 'Файл тым үлкен (1 МБ-тан аспауы керек).',", "  errTooLarge: 'Файл тым үлкен (5 МБ-тан аспауы керек).',")
rep("  MAX_IMPORT_BYTES: 1024 * 1024,   // 1 MB", "  MAX_IMPORT_BYTES: 5 * 1024 * 1024,   // 5 MB (a Word file carries the readable text too)")
rep('accept=".json,application/json"', 'accept=".doc,.json,application/msword,application/json"')

# ---- Save buttons → the Word/PDF choice ----
rep("""function exportJson() {
  offerFile(JSON.stringify(exportData(), null, 2), state.meta.title);
}""", """function exportJson() {
  saveStateNow();
  chooseSaveFormat([analysisData(state)], exportData(), state.meta.title, t('saveTitle'));
}""")
rep("""  const data = Object.assign({ app: CONFIG.APP_ID, version: CONFIG.DATA_VERSION, exportedAt: new Date().toISOString() }, entry.data);
  offerFile(JSON.stringify(data, null, 2), entry.data.meta && entry.data.meta.title);""",
    """  const data = Object.assign({ app: CONFIG.APP_ID, version: CONFIG.DATA_VERSION, exportedAt: new Date().toISOString() }, entry.data);
  chooseSaveFormat([entry.data], data, entry.data.meta && entry.data.meta.title, t('saveTitle'));""")
rep("""  offerFile(JSON.stringify(data, null, 2), t('libAllFile'));""",
    """  chooseSaveFormat(data.analyses, data, t('libAllFile'), t('saveAllTitle'));""")

# ---- Import: a Word file from this site carries the data in a hidden note ----
rep("""  let data;
  try { data = JSON.parse(text.replace(/^\\uFEFF/, '')); }
  catch (e) { showBanner('error', t('errNotJson')); return; }""",
    """  let data;
  const raw = text.replace(/^\\uFEFF/, '');
  const note = /<!--KOBEM-DATA:([A-Za-z0-9+\\/=\\s]+)-->/.exec(raw);
  try { data = JSON.parse(note ? decodeData(note[1]) : raw); }
  catch (e) { showBanner('error', t(/<html|<body/i.test(raw) ? 'errNoData' : 'errNotJson')); return; }""")

# ---- Document building ----
rep("""class ImportError extends Error {}""", """/* ---- Word / PDF: the filled analysis as a document ---- */
function encodeData(json) {
  const bytes = new TextEncoder().encode(json);
  let bin = '';
  for (let i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(bin).replace(/(.{76})/g, '$1\\n');
}
function decodeData(b64) {
  const bin = atob(b64.replace(/\\s+/g, ''));
  return new TextDecoder().decode(Uint8Array.from(bin, c => c.charCodeAt(0)));
}

/** One field's answer as document nodes, or null when it is empty. */
function docAnswer(field, v) {
  const text = x => h('p', { text: x });
  switch (field.type) {
    case 'text': case 'long': case 'dropdown': return filled(v) ? text(v.trim()) : null;
    case 'tags': return Array.isArray(v) && v.length ? text(v.join(', ')) : null;
    case 'list': {
      const items = (Array.isArray(v) ? v : []).filter(filled);
      return items.length ? h('ol', null, items.map(x => h('li', { text: x.trim() }))) : null;
    }
    case 'table': {
      const rows = (Array.isArray(v) ? v : []).filter(r => Array.isArray(r) && r.some(filled));
      return rows.length ? h('table', null,
        h('thead', null, h('tr', null, field.columns.map(c => h('th', { text: c })))),
        h('tbody', null, rows.map(r => h('tr', null, field.columns.map((c, i) => h('td', { text: (r[i] || '').trim() })))))) : null;
    }
  }
  return null;   // rubric: nothing to show
}

/** The analysis `d` ({ meta, answers, lessonPlan }) as a document section. */
function analysisDoc(d) {
  const saved = state;
  try {
    state = Object.assign(entryToState({ data: d }), { ui: saved.ui });
    const m = state.meta;
    const metaLine = [filled(m.author) ? oneLine(m.author) : '', t('docGenre') + ': ' + genre().label,
      m.grade ? t('docGrade') + ': ' + m.grade + t('gradeSuffix') : '', t('docDate') + ': ' + formatDate(new Date().toISOString()).slice(0, 10)]
      .filter(Boolean).join(' · ');
    const sheets = [];
    fillableSheets().forEach(ws => {
      const ans = state.answers[ws.id] || {};
      const parts = [];
      ws.fields.forEach(f => {
        const node = docAnswer(f, ans[f.id]);
        if (node) parts.push(h('h3', { text: f.label }), node);
      });
      if (parts.length) sheets.push(h('h2', { text: ws.order + '. ' + ws.title }), parts);
    });
    const plan = state.lessonPlan.edited && filled(state.lessonPlan.text) ? state.lessonPlan.text
      : sheets.length ? generateLessonPlan().text : '';
    return h('section', { class: 'print-section doc-analysis' },
      h('h1', { text: filled(m.title) ? '«' + oneLine(m.title) + '»' : t('docUntitled') }),
      h('p', { class: 'doc-meta', text: metaLine }),
      sheets.length ? sheets : h('p', { text: t('docEmpty') }),
      plan ? [h('h2', { text: t('docPlan') }), h('div', { class: 'doc-plan' }, plan.split('\\n').map(line => h('p', { text: line || '\\u00a0' })))] : null);
  } finally {
    state = saved;
  }
}

function fileSlug(name) {
  return ((name || 'talday').trim().replace(/[\\\\/:*?"<>|«»]+/g, '').replace(/\\s+/g, '-').slice(0, 60) || 'talday')
    + '-' + new Date().toISOString().slice(0, 10);
}

/** Word opens HTML saved as .doc; the hidden note keeps the data for «Файлдан ашу». */
function downloadWord(list, data, name) {
  const body = h('div', null, list.map(analysisDoc), h('p', { class: 'doc-foot', text: t('docSaved') }));
  const title = list.length === 1 && filled(list[0].meta && list[0].meta.title) ? oneLine(list[0].meta.title) : t('docTitle');
  const esc = x => x.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const html = '\\ufeff<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">'
    + '<head><meta charset="utf-8"><title>' + esc(title) + '</title>'
    + '<!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom></w:WordDocument></xml><![endif]-->'
    + '<style>@page { size: 21cm 29.7cm; margin: 2cm; } body { font-family: "Times New Roman", serif; font-size: 12pt; line-height: 1.35; }'
    + ' h1 { font-size: 18pt; margin: 0 0 4pt; } h2 { font-size: 14pt; margin: 16pt 0 6pt; color: #0b4f8a; border-bottom: 1px solid #999; }'
    + ' h3 { font-size: 12pt; margin: 8pt 0 2pt; } p { margin: 0 0 4pt; } .doc-meta { color: #444; margin-bottom: 10pt; }'
    + ' table { border-collapse: collapse; width: 100%; margin: 2pt 0 8pt; } th, td { border: 1px solid #666; padding: 3pt 5pt; vertical-align: top; text-align: left; }'
    + ' th { background: #e8eef5; } .print-section { page-break-after: always; } .print-section:last-of-type { page-break-after: auto; }'
    + ' .doc-foot { color: #777; font-size: 9pt; margin-top: 18pt; }</style></head><body>'
    + body.innerHTML + '\\n<!--KOBEM-DATA:' + encodeData(JSON.stringify(data)) + '-->\\n</body></html>';
  const a = h('a', { href: URL.createObjectURL(new Blob([html], { type: 'application/msword' })),
    download: 'korkem-talday-' + fileSlug(name) + '.doc' });
  document.body.append(a);
  a.click();
  setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
}

/** PDF: the same document through the browser's print dialog («PDF ретінде сақтау»). */
function printAnalyses(list) {
  if (EMBEDDED) { printHelp('analysis'); return; }
  document.getElementById('print-area').replaceChildren.apply(document.getElementById('print-area'), list.map(analysisDoc));
  printPrepared = true;
  window.print();
}

function chooseSaveFormat(list, data, name, title) {
  if (EMBEDDED) { offerFile(JSON.stringify(data, null, 2), name); return; }
  let close = null;
  const choice = (cls, label, hint, run) => h('button', { type: 'button', class: 'save-choice',
    onclick: () => { close(); run(); } },
    h('span', { class: 'save-ico ' + cls, 'aria-hidden': 'true' }, cls === 'word' ? 'W' : 'PDF'),
    h('span', null, h('b', { text: label }), h('small', { text: hint })));
  close = openDialog(title, [
    h('div', { class: 'save-choices' },
      choice('word', t('saveWord') + ' (.doc)', t('saveWordHint'), () => { downloadWord(list, data, name); showBanner('ok', t('saveWordDone')); }),
      choice('pdf', t('savePdf'), t('savePdfHint'), () => printAnalyses(list))),
    h('p', { class: 'save-note', text: t('saveNote') }),
  ], [{ label: t('cancel') }]);
}

class ImportError extends Error {}""")

s = s.replace('      python3 kids.py gloss.html kids.json kobem-talday.html',
              '      python3 kids.py gloss.html kids.json kids.html\n'
              '      python3 save.py kids.html kobem-talday.html          # save as Word / PDF')
open(out, 'w', encoding='utf8').write(s)
print('save ->', out)
