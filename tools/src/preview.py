"""Guide preview: the site keeps only the lead-in and chapters 1–2 (intro) in full; every other
section keeps its title and, where worksheets link to it, a 2–3 sentence tip taken from the
guide itself. The full text is not in the page at all (a static site cannot hide text).
Locked sections show «Толық нұсқасы PDF-те» with a «Сатып алу» button.
Usage: python3 -I preview.py in.html out.html   (run after plot.py)"""
import json, re, sys

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('preview anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

FREE = {'pre', '1', '2'}   # lead-in, chapter 1, the chapter 2 introduction (its 2.x parts are tips)

# Tips for chapters 3–14 (the sections the worksheets link to), written from each chapter's opening.
TIPS = {
    '3': 'Кейіпкерді «жақсы ма, жаман ба?» деп бағалаудан бұрын оны түсінуге тырысыңыз: ол неге дәл осылай әрекет етті, таңдауы қандай құндылықтан туындайды? Нұсқаулық кейіпкерді портрет пен мінезден бастап 13 аспект бойынша талдауды ұсынады. Бағалау тек дәлелденген түсінуден кейін жасалады.',
    '4.1': 'Классикалық сюжет алты сатыдан тұрады: экспозиция, байланыс, оқиғаның дамуы, шиеленіс, шарықтау шегі және шешім. Әр сатыда «Қандай оқиға бәрін өзгертті?», «Әр келесі оқиға алдыңғысынан қалай күрделі?» деген сұрақтарды қойыңыз.',
    '4.2': 'Конфликт сипаты бойынша (сыртқы немесе ішкі) және қатысушылары бойынша (тұлға – тұлға, тұлға – қоғам, тұлға – табиғат, тұлға – өзі) жіктеледі. Алдымен қақтығысқа қатысушы екі тараптың нақты кім немесе не екенін анықтаңыз, ал ішкі конфликтте кейіпкердің толғанысы мен кідірісіне назар аударыңыз.',
    '5': 'Close reading («мұқият оқу») – әр сөзге, сөйлемге, детальға назар аударып, олардың мағыналық қызметін ашатын «баяу» оқу тәсілі. Оқушыға назар аударарлық жерлерді белгілеуді және тұжырымын дәлелдейтін қысқа, нақты дәйексөз таңдауды үйретіңіз.',
    '6': 'Өлеңге прозаның сюжеттік алгоритмін механикалық түрде қолданбаңыз: өлеңде көбіне дамыған сюжет болмайды, оның орталығында лирикалық субъект тұрады. Талдауды «Кім сөйлеп тұр?» деген сұрақтан бастап, лирикалық көңіл-күйге, образға, ұйқас пен ырғаққа назар аударыңыз.',
    '7': '2-бөлімдегі әмбебап алгоритм барлық прозалық жанрға қолданылады, бірақ әңгіме, повесть және роман құрылымы жағынан ерекшеленеді. Әңгіме шағын, бір оқиғаға құрылады, сондықтан онда әр деталь мен сөйлем ерекше маңызды; повесте кейіпкер эволюциясы, романда композиция мен кейіпкерлер жүйесі алдыңғы орынға шығады.',
    '8': 'Драмада баяндаушы жоқ: оқиға диалог пен әрекет арқылы көрсетіледі, автордың дауысы тек ремаркаларда естіледі. Сондықтан пьесаны талдағанда ремаркаға, диалогқа және акт пен көріністің бөлінуіне назар аударыңыз.',
    '9': 'Балалар шығармасын тек «не үйретеді?» деген сұрақпен шектемеңіз: тәрбиелік мән – талдаудың соңғы қыры ғана. Алдымен бала бейнесін, оның ішкі әлемін, қиялы мен қорқынышын және мұның қандай көркемдік тәсілдермен берілгенін ашыңыз.',
    '10': 'Сұрақтарды Блум таксономиясының деңгейлері (білу, түсіну, қолдану, талдау, бағалау, жасау) бойынша құрастырыңыз. Төменгі деңгейлерде ұзақ тоқтамаңыз: 5-сыныпта да оқушыны талдау мен бағалау деңгейіне жеткізетін қарапайым сұрақтар қоюға болады.',
    '11': 'Нұсқаулықта сыныпта қолдануға дайын 11 әдіс берілген (close reading, пікірталас, әдеби кейс т.б.). Әр әдістің мақсатын, жүргізілу тәртібін, мұғалім мен оқушының рөлін алдын ала жоспарлаңыз; күтілетін нәтиже – дәйексөзге негізделген тұжырым.',
    '12': 'Фольклорлық шығарманы жазба әдебиеттің қалыбымен талдамаңыз: оның авторы – халық, мәтіні ауызша таралып нұсқаланады, құрылымы дәстүрлі формулаларға бағынады. Кейіпкердің жеке психологиясынан гөрі оның сюжеттегі қызметіне (В.Я.Пропп әдісі) назар аударыңыз.',
    '13': 'Экокритика, гендерлік зерттеу, постколониалдық сын, психоаналитикалық талдау сияқты заманауи перспективалар міндетті емес, бірақ әсіресе 9–11 сыныпта талдауды байытады. Олар мәтінге негізделген талдауды алмастырмайды.',
    '14': 'Оқушы жұмысы мәтіндік дәлел, түсіндіру тереңдігі, құрылым және терминдерді қолдану критерийлері бойынша 3 баллдық шкаламен бағаланады. Ең бастысы – тұжырымның нақты дәйексөзбен дәлелденуі және дәлел мен қорытынды арасындағы байланыстың түсіндірілуі.',
}

def tip_2x(text):
    """2.x: the guide's own «Негізгі ұғым» definition + the first sentence of
    «Сабақта қалай қолдануға болады?» (or «Мұғалім нені байқауы керек?» when absent)."""
    heads = {}
    for p in text.split('\n\n'):
        m = re.match(r'^(Негізгі ұғым\.|Мұғалім нені байқауы керек\?|Сабақта қалай қолдануға болады\?)\s*(.*)$', p, re.S)
        if m:
            heads[m[1]] = m[2].strip()
    first = lambda p: re.match(r'(.+?[.!?])(\s|$)', p, re.S)[1]
    use = heads.get('Сабақта қалай қолдануға болады?') or heads['Мұғалім нені байқауы керек?']
    return heads['Негізгі ұғым.'] + ' ' + first(use)

m = re.search(r'const GUIDE = (\{.*?\n\});\n', s, re.S)
guide = json.loads(m[1])
locked = 0
for sec in guide['sections']:
    if sec['id'] in FREE:
        continue
    tip = tip_2x(sec['text']) if re.match(r'^2\.\d+$', sec['id']) else TIPS.get(sec['id'], '')
    sec['text'] = tip
    sec['locked'] = True
    locked += 1
missing = [x for x in TIPS if not any(sec['id'] == x for sec in guide['sections'])]
if missing:
    sys.exit('tips for unknown sections: %r' % missing)
s = s[:m.start(1)] + json.dumps(guide, ensure_ascii=False, indent=1).replace('</', '<\\/') + s[m.end(1):]
rep("   the PDF's text layer. Wording is unchanged; do not edit by hand — rebuild.",
    "   the PDF's text layer. Wording is unchanged; do not edit by hand — rebuild.\n"
    "   PREVIEW (preview.py): only the lead-in and chapters 1–2 are full; other sections carry\n"
    "   `locked: true` and a short tip (or nothing). The full guide is sold as a PDF.")

# ---- CSS ----
rep('</style>\n</head>', r"""</style>
<style id="guide-preview">
  /* GUIDE PREVIEW — short tips and «Толық нұсқасы PDF-те» */
  .g-tip { margin: 0 0 14px; padding: 14px 16px; border-radius: 14px; background: var(--accent-soft); border: 1px solid var(--line); }
  .g-tip h3 { margin: 0 0 6px; font-size: 14px; letter-spacing: .04em; text-transform: uppercase; color: var(--accent); }
  .g-tip p { margin: 0; line-height: 1.6; }
  .g-locked { display: flex; flex-wrap: wrap; gap: 12px 16px; align-items: center; justify-content: space-between;
    margin: 0 0 16px; padding: 16px 18px; border-radius: 14px; border: 1px dashed var(--gold, var(--accent)); background: var(--surface); }
  .g-locked div { flex: 1 1 260px; }
  .g-locked h3 { margin: 0 0 4px; font-size: 16px; }
  .g-locked p { margin: 0; color: var(--ink-2); font-size: 14px; line-height: 1.5; }
  .g-pdf { flex: none; margin-left: 6px; font-size: 10.5px; font-weight: 800; letter-spacing: .04em; color: #b3261e;
    background: rgba(179, 38, 30, .1); border-radius: 5px; padding: 1px 5px; }
  @media (max-width: 520px) { .g-locked .btn { width: 100%; } }
</style>
</head>""")

# ---- Strings ----
rep("  guideSearch: 'Нұсқаулықтан іздеу',", """  guideSearch: 'Нұсқаулықтан іздеу',
  guideTip: 'Қысқа кеңес',
  guideLockedTitle: 'Толық нұсқасы PDF-те',
  guideLockedText: 'Бұл бөлімнің толық мәтіні (түсіндірме, сұрақтар, мысалдар, жиі кездесетін қателер және тапсырмалар) «Көркем шығарманы талдау» әдістемелік нұсқаулығының PDF нұсқасында берілген.',
  guideLockedBuy: 'Сатып алу',
  guideLockedPrint: 'Бөлімнің толық мәтіні «Көркем шығарманы талдау» әдістемелік нұсқаулығының PDF нұсқасында.',
  guidePdfMark: 'PDF',""")
rep("      'Әр парақтағы «Нұсқаулық: 2.8 →» сияқты батырма әдістемелік түсініктемені ашады.",
    "      'Әр парақтағы «Нұсқаулық: 2.8 →» сияқты батырма сол тармақ бойынша қысқа әдістемелік кеңесті ашады.")
rep("    'Әдістемелік нұсқаулық: 16 бөлім, әр параққа сілтеме, ішінен іздеу',",
    "    'Әдістемелік нұсқаулық: кіріспе мен алғашқы бөлімдер, әр параққа қысқа кеңес; толық нұсқасы PDF-те',")

# ---- Guide view ----
rep("""    h('div', { class: 'g-body' }, renderGuideText(sec.text, q)),""",
    """    sec.locked && filled(sec.text) ? h('section', { class: 'g-tip' }, h('h3', { text: t('guideTip') }), renderGuideText(sec.text, q)) : null,
    sec.locked ? h('div', { class: 'g-locked' },
      h('div', null, h('h3', { text: t('guideLockedTitle') }), h('p', { text: t('guideLockedText') })),
      h('button', { class: 'btn primary', type: 'button', text: t('guideLockedBuy'), onclick: showShop }))
      : h('div', { class: 'g-body' }, renderGuideText(sec.text, q)),""")
rep("""  }, h('span', { class: 'step-label' }, guideNavLabel(sec)),""",
    """  }, h('span', { class: 'step-label' }, guideNavLabel(sec), sec.locked ? h('span', { class: 'g-pdf', title: t('guideLockedTitle'), text: t('guidePdfMark') }) : null),""")
rep("""      h('h2', { text: guideHeading(sec) }), renderGuideText(sec.text, ''));""",
    """      h('h2', { text: guideHeading(sec) }), renderGuideText(sec.text, ''),
      sec.locked ? h('p', { class: 'print-note', text: t('guideLockedPrint') }) : null);""")

s = s.replace('      python3 plot.py lab.html kobem-talday.html           # «Зертхана»: сюжет пен композиция',
              '      python3 plot.py lab.html plot.html                   # «Зертхана»: сюжет пен композиция\n'
              '      python3 preview.py plot.html kobem-talday.html       # guide preview: full text only in the PDF')
open(out, 'w', encoding='utf8').write(s)
print('preview: %d sections locked -> %s' % (locked, out))
