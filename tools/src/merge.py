"""Merge «Нұсқаулық» into «Дәптер»: one tab with a «Парақтар | Нұсқаулық» switch in the side
list, and each sheet's guide tips inline under «Әдістемелік кеңес» (no jump to another tab).
The guide view itself is unchanged; state.ui.tab 'guide' is now the guide mode of «Дәптер».
Usage: python3 -I merge.py in.html out.html   (run after tidy.py)"""
import sys

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('merge anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

# ---- CSS ----
rep('</style>\n</head>', r"""</style>
<style id="merge">
  /* MERGE — «Парақтар | Нұсқаулық» switch and inline sheet tips */
  .book-modes { display: flex; padding: 3px; gap: 2px; margin: 0 0 14px; border-radius: 10px; background: var(--surface-2); border: 1px solid var(--line); }
  .book-modes button { flex: 1; border: 0; background: none; padding: 7px 10px; border-radius: 8px; font-weight: 600; color: var(--ink-2); }
  .book-modes button[aria-pressed="true"] { background: var(--surface); color: var(--accent); box-shadow: var(--shadow-sm); }
  .ws-guide-tip { margin: 2px 0 14px; }
  .ws-guide-tip > div { display: grid; gap: 12px; padding: 12px 14px; border-radius: 12px; background: var(--accent-soft); border: 1px solid var(--line); }
  .ws-tip-item h4 { margin: 0 0 4px; font-size: 14px; color: var(--accent); }
  .ws-tip-item p { margin: 0 0 6px; line-height: 1.55; }
  .ws-tip-pdf { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 10px; font-size: 13.5px; color: var(--ink-2); }
  .link-btn { border: 0; background: none; padding: 0; color: var(--accent); font-weight: 600; text-decoration: underline; cursor: pointer; }
  @media (max-width: 520px) { .tabs .tab { padding: 7px 5px; font-size: 12.5px; } }   /* five tabs fit without scrolling */
  @media (max-width: 400px) { .tabs .tab { padding: 7px 3px; font-size: 12px; } }
  @media print { .book-modes, .ws-guide-tip { display: none; } }
</style>
</head>""")

# ---- Strings ----
rep("  guideBtn: 'Нұсқаулық: {id} →',", """  guideBtn: 'Нұсқаулық: {id} →',
  modeSheets: 'Парақтар',
  modeGuide: 'Нұсқаулық',
  modesLabel: 'Дәптер бөлімі',
  sheetTip: 'Әдістемелік кеңес',
  sheetTipRead: 'Нұсқаулықта оқу →',""")
# Help: one line for the new place of the tips; the outdated «екі талдау құралы» line goes.
import re
m = re.search(r"      'Әр парақтағы «Нұсқаулық: 2\.8 →» сияқты батырма[^\n]*\n", s)
if not m:
    sys.exit('merge: help line not found')
s = s[:m.start()] + ("      'Әр парақтағы «? Әдістемелік кеңес» батырмасы сол параққа арналған қысқа кеңесті ашады. "
                     "Нұсқаулықтың кіріспесі мен 1-бөлімі сол жақтағы тізімнің үстіндегі «Нұсқаулық» ауыстырғышы арқылы ашылады.',\n") + s[m.end():]
m = re.search(r"      '«Зертхана» қойындысында екі талдау құралы бар[^\n]*\n", s)
if m:
    s = s[:m.start()] + s[m.end():]

# ---- Tabs: no «Нұсқаулық» tab; «Дәптер» is selected in both modes ----
rep("      ['library', 'book', 'guide', 'glossary', 'kids', 'lab'].map(tab => h('button', {\n"
    "        type: 'button', role: 'tab', class: 'tab', id: 'tab-' + tab,\n"
    "        'aria-selected': state.ui.tab === tab ? 'true' : 'false',",
    "      ['library', 'book', 'glossary', 'kids', 'lab'].map(tab => h('button', {\n"
    "        type: 'button', role: 'tab', class: 'tab', id: 'tab-' + tab,\n"
    "        'aria-selected': state.ui.tab === tab || (tab === 'book' && state.ui.tab === 'guide') ? 'true' : 'false',")

# ---- Side list: the mode switch on top, in both modes ----
rep("""  const active = currentStep().key;
  const parts = [];""", """  const active = currentStep().key;
  const parts = [bookModeSwitch()];""")
rep("""function renderGuideSidebar() {
  const nav = document.getElementById('sidebar');
  nav.replaceChildren(
""", """function bookModeSwitch() {
  return h('div', { class: 'book-modes', role: 'group', 'aria-label': t('modesLabel') },
    [['book', 'modeSheets'], ['guide', 'modeGuide']].map(([id, key]) => h('button', {
      type: 'button', 'aria-pressed': state.ui.tab === id ? 'true' : 'false', text: t(key),
      onclick: () => { closeNav(); switchTab(id); },
    })));
}

function renderGuideSidebar() {
  const nav = document.getElementById('sidebar');
  nav.replaceChildren(
    bookModeSwitch(),
""")

# ---- Sheet: tips inline instead of buttons to another tab ----
rep("""  const meta = [ws.guide ? t('guideRef', { guide: ws.guide }) : '', ws.standard ? t('standardRef', { standard: ws.standard }) : '']
    .filter(Boolean).join(' · ');""", """  const meta = ws.standard ? t('standardRef', { standard: ws.standard }) : '';""")
rep("""    guideRefs(ws.guide).length ? h('div', { class: 'ws-tools' }, guideRefs(ws.guide).map(id => h('button', {
      class: 'btn guide-link', type: 'button', title: guideHeading(GUIDE_INDEX[id]),
      onclick: () => openGuide(id),
    }, t('guideBtn', { id: id })))) : null,""", """    guideRefs(ws.guide).length ? h('details', { class: 'lab-tip ws-guide-tip' }, h('summary', { text: t('sheetTip') }),
      h('div', null, guideRefs(ws.guide).map(id => {
        const sec = GUIDE_INDEX[id];
        return h('div', { class: 'ws-tip-item' }, h('h4', { text: guideHeading(sec) }),
          sec.locked
            ? [filled(sec.text) ? renderGuideText(sec.text, '') : null,
              h('p', { class: 'ws-tip-pdf' }, h('span', { text: t('guideLockedTitle') }),
                h('button', { type: 'button', class: 'link-btn', text: t('guideLockedBuy'), onclick: showShop }))]
            : h('button', { type: 'button', class: 'btn', text: t('sheetTipRead'), onclick: () => openGuide(id) }));
      }))) : null,""")

s = s.replace('      python3 tidy.py more.html kobem-talday.html          # fewer words: «Кеңес» toggles, «Файл ▾» menu',
              '      python3 tidy.py more.html tidy.html                  # fewer words: «Кеңес» toggles, «Файл ▾» menu\n'
              '      python3 merge.py tidy.html kobem-talday.html         # «Нұсқаулық» inside «Дәптер»')
open(out, 'w', encoding='utf8').write(s)
print('merge ->', out)
