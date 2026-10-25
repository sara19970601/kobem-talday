"""Lab, part 3: eight more analysis tools, a «Теориялық негіз / дереккөздер» step in every
tool, and a «Мектеп / Университет» level that adds university-only questions and makes the
AI tutor prompt stricter. The two existing tools keep their steps, answers and storage keys.
Usage: python3 -I labmore.py in.html out.html   (run after tutor.py)"""
import sys

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('labmore anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

# ---- CSS: ten tools as chips (a list on phones), level switch ----
rep('</style>\n</head>', r"""</style>
<style id="lab-more">
  /* LAB MORE — ten tools, level switch */
  .lab-tools { display: flex; flex-wrap: wrap; gap: 6px; }
  .lab-tool { padding: 6px 13px; border-radius: 999px; }
  .lab-tool b { font-size: 14px; font-weight: 600; }
  .lab-tool small { display: none; }
  .lab-tool-select { display: none; width: 100%; margin: 0 0 12px; font-weight: 600; }
  .lab-tool-hint { margin: -6px 0 6px; font-size: 13px; color: var(--ink-2); }
  .lab-level { display: inline-flex; align-items: center; gap: 8px; flex-wrap: wrap; font-size: 14px; }
  .lab-level-opts { display: inline-flex; padding: 3px; gap: 2px; border-radius: 10px; background: var(--surface-2); border: 1px solid var(--line); }
  .lab-level-opts button { border: 0; background: none; padding: 5px 12px; border-radius: 8px; font-weight: 600; color: var(--ink-2); }
  .lab-level-opts button[aria-pressed="true"] { background: var(--surface); color: var(--accent); box-shadow: var(--shadow-sm); }
  .lab-uni-tag { display: inline-block; margin-left: 6px; font-size: 11px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase;
    color: var(--accent); background: var(--accent-soft); border-radius: 5px; padding: 1px 6px; vertical-align: middle; }
  /* Desktop: «Сақталды» sits under the buttons instead of taking a place in the first row. */
  @media (min-width: 901px) {
    .save-status { position: absolute; right: 22px; top: 64px; min-width: 0; text-align: right; }
  }
  @media (max-width: 520px) {
    .lab-tools { display: none; }
    .lab-tool-select { display: block; }
  }
</style>
</head>""")

# ---- Strings ----
rep("  labToolsLabel: 'Талдау түрі',", r"""  labToolsLabel: 'Талдау түрі',
  labLevel: 'Деңгей:',
  labLevelSchool: 'Мектеп',
  labLevelUni: 'Университет',
  labUniTag: 'Университет',
  labStagePos: '{n}-кезең / {total}',
  labTheoryPos: 'Теориялық негіз',
  labCommonRules: [
    'Талдау тек сіз енгізген мәтін мен жауаптарыңызға сүйенеді. Мәтінде жоқ эпизодты немесе дәйексөзді ойдан қоспаңыз.',
    'Әр тұжырымды мәтіннен мысалмен бекітіңіз: әр кезеңде «Мәтіндік дәлел» өрісі бар.',
    'Мәтінге қатысы жоқ сұрақты бос қалдыра аласыз: бос жауап нәтижеге кірмейді.',
  ],
  labGenDocNote: 'Бұл талдау пайдаланушы енгізген мәтін мен жауаптарға сүйенеді.',""")
rep("      'Зертхананың әр кезеңінде «ЖИ тәлімгерінен кері байланыс алу» батырмасы бар.",
    "      'Зертханада 10 талдау құралы бар (кейіпкер психологиясы, сюжет пен композиция, нарратология, символдар мен мотивтер, уақыт пен кеңістік, мифопоэтика, салыстырмалы талдау, көркем тіл мен стиль, герменевтика, экокритика). «Мектеп / Университет» деңгейін таңдаңыз: университет деңгейінде теориялық сұрақтар қосылып, ЖИ тәлімгерінің талабы күшейеді. Әр құралдың соңында «Теориялық негіз / дереккөздер» кезеңі бар.',\n"
    "      'Зертхананың әр кезеңінде «ЖИ тәлімгерінен кері байланыс алу» батырмасы бар.")
rep("    'Зертхана: кейіпкер психологиясын және сюжет пен композицияны кезең-кезеңімен талдау, нәтижені көшіру және PDF',",
    "    'Зертхана: 10 талдау құралы (кейіпкер, сюжет, нарратология, символ, хронотоп, мифопоэтика т.б.), мектеп және университет деңгейі, ЖИ тәлімгеріне дайын сұрау',")

# ---- New tools (data), the theory step, and the registry ----
rep("const LAB_TOOLS = {\n", r"""/* Eight more tools: a preparation step, three or four stages of questions (each with a
   «Мәтіндік дәлел» field), the theory step and the summary. `labStage(n, id, title, questions)`
   numbers the questions; a question is a string or [text, hints]. */
function labPrepStep(fields) {
  return { id: 'prep', title: 'Шығарма мен үзінді', badge: '✎', pos: 'plotPrep', rules: true,
    intro: 'Талдайтын шығарманы және үзіндіні енгізіңіз. Барлық кезең осы мәтінге сүйенеді.',
    fields: fields || [
      { id: 'work', type: 'text', label: 'Шығарманың атауы', hints: ['Шығарманың толық атауын жазыңыз.'] },
      { id: 'author', type: 'text', label: 'Автордың аты-жөні', hints: ['Автордың аты-жөнін толық жазыңыз.'] },
      { id: 'excerpt', type: 'long', label: 'Талдайтын үзінді', cls: 'lab-excerpt',
        hints: ['Талдайтын үзіндіні немесе эпизодтарды осында қойыңыз.', 'Шығарма көлемді болса, негізгі эпизодтарды өз сөзіңізбен қысқаша жазып, маңызды сөйлемдерін тырнақшаға алыңыз.'] },
    ] };
}
function labStage(n, id, title, questions, note) {
  const qs = questions.map((q, i) => plotQ(id + (i + 1), (i + 1) + '. ' + (Array.isArray(q) ? q[0] : q), Array.isArray(q) ? q[1] : []));
  return { id: id, title: title, badge: String(n), stage: n, note: note,
    fields: qs.concat(plotEvidence(id + 'Ev', qs.map(f => f.id))) };
}
function labSummaryStep() {
  return { id: 'summary', title: 'Талдауды жинақтау', badge: '≡', pos: 'plotSummaryPos', summary: true,
    intro: 'Жауаптарыңыз бір құрылымды құжатқа жиналды. Бос өрістер құжатқа кірмейді.' };
}
/** «Теориялық негіз / дереккөздер»: in every tool, before the summary. */
function labTheoryStep() {
  return { id: 'theory', title: 'Теориялық негіз / дереккөздер', badge: 'Т', pos: 'labTheoryPos',
    intro: 'Талдауыңыз сүйенген ұғымдар мен ғылыми еңбектерді көрсетіңіз.',
    fields: [
      { id: 'uniFrame', type: 'long', level: 'uni', label: 'Теориялық тұрғы',
        hints: ['Талдауыңыз қандай әдебиеттану теориясына, ұғымына немесе ғалымның еңбегіне сүйенеді?', 'Бұл тұрғы шығарманы түсінуге не береді және оның шегі қандай?'] },
      { id: 'sources', type: 'long', label: 'Теориялық негіз және дереккөздер',
        hints: ['Талдауда сүйенген ұғымдарды, ғалымдарды және еңбектерді жазыңыз: автор, еңбек атауы, жыл, бет.', 'Тек өзіңіз оқыған дереккөзді көрсетіңіз; сілтемені ойдан құрастырмаңыз.'],
        hintsSchool: ['Мектеп деңгейінде бұл өріс міндетті емес: оқулықтағы, нұсқаулықтағы немесе сөздіктегі ұғымды атасаңыз жеткілікті.'],
        hintsUni: ['Университет деңгейінде кемінде бір-екі ғылыми дереккөзге сілтеме жасап, оның талдауыңызға қалай қатысты екенін түсіндіріңіз.'] },
    ] };
}
[LAB_HERO_STEPS, LAB_PLOT_STEPS].forEach(arr => arr.splice(arr.length - 1, 0, labTheoryStep()));

const LAB_MORE = [
  { id: 'narratology', label: 'Нарратология', hint: 'Баяндаушы, фокализация, баяндау тәртібі',
    title: 'Нарратологиялық талдау',
    intro: 'Шығармада оқиғаны кім, кімнің көзімен және қандай ретпен баяндайтынын, оқырманға ақпарат қалай берілетінін талдаңыз.',
    rule: 'Баяндаушыны автормен шатастырмаңыз: олардың көзқарасы сәйкес келмеуі мүмкін.',
    stages: [
      ['Баяндаушы', 'Баяндаушы', [
        ['Оқиғаны кім баяндайды: кейіпкер-баяндаушы ма, әлде оқиғаға қатыспайтын баяндаушы ма?', ['Баяндау қай жақтан жүреді: I жақ па, III жақ па?']],
        'Баяндаушы оқиға туралы қаншалықты көп біледі: бәрін біле ме, әлде білімі шектеулі ме?',
        'Баяндаушыға сенуге бола ма? Оның бағасы біржақты болуы мүмкін бе?',
        ['Баяндаушы мен автордың көзқарасы сәйкес келе ме, әлде алшақ па?', [], 'uni']]],
      ['Фокализация', 'Фокализация', [
        ['Оқиға кімнің көзімен, кімнің қабылдауы арқылы көрсетіледі?', ['«Кім сөйлейді?» және «Кім көреді?» деген екі сұрақты ажыратыңыз.']],
        'Фокализация шығарма бойы ауыса ма? Қай тұста және не үшін?',
        'Кейіпкердің ішкі ойы мен сезімі қаншалықты ашық беріледі (ішкі монолог, сана ағымы)?',
        'Кімнің көзқарасы көрсетілмей қалады және бұл оқырманға қалай әсер етеді?']],
      ['Баяндау тәртібі және ақпарат', 'Баяндау тәртібі және оқырманға ақпарат беру', [
        'Оқиғалар қандай ретпен баяндалады: хронологиялық па, әлде ретроспекция немесе алдын ала ишара бар ма?',
        'Баяндау жылдамдығы қалай өзгереді: қай оқиға ұзақ суреттеледі, қайсысы бір сөйлеммен өтеді?',
        'Оқырман қай ақпаратты кейіпкерден бұрын не кейін біледі? Автор нені жасырып, нені кейін ашады?',
        'Баяндау тәсілі шығарманың мағынасына және оқырман әсеріне қалай ықпал етеді?']],
    ] },
  { id: 'symbols', label: 'Символдар мен мотивтер', hint: 'Қайталанатын бейнелер, контекст, ықтимал мағыналар',
    title: 'Символдар мен мотивтерді талдау',
    intro: 'Шығармада қайталанатын бейнелерді тауып, олардың мәтіндегі контексін және ықтимал мағыналарын талдаңыз.',
    rule: 'Символдың мағынасын кесімді түрде бекітпеңіз: мәтін бірнеше түсіндіруге жол беруі мүмкін. Әр мағынаны контекспен дәлелдеңіз.',
    stages: [
      ['Бейнені табу', 'Қайталанатын бейнелер', [
        'Шығармада қандай бейне, зат, түс, дыбыс не жағдай қайталанып келеді?',
        'Ол қай эпизодтарда кездеседі? Әр жолы қандай жағдайда пайда болады?',
        'Бұл бейне тура мағынасында ғана қолданыла ма, әлде қосымша мағына үстей ме?']],
      ['Контекст', 'Контекст', [
        'Бейненің мағынасы мәтіннің өз ішінде қалай өзгереді (басында, ортасында, соңында)?',
        'Ол қай кейіпкермен, қай тақырыппен байланысты?',
        'Бұл бейненің мәдени, фольклорлық немесе тарихи мәні бар ма? Мәтін оны қалай қолданады?']],
      ['Ықтимал мағыналар', 'Ықтимал мағыналар', [
        'Бұл бейнені қалай түсінуге болады? Бірнеше ықтимал мағынаны атаңыз.',
        'Қай түсіндіру мәтінмен көбірек дәлелденеді және неге?',
        'Символды алып тастасақ, шығарманың мағынасы қалай өзгерер еді?',
        ['Мотив пен символдың айырмасын осы шығарма мысалында қалай көрсетер едіңіз?', [], 'uni']]],
    ] },
  { id: 'chronotope', label: 'Уақыт пен кеңістік', hint: 'Хронотоп, кеңістіктің қызметі, уақыт құрылымы',
    title: 'Уақыт пен кеңістікті талдау',
    intro: 'Шығармадағы көркем уақыт пен кеңістіктің құрылымын және олардың біртұтастығын (хронотопты) талдаңыз.',
    rule: 'Көркем уақыт пен кеңістік нақты уақыт пен жерден өзгеше: автор оларды мағына үшін қалай құрғанына назар аударыңыз.',
    stages: [
      ['Көркем уақыт', 'Көркем уақыт', [
        'Оқиға қай уақытта өтеді (тарихи кезең, жыл мезгілі, тәулік уақыты)?',
        'Шығармадағы оқиға қанша уақытты қамтиды және ол қалай беріледі?',
        'Уақыт қалай ағады: бірқалыпты ма, баяулай ма, үзіле ме, өткенге оралады ма?']],
      ['Көркем кеңістік', 'Көркем кеңістік', [
        'Оқиға қай жерлерде өтеді? Негізгі мекендерді атаңыз.',
        'Кеңістік қалай қарама-қарсы қойылады (үй/дала, ауыл/қала, ішкі/сыртқы, жабық/ашық)?',
        'Кейіпкер кеңістікте қалай қозғалады және бұл оның күйін қалай білдіреді?',
        'Пейзаж немесе интерьер кейіпкердің ішкі әлемімен байланыса ма?']],
      ['Хронотоп', 'Хронотоп', [
        'Шығармада уақыт пен кеңістік қай жерде біртұтас бейне құрайды (жол, табалдырық, үй, кездесу орны т.б.)?',
        'Бұл хронотоп шығарманың тартысымен немесе идеясымен қалай байланысты?',
        'Уақыт пен кеңістік құрылымы оқырманның шығарманы қабылдауына қалай әсер етеді?',
        ['Бұл хронотопты М. Бахтин сипаттаған хронотоп түрлерімен (жол, табалдырық, идиллия т.б.) салыстырсақ, не байқалады?', [], 'uni']]],
    ] },
  { id: 'mythopoetics', label: 'Мифопоэтика', hint: 'Мифтік үлгілер, фольклорлық мотивтер, олардың өзгеруі',
    title: 'Мифопоэтикалық талдау',
    intro: 'Шығармадағы мифтік үлгілерді, фольклорлық мотивтерді және автордың оларды қалай өзгерткенін талдаңыз.',
    rule: 'Мифтік үлгіні мәтінге таңбаламаңыз: ұқсастық мәтіндегі нақты белгілермен дәлелденсе ғана талдауға негіз болады.',
    stages: [
      ['Мифтік және фольклорлық негіз', 'Мифтік және фольклорлық негіз', [
        'Шығармада қандай миф, аңыз, ертегі не эпос үлгісі (сюжет, кейіпкер, мотив) байқалады?',
        'Ол мәтінде қалай көрінеді: тікелей аталады ма, әлде жасырын ишара ма?',
        'Қандай фольклорлық мотивтер кездеседі (жол, сынақ, қайта туу, басқа әлемге сапар, тотем т.б.)?']],
      ['Архетиптер мен мифтік кеңістік', 'Архетиптер мен мифтік кеңістік', [
        'Кейіпкерлерде қандай тұрақты үлгілер (батыр, дана қария, жол көрсетуші, айлакер т.б.) бар?',
        'Мифтік кеңістік пен уақыттың белгілері бар ма (әлемдер шекарасы, бастапқы уақыт, киелі орын)?',
        'Табиғат құбылыстары немесе жануарлар мифтік мағына үстей ме?']],
      ['Өзгеріс және мағына', 'Мифтік үлгінің өзгеруі және мағынасы', [
        'Автор мифтік үлгіні қалай өзгертеді: сақтай ма, қайта түсіндіре ме, әлде теріске шығара ма?',
        'Бұл өзгерістің шығарма идеясы үшін мәні қандай?',
        'Мифопоэтикалық оқу шығарманың қандай қырын ашады, ал нені түсіндіре алмайды?',
        ['Талдауыңыз мифопоэтиканың қай тұжырымдамасына (мысалы, архетиптер, мифтік кеңістік модельдері) сүйенеді?', [], 'uni']]],
    ] },
  { id: 'comparative', label: 'Салыстырмалы талдау', hint: 'Ұқсастықтар, айырмашылықтар, мәтіндік негіздер',
    title: 'Салыстырмалы талдау',
    intro: 'Екі шығарманы нақты өлшемдер бойынша салыстырып, ұқсастықтары мен айырмашылықтарын мәтінмен дәлелдеңіз.',
    rule: 'Әр ұқсастық пен айырмашылықты екі шығармадан да мысалмен дәлелдеңіз.',
    prep: [
      { id: 'work', type: 'text', label: '1-шығарманың атауы' },
      { id: 'author', type: 'text', label: '1-шығарманың авторы' },
      { id: 'work2', type: 'text', label: '2-шығарманың атауы' },
      { id: 'author2', type: 'text', label: '2-шығарманың авторы' },
      { id: 'excerpt', type: 'long', label: '1-шығармадан үзінді', cls: 'lab-excerpt', hints: ['Салыстыратын үзіндіні немесе эпизодтарды қойыңыз.'] },
      { id: 'excerpt2', type: 'long', label: '2-шығармадан үзінді', cls: 'lab-excerpt', hints: ['Салыстыратын үзіндіні немесе эпизодтарды қойыңыз.'] },
    ],
    stages: [
      ['Салыстыру негізі', 'Салыстыру негізі', [
        'Неліктен дәл осы екі шығарманы салыстыру мағыналы?',
        'Салыстырудың өлшемдері қандай (тақырып, кейіпкер, сюжет, стиль, баяндау)?',
        ['Шығармалар арасында тарихи, жанрлық немесе генетикалық байланыс бар ма (әсер, аударма, ортақ дерек)?', [], 'uni']]],
      ['Ұқсастықтар', 'Ұқсастықтар', [
        'Екі шығармада қандай ұқсас тақырып, мотив не жағдай бар?',
        'Кейіпкерлерде немесе тартыста қандай ұқсастық байқалады?',
        'Бұл ұқсастық кездейсоқ па, әлде ортақ дәстүрден, дәуірден туындай ма?']],
      ['Айырмашылықтар', 'Айырмашылықтар', [
        'Ұқсас материалды авторлар қалай әртүрлі шешеді?',
        'Баяндау, стиль немесе композиция тұрғысынан қандай айырма бар?',
        'Бұл айырмашылық әр шығарманың мағынасына қалай әсер етеді?']],
      ['Қорытынды', 'Қорытынды', [
        'Салыстыру әр шығарманың қандай жаңа қырын ашты?',
        'Салыстырудан шығатын негізгі тұжырым қандай?']],
    ] },
  { id: 'style', label: 'Көркем тіл мен стиль', hint: 'Тілдік тәсілдер, олардың қызметі, мағына',
    title: 'Көркем тіл мен стильді талдау',
    intro: 'Шығармадағы тілдік тәсілдерді тауып, олардың қызметін және мағына қалыптастыруын талдаңыз.',
    rule: 'Тәсілді тек атап шықпаңыз: әр мысалдың мәтінде қандай қызмет атқаратынын түсіндіріңіз.',
    stages: [
      ['Тілдік тәсілдер', 'Тілдік тәсілдер', [
        'Мәтінде қандай троптар (теңеу, эпитет, метафора, кейіптеу т.б.) кездеседі? Мысалдарын келтіріңіз.',
        'Қандай стилистикалық фигуралар (қайталау, риторикалық сұрақ, қарсылау, инверсия т.б.) бар?',
        'Сөздік қорда ерекше қабаттар бар ма (көнерген сөз, диалект, кірме сөз, сөйлеу тілі)?']],
      ['Тәсілдердің қызметі', 'Тәсілдердің қызметі', [
        'Бұл тәсілдер нені суреттеуге, кімнің бейнесін ашуға қызмет етеді?',
        'Сөйлем құрылымы мен ырғағы (ұзын не қысқа сөйлемдер, үзіктік) қандай әсер береді?',
        'Кейіпкерлердің сөйлеу мәнері олардың мінезін қалай көрсетеді?']],
      ['Стиль және мағына', 'Стиль және мағына', [
        'Автор стилінің негізгі ерекшелігін қалай сипаттар едіңіз?',
        'Тіл мен стиль шығарманың көңіл-күйі мен идеясын қалай қалыптастырады?',
        'Бір үзіндіні қарапайым тілмен мазмұндасақ, не жоғалады?',
        ['Автор стилін дәуірдің немесе әдеби бағыттың стильдік ерекшеліктерімен қалай байланыстырар едіңіз?', [], 'uni']]],
    ] },
  { id: 'hermeneutics', label: 'Герменевтика', hint: 'Түсіндіру, контекст, бөлік пен тұтастың байланысы',
    title: 'Герменевтикалық талдау',
    intro: 'Шығарманы түсіну жолыңызды бақылап, бөлік пен тұтастың, мәтін мен контекстің байланысы арқылы түсіндіріңіз.',
    rule: 'Герменевтикалық шеңбер: бөлікті тұтас арқылы, тұтасты бөлік арқылы түсінеміз. Алғашқы түсінікті мәтінмен тексеріп, қажет болса өзгертіңіз.',
    stages: [
      ['Алғашқы түсінік', 'Алғашқы түсінік', [
        'Шығарманы алғаш оқығанда қандай түсінік қалыптасты? Оны бір-екі сөйлеммен жазыңыз.',
        'Қай жерлер түсініксіз, екіұшты немесе таңғаларлық болып көрінді?',
        'Сіздің түсінігіңізге қандай алдын ала білім, күту немесе тәжірибе әсер етті?']],
      ['Бөлік пен тұтас', 'Бөлік пен тұтас', [
        'Бір маңызды эпизод (сөз, бейне) бүкіл шығарманы түсінуге қалай әсер етеді?',
        'Тұтас шығарманы түсіну сол эпизодтың мағынасын қалай өзгертеді?',
        'Алғашқы түсінігіңіздің қай тұсы мәтінмен расталды, қайсысы өзгерді?']],
      ['Контекст', 'Контекст', [
        'Шығарма жазылған тарихи-мәдени контекст оның мағынасына қалай әсер етеді?',
        'Автордың шығармашылығы немесе дәуірдің идеялары мәтінде қалай көрінеді?',
        'Бүгінгі оқырман үшін шығарманың мағынасы қалай өзгереді?']],
      ['Түсіндіру', 'Түсіндіру', [
        'Шығарманы түсіндірудің сіз ұсынатын нұсқасы қандай?',
        'Қандай балама түсіндірулер мүмкін және олар неге сүйенеді?',
        'Сіздің түсіндіруіңіз мәтінмен қаншалықты дәлелденеді?',
        ['Түсіндіруіңіз герменевтиканың қай тұжырымына (мысалы, Х.-Г. Гадамер, П. Рикёр) жақын және неге?', [], 'uni']]],
    ] },
  { id: 'ecocriticism', label: 'Экокритика', hint: 'Адам, табиғат және адамнан тыс әлем',
    title: 'Экокритикалық талдау',
    intro: 'Шығармада адамның, табиғаттың және адамнан тыс әлемнің қалай бейнеленетінін және олардың байланысын талдаңыз.',
    rule: 'Шығармаға қазіргі экологиялық ұғымдарды таңбаламаңыз: тұжырымды мәтіндегі табиғат пен адам бейнесіне сүйеніп жасаңыз.',
    stages: [
      ['Табиғат бейнесі', 'Табиғат бейнесі', [
        'Шығармада табиғат қалай бейнеленеді: оқиғаның фоны ма, әлде әрекет етуші күш пе?',
        'Қандай жануарлар, өсімдіктер, табиғат құбылыстары маңызды орын алады?',
        'Табиғат кімнің көзімен суреттеледі?']],
      ['Адам мен табиғат', 'Адам мен табиғаттың қарым-қатынасы', [
        'Адам мен табиғаттың қарым-қатынасы қандай: үйлесім, тұтыну, күрес, қорғау?',
        'Кейіпкерлердің табиғатқа көзқарасы қалай ерекшеленеді?',
        'Жануар не табиғат құбылысы өз «даусы» бар субъект ретінде көрсетіле ме?']],
      ['Мағына және бүгінгі оқу', 'Мағына және бүгінгі оқу', [
        'Автордың табиғатқа қатысты ұстанымы мәтінде қалай көрінеді?',
        'Шығарма табиғатты пайдалану, жою немесе тепе-теңдік мәселелерін қалай көтереді?',
        'Экокритикалық оқу шығарманың қандай жаңа мағынасын ашады?',
        ['Талдауыңызды экокритиканың қай ұғымымен (мысалы, антропоцентризм, адамнан тыс әлем) байланыстырасыз?', [], 'uni']]],
    ] },
];
LAB_MORE.forEach(m => {
  m.steps = [labPrepStep(m.prep)].concat(m.stages.map((sg, i) => {
    const st = labStage(i + 1, m.id.slice(0, 3) + (i + 1) + 'q', sg[0], sg[2].map(q => Array.isArray(q) ? [q[0], q[1]] : q));
    st.docTitle = sg[1];
    sg[2].forEach((q, qi) => { if (Array.isArray(q) && q[2] === 'uni') st.fields[qi].level = 'uni'; });
    return st;
  }), labTheoryStep(), labSummaryStep());
});

const LAB_TOOLS = {
""")
rep("""    rules: 'plotRules', diagnosis: false, doc: () => labPlotDoc() },
};""", """    rules: 'plotRules', diagnosis: false, doc: () => labPlotDoc() },
};
LAB_MORE.forEach(m => {
  LAB_TOOLS[m.id] = { key: 'kobem-talday:lab-' + m.id, steps: m.steps, labelText: m.label, hintText: m.hint, titleText: m.title,
    introText: m.intro, rulesList: STRINGS.labCommonRules.concat(m.rule), diagnosis: false, doc: () => labGenericDoc(m) };
});
/** Tool texts: the first two tools name STRINGS keys, the others carry the text itself. */
function toolText(tool, kind) { return tool[kind + 'Text'] || t(tool[kind]); }""")

# Use toolText everywhere a tool's label / hint / title / intro is shown.
rep("    }, h('b', { text: t(LAB_TOOLS[id].label) }), h('small', { text: t(LAB_TOOLS[id].hint) })))),\n"
    "    h('h2', { class: 'ws-title', text: t(LAB_TOOLS[labTool].title) }),\n"
    "    h('p', { class: 'k-intro', text: t(LAB_TOOLS[labTool].intro) }),",
    "    }, h('b', { text: toolText(LAB_TOOLS[id], 'label') }), h('small', { text: toolText(LAB_TOOLS[id], 'hint') })))),\n"
    "    h('select', { class: 'lab-tool-select', 'aria-label': t('labToolsLabel'), value: labTool, onchange: e => labSwitch(e.target.value) },\n"
    "      Object.keys(LAB_TOOLS).map(id => h('option', { value: id }, toolText(LAB_TOOLS[id], 'label')))),\n"
    "    h('h2', { class: 'ws-title', text: toolText(LAB_TOOLS[labTool], 'title') }),\n"
    "    h('p', { class: 'lab-tool-hint', text: toolText(LAB_TOOLS[labTool], 'hint') }),\n"
    "    h('p', { class: 'k-intro', text: toolText(LAB_TOOLS[labTool], 'intro') }),")
rep("      h('ul', null, STRINGS[LAB_TOOLS[labTool].rules].map(x => h('li', { text: x })))) : null,",
    "      h('ul', null, (LAB_TOOLS[labTool].rulesList || STRINGS[LAB_TOOLS[labTool].rules]).map(x => h('li', { text: x })))) : null,")
rep("    h('h2', { text: t(LAB_TOOLS[labTool].label) }),\n    h('ul', { class: 'steps', id: 'lab-nav' }",
    "    h('h2', { text: toolText(LAB_TOOLS[labTool], 'label') }),\n    h('ul', { class: 'steps', id: 'lab-nav' }")
rep("  p.push('ТАЛДАУ ТҮРІ: ' + t(tool.label) +", "  p.push('ТАЛДАУ ТҮРІ: ' + toolText(tool, 'label') +")

# Stage position for any number of stages.
rep("  if (st.stage) return t('plotStagePos', { n: st.stage });",
    "  if (st.stage) return t('labStagePos', { n: st.stage, total: LAB_STEPS.filter(x => x.stage).length });")

# ---- Level: «Мектеп / Университет» ----
rep("const labStates = {};", """const LAB_LEVEL_KEY = 'kobem-talday:lab-level';
let labLevel = (() => { try { return labConsent && window.localStorage.getItem(LAB_LEVEL_KEY) === 'uni' ? 'uni' : 'school'; } catch (e) { return 'school'; } })();
function setLabLevel(level) {
  labLevel = level;
  try { if (labConsent) window.localStorage.setItem(LAB_LEVEL_KEY, level); } catch (e) { /* storage blocked */ }
  renderMain(); renderFooter();
}
/** University-only questions are shown (and sent to the tutor) at the university level only. */
function labFieldVisible(f) { return f.level !== 'uni' || labLevel === 'uni'; }
function labFieldHints(f) { return labHints((f.hints || []).concat(labLevel === 'uni' ? f.hintsUni || [] : f.hintsSchool || [])); }
const labStates = {};""")
rep("""      window.localStorage.removeItem(LAB_TOOL_KEY);""", """      window.localStorage.removeItem(LAB_TOOL_KEY);
      window.localStorage.removeItem(LAB_LEVEL_KEY);""")
rep("""      labSaveNow();
    } else {""", """      labSaveNow();
      window.localStorage.setItem(LAB_LEVEL_KEY, labLevel);
    } else {""")
rep("""    h('div', { class: 'lab-bar' },""", """    h('div', { class: 'lab-bar' },
      h('div', { class: 'lab-level', role: 'group', 'aria-label': t('labLevel') }, h('span', { text: t('labLevel') }),
        h('span', { class: 'lab-level-opts' }, [['school', 'labLevelSchool'], ['uni', 'labLevelUni']].map(([id, key]) => h('button', {
          type: 'button', 'aria-pressed': labLevel === id ? 'true' : 'false', text: t(key), onclick: () => { if (labLevel !== id) setLabLevel(id); },
        })))),""")
rep("    st.summary ? renderLabSummary() : st.fields.map(f => renderLabField(f, evWarns)),",
    "    st.summary ? renderLabSummary() : st.fields.filter(labFieldVisible).map(f => renderLabField(f, evWarns)),")
rep("""  const label = h('label', { class: 'field-label', for: id, text: f.label });
  if (f.type === 'choice') {""", """  const label = h('label', { class: 'field-label', for: id }, f.label, f.level === 'uni' ? h('span', { class: 'lab-uni-tag', text: t('labUniTag') }) : null);
  if (f.type === 'choice') {""")
rep("  return h('div', { class: 'card' + (f.cls ? ' ' + f.cls : '') }, label, labHints(f.hints),",
    "  return h('div', { class: 'card' + (f.cls ? ' ' + f.cls : '') }, label, labFieldHints(f),")
rep("  (st.fields || []).forEach(f => {\n    const v = lab.data[f.id];",
    "  (st.fields || []).filter(labFieldVisible).forEach(f => {\n    const v = lab.data[f.id];")

# Tutor: level-aware requirements, and the context of every tool.
rep("""  p.push('ТАЛДАУ ТҮРІ: ' + toolText(tool, 'label') +""", """  p.push(labLevel === 'uni'
    ? 'ДЕҢГЕЙ: университет (филология студенті). Талапты күшейт: әдебиеттану терминдерінің дәл қолданылуын, тұжырымның теориялық негізделуін, балама интерпретацияларға сыни қатынасты және ғылыми дереккөздерге сүйенуді тексер. Академиялық стильге назар аудар. Пайдаланушы көрсеткен дереккөздің мазмұнын білмесең, оны растама; жаңа дереккөз ұсынсаң, библиографиялық сілтемені ойдан құрастырма — нақты екеніне сенімді болмасаң, тек ұғымды немесе ғалымның атын бағыт ретінде ата.'
    : 'ДЕҢГЕЙ: мектеп (5–11 сынып оқушысы). Тілің қарапайым әрі түсінікті болсын; терминді қолдансаң, оны түсіндір; бір кері байланыста тым көп талап қойма.');
  p.push('ТАЛДАУ ТҮРІ: ' + toolText(tool, 'label') +""")
rep("""  const work = d.work || d.plWork, author = d.author || d.plAuthor;
  if (filled(work)) out.push('Шығарма: «' + work.trim().replace(/^«|»$/g, '') + '»');
  if (filled(author)) out.push('Автор: ' + author.trim());
  if (filled(d.hero)) out.push('Талданатын кейіпкер: ' + d.hero.trim());
  if (filled(d.plExcerpt)) out.push('Пайдаланушы енгізген үзінді (дәлелдерді осы мәтінмен ғана салыстыр):\\n-----\\n' + d.plExcerpt.trim() + '\\n-----');
  else out.push(""", """  const work = d.work || d.plWork, author = d.author || d.plAuthor;
  const two = filled(d.work2);
  if (filled(work)) out.push((two ? '1-шығарма' : 'Шығарма') + ': «' + work.trim().replace(/^«|»$/g, '') + '»');
  if (filled(author)) out.push((two ? '1-шығарманың авторы' : 'Автор') + ': ' + author.trim());
  if (two) out.push('2-шығарма: «' + d.work2.trim().replace(/^«|»$/g, '') + '»');
  if (filled(d.author2)) out.push('2-шығарманың авторы: ' + d.author2.trim());
  if (filled(d.hero)) out.push('Талданатын кейіпкер: ' + d.hero.trim());
  const excerpts = [[d.plExcerpt || d.excerpt, two ? '1-шығармадан үзінді' : 'Пайдаланушы енгізген үзінді'], [d.excerpt2, '2-шығармадан үзінді']]
    .filter(x => filled(x[0]));
  excerpts.forEach(x => out.push(x[1] + ' (дәлелдерді осы мәтінмен ғана салыстыр):\\n-----\\n' + x[0].trim() + '\\n-----'));
  if (!excerpts.length) out.push(""")
rep("""  return LAB_STEPS.filter(st => st.fields).map(st => '## ' + st.title + '\\n' + tutorStepText(st)).join('\\n\\n');""",
    """  return LAB_STEPS.filter(st => st.fields && st.fields.some(labFieldVisible)).map(st => '## ' + st.title + '\\n' + tutorStepText(st)).join('\\n\\n');""")

# ---- Documents: theory section in the two first tools, a generic document for the others ----
THEORY = "    { title: 'Теориялық негіз және дереккөздер', parts: [field('Теориялық тұрғы', v('uniFrame')), field('Дереккөздер', v('sources'))] },\n"
rep("    { title: 'Қорытынды интерпретация', parts: [field('Менің интерпретациям', v('interp')), field('Басқаша оқу мүмкіндігі', v('alt'))] },\n",
    "    { title: 'Қорытынды интерпретация', parts: [field('Менің интерпретациям', v('interp')), field('Басқаша оқу мүмкіндігі', v('alt'))] },\n" + THEORY)
rep("    { title: 'Қорытынды интерпретация', parts: qa(4) },\n",
    "    { title: 'Қорытынды интерпретация', parts: qa(4) },\n" + THEORY.replace("v('sources'))] },", "v('sources'))].filter(Boolean) },"))
rep("""/** «Сюжет пен композиция»: answers grouped""", """/** Tools 3–10: one section per stage (questions as labels), the text evidence, the theory. */
function labGenericDoc(m) {
  const d = lab.data;
  const v = x => (d[x] || '').trim();
  const field = (label, text) => filled(text) ? { label: label, text: text } : null;
  const stages = m.steps.filter(st => st.stage);
  const qa = st => st.fields.filter(f => !f.evidenceFor && filled(d[f.id])).map(f => ({ label: f.label.replace(/^\\d+\\.\\s*/, ''), text: v(f.id) }));
  const two = filled(v('work2'));
  const name = x => '«' + x.replace(/^«|»$/g, '') + '»';
  const sections = stages.map(st => ({ title: st.docTitle || st.title, parts: qa(st) })).concat([
    { title: 'Мәтіндік дәлелдер', parts: [
      field(two ? '1-шығармадан үзінді' : 'Талданған үзінді', v('excerpt')), field('2-шығармадан үзінді', v('excerpt2'))]
      .concat(stages.map(st => field(st.title + ' бойынша', v(st.fields[st.fields.length - 1].id)))).filter(Boolean) },
    { title: 'Теориялық негіз және дереккөздер', parts: [field('Теориялық тұрғы', v('uniFrame')), field('Дереккөздер', v('sources'))].filter(Boolean) },
  ]);
  const works = [[v('work'), v('author')], [v('work2'), v('author2')]].filter(x => x[0]);
  return {
    title: m.title + (works.length === 1 ? ': ' + name(works[0][0]) : ''),
    meta: works.length > 1 ? works.map(x => name(x[0]) + (x[1] ? ' (' + x[1] + ')' : '')).join(' · ') : (v('author') ? 'Автор: ' + v('author') : ''),
    note: t('labGenDocNote'),
    sections: sections.filter(sec => sec.parts.length).map((sec, i) => Object.assign(sec, { title: (i + 1) + '. ' + sec.title })),
  };
}

/** «Сюжет пен композиция»: answers grouped""")

s = s.replace('      python3 tutor.py preview.html kobem-talday.html      # «ЖИ тәлімгері» prompt (no AI call)',
              '      python3 tutor.py preview.html tutor.html             # «ЖИ тәлімгері» prompt (no AI call)\n'
              '      python3 labmore.py tutor.html kobem-talday.html      # 8 more lab tools, theory step, school/university level')
open(out, 'w', encoding='utf8').write(s)
print('labmore ->', out)
