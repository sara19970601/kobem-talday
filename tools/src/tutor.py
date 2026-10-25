"""AI tutor prompt: «ЖИ тәлімгерінен кері байланыс алу» in every lab tool.
The site calls no AI service. The button builds one ready prompt (the user's answers plus
the tutor's pedagogical rules and the feedback structure) for the user to copy into an
AI assistant of their own choice. For a revised answer the prompt carries the previous
version too, so the assistant can compare them.
Usage: python3 -I tutor.py in.html out.html   (run after preview.py)"""
import sys

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('tutor anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

# ---- CSS ----
rep('</style>\n</head>', r"""</style>
<style id="tutor">
  /* TUTOR — «ЖИ тәлімгері» card and dialog */
  .tutor-card { display: flex; flex-wrap: wrap; gap: 10px 16px; align-items: center; justify-content: space-between;
    margin: 4px 0 14px; padding: 14px 16px; border-radius: 14px; border: 1px solid var(--accent); background: var(--accent-soft); }
  .tutor-card div { flex: 1 1 260px; }
  .tutor-card h3 { margin: 0 0 3px; font-size: 15.5px; color: var(--accent); }
  .tutor-card p { margin: 0; font-size: 13.5px; color: var(--ink-2); line-height: 1.45; }
  .dlg.tutor-dlg { max-width: 760px; width: calc(100% - 32px); }
  .tutor-steps { margin: 0 0 10px; padding-left: 20px; }
  .tutor-steps li { margin-bottom: 4px; line-height: 1.45; }
  .tutor-modes { display: grid; gap: 6px; margin: 0 0 10px; padding: 10px 12px; border: 1px solid var(--line); border-radius: 12px; background: var(--surface-2); }
  .tutor-modes label { display: flex; gap: 8px; align-items: flex-start; font-size: 14px; line-height: 1.4; cursor: pointer; }
  .tutor-modes input { margin-top: 3px; }
  .tutor-modes input:disabled + span { color: var(--ink-2); }
  .tutor-dlg textarea.dlg-code { min-height: 220px; font-size: 12.5px; }
  .tutor-links { display: flex; flex-wrap: wrap; gap: 6px 12px; margin: 8px 0 0; font-size: 13.5px; }
  .tutor-note { margin: 8px 0 0; font-size: 13px; color: var(--ink-2); }
  @media (max-width: 520px) { .tutor-card .btn { width: 100%; } }
  @media print { .tutor-card { display: none; } }
</style>
</head>""")

# ---- Strings ----
rep("  labToolsLabel: 'Талдау түрі',", r"""  labToolsLabel: 'Талдау түрі',
  tutorTitle: 'ЖИ тәлімгері',
  tutorCardText: 'Осы кезеңдегі жауаптарыңызға кері байланыс алу үшін дайын сұрауды көшіріп, өзіңіз таңдаған ЖИ-ге қойыңыз.',
  tutorCardFinal: 'Бүкіл талдауға қорытынды кері байланыс алу үшін дайын сұрауды көшіріп, өзіңіз таңдаған ЖИ-ге қойыңыз.',
  tutorBtn: 'ЖИ тәлімгерінен кері байланыс алу',
  tutorDlgTitle: 'ЖИ тәлімгері: кері байланыс сұрауы',
  tutorSteps: [
    '«Сұрауды көшіру» батырмасын басыңыз.',
    'Өзіңіз таңдаған ЖИ көмекшісін (ChatGPT, Claude, Gemini т.б.) ашып, көшірілген мәтінді қойып жіберіңіз.',
    'Кері байланысты оқып, жауабыңызды осы сайтта жетілдіріңіз.',
    'Жетілдірілген нұсқаны тексерту үшін осы батырманы қайта басып, «Қайта өңделген нұсқа» түрін таңдаңыз: ЖИ оны бұрынғы нұсқамен салыстырады.',
  ],
  tutorModeFirst: 'Кері байланыс: қазіргі жауаптарыма',
  tutorModeRevision: 'Қайта өңделген нұсқа: бұрынғы нұсқаммен салыстыру',
  tutorNoPrevious: '(алдымен бір рет кері байланыс сұрауын көшіріңіз)',
  tutorSame: '(жауап әлі өзгерген жоқ)',
  tutorCopy: 'Сұрауды көшіру',
  tutorPrivacy: 'Сайт бұл мәтінді ешқайда жібермейді: оны ЖИ-ге жіберу-жібермеуді өзіңіз шешесіз. Сұрауға оқушының аты-жөнін немесе басқа жеке деректерін қоспаңыз.',
  tutorOpen: 'ЖИ көмекшісін ашу:',""")
rep("      '«Балалар әдебиеті» қойындысында",
    "      'Зертхананың әр кезеңінде «ЖИ тәлімгерінен кері байланыс алу» батырмасы бар. Ол жауаптарыңызды педагогикалық нұсқаулармен бірге дайын сұрауға жинайды; оны өзіңіз таңдаған ЖИ-ге қойып, кері байланыс аласыз. Сайт мәтінді ешқайда жібермейді.',\n"
    "      '«Балалар әдебиеті» қойындысында")

# Keep the copied versions (for «бұрынғы нұсқамен салыстыру») with the tool's answers.
rep("  return { version: 1, step: 0, data: data };", "  return { version: 1, step: 0, data: data, tutor: {} };")
rep("""  const step = Number(raw.step);
  out.step = Number.isInteger(step)""", """  if (isObj(raw.tutor)) Object.keys(raw.tutor).slice(0, 40).forEach(k => {
    if (typeof raw.tutor[k] === 'string') out.tutor[k] = raw.tutor[k].slice(0, 200000);
  });
  const step = Number(raw.step);
  out.step = Number.isInteger(step)""")

# ---- Prompt building and the dialog ----
rep("""function labDocNodes() {""", r"""/* ==============================================================================
   TUTOR — «ЖИ тәлімгері». No AI service is called: the prompt is copied by the user.
   TUTOR_FOCUS: what the feedback should look at in each kind of analysis. Lab tools use
   their own id; the other kinds are ready for tools added later.
   ============================================================================== */
const TUTOR_FOCUS = {
  hero: 'кейіпкер психологиясы: мінез, мотив, ішкі қайшылық, даму динамикасы. Кейіпкерге клиникалық диагноз қойма; мақсат, мотив және эмоцияны бөлек ұғым ретінде қара; кейіпкердің өзгермеуі де маңызды нәтиже болуы мүмкін.',
  plot: 'сюжет пен композиция: оқиғалар байланысы, тартыс, шарықтау шегі, композициялық шешім. Сюжетті (оқиғалар тізбегі) композициядан (бөліктердің орналасуы мен байланысы) ажырат.',
  narratology: 'нарратология: баяндаушы, фокализация, баяндау тәртібі және оқырманға ақпарат беру.',
  symbols: 'символдар мен мотивтер: қайталанатын бейнелер, контекст және ықтимал мағыналар.',
  chronotope: 'уақыт пен кеңістік: хронотоп, кеңістіктің қызметі және уақыт құрылымы.',
  mythopoetics: 'мифопоэтика: мифтік үлгілер, фольклорлық мотивтер және олардың көркем шығармада өзгеруі.',
  comparative: 'салыстырмалы талдау: ұқсастықтар, айырмашылықтар және олардың мәтіндік негіздері.',
  style: 'көркем тіл мен стиль: тілдік тәсілдер, олардың қызметі және мағына қалыптастыруы.',
  hermeneutics: 'герменевтика: түсіндіру, контекст, тұтас мәтін мен оның бөліктерінің байланысы.',
  ecocriticism: 'экокритика: адам, табиғат және адамнан тыс әлемнің көркем репрезентациясы.',
};

const TUTOR_RULES = [
  'Пайдаланушының орнына тапсырманы толық орындама.',
  'Жауапты бірден дайын қорытындымен алмастырма; алдымен бағыттаушы сұрақ қой.',
  'Пайдаланушы мәтіндік дәлел келтірмесе, оны ойдан жасама: қажетті эпизодты өзі табуы үшін бағыт бер. Шығарма мәтінінде бар-жоғын білмейтін эпизодты немесе дәйексөзді келтірме.',
  'Бірнеше әдеби интерпретация болуы мүмкін екенін ескер. Негізделген балама пікірді қате деп көрсетпе.',
  'Мәтінді мазмұндау мен әдеби талдаудың айырмасын түсінуге көмектес: жауап тек мазмұндаумен шектелсе, оны байқат.',
  'Кейіпкердің психологиясын, автордың ұстанымын немесе символдың мағынасын нақты дәлелсіз кесімді түрде тұжырымдама.',
  'Пайдаланушының жауабын кемсітетін, ұялтатын немесе жеке қабілетін бағалайтын сөздер қолданба.',
  'Әр кері байланыс төмендегі нақты жауапқа сүйенсін; жалпы шаблонды қайталама.',
  'Жауап өте қысқа болса, оны автоматты түрде сапасыз деп бағалама: алдымен қандай ақпарат жетіспейтінін көрсет.',
  'Пайдаланушы сұрамайынша, толық дайын талдауды оның орнына жазба. Қажет болса, бір қысқа үлгі келтіріп, оны өз жауабына қалай қолдануға болатынын түсіндір.',
  'Сандық балл қойма. Қажет болса, сапа көрсеткіштерін тек диагностикалық мақсатта сөзбен сипатта (мысалы, «дәлелділігі: нақтылауды қажет етеді»).',
];

/** One step's questions and answers as plain text (unanswered questions are named, not hidden). */
function tutorStepText(st) {
  const none = '(жауап берілмеген)';
  const lines = [];
  (st.fields || []).forEach(f => {
    const v = lab.data[f.id];
    if (f.type === 'rows') {
      const rows = v.filter(filledRow);
      lines.push('▸ ' + f.label + ':');
      if (!rows.length) lines.push('  ' + none);
      rows.forEach((r, i) => lines.push('  ' + (i + 1) + ') ' + f.columns.map((c, ci) => c + ': ' + (filled(r[ci]) ? r[ci].trim() : '—')).join('; ')));
    } else if (f.type === 'techniques') {
      lines.push('▸ ' + f.label + ':');
      const used = LAB_TECHNIQUES.filter(x => v[x.id].on || filled(v[x.id].text));
      if (!used.length) lines.push('  ' + none);
      used.forEach(x => lines.push('  – ' + x.label + (filled(v[x.id].text) ? ': ' + v[x.id].text.trim() : ' (мысал келтірілмеген)')));
    } else {
      lines.push('▸ ' + f.label + ': ' + (filled(v) ? v.trim() : none));
    }
  });
  return lines.join('\n');
}

/** The work, author and (for the plot tool) the excerpt the user entered. */
function tutorContext() {
  const d = lab.data, out = [];
  const work = d.work || d.plWork, author = d.author || d.plAuthor;
  if (filled(work)) out.push('Шығарма: «' + work.trim().replace(/^«|»$/g, '') + '»');
  if (filled(author)) out.push('Автор: ' + author.trim());
  if (filled(d.hero)) out.push('Талданатын кейіпкер: ' + d.hero.trim());
  if (filled(d.plExcerpt)) out.push('Пайдаланушы енгізген үзінді (дәлелдерді осы мәтінмен ғана салыстыр):\n-----\n' + d.plExcerpt.trim() + '\n-----');
  else out.push('Шығарманың мәтіні берілмеген: пайдаланушы келтірген дәлелдерге ғана сүйен, мәтінде бар-жоғын білмейтін нәрсені растама.');
  return out.join('\n');
}

function tutorAnswers(final) {
  if (!final) return tutorStepText(LAB_STEPS[lab.step]);
  return LAB_STEPS.filter(st => st.fields).map(st => '## ' + st.title + '\n' + tutorStepText(st)).join('\n\n');
}

function tutorKey(final) { return final ? 'final' : LAB_STEPS[lab.step].id; }

function tutorPrompt(final, previous) {
  const st = LAB_STEPS[lab.step];
  const tool = LAB_TOOLS[labTool];
  const p = [];
  p.push('Сен — әдебиет пәнінің талапшыл, бірақ қолдаушы оқытушысысың (ЖИ тәлімгері). Мақсатың — балл қою немесе пайдаланушының орнына дайын әдеби талдау жазу емес, оған көркем мәтінді өз бетінше түсіну, интерпретациялау, дәлелдеу және қорытындылау дағдыларын дамытуға көмектесу. Кері байланыс нақты, сыпайы, түсінікті және әрекетке бағытталған болсын. Жауабыңды қазақ тілінде жаз.');
  p.push('ТАЛДАУ ТҮРІ: ' + t(tool.label) + (final ? ' (бүкіл талдау)' : '. Кезең: ' + st.title) +
    '\nКері байланыста мынаған назар аудар: ' + TUTOR_FOCUS[labTool]);
  p.push('МӘЛІМЕТ:\n' + tutorContext());
  p.push('ПЕДАГОГИКАЛЫҚ ҚАҒИДАЛАР:\n' + TUTOR_RULES.map(x => '- ' + x).join('\n'));
  if (previous) {
    p.push('БҰРЫНҒЫ НҰСҚА:\n' + previous);
    p.push('ЖАҢА (ҚАЙТА ӨҢДЕЛГЕН) НҰСҚА:\n' + tutorAnswers(final));
    p.push('Алдымен «Өзгерістер» деген бөлімде жаңа нұсқаны бұрынғымен салыстыр: нақты не өзгерді, қай тұжырым дәлелденіп, тереңдеді, ал қай мәселе әлі сол күйінде қалды. Содан кейін төмендегі құрылыммен кері байланыс бер.');
  } else {
    p.push('ПАЙДАЛАНУШЫНЫҢ ЖАУАПТАРЫ:\n' + tutorAnswers(final));
  }
  if (final) {
    p.push('ҚОРЫТЫНДЫ КЕРІ БАЙЛАНЫС ҚҰРЫЛЫМЫ:\n' +
      '1. Ең сәтті үш байқау — пайдаланушының нақты ойын, байқауын немесе талдау тәсілін ата; жалпылама мақтаумен шектелме.\n' +
      '2. Тереңдетуге тұратын бір немесе екі бағыт — дәлелсіз тұжырым, үстірт түсіндіру немесе байқалмаған байланыс. Мәселе болмаса, кемшілік ойлап таппа.\n' +
      '3. Дәлелділікті арттыруға арналған нақты ұсыныстар — пайдаланушы өзі орындай алатын әрекеттер (мәтіннен эпизод табу, екі көріністі салыстыру, тұжырым мен дәлел арасындағы байланысты нақтылау т.б.).\n' +
      '4. Әрі қарай өз бетінше ойлануға арналған бір қорытынды сұрақ.\n' +
      'Соңында пайдаланушыға талдауын жетілдіріп, жаңа нұсқасын қайта жіберуге болатынын айт.');
  } else {
    p.push('КЕРІ БАЙЛАНЫС ҚҰРЫЛЫМЫ:\n' +
      '1. Сәтті шыққан тұсы — жауаптағы нақты сәтті ойды, байқауды немесе талдау тәсілін ата; жалпылама мақтаумен шектелме.\n' +
      '2. Тереңдетуге болатын тұсы — дәлелсіз тұжырымды, үстірт түсіндіруді, байқалмаған байланысты немесе нақтылауды қажет ететін ойды көрсет. Мәселе болмаса, жасанды кемшілік ойлап таппа.\n' +
      '3. Ойлануға арналған сұрақ — тұжырымды қайта қарауға көмектесетін бір немесе екі нақты сұрақ (осы талдау түріне сәйкес).\n' +
      '4. Келесі қадам — пайдаланушы өзі орындай алатын бір нақты әрекет.\n' +
      '5. Қайта өңдеу — пайдаланушыға жауабын жетілдіріп, жаңа нұсқасын қайта жіберуге болатынын айт; жаңа нұсқа келгенде оны бұрынғымен салыстыратыныңды ескерт.');
  }
  return p.join('\n\n');
}

function showTutor(final) {
  const key = tutorKey(final);
  const previous = lab.tutor[key] || '';
  const current = tutorAnswers(final);
  const canRevise = filled(previous) && previous !== current;
  let revision = canRevise;
  const ta = h('textarea', { class: 'dlg-code', readonly: true, 'aria-label': t('tutorDlgTitle') });
  const fill = () => { ta.value = tutorPrompt(final, revision ? previous : ''); };
  const mode = (value, label, note, disabled) => {
    const r = h('input', { type: 'radio', name: 'tutor-mode', value: value, disabled: disabled,
      onchange: () => { revision = value === 'revision'; fill(); } });
    r.checked = (value === 'revision') === revision;
    return h('label', null, r, h('span', null, label, note ? ' ' + note : ''));
  };
  fill();
  const links = [['ChatGPT', 'https://chatgpt.com/'], ['Claude', 'https://claude.ai/'], ['Gemini', 'https://gemini.google.com/']];
  openDialog(t('tutorDlgTitle'), [
    h('ol', { class: 'tutor-steps' }, STRINGS.tutorSteps.map(x => h('li', { text: x }))),
    h('div', { class: 'tutor-modes', role: 'radiogroup', 'aria-label': t('tutorTitle') },
      mode('first', t('tutorModeFirst'), '', false),
      mode('revision', t('tutorModeRevision'), canRevise ? '' : filled(previous) ? t('tutorSame') : t('tutorNoPrevious'), !canRevise)),
    ta,
    h('p', { class: 'tutor-links' }, h('span', { text: t('tutorOpen') }),
      links.map(([name, href]) => h('a', { href: href, target: '_blank', rel: 'noopener noreferrer', text: name }))),
    h('p', { class: 'tutor-note', text: t('tutorPrivacy') }),
  ], [
    { label: t('close') },
    { label: t('tutorCopy'), primary: true, onclick: e => {
      copyText(ta, e.currentTarget);
      lab.tutor[key] = current;   // the version this feedback is about: the next one is compared with it
      labSaveNow();
      return false;
    } },
  ]);
  const box = document.querySelector('.dlg');
  if (box) { box.classList.add('tutor-dlg'); box.scrollTop = 0; }
}

function tutorCard(final) {
  return h('div', { class: 'tutor-card' },
    h('div', null, h('h3', { text: t('tutorTitle') }), h('p', { text: t(final ? 'tutorCardFinal' : 'tutorCardText') })),
    h('button', { type: 'button', class: 'btn primary', text: t('tutorBtn'), onclick: () => showTutor(final) }));
}

function labDocNodes() {""")

# Card under each stage's fields (not on the preparation step) and in the summary.
rep("    st.summary ? renderLabSummary() : st.fields.map(f => renderLabField(f, evWarns)));\n}",
    "    st.summary ? renderLabSummary() : st.fields.map(f => renderLabField(f, evWarns)),\n"
    "    !st.summary && !st.rules ? tutorCard(false) : null);\n}")
rep("""    h('p', { class: 'lab-step-intro', text: t('labPrintHint') }),
    h('div', { class: 'card lab-doc' }, labDocNodes()),""", """    h('p', { class: 'lab-step-intro', text: t('labPrintHint') }),
    tutorCard(true),
    h('div', { class: 'card lab-doc' }, labDocNodes()),""")
# Clearing a tool also forgets its saved versions (labFresh includes an empty tutor map).

s = s.replace('      python3 preview.py plot.html kobem-talday.html       # guide preview: full text only in the PDF',
              '      python3 preview.py plot.html preview.html            # guide preview: full text only in the PDF\n'
              '      python3 tutor.py preview.html kobem-talday.html      # «ЖИ тәлімгері» prompt (no AI call)')
open(out, 'w', encoding='utf8').write(s)
print('tutor ->', out)
