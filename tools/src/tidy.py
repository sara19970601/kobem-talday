"""Tidy: fewer words on screen. «Бір экран: бір тақырып, бір сөйлем, қалғаны сұраған адамға ғана».
- Lab: no kicker or extra hint line; one-sentence intros; the step's intro, rules and notes
  sit under one «Кеңес» toggle; every field's guiding questions under a small «Кеңес» toggle;
  the tutor card is one button; the save note moves into a tooltip.
- Guide: the «Толық нұсқасы PDF-те» card is a title and a button.
- Glossary: one-sentence intro.
- Top bar: «Файлға сақтау», «Файлдан ашу», «Жаңа талдау» go into one «Файл ▾» menu.
The author's own texts (cover, children's books intro, guide) are not touched.
Usage: python3 -I tidy.py in.html out.html   (run after labmore.py)"""
import sys

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('tidy anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

# ---- CSS ----
rep('</style>\n</head>', r"""</style>
<style id="tidy">
  /* TIDY — «Кеңес» toggles, compact cards, «Файл ▾» menu */
  .lab-tip { margin: -2px 0 8px; }
  .lab-tip > summary { display: inline-flex; align-items: center; gap: 5px; cursor: pointer; list-style: none;
    font-size: 13px; font-weight: 600; color: var(--accent); padding: 2px 8px 2px 6px; border-radius: 999px; background: var(--accent-soft); }
  .lab-tip > summary::-webkit-details-marker { display: none; }
  .lab-tip > summary::before { content: "?"; display: inline-flex; align-items: center; justify-content: center; width: 16px; height: 16px;
    border-radius: 50%; background: var(--accent); color: #fff; font-size: 11px; font-weight: 800; }
  .lab-tip[open] > summary { margin-bottom: 6px; }
  .lab-tip .lab-hint { margin: 0; }
  .lab-step-tip { margin: 0 0 14px; }
  .lab-step-tip > div { padding: 12px 14px; border-radius: 12px; background: var(--surface); border: 1px solid var(--line); }
  .lab-step-tip p { margin: 0 0 8px; line-height: 1.5; font-size: 14.5px; }
  .lab-step-tip p:last-child, .lab-step-tip ul:last-child { margin-bottom: 0; }
  .lab-step-tip ul { margin: 0 0 8px; padding-left: 20px; font-size: 14.5px; }
  .lab-step-tip li { margin-bottom: 4px; line-height: 1.5; }
  .lab-step-head { display: flex; flex-wrap: wrap; align-items: baseline; gap: 4px 12px; margin: 0 0 8px; }
  .lab-step-head .lab-pos { margin: 0; }
  .lab-step-head .lab-step-title { margin: 0; }
  .tutor-row { display: flex; justify-content: flex-end; margin: 4px 0 14px; }
  .tutor-row .btn { display: inline-flex; align-items: center; gap: 8px; border-color: var(--accent); color: var(--accent); font-weight: 600; }
  .tutor-row .btn::before { content: "✦"; }
  .lab-actions .tutor-row { margin: 0; }
  .tb-menu { position: relative; }
  .tb-menu > summary { list-style: none; cursor: pointer; }
  .tb-menu > summary::-webkit-details-marker { display: none; }
  .tb-menu-list { position: absolute; right: 0; top: calc(100% + 6px); z-index: 60; min-width: 210px; display: grid; gap: 2px; padding: 6px;
    background: var(--surface); border: 1px solid var(--line); border-radius: 12px; box-shadow: var(--shadow-md, 0 8px 24px rgba(0, 0, 0, .15)); }
  .tb-menu-item { text-align: left; border: 0; background: none; padding: 9px 12px; border-radius: 8px; font-size: 14.5px; color: var(--ink); }
  .tb-menu-item:hover, .tb-menu-item:focus-visible { background: var(--surface-2); }
  @media (max-width: 900px) { .tb-menu-list { left: 0; right: auto; } }
  @media (max-width: 520px) { .tutor-row .btn { width: 100%; justify-content: center; } }
  @media print { .lab-tip, .lab-step-tip, .tutor-row { display: none; } }
</style>
</head>""")

# ---- Strings: one-sentence intros, menu ----
rep("  labIntro: 'Кейіпкердің мінезін, мақсатын, эмоциясын, ішкі қайшылығын, қарым-қатынасын және өзгерісін мәтінге сүйеніп, кезең-кезеңімен талдаңыз. Соңында жауаптарыңыз бір құжатқа жиналады.',",
    "  labIntro: 'Кейіпкердің мінезін, мақсатын, эмоциясын, ішкі қайшылығын, қарым-қатынасын және өзгерісін мәтінге сүйеніп, кезең-кезеңімен талдаңыз.',")
rep("  plotIntro: 'Шығарманың сюжетін, тартысын және композициялық құрылымын төрт кезеңде талдаңыз. Соңында жауаптарыңыз бір құжатқа жиналады.',",
    "  plotIntro: 'Шығарманың сюжетін, тартысын және композициялық құрылымын төрт кезеңде талдаңыз.',")
rep("  glIntro: 'Шығарманы талдауда жиі қолданылатын 63 терминнің қысқаша анықтамасы. Терминді табу үшін «Сөздіктен іздеу» жолағына сөзді жазыңыз (телефонда ол ☰ батырмасының ішінде).',",
    "  glIntro: 'Шығарманы талдауда жиі қолданылатын 63 терминнің қысқаша анықтамасы.',")
rep("  exportBtn: 'Файлға сақтау',", "  exportBtn: 'Файлға сақтау',\n  fileMenu: 'Файл ▾',\n  tipLabel: 'Кеңес',")

# ---- Lab ----
rep("function labHints(list) { return list && list.length ? h('ul', { class: 'lab-hint' }, list.map(x => h('li', { text: x }))) : null; }",
    "function labHints(list) {\n"
    "  return list && list.length ? h('details', { class: 'lab-tip' }, h('summary', { text: t('tipLabel') }),\n"
    "    h('ul', { class: 'lab-hint' }, list.map(x => h('li', { text: x })))) : null;\n}")
rep("        h('p', { text: x.hint }),", "        labHints([x.hint]),")
rep("    h('p', { class: 'privacy', text: t('labConsentOn') }));\n}", "  );\n}")
rep("""    h('p', { class: 'ws-kicker', text: t('tabLab') }),
    h('div', { class: 'lab-tools', role: 'group',""", """    h('div', { class: 'lab-tools', role: 'group',""")
rep("    h('p', { class: 'lab-tool-hint', text: toolText(LAB_TOOLS[labTool], 'hint') }),\n", "")
rep("""      h('label', { class: 'lab-consent', for: 'lab-consent' }, consent,
        h('span', null, t('labConsent'), h('small', { id: 'lab-consent-note', text: t(labConsent ? 'labConsentOn' : 'labConsentOff') }))),""",
    """      h('label', { class: 'lab-consent', for: 'lab-consent', title: t(labConsent ? 'labConsentOn' : 'labConsentOff') }, consent,
        h('span', null, t('labConsent'))),""")
rep("""    h('p', { class: 'lab-pos', text: labPosText(lab.step) }),
    h('h3', { class: 'lab-step-title', text: st.title }),
    st.intro ? h('p', { class: 'lab-step-intro', text: st.intro }) : null,
    st.rules ? h('div', { class: 'card lab-rules' }, h('h3', { text: t('labRulesTitle') }),
      h('ul', null, (LAB_TOOLS[labTool].rulesList || STRINGS[LAB_TOOLS[labTool].rules]).map(x => h('li', { text: x })))) : null,
    st.note ? h('p', { class: 'lab-note', text: st.note }) : null,""", """    h('div', { class: 'lab-step-head' },
      h('p', { class: 'lab-pos', text: labPosText(lab.step) }),
      h('h3', { class: 'lab-step-title', text: st.title })),
    st.intro || st.rules || st.note ? h('details', { class: 'lab-tip lab-step-tip' }, h('summary', { text: t('tipLabel') }),
      h('div', null,
        st.intro ? h('p', { text: st.intro }) : null,
        st.note ? h('p', { text: st.note }) : null,
        st.rules ? [h('p', null, h('b', { text: t('labRulesTitle') })),
          h('ul', null, (LAB_TOOLS[labTool].rulesList || STRINGS[LAB_TOOLS[labTool].rules]).map(x => h('li', { text: x })))] : null)) : null,""")
rep("""function tutorCard(final) {
  return h('div', { class: 'tutor-card' },
    h('div', null, h('h3', { text: t('tutorTitle') }), h('p', { text: t(final ? 'tutorCardFinal' : 'tutorCardText') })),
    h('button', { type: 'button', class: 'btn primary', text: t('tutorBtn'), onclick: () => showTutor(final) }));
}""", """function tutorCard(final) {
  return h('div', { class: 'tutor-row' },
    h('button', { type: 'button', class: 'btn', text: t('tutorBtn'), title: t(final ? 'tutorCardFinal' : 'tutorCardText'), onclick: () => showTutor(final) }));
}""")
rep("""      h('button', { type: 'button', class: 'btn', text: t('labPrint'), onclick: () => printOutputs('lab') })),
    h('p', { class: 'lab-step-intro', text: t('labPrintHint') }),
    tutorCard(true),""", """      h('button', { type: 'button', class: 'btn', text: t('labPrint'), title: t('labPrintHint'), onclick: () => printOutputs('lab') }),
      tutorCard(true)),""")

# ---- Guide: locked card is a title and a button ----
rep("      h('div', null, h('h3', { text: t('guideLockedTitle') }), h('p', { text: t('guideLockedText') })),",
    "      h('div', { title: t('guideLockedText') }, h('h3', { text: t('guideLockedTitle') })),")

# ---- Top bar: «Файл ▾» ----
rep("""    h('div', { class: 'tb-actions' },
      h('button', { class: 'btn', type: 'button', onclick: exportJson, text: t('exportBtn') }),
      h('button', { class: 'btn', type: 'button', onclick: openImport, text: t('importBtn') }),
      h('button', { class: 'btn primary', type: 'button', onclick: () => printOutputs(defaultPrintTarget()), text: t('printBtn') }),
      h('button', { class: 'btn', type: 'button', onclick: newAnalysis, text: t('resetBtn') })),""",
    """    h('div', { class: 'tb-actions' },
      h('details', { class: 'tb-menu' },
        h('summary', { class: 'btn', text: t('fileMenu') }),
        h('div', { class: 'tb-menu-list', role: 'menu' }, [[exportJson, 'exportBtn'], [openImport, 'importBtn'], [newAnalysis, 'resetBtn']].map(([run, key]) =>
          h('button', { class: 'tb-menu-item', type: 'button', role: 'menuitem', text: t(key),
            onclick: e => { e.currentTarget.closest('details').open = false; run(); } })))),
      h('button', { class: 'btn primary', type: 'button', onclick: () => printOutputs(defaultPrintTarget()), text: t('printBtn') })),""")
# The menu closes on a click elsewhere and on Esc.
rep("document.addEventListener('keydown', e => { if (e.key === 'Escape') closeNav(); });",
    "document.addEventListener('keydown', e => { if (e.key === 'Escape') { closeNav(); document.querySelectorAll('.tb-menu[open]').forEach(d => { d.open = false; }); } });\n"
    "document.addEventListener('click', e => { document.querySelectorAll('.tb-menu[open]').forEach(d => { if (!d.contains(e.target)) d.open = false; }); });")
# Help text: the buttons now live in the menu.
s = s.replace("батырмасын басыңыз да, файлды өзіңізге", "батырмасын басыңыз да, файлды өзіңізге")

s = s.replace('      python3 labmore.py tutor.html kobem-talday.html      # 8 more lab tools, theory step, school/university level',
              '      python3 labmore.py tutor.html more.html              # 8 more lab tools, theory step, school/university level\n'
              '      python3 tidy.py more.html kobem-talday.html          # fewer words: «Кеңес» toggles, «Файл ▾» menu')
open(out, 'w', encoding='utf8').write(s)
print('tidy ->', out)
