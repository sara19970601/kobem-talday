"""Lab: «Кейіпкер психологиясын талдау зертханасы» — a step-by-step character analysis.
Answers live in memory; with the user's consent they are also kept in this browser
(localStorage). Nothing is sent anywhere. The result is one structured document to copy
or print / save as PDF.
Usage: python3 -I lab.py in.html out.html   (run after shop.py)"""
import sys

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('lab anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

# ---- CSS ----
rep('</style>\n</head>', r"""</style>
<style id="lab">
  /* LAB — «Кейіпкер психологиясын талдау зертханасы» */
  .lab-bar { display: flex; flex-wrap: wrap; gap: 8px 14px; align-items: center; justify-content: space-between;
    margin: 0 0 14px; padding: 10px 14px; border: 1px solid var(--line); border-radius: 12px; background: var(--surface); }
  .lab-consent { display: inline-flex; gap: 8px; align-items: flex-start; font-size: 14px; line-height: 1.4; cursor: pointer; }
  .lab-consent input { margin-top: 3px; width: 17px; height: 17px; flex: none; }
  .lab-consent small { display: block; color: var(--ink-2); font-size: 12.5px; }
  .lab-steps { display: flex; gap: 6px; overflow-x: auto; padding: 2px 2px 8px; margin: 0 0 12px; scrollbar-width: thin; }
  .lab-dot { flex: none; display: inline-flex; align-items: center; gap: 6px; border: 1px solid var(--line-strong);
    background: var(--surface); color: var(--ink-2); border-radius: 999px; padding: 5px 12px 5px 5px; font-size: 13px; font-weight: 600; }
  .lab-dot .n { width: 22px; height: 22px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center;
    background: var(--surface-2); color: var(--ink-2); font-size: 12px; }
  .lab-dot.done .n { background: var(--ok-soft, var(--accent-soft)); color: var(--ok, var(--accent)); }
  .lab-dot[aria-current="step"] { border-color: var(--accent); color: var(--accent); background: var(--accent-soft); }
  .lab-dot[aria-current="step"] .n { background: var(--accent); color: #fff; }
  .lab-pos { margin: 0 0 4px; font-size: 13px; font-weight: 700; color: var(--accent); letter-spacing: .04em; text-transform: uppercase; }
  .lab-step-title { margin: 0 0 6px; font-family: var(--display); font-size: 22px; }
  .lab-step-intro { margin: 0 0 14px; color: var(--ink-2); }
  .lab-rules { margin: 0 0 14px; }
  .lab-rules h3 { margin: 0 0 8px; font-size: 15px; }
  .lab-rules ul { margin: 0; padding-left: 20px; }
  .lab-rules li { margin-bottom: 5px; line-height: 1.5; }
  .lab-note { margin: 0 0 14px; padding: 10px 14px; border-left: 3px solid var(--gold, var(--accent)); background: var(--surface-2);
    border-radius: 0 10px 10px 0; font-size: 14.5px; line-height: 1.5; }
  .lab-hint { margin: -2px 0 8px; padding-left: 18px; color: var(--ink-2); font-size: 13.5px; line-height: 1.45; }
  .lab-hint li { margin-bottom: 2px; }
  .lab-warn { margin: 6px 0 0; font-size: 13px; color: var(--warn); }
  .lab-warn:empty { display: none; }
  .lab-rows { display: grid; gap: 10px; }
  .lab-row { position: relative; display: grid; gap: 8px; padding: 10px 12px; border: 1px solid var(--line); border-radius: 12px; background: var(--surface-2); }
  .lab-row-head { display: flex; justify-content: space-between; align-items: center; font-size: 12.5px; font-weight: 700; color: var(--ink-2); }
  .lab-row-cells { display: grid; gap: 8px; grid-template-columns: repeat(auto-fit, minmax(min(100%, 180px), 1fr)); }
  .lab-cell label { display: block; font-size: 12.5px; font-weight: 600; color: var(--ink-2); margin-bottom: 3px; }
  .lab-cell textarea { min-height: 54px; }
  .lab-del { border: 0; background: none; color: var(--ink-2); font-size: 13px; padding: 2px 6px; border-radius: 6px; }
  .lab-del:hover { color: var(--warn); background: var(--warn-soft); }
  .lab-add { margin-top: 10px; }
  .lab-tech { display: grid; gap: 6px; padding: 10px 0; border-top: 1px solid var(--line); }
  .lab-tech:first-of-type { border-top: 0; padding-top: 0; }
  .lab-tech-head { display: inline-flex; gap: 8px; align-items: center; font-weight: 600; cursor: pointer; }
  .lab-tech-head input { width: 17px; height: 17px; }
  .lab-tech p { margin: 0; color: var(--ink-2); font-size: 13.5px; }
  .lab-doc { padding: 22px 26px; }
  .lab-doc h3 { margin: 18px 0 6px; font-size: 17px; color: var(--accent); }
  .lab-doc h3:first-of-type { margin-top: 4px; }
  .lab-doc h4 { margin: 10px 0 3px; font-size: 14.5px; }
  .lab-doc p { margin: 0 0 6px; line-height: 1.55; white-space: pre-wrap; }
  .lab-doc ul { margin: 0 0 6px; padding-left: 20px; }
  .lab-doc li { margin-bottom: 4px; line-height: 1.5; white-space: pre-wrap; }
  .lab-doc .lab-noev { color: var(--warn); font-size: 13px; }
  .lab-doc-title { margin: 0 0 4px; font-size: 20px; }
  .lab-empty { color: var(--ink-2); }
  .lab-actions { display: flex; flex-wrap: wrap; gap: 8px; margin: 0 0 14px; }
  @media (max-width: 520px) { .lab-doc { padding: 16px; } .lab-bar { padding: 10px 12px; } }
  /* Six tabs: on screens up to 1440px the children's tab uses its short name and tabs sit closer,
     so «Сатып алу» and «Көмек» stay on the first row. */
  @media (min-width: 901px) and (max-width: 1440px) {
    .tab-long { display: none; } .tab-short { display: inline; }
    .tab { padding: 7px 12px; }
  }
  @media (min-width: 901px) and (max-width: 1080px) { .brand { min-width: 0; } .brand h1 { display: none; } .brand .brand-mark { display: block; } .tab { padding: 7px 9px; } }   /* logo only */
  @media (min-width: 901px) and (max-width: 1260px) {   /* icons only, so both buttons fit beside the tabs */
    .shop-btn .shop-label, .help-btn .help-label { display: none; }
    .help-btn .help-q { margin-right: 0; }
    .shop-btn, .help-btn { height: 42px; padding: 0 12px; }
  }
  @media print {
    .print-lab h2 { font-size: 15pt; margin: 0 0 4pt; }
    .print-lab h3 { font-size: 12.5pt; margin: 12pt 0 4pt; border-bottom: 1px solid #000; padding-bottom: 2pt; break-after: avoid; }
    .print-lab h4 { font-size: 11pt; margin: 6pt 0 2pt; break-after: avoid; }
    .print-lab p, .print-lab li { white-space: pre-wrap; margin: 0 0 3pt; }
    .print-lab ul { margin: 0 0 4pt; padding-left: 16pt; }
    .print-lab .lab-noev { font-style: italic; }
  }
</style>
</head>""")

# ---- Strings ----
rep("  tabKids: 'Балалар әдебиеті',", r"""  tabKids: 'Балалар әдебиеті',
  tabLab: 'Зертхана',
  labTitle: 'Кейіпкер психологиясын талдау зертханасы',
  labIntro: 'Кейіпкердің мінезін, мақсатын, эмоциясын, ішкі қайшылығын, қарым-қатынасын және өзгерісін мәтінге сүйеніп, кезең-кезеңімен талдаңыз. Соңында жауаптарыңыз бір құжатқа жиналады.',
  labPos: '{n}-кезең / {total}',
  labSteps: 'Талдау кезеңдері',
  labConsent: 'Жауаптарымды осы браузерде сақтау',
  labConsentOn: 'Жауаптар тек осы құрылғыда сақталады, ешқайда жіберілмейді.',
  labConsentOff: 'Белгілемесеңіз, бетті жапқанда немесе жаңартқанда жауаптар өшеді.',
  labSavedOff: 'Жауаптар браузерден өшірілді. Енді олар тек бет ашық тұрғанда сақталады.',
  labClear: 'Жауаптарды тазарту',
  labClearAsk: 'Зертханадағы барлық жауап өшіріледі. Бұл әрекетті қайтару мүмкін емес. Жалғастырасыз ба?',
  labCleared: 'Зертхана жауаптары тазартылды.',
  labCopy: 'Талдауды көшіру',
  labCopied: 'Талдау көшірілді. Оны Word құжатына немесе хатқа қоя аласыз.',
  labCopyManual: 'Мәтін белгіленді: Ctrl+C (телефонда «Көшіру») арқылы көшіріңіз.',
  labPrint: 'Басып шығару / PDF сақтау',
  labPrintHint: 'PDF алу үшін басып шығару терезесінде «PDF ретінде сақтау» (Save as PDF) таңдаңыз.',
  labPrev: '← Алдыңғы кезең',
  labNext: 'Келесі кезең →',
  labToSummary: 'Жинақтауға өту →',
  labAddRow: '+ Жол қосу',
  labDelRow: 'Жолды өшіру',
  labRow: '{n}-жол',
  labSelect: 'Таңдаңыз',
  labNoEvidence: 'Бұл тұжырымға мәтіннен дәлел қосыңыз: эпизод, дәйексөз немесе бет.',
  labDiagnosis: 'Ескерту: «{word}» — клиникалық термин. Зертхана кейіпкерге диагноз қоймайды: оның мәтіндегі сөзін, әрекетін, сезімін сипаттап жазыңыз.',
  labLeave: 'Зертханадағы жауаптар браузерде сақталмаған. Бетті жапсаңыз, олар өшеді.',
  labRulesTitle: 'Зертхана ережелері',
  labRules: [
    'Бұл — әдеби кейіпкерді талдау құралы, клиникалық психологиялық диагноз қоюға арналмаған. Кейіпкерге «ауру» атауын таңбаламаймыз, оның мінез-құлқын мәтін арқылы сипаттаймыз.',
    'Әр тұжырымды мәтіннен дәлелмен (эпизод, дәйексөз, бет) бекітіңіз. Мәтінде жоқ нәрсені ойдан қоспаңыз.',
    'Мақсат, мотив және эмоция — әртүрлі ұғымдар: мақсат — кейіпкер неге жеткісі келеді, мотив — неге соған ұмтылады, эмоция — белгілі бір сәтте не сезінеді.',
    'Кейіпкердің өзгермеуі де — маңызды әдеби нәтиже.',
    'Интерпретацияның бір ғана дұрыс жауабы жоқ: дәлелге сүйенген әртүрлі оқу болуы мүмкін.',
  ],
  labDocTitle: 'Кейіпкер психологиясын талдау',
  labDocEmpty: 'Талдау әлі бос. Алдыңғы кезеңдердегі өрістерді толтырыңыз, нәтиже осында жиналады.',
  labDocNoEv: '(мәтіндік дәлел көрсетілмеген)',
  labDocNote: 'Бұл — әдеби кейіпкердің талдауы, психологиялық диагноз емес.',""")

# ---- Tabs and dispatch ----
rep("['library', 'book', 'guide', 'glossary', 'kids'].map(tab", "['library', 'book', 'guide', 'glossary', 'kids', 'lab'].map(tab")
rep("        : t({ library: 'tabLibrary', book: 'tabBook', guide: 'tabGuide', glossary: 'tabGlossary' }[tab])))),",
    "        : t({ library: 'tabLibrary', book: 'tabBook', guide: 'tabGuide', glossary: 'tabGlossary', lab: 'tabLab' }[tab])))),")
rep("t(['guide', 'glossary', 'kids'].includes(state.ui.tab) ? 'navGuide' : 'navBook')",
    "t(['guide', 'glossary', 'kids', 'lab'].includes(state.ui.tab) ? 'navGuide' : 'navBook')")
rep("tab: ['guide', 'library', 'glossary', 'kids'].includes(u.tab) ? u.tab : 'book',",
    "tab: ['guide', 'library', 'glossary', 'kids', 'lab'].includes(u.tab) ? u.tab : 'book',", count=2)
rep("  if (state.ui.tab === 'kids') { renderKidsSidebar(); return; }",
    "  if (state.ui.tab === 'kids') { renderKidsSidebar(); return; }\n"
    "  if (state.ui.tab === 'lab') { renderLabSidebar(); return; }")
rep("  if (state.ui.tab === 'kids') { renderKidsFooter(); return; }",
    "  if (state.ui.tab === 'kids') { renderKidsFooter(); return; }\n"
    "  if (state.ui.tab === 'lab') { renderLabFooter(); return; }")
rep(": state.ui.tab === 'kids' ? renderKidsMain() : renderLibraryMain());",
    ": state.ui.tab === 'kids' ? renderKidsMain() : state.ui.tab === 'lab' ? renderLabMain() : renderLibraryMain());")
rep("  if (state.ui.tab === 'kids') return 'kids';",
    "  if (state.ui.tab === 'kids') return 'kids';\n"
    "  if (state.ui.tab === 'lab') return 'lab';")
rep("""  } else if (target === 'kids') {""",
    """  } else if (target === 'lab') {
    section = h('section', { class: 'print-section print-lab' }, labDocNodes());
  } else if (target === 'kids') {""")

# ---- Data, state and views ----
rep("""/* ==============================================================================
   PRINT — fills #print-area""", r"""/* ==============================================================================
   LAB — «Кейіпкер психологиясын талдау зертханасы».
   LAB_STEPS describes the form: each step is one card of fields. Answers sit in `lab`
   (memory); with consent (the checkbox) they are also kept in localStorage.
   ============================================================================== */
const LAB_KEY = 'kobem-talday:lab';
const LAB_CONSENT_KEY = 'kobem-talday:lab-consent';
const LAB_MAX_ROWS = 12;
const LAB_TECHNIQUES = [
  { id: 'portrait', label: 'Портрет', hint: 'Сырт келбеті, киімі, жүзіндегі өзгеріс оның ішкі күйін қалай білдіреді?' },
  { id: 'dialogue', label: 'Диалог', hint: 'Кейіпкер қалай сөйлейді: сөз таңдауы, үні, үнсіздігі не туралы хабар береді?' },
  { id: 'monologue', label: 'Ішкі монолог', hint: 'Кейіпкердің ойы мен күдігі тікелей берілген бе? Ол не туралы толғанады?' },
  { id: 'action', label: 'Іс-әрекет', hint: 'Оның әрекеті сөзімен сәйкес келе ме? Шешуші сәтте не істейді?' },
  { id: 'narrator', label: 'Баяндаушының бағалауы', hint: 'Баяндаушы кейіпкерді бағалай ма? Ол бағаға толық сенуге бола ма, әлде ол біржақты ма?' },
];
const LAB_STEPS = [
  { id: 'about', title: 'Шығарма мен кейіпкер', rules: true,
    intro: 'Талдайтын шығарманы және бір кейіпкерді таңдаңыз.',
    fields: [
      { id: 'work', type: 'text', label: 'Шығарманың атауы', hints: ['Шығарманың толық атауын жазыңыз.'] },
      { id: 'author', type: 'text', label: 'Автордың аты-жөні', hints: ['Автордың аты-жөнін толық жазыңыз.'] },
      { id: 'hero', type: 'text', label: 'Кейіпкердің аты', hints: ['Бір кейіпкерді таңдаңыз. Ол басты кейіпкер болуы міндетті емес.', 'Кейіпкердің шығармадағы рөлін (басты, қосалқы) өзіңіз үшін анықтап алыңыз.'] },
    ] },
  { id: 'traits', title: 'Мінез ерекшеліктері',
    intro: 'Кейіпкердің мінезін сипаттайтын белгілерді жазыңыз. Әр белгінің жанына оны көрсететін эпизодты не дәйексөзді қосыңыз.',
    fields: [
      { id: 'traits', type: 'rows', label: 'Мінез белгілері және дәлелдері', claim: 0, evidence: [1, 2],
        columns: ['Мінез белгісі', 'Мәтіндегі дәлел (эпизод немесе дәйексөз)', 'Беті / тарауы'],
        hints: ['Кейіпкер қиын жағдайда қалай әрекет етеді?', 'Оның қай қасиеті шығарма бойы қайталанып көрінеді?', 'Басқалар ол туралы не айтады, ал өзі өзін қалай көрсетеді?', 'Бір белгі — кемінде бір дәлел.'] },
    ] },
  { id: 'goals', title: 'Мақсаты мен қажеттіліктері',
    note: 'Мақсат — кейіпкер нені қалайды; мотив — неге соны қалайды; ішкі қажеттілік — ол шын мәнінде неге мұқтаж. Үшеуін бөлек жазыңыз: олар сәйкес келмеуі де мүмкін.',
    fields: [
      { id: 'goal', type: 'long', label: 'Сыртқы мақсаты', hints: ['Кейіпкер нақты неге қол жеткізгісі келеді?', 'Ол бұл мақсатын өзі айта ма, әлде әрекетінен ғана байқала ма?'] },
      { id: 'need', type: 'long', label: 'Ішкі қажеттілігі', hints: ['Ол шын мәнінде неге мұқтаж: қауіпсіздік, мойындалу, махаббат, еркіндік, әділдік т.б.?', 'Мақсаты мен қажеттілігі бір-біріне сәйкес келе ме?'] },
      { id: 'motive', type: 'long', label: 'Мотиві', hints: ['Ол неге дәл осы мақсатқа ұмтылады?', 'Қандай оқиға, тәжірибе не құндылық оны итермелейді?'] },
      { id: 'goalEvidence', type: 'long', label: 'Мәтіндегі дәлел', evidenceFor: ['goal', 'need', 'motive'], hints: ['Мақсатын, қажеттілігін не мотивін көрсететін эпизодты немесе дәйексөзді жазыңыз.'] },
    ] },
  { id: 'emotions', title: 'Эмоциялары мен ішкі қайшылықтары',
    note: 'Эмоция — белгілі бір сәттегі күй. Ол мақсат пен мотивтен бөлек: бір мақсатқа ұмтылған кейіпкер әр сәтте түрлі сезімде болуы мүмкін.',
    fields: [
      { id: 'emotions', type: 'rows', label: 'Эмоциялары', claim: 1, evidence: [2],
        columns: ['Эпизод', 'Эмоция', 'Мәтіндегі белгісі (сөз, қимыл, дене күйі)'],
        hints: ['Автор эмоцияны тікелей атай ма, әлде қимыл, үн, дене күйі арқылы көрсете ме?', 'Эмоция шығарма барысында қалай ауысады?'] },
      { id: 'conflict', type: 'long', label: 'Ішкі қайшылығы', hints: ['Кейіпкердің ішінде қандай екі тілек, құндылық не міндет қақтығысады?', 'Ол бұл қайшылықты өзі сезіне ме?'] },
      { id: 'conflictEvidence', type: 'long', label: 'Ішкі қайшылықтың дәлелі', evidenceFor: ['conflict'], hints: ['Күдік, екіұдай шешім немесе ішкі монолог көрінетін жерді табыңыз.'] },
    ] },
  { id: 'relations', title: 'Басқа кейіпкерлермен қарым-қатынасы',
    intro: 'Кейіпкердің басқалармен байланысы оның қандай қырын ашатынын көрсетіңіз.',
    fields: [
      { id: 'relations', type: 'rows', label: 'Қарым-қатынас жүйесі', claim: 1, evidence: [2],
        columns: ['Кейіпкер', 'Қарым-қатынас сипаты', 'Мәтіндегі көрінісі', 'Шығарма барысында өзгереді ме?'],
        hints: ['Ол кіммен жақын, кіммен қақтығыста?', 'Басқа кейіпкер оның қандай қырын ашады?', 'Қарым-қатынас шығарма барысында өзгере ме?'] },
    ] },
  { id: 'techniques', title: 'Психологиялық бейнелеу тәсілдері',
    intro: 'Автор кейіпкердің ішкі әлемін қай тәсілдермен ашады? Мәтінде бар тәсілдерді ғана белгілеп, әрқайсысына мысал келтіріңіз.',
    fields: [{ id: 'techniques', type: 'techniques', label: 'Бейнелеу тәсілдері' }] },
  { id: 'quotes', title: 'Мәтіндік дәлелдер',
    intro: 'Талдауыңызды бекітетін ең маңызды дәйексөздерді жинаңыз.',
    fields: [
      { id: 'quotes', type: 'rows', label: 'Дәйексөздер', claim: 0, evidence: [2],
        columns: ['Қысқа дәйексөз', 'Беті / тарауы', 'Нені дәлелдейді?'],
        hints: ['Дәйексөз қысқа болсын: бір-екі сөйлем жеткілікті.', 'Дәйексөзді өзгертпей көшіріңіз.', 'Әр дәйексөздің қай тұжырымыңызды дәлелдейтінін көрсетіңіз.'] },
    ] },
  { id: 'dynamics', title: 'Кейіпкердің даму динамикасы',
    note: 'Кейіпкердің өзгермеуі де маңызды нәтиже: автор оның тұрақтылығы арқылы да белгілі бір ой айтуы мүмкін.',
    fields: [
      { id: 'start', type: 'long', label: 'Шығарма басындағы күйі', hints: ['Алғашқы көріністерде кейіпкер қандай?', 'Ол неге сенеді, неден қорқады, неге ұмтылады?'] },
      { id: 'end', type: 'long', label: 'Шығарма соңындағы күйі', hints: ['Соңында оның көзқарасы, мінезі, жағдайы қандай?'] },
      { id: 'change', type: 'choice', label: 'Өзгеріс сипаты', options: ['Өзгерді', 'Ішінара өзгерді', 'Өзгермеді'], hints: ['Мәтінге сүйеніп таңдаңыз. «Өзгермеді» де — дұрыс әрі маңызды жауап болуы мүмкін.'] },
      { id: 'cause', type: 'long', label: 'Өзгерістің (немесе өзгермеуінің) себебі мен дәлелі', evidenceFor: ['start', 'end', 'change'], hints: ['Қандай оқиға бетбұрыс болды?', 'Бетбұрыс болмаса, кейіпкер неге бұрынғы қалпында қалды?'] },
    ] },
  { id: 'interpretation', title: 'Жеке интерпретация',
    note: 'Интерпретацияның бір ғана дұрыс жауабы жоқ. Дәлелге сүйенген оқу — құнды оқу.',
    fields: [
      { id: 'interp', type: 'long', label: 'Менің интерпретациям', hints: ['Автор бұл кейіпкер арқылы не айтқысы келеді деп ойлайсыз?', 'Кейіпкер сізде қандай сезім туғызды, неге?', 'Тұжырымыңызды алдыңғы кезеңдердегі дәлелдерге сүйеңіз.'] },
      { id: 'alt', type: 'long', label: 'Басқаша оқу мүмкіндігі', hints: ['Бұл кейіпкерді басқаша түсінуге бола ма?', 'Мәтіндегі қай дәлел басқа оқуға жол ашады?'] },
    ] },
  { id: 'summary', title: 'Талдауды жинақтау', summary: true,
    intro: 'Жауаптарыңыз бір құрылымды құжатқа жиналды. Бос өрістер құжатқа кірмейді.' },
];
const LAB_FIELDS = {};
LAB_STEPS.forEach(st => (st.fields || []).forEach(f => { LAB_FIELDS[f.id] = f; }));

// Clinical labels: the lab warns (never blocks) and asks for a description from the text instead.
const LAB_DIAGNOSIS = ['депрессия', 'депрессиясы', 'депрессиялық', 'психоз', 'шизофрения', 'шизофреник', 'биполяр', 'невроз', 'невротик',
  'психопат', 'психопатия', 'социопат', 'нарциссизм', 'нарцисс', 'паранойя', 'параноик', 'аутизм', 'аутист', 'птср', 'сдвг', 'диагноз', 'психикалық ауру'];

function labFresh() {
  const data = {};
  Object.values(LAB_FIELDS).forEach(f => {
    data[f.id] = f.type === 'rows' ? [f.columns.map(() => '')]
      : f.type === 'techniques' ? Object.fromEntries(LAB_TECHNIQUES.map(x => [x.id, { on: false, text: '' }])) : '';
  });
  return { version: 1, step: 0, data: data };
}

/** Accept only the known shape (stored data may be old or edited by hand). */
function labClean(raw) {
  const out = labFresh();
  if (!isObj(raw) || !isObj(raw.data)) return out;
  const str = v => typeof v === 'string' ? v.slice(0, CONFIG.MAX_TEXT_LENGTH) : '';
  Object.values(LAB_FIELDS).forEach(f => {
    const v = raw.data[f.id];
    if (f.type === 'rows') {
      if (Array.isArray(v) && v.length) out.data[f.id] = v.slice(0, LAB_MAX_ROWS).map(r => f.columns.map((c, i) => str(Array.isArray(r) ? r[i] : '')));
    } else if (f.type === 'techniques') {
      if (isObj(v)) LAB_TECHNIQUES.forEach(x => { const o = isObj(v[x.id]) ? v[x.id] : {}; out.data[f.id][x.id] = { on: o.on === true, text: str(o.text) }; });
    } else if (f.type === 'choice') {
      out.data[f.id] = f.options.includes(v) ? v : '';
    } else {
      out.data[f.id] = str(v);
    }
  });
  const step = Number(raw.step);
  out.step = Number.isInteger(step) && step >= 0 && step < LAB_STEPS.length ? step : 0;
  return out;
}

function labConsentGiven() {
  try { return window.localStorage.getItem(LAB_CONSENT_KEY) === '1'; } catch (e) { return false; }
}
let labConsent = labConsentGiven();
let lab = (() => {
  if (!labConsent) return labFresh();
  try { return labClean(JSON.parse(window.localStorage.getItem(LAB_KEY) || 'null')); } catch (e) { return labFresh(); }
})();
let labTimer = null;

function labSaveNow() {
  clearTimeout(labTimer);
  if (!labConsent) return;
  try { window.localStorage.setItem(LAB_KEY, JSON.stringify(lab)); } catch (e) { /* storage full or blocked */ }
}
function labChanged() { clearTimeout(labTimer); labTimer = setTimeout(labSaveNow, 400); updateLabProgress(); }

function setLabConsent(on) {
  labConsent = on;
  try {
    if (on) { window.localStorage.setItem(LAB_CONSENT_KEY, '1'); labSaveNow(); }
    else { window.localStorage.removeItem(LAB_CONSENT_KEY); window.localStorage.removeItem(LAB_KEY); }
  } catch (e) { /* storage blocked: answers stay in memory */ }
  const note = document.getElementById('lab-consent-note');
  if (note) note.textContent = t(on ? 'labConsentOn' : 'labConsentOff');
  if (!on && labHasContent()) showBanner('ok', t('labSavedOff'));
}

function filledRow(r) { return r.some(filled); }
function labFieldFilled(f) {
  const v = lab.data[f.id];
  if (f.type === 'rows') return v.some(filledRow);
  if (f.type === 'techniques') return LAB_TECHNIQUES.some(x => v[x.id].on || filled(v[x.id].text));
  return filled(v);
}
function labStepDone(st) { return !!st.fields && st.fields.some(labFieldFilled); }
function labHasContent() { return Object.values(LAB_FIELDS).some(labFieldFilled); }

// Leaving the page with unsaved answers (no consent): the browser asks first.
window.addEventListener('beforeunload', e => {
  if (!labConsent && labHasContent()) { e.preventDefault(); e.returnValue = t('labLeave'); return t('labLeave'); }
  labSaveNow();
});

function labGo(i) {
  lab.step = Math.max(0, Math.min(LAB_STEPS.length - 1, i));
  labSaveNow();
  closeNav();
  renderSidebar(); renderMain(); renderFooter();
  document.getElementById('main').scrollTop = 0;
}

function diagnosisWord(text) {
  const words = fold(text || '').split(/[^a-zа-яёәіңғүұқөһ]+/);
  const joined = ' ' + words.join(' ') + ' ';
  return LAB_DIAGNOSIS.find(w => joined.indexOf(' ' + w + ' ') !== -1 || words.some(x => w.length > 5 && x.indexOf(w) === 0)) || '';
}

/* ---- Views ---- */
function renderLabSidebar() {
  const nav = document.getElementById('sidebar');
  nav.replaceChildren(
    h('h2', { text: t('labSteps') }),
    h('ul', { class: 'steps', id: 'lab-nav' }, LAB_STEPS.map((st, i) => h('li', null, h('button', {
      type: 'button', class: 'step-btn' + (labStepDone(st) ? ' done' : ''), 'aria-current': i === lab.step ? 'step' : null,
      onclick: () => labGo(i),
    }, h('span', { class: 'step-num', 'aria-hidden': 'true' }, labStepDone(st) ? '✓' : st.summary ? '≡' : String(i + 1)),
      h('span', { class: 'step-label' }, st.title))))),
    h('p', { class: 'privacy', text: t('labConsentOn') }));
}

/** Refresh the ✓ marks without rebuilding the form (keeps focus while typing). */
function updateLabProgress() {
  document.querySelectorAll('#lab-nav .step-btn').forEach((b, i) => {
    const done = labStepDone(LAB_STEPS[i]);
    b.classList.toggle('done', done);
    b.querySelector('.step-num').textContent = done ? '✓' : LAB_STEPS[i].summary ? '≡' : String(i + 1);
  });
  document.querySelectorAll('.lab-dot').forEach((d, i) => d.classList.toggle('done', labStepDone(LAB_STEPS[i])));
}

function labHints(list) { return list && list.length ? h('ul', { class: 'lab-hint' }, list.map(x => h('li', { text: x }))) : null; }

function labTextInput(f, id, value, onValue, tag) {
  const warn = h('p', { class: 'lab-warn', 'aria-live': 'polite' });
  const check = v => { const w = diagnosisWord(v); warn.textContent = w ? t('labDiagnosis', { word: w }) : ''; };
  const el = h(tag || (f.type === 'text' ? 'input' : 'textarea'), {
    id: id, type: (tag || f.type) === 'text' ? 'text' : null, value: value, maxlength: CONFIG.MAX_TEXT_LENGTH,
    oninput: e => { onValue(e.target.value); check(e.target.value); },
  });
  check(value);
  return [el, warn];
}

/** A field whose claims need evidence: warn when they are written but the evidence is not. */
function labEvidenceWarn(f) {
  const el = h('p', { class: 'lab-warn', 'aria-live': 'polite' });
  const update = () => {
    const claims = f.evidenceFor.some(id => filled(lab.data[id]));
    el.textContent = claims && !filled(lab.data[f.id]) ? t('labNoEvidence') : '';
  };
  update();
  return { el: el, update: update };
}

function renderLabRows(f) {
  const rows = lab.data[f.id];
  const box = h('div', { class: 'lab-rows' });
  const draw = () => box.replaceChildren.apply(box, rows.map((r, ri) => {
    const warn = h('p', { class: 'lab-warn', 'aria-live': 'polite' });
    const checkRow = () => {
      const w = r.map(diagnosisWord).find(Boolean);
      warn.textContent = w ? t('labDiagnosis', { word: w })
        : filled(r[f.claim]) && !f.evidence.some(i => filled(r[i])) ? t('labNoEvidence') : '';
    };
    checkRow();
    return h('div', { class: 'lab-row' },
      h('div', { class: 'lab-row-head' }, h('span', { text: t('labRow', { n: ri + 1 }) }),
        rows.length > 1 ? h('button', { type: 'button', class: 'lab-del', text: '× ' + t('labDelRow'),
          onclick: () => { rows.splice(ri, 1); labChanged(); draw(); } }) : null),
      h('div', { class: 'lab-row-cells' }, f.columns.map((c, ci) => {
        const id = 'lab-' + f.id + '-' + ri + '-' + ci;
        return h('div', { class: 'lab-cell' }, h('label', { for: id, text: c }),
          h('textarea', { id: id, value: r[ci], maxlength: CONFIG.MAX_TEXT_LENGTH, rows: 2,
            oninput: e => { r[ci] = e.target.value; labChanged(); checkRow(); } }));
      })),
      warn);
  }));
  draw();
  return h('div', { class: 'card' },
    h('span', { class: 'field-label', text: f.label }), labHints(f.hints), box,
    h('button', { type: 'button', class: 'btn lab-add', text: t('labAddRow'),
      onclick: e => {
        if (rows.length >= LAB_MAX_ROWS) { e.currentTarget.disabled = true; return; }
        rows.push(f.columns.map(() => ''));
        labChanged(); draw();
        const cells = box.querySelectorAll('.lab-row:last-child textarea');
        if (cells[0]) cells[0].focus();
        if (rows.length >= LAB_MAX_ROWS) e.currentTarget.disabled = true;
      }, disabled: rows.length >= LAB_MAX_ROWS }));
}

function renderLabTechniques(f) {
  const v = lab.data[f.id];
  return h('div', { class: 'card' },
    LAB_TECHNIQUES.map(x => {
      const id = 'lab-tech-' + x.id;
      const box = h('input', { type: 'checkbox', id: id + '-on', onchange: e => { v[x.id].on = e.target.checked; labChanged(); } });
      box.checked = v[x.id].on;
      return h('div', { class: 'lab-tech' },
        h('label', { class: 'lab-tech-head', for: id + '-on' }, box, x.label),
        h('p', { text: x.hint }),
        h('label', { class: 'sr-only', for: id, text: x.label }),
        labTextInput(f, id, v[x.id].text, val => { v[x.id].text = val; if (filled(val) && !v[x.id].on) { v[x.id].on = true; box.checked = true; } labChanged(); }, 'textarea'));
    }));
}

function renderLabField(f, evWarns) {
  if (f.type === 'rows') return renderLabRows(f);
  if (f.type === 'techniques') return renderLabTechniques(f);
  const id = 'lab-' + f.id;
  const label = h('label', { class: 'field-label', for: id, text: f.label });
  if (f.type === 'choice') {
    return h('div', { class: 'card' }, label, labHints(f.hints),
      h('select', { id: id, value: lab.data[f.id], onchange: e => { lab.data[f.id] = e.target.value; labChanged(); evWarns.forEach(w => w.update()); } },
        h('option', { value: '' }, t('labSelect')), f.options.map(o => h('option', { value: o }, o))));
  }
  const ev = f.evidenceFor ? labEvidenceWarn(f) : null;
  if (ev) evWarns.push(ev);
  return h('div', { class: 'card' }, label, labHints(f.hints),
    labTextInput(f, id, lab.data[f.id], val => { lab.data[f.id] = val; labChanged(); evWarns.forEach(w => w.update()); }),
    ev ? ev.el : null);
}

function renderLabMain() {
  const st = LAB_STEPS[lab.step];
  const consent = h('input', { type: 'checkbox', id: 'lab-consent', onchange: e => setLabConsent(e.target.checked) });
  consent.checked = labConsent;
  const evWarns = [];
  return h('article', { class: 'lab' },
    h('p', { class: 'ws-kicker', text: t('tabLab') }),
    h('h2', { class: 'ws-title', text: t('labTitle') }),
    h('p', { class: 'k-intro', text: t('labIntro') }),
    h('div', { class: 'lab-bar' },
      h('label', { class: 'lab-consent', for: 'lab-consent' }, consent,
        h('span', null, t('labConsent'), h('small', { id: 'lab-consent-note', text: t(labConsent ? 'labConsentOn' : 'labConsentOff') }))),
      h('button', { type: 'button', class: 'btn', text: t('labClear'), onclick: () => askConfirm(t('labClearAsk'), () => {
        lab = labFresh(); labSaveNow(); render(); document.getElementById('main').scrollTop = 0; showBanner('ok', t('labCleared'));
      }) })),
    h('nav', { class: 'lab-steps', 'aria-label': t('labSteps') }, LAB_STEPS.map((x, i) => h('button', {
      type: 'button', class: 'lab-dot' + (labStepDone(x) ? ' done' : ''), 'aria-current': i === lab.step ? 'step' : null,
      title: x.title, onclick: () => labGo(i),
    }, h('span', { class: 'n', text: x.summary ? '≡' : String(i + 1) }), h('span', { text: x.title })))),
    h('p', { class: 'lab-pos', text: t('labPos', { n: lab.step + 1, total: LAB_STEPS.length }) }),
    h('h3', { class: 'lab-step-title', text: st.title }),
    st.intro ? h('p', { class: 'lab-step-intro', text: st.intro }) : null,
    st.rules ? h('div', { class: 'card lab-rules' }, h('h3', { text: t('labRulesTitle') }),
      h('ul', null, STRINGS.labRules.map(x => h('li', { text: x })))) : null,
    st.note ? h('p', { class: 'lab-note', text: st.note }) : null,
    st.summary ? renderLabSummary() : st.fields.map(f => renderLabField(f, evWarns)));
}

/* ---- The document: sections built once, rendered as DOM (screen, print) or as text (copy) ---- */
function labDoc() {
  const d = lab.data;
  const v = x => (d[x] || '').trim();
  const rows = (id, fmt) => d[id].filter(filledRow).map(r => fmt(r.map(c => c.trim())));
  const noEv = (r, f) => filled(r[f.claim]) && !f.evidence.some(i => filled(r[i]));
  const field = (label, text) => filled(text) ? { label: label, text: text } : null;
  const list = (label, items) => items.length ? { label: label, items: items } : null;
  const join = parts => parts.filter(filled).join(' — ');
  const where = x => filled(x) ? ' (' + x + ')' : '';
  const sections = [
    { title: 'Шығарма мен кейіпкер туралы мәлімет', parts: [
      field('Шығарма', v('work') ? '«' + v('work').replace(/^«|»$/g, '') + '»' : ''), field('Автор', v('author')), field('Кейіпкер', v('hero'))] },
    { title: 'Кейіпкердің психологиялық портреті', parts: [
      list('Мінез ерекшеліктері', rows('traits', r => ({ text: join([r[0], r[1]]) + where(r[2]), noEv: noEv(r, LAB_FIELDS.traits) }))),
      list('Эмоциялары', rows('emotions', r => ({ text: [r[0] ? r[0] + ':' : '', r[1], r[2] ? '— ' + r[2] : ''].filter(filled).join(' '), noEv: noEv(r, LAB_FIELDS.emotions) }))),
      list('Автордың бейнелеу тәсілдері', LAB_TECHNIQUES.filter(x => d.techniques[x.id].on || filled(d.techniques[x.id].text))
        .map(x => ({ text: x.label + (filled(d.techniques[x.id].text) ? ': ' + d.techniques[x.id].text.trim() : '') })))] },
    { title: 'Мақсаттары мен ішкі қайшылықтары', parts: [
      field('Сыртқы мақсаты', v('goal')), field('Ішкі қажеттілігі', v('need')), field('Мотиві', v('motive')),
      field('Дәлел', v('goalEvidence')),
      field('Ішкі қайшылығы', v('conflict')), field('Ішкі қайшылықтың дәлелі', v('conflictEvidence'))] },
    { title: 'Қарым-қатынас жүйесі', parts: [
      list('', rows('relations', r => ({ text: join([r[0], r[1]]) + (r[2] ? '. Мәтінде: ' + r[2] : '') + (r[3] ? '. Өзгерісі: ' + r[3] : ''), noEv: noEv(r, LAB_FIELDS.relations) })))] },
    { title: 'Мәтіндік дәлелдер', parts: [
      list('', rows('quotes', r => ({ text: (r[0] ? '«' + r[0].replace(/^«|»$/g, '') + '»' : '') + where(r[1]) + (r[2] ? ' — ' + r[2] : '') })))] },
    { title: 'Кейіпкердің даму динамикасы', parts: [
      field('Шығарма басында', v('start')), field('Шығарма соңында', v('end')), field('Өзгеріс сипаты', v('change')),
      field('Себебі мен дәлелі', v('cause'))] },
    { title: 'Қорытынды интерпретация', parts: [field('Менің интерпретациям', v('interp')), field('Басқаша оқу мүмкіндігі', v('alt'))] },
  ];
  sections.forEach(sec => { sec.parts = sec.parts.filter(Boolean); });
  // Only filled sections are shown, numbered in the order they appear.
  return { hero: v('hero'), sections: sections.filter(sec => sec.parts.length).map((sec, i) => Object.assign(sec, { title: (i + 1) + '. ' + sec.title })) };
}

function labDocNodes() {
  const doc = labDoc();
  const title = t('labDocTitle') + (doc.hero ? ': ' + doc.hero : '');
  if (!doc.sections.length) return [h('h2', { class: 'lab-doc-title', text: title }), h('p', { class: 'lab-empty', text: t('labDocEmpty') })];
  return [h('h2', { class: 'lab-doc-title', text: title }),
    doc.sections.map(sec => [h('h3', { text: sec.title }), sec.parts.map(p => p.items
      ? [p.label ? h('h4', { text: p.label }) : null, h('ul', null, p.items.map(x => h('li', null, x.text, x.noEv ? h('span', { class: 'lab-noev', text: ' ' + t('labDocNoEv') }) : null)))]
      : [h('h4', { text: p.label }), h('p', { text: p.text })])]),
    h('p', { class: 'lab-empty', text: t('labDocNote') })];
}

function labDocText() {
  const doc = labDoc();
  const lines = [t('labDocTitle') + (doc.hero ? ': ' + doc.hero : ''), ''];
  if (!doc.sections.length) return lines.concat(t('labDocEmpty')).join('\n');
  doc.sections.forEach(sec => {
    lines.push(sec.title.toUpperCase());
    sec.parts.forEach(p => {
      if (p.items) {
        if (p.label) lines.push(p.label + ':');
        p.items.forEach(x => lines.push('• ' + x.text + (x.noEv ? ' ' + t('labDocNoEv') : '')));
      } else lines.push(p.label + ': ' + p.text);
    });
    lines.push('');
  });
  lines.push(t('labDocNote'));
  return lines.join('\n');
}

function labCopy(btn) {
  const text = labDocText();
  const manual = () => {
    const ta = h('textarea', { class: 'dlg-code', readonly: true, value: text, 'aria-label': t('labCopy') });
    openDialog(t('labCopy'), [h('p', { text: t('labCopyManual') }), ta], [{ label: t('close'), primary: true }]);
    ta.focus(); ta.select();
  };
  try {
    navigator.clipboard.writeText(text).then(() => showBanner('ok', t('labCopied')), manual);
  } catch (e) { manual(); }
}

function renderLabSummary() {
  return [
    h('div', { class: 'lab-actions' },
      h('button', { type: 'button', class: 'btn primary', text: t('labCopy'), onclick: e => labCopy(e.currentTarget) }),
      h('button', { type: 'button', class: 'btn', text: t('labPrint'), onclick: () => printOutputs('lab') })),
    h('p', { class: 'lab-step-intro', text: t('labPrintHint') }),
    h('div', { class: 'card lab-doc' }, labDocNodes()),
  ];
}

function renderLabFooter() {
  const i = lab.step, last = LAB_STEPS.length - 1;
  document.getElementById('footer').replaceChildren(
    h('button', { class: 'btn', type: 'button', disabled: i === 0, text: t('labPrev'), onclick: () => labGo(i - 1) }),
    h('div', { class: 'progress' }, h('span', { class: 'progress-label', text: t('labPos', { n: i + 1, total: LAB_STEPS.length }) })),
    i < last ? h('button', { class: 'btn primary', type: 'button', text: t(i === last - 1 ? 'labToSummary' : 'labNext'), onclick: () => labGo(i + 1) })
      : h('button', { class: 'btn primary', type: 'button', text: t('labPrint'), onclick: () => printOutputs('lab') }));
}

/* ==============================================================================
   PRINT — fills #print-area""")

# Help and cover mention the lab.
rep("      '«Балалар әдебиеті» қойындысында",
    "      '«Зертхана» қойындысында кейіпкер психологиясын кезең-кезеңімен талдап, нәтижені бір құжатқа жинайсыз. Оны көшіруге немесе PDF ретінде сақтауға болады.',\n"
    "      '«Балалар әдебиеті» қойындысында")
rep("    'Балалар әдебиеті: жас санатына",
    "    'Кейіпкер психологиясын талдау зертханасы: кезең-кезеңімен талдау, нәтижені көшіру және PDF',\n"
    "    'Балалар әдебиеті: жас санатына")

s = s.replace('      python3 shop.py saved.html kobem-talday.html         # «Сатып алу» (WhatsApp orders)',
              '      python3 shop.py saved.html shop.html                 # «Сатып алу» (WhatsApp orders)\n'
              '      python3 lab.py shop.html kobem-talday.html           # «Зертхана» (character psychology lab)')
open(out, 'w', encoding='utf8').write(s)
print('lab ->', out)
