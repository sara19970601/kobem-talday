"""«Қалай қолдану керек?» help: a top-bar button and a one-time welcome.
Usage: python3 -I help.py in.html out.html   (run after library.py)"""
import sys

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('help anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

rep("  /* ---------- PRINT (A4) ---------- */", """  /* HELP — «Қалай қолдану керек?» */
  .help-btn { flex: none; font-weight: 600; }
  .help-btn .help-q {
    display: inline-flex; align-items: center; justify-content: center; width: 20px; height: 20px;
    border-radius: 50%; background: var(--gold); color: #1b1407; font-size: 13px; margin-right: 6px;
  }
  .help-body h3 { font-family: var(--display); font-size: 16px; margin: 16px 0 6px; }
  .help-body h3:first-child { margin-top: 4px; }
  .help-body ol, .help-body ul { margin: 0; padding-left: 20px; }
  .help-body li { margin-bottom: 5px; line-height: 1.5; }
  .help-body p { margin: 0 0 6px; }
  @media (max-width: 900px) {
    .help-btn { order: 2; min-height: 42px; }
    .help-btn .help-label { display: none; }
    .help-btn .help-q { margin-right: 0; }
  }

  /* ---------- PRINT (A4) ---------- */""")

rep("  tabLibrary: 'Талдауларым',", """  helpBtn: 'Көмек',
  helpTitle: 'Қалай қолдану керек?',
  helpClose: 'Түсінікті',
  helpSections: [
    { title: '1. Талдауды бастау', items: [
      '«Талдауларым» қойындысында «+ Жаңа талдау» басыңыз.',
      'Жоғарыда жанрды, шығарманы, авторды және сыныпты толтырыңыз. Телефонда олар ⚙ батырмасының артында.',
    ] },
    { title: '2. Парақтарды толтыру', items: [
      '«Дәптер» қойындысында сол жақтағы тізімнен парақты таңдаңыз. Телефонда «☰ Парақтар» батырмасын басыңыз.',
      'Толтырылған парақтың жанына ✓ белгісі қойылады, ал төменгі жолақ қанша парақ қалғанын көрсетеді.',
      'Әр парақтағы «Нұсқаулық: 2.8 →» сияқты батырма әдістемелік түсініктемені ашады. «Дәптерге оралу» сізді сол параққа қайтарады, жазғаныңыз өшпейді.',
    ] },
    { title: '3. Сабақ жоспары мен рубрика', items: [
      'Парақтар тізімінің соңындағы «Сабақ жоспары (45 мин)» жауаптарыңыздан өзі құрылады. Оны еркін өңдеуге болады.',
      'Жоспарды «Басып шығару» арқылы қағазға шығарасыз немесе «Мәтінді көшіру» арқылы Word құжатына қоясыз.',
      '«Бағалау рубрикасы» оқушы жұмысын бағалауға арналған. Оны да басып шығаруға болады.',
    ] },
    { title: '4. Оқушыларға парақ тарату', items: [
      'Керекті парақты ашып, «Бос парақты басып шығару» басыңыз. A4 форматындағы бос парақ шығады.',
    ] },
    { title: '5. Жұмысты сақтау', items: [
      'Жазғаныңыз осы браузерде өзі сақталады. Жоғарыда «Сақталды» деген жазу шығады.',
      'Басқа компьютерде жалғастыру үшін «Талдауларым» бөлімінде «Барлығын файлға сақтау» басыңыз да, файлды өзіңізге (поштаға, WhatsApp-қа) жіберіңіз. Басқа компьютерде korkemtaldau.com ашып, «Файлдан ашу» арқылы сол файлды таңдайсыз.',
      'Браузер тарихын тазаласаңыз, файлға сақталмаған жұмыс өшеді. Сондықтан анда-санда «Барлығын файлға сақтау» басып тұрыңыз.',
    ] },
    { title: '6. Деректер қауіпсіздігі', items: [
      'Сайт оқушылар туралы ештеңе сақтамайды. Сіздің талдауларыңыз тек өз браузеріңізде тұрады, оларды ешкім көрмейді.',
    ] },
  ],
  tabLibrary: 'Талдауларым',""")

# Button in the top bar, right after the tabs (always visible, also on phones).
rep("""      }, t({ library: 'tabLibrary', book: 'tabBook', guide: 'tabGuide' }[tab])))),""",
"""      }, t({ library: 'tabLibrary', book: 'tabBook', guide: 'tabGuide' }[tab])))),
    h('button', { class: 'btn help-btn', type: 'button', onclick: showHelp, title: t('helpTitle'), 'aria-label': t('helpTitle') },
      h('span', { class: 'help-q', 'aria-hidden': 'true' }, '?'), h('span', { class: 'help-label', text: t('helpBtn') })),""")

rep("""/* ==============================================================================
   INIT""", """/* ==============================================================================
   HELP — «Қалай қолдану керек?» (shown once on the first visit, then on demand)
   ============================================================================== */
const HELP_SEEN_KEY = 'kobem-talday:help-seen';

function showHelp() {
  const body = h('div', { class: 'help-body' }, STRINGS.helpSections.map(sec => [
    h('h3', { text: sec.title }),
    h('ul', null, sec.items.map(x => h('li', { text: x }))),
  ]));
  openDialog(t('helpTitle'), body, [{ label: t('helpClose'), primary: true }]);
  const box = document.querySelector('.dlg');
  if (box) box.scrollTop = 0;   // start reading at section 1, not at the focused button
  try { window.localStorage.setItem(HELP_SEEN_KEY, '1'); } catch (e) { /* storage blocked */ }
}

function showHelpOnFirstVisit() {
  let seen = true;
  try { seen = !!window.localStorage.getItem(HELP_SEEN_KEY); } catch (e) { seen = true; }
  if (!seen) showHelp();
}

/* ==============================================================================
   INIT""")
rep("loadState();\nrender();", "loadState();\nrender();\nshowHelpOnFirstVisit();")

rep("      python3 library.py themed.html kobem-talday.html  # «Менің талдауларым»",
    "      python3 library.py themed.html library.html       # «Менің талдауларым»\n"
    "      python3 help.py library.html kobem-talday.html    # «Қалай қолдану керек?»")

open(out, 'w', encoding='utf8').write(s)
print('wrote', out, len(s.encode('utf8')) // 1024, 'KB')
