"""Shop: three paid products (PDF and Word), ordered through WhatsApp (payment checked by hand via Kaspi).
No files, no payment code: the buttons only open a WhatsApp chat with a ready message.
Usage: python3 -I shop.py in.html out.html   (run after save.py)"""
import sys

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('shop anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

# ---- Settings: the number and the prices, at the very start of the code ----
rep("""<script>
'use strict';
/* ==============================================================================
   CONFIG""", """<script>
'use strict';
/* ==============================================================================
   SHOP SETTINGS — WhatsApp нөмірі мен өнім бағалары осы жерден өзгертіледі.
   Нөмір халықаралық форматта: + белгісіз, бос орынсыз (7 778 263 3831 → "77782633831").
   ============================================================================== */
const whatsappNumber = "77782633831";
const SHOP_PRODUCTS = [
  {
    id: 'workbook',
    title: '«Көркем шығарманы талдау» жұмыс дәптері',
    badge: 'WORD',
    kind: 'Жұмыс дәптері',
    format: 'Word (.docx), электронды нұсқа',
    description: 'Көркем шығарманы жүйелі талдауға, мәтінмен жұмыс істеуге және әдеби талдау дағдыларын дамытуға арналған практикалық жұмыс дәптері.',
    price: 3000,
    message: 'Сәлеметсіз бе! “Көркем шығарманы талдау” жұмыс дәптерінің Word нұсқасын сатып алғым келеді. Бағасы мен Kaspi арқылы төлем жасау жолын жіберсеңіз.',
  },
  {
    id: 'guide',
    title: '«Көркем шығарманы талдау» әдістемелік нұсқаулығы',
    kind: 'Әдістемелік нұсқаулық',
    format: 'PDF, электронды нұсқа',
    description: 'Көркем шығарманы талдаудың әдістері мен кезеңдерін түсіндіретін, әдеби шығарманы оқыту мен талдауға көмектесетін әдістемелік құрал.',
    price: 3000,
    message: 'Сәлеметсіз бе! “Көркем шығарманы талдау” әдістемелік нұсқаулығының PDF нұсқасын сатып алғым келеді. Бағасы мен Kaspi арқылы төлем жасау жолын жіберсеңіз.',
  },
  {
    id: 'grade5',
    badge: 'WORD',
    title: 'Қазақ әдебиеті, 5-сынып: оқу мақсаттарына негізделген әмбебап жұмыс дәптері',
    kind: '5-сынып · Жұмыс дәптері',
    format: 'Word (.docx), электронды нұсқа',
    description: 'Бір оқу жылына арналған: 4 тоқсан, 14 шығарма, 68 сабақ. Оқу бағдарламасының 12 оқу мақсатына негізделген. «Арман-ПВ», «Мектеп», «Атамұра» оқулықтарының кез келгенімен қолданылады. Тапсырмалар үш деңгейде, жауап кілті мен бағалау критерийлері бар.',
    contents: [
      ['1-тоқсан. Таза, мінсіз асыл сөз', ['«Керқұла атты Кендебай» ертегісі', '«Қобыланды батыр» жыры', 'Асанқайғы аңызы']],
      ['2-тоқсан. Тәрбиенің қайнар бұлағы', ['Дулат Бабатайұлы', 'Қыпшақ Сейітқұл', 'Атымтай жомарт', 'Дүние қалай етсең табылады?']],
      ['3-тоқсан. Адамгершілік: асыл қасиет', ['Егіннің бастары', 'Адамдық диқаншысы', 'Менің атым Қожа', 'Бауыр']],
      ['4-тоқсан. Отбасы құндылықтары', ['Анасын сағынған бала', 'Нағыз әже қайда?', 'Мексика ұлы']],
    ],
    price: 3900,
    message: 'Сәлеметсіз бе! “Қазақ әдебиеті, 5-сынып” әмбебап жұмыс дәптерінің Word нұсқасын сатып алғым келеді. Бағасы мен Kaspi арқылы төлем жасау жолын жіберсеңіз.',
  },
];

/* ==============================================================================
   CONFIG""")

# ---- Strings ----
rep("  helpBtn: 'Көмек',", """  shopBtn: 'Сатып алу',
  shopTitle: 'Электронды нұсқаларды сатып алу',
  shopLead: 'Жұмыс дәптерлері мен әдістемелік нұсқаулықтың электронды нұсқаларын WhatsApp арқылы тапсырыс беріп сатып алуға болады.',
  shopNum: '{n}-өнім',
  shopBuy: 'WhatsApp арқылы сатып алу',
  shopCurrency: 'теңге',
  shopHow: 'Қажетті өнімді таңдап, WhatsApp арқылы тапсырыс беріңіз. Kaspi арқылы төлем жасау нұсқаулығын алғаннан кейін төлем жасайсыз. Төлем расталған соң файл (PDF немесе Word) сізге жіберіледі.',
  shopHowTitle: 'Тапсырыс беру тәртібі',
  shopSteps: ['WhatsApp арқылы тапсырыс', 'Kaspi арқылы төлем', 'Файлды алу'],
  shopContents: 'Мазмұны',
  coverShop: 'Электронды нұсқасын сатып алу',
  helpBtn: 'Көмек',""")

# ---- CSS ----
rep('</style>\n</head>', """</style>\n<style id="shop">
  /* SHOP — «Сатып алу»: product cards + WhatsApp order buttons */
  .shop-btn { flex: none; font-weight: 600; display: inline-flex; align-items: center; gap: 7px; }
  .shop-ico { width: 18px; height: 18px; flex: none; }
  @media (min-width: 901px) {
    .shop-btn { order: 2; margin-left: auto; }
    .shop-btn + .help-btn { margin-left: 0; }
  }
  @media (max-width: 900px) { .shop-btn { order: 2; min-height: 42px; } .shop-btn .shop-label { display: none; } }
  @media (max-width: 520px) { .shop-btn { padding: 8px 11px; } }
  /* Very narrow phones: the logo stands in for the name, which would be cut to a few letters. */
  @media (max-width: 380px) { .brand h1 { display: none; } .brand .brand-mark { display: block; } }
  .dlg.shop-dlg { max-width: 960px; width: calc(100% - 32px); }
  .shop-lead { margin: 0 0 14px; color: var(--ink-2); }
  .shop-photo { height: 130px; margin-bottom: 14px; }
  @media (max-width: 680px) { .shop-photo { height: 90px; } }
  .shop-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 260px), 1fr)); gap: 14px; }
  .shop-card { display: flex; flex-direction: column; border: 1px solid var(--line); border-radius: 16px; overflow: hidden;
    background: var(--surface); box-shadow: var(--shadow-sm); }
  .shop-cover { position: relative; height: 150px; display: flex; flex-direction: column; justify-content: flex-end;
    padding: 14px 16px; color: #fff; background-size: cover; background-position: center; }
  .shop-cover::before { content: ""; position: absolute; inset: 0; }
  .shop-cover.workbook { background-image: var(--photo-plan); }
  .shop-cover.workbook::before { background: linear-gradient(160deg, rgba(11, 102, 176, .55), rgba(6, 34, 62, .92)); }
  .shop-cover.guide { background-image: var(--photo-guide); }
  .shop-cover.guide::before { background: linear-gradient(160deg, rgba(150, 100, 20, .55), rgba(60, 30, 6, .92)); }
  .shop-cover.grade5 { background-image: var(--photo-class); }
  .shop-cover.grade5::before { background: linear-gradient(160deg, rgba(23, 103, 58, .55), rgba(6, 40, 22, .92)); }
  .shop-cover > * { position: relative; }
  .shop-cover-kind { font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; opacity: .9; }
  .shop-cover-name { font-family: var(--display); font-size: 21px; font-weight: 700; line-height: 1.2; text-shadow: 0 1px 6px rgba(0, 0, 0, .4); }
  .shop-cover-pdf { position: absolute; top: 12px; right: 12px; font-size: 11.5px; font-weight: 800; letter-spacing: .05em;
    background: rgba(255, 255, 255, .92); color: #b3261e; border-radius: 6px; padding: 3px 7px; }
  .shop-cover-pdf.word { color: #185abd; }
  .shop-toc { font-size: 14px; }
  .shop-toc summary { cursor: pointer; font-weight: 600; color: var(--accent); min-height: 44px; display: flex; align-items: center; }
  .shop-toc dl { margin: 6px 0 0; }
  .shop-toc dt { font-weight: 700; margin-top: 8px; }
  .shop-toc dd { margin: 2px 0 0 14px; color: var(--ink-2); line-height: 1.45; }
  .shop-body { display: flex; flex-direction: column; gap: 8px; padding: 14px 16px 16px; flex: 1; }
  .shop-num { font-size: 12.5px; font-weight: 700; color: var(--accent); letter-spacing: .04em; text-transform: uppercase; }
  .shop-title { margin: 0; font-size: 17px; line-height: 1.3; }
  .shop-format { align-self: flex-start; font-size: 12.5px; font-weight: 600; color: var(--ink-2);
    background: var(--surface-2); border: 1px solid var(--line); border-radius: 999px; padding: 2px 10px; }
  .shop-desc { margin: 0; line-height: 1.5; font-size: 14.5px; }
  .shop-foot { margin-top: auto; padding-top: 8px; display: flex; flex-direction: column; gap: 10px; }
  .shop-price { font-size: 24px; font-weight: 800; color: var(--ink); }
  .shop-price small { font-size: 15px; font-weight: 700; color: var(--ink-2); margin-left: 4px; }
  .wa-btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; min-height: 46px; padding: 10px 16px;
    border-radius: 12px; background: #1fa855; color: #fff; font-weight: 700; font-size: 15.5px; text-decoration: none;
    transition: background .15s, box-shadow .15s; }
  .wa-btn:hover { background: #178a45; box-shadow: var(--shadow-sm); }
  .wa-btn:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
  .wa-btn svg { width: 20px; height: 20px; flex: none; }
  .shop-how { margin: 16px 0 0; padding: 14px 16px; border-radius: 14px; background: var(--accent-soft); }
  .shop-how h3 { margin: 0 0 8px; font-size: 15px; }
  .shop-steps { list-style: none; margin: 0 0 10px; padding: 0; display: flex; flex-wrap: wrap; gap: 6px 10px; counter-reset: st; }
  .shop-steps li { counter-increment: st; display: inline-flex; align-items: center; gap: 6px; font-weight: 600; font-size: 14px; }
  .shop-steps li::before { content: counter(st); width: 22px; height: 22px; border-radius: 50%; background: var(--accent); color: #fff;
    display: inline-flex; align-items: center; justify-content: center; font-size: 12.5px; }
  .shop-steps li + li::after { content: none; }
  .shop-how p { margin: 0; line-height: 1.5; }
  @media print { .shop-btn { display: none; } }
</style>
</head>""")

# ---- Code ----
WA_SVG = ("M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.3-1.2l-.3-.2-3 .8.8-2.9-.2-.3"
          "A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9"
          "c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7"
          "c.1.2 1.9 2.9 4.6 4 1.7.7 2.4.8 3.2.7.5-.1 1.5-.6 1.8-1.2.2-.6.2-1.1.1-1.2l-.5-.3z")
rep("""/* ---- COVER — the opening window""", """/* ==============================================================================
   SHOP — «Сатып алу»: product cards; each button opens WhatsApp with a ready message.
   Payment is agreed and checked by hand (Kaspi); the PDF is sent by the author.
   No files or payment code here. Settings: whatsappNumber and SHOP_PRODUCTS at the top.
   ============================================================================== */
const SHOP_HASH = '#duken';   // korkemtaldau.com/#duken opens the shop directly

function waLink(message) {
  const number = String(whatsappNumber).replace(/\\D/g, '');   // tolerate "+7 778 …" if typed that way
  return 'https://wa.me/' + number + '?text=' + encodeURIComponent(message);
}

function svgIcon(path, cls) {
  const NS = 'http://www.w3.org/2000/svg';
  const svg = document.createElementNS(NS, 'svg');
  svg.setAttribute('viewBox', '0 0 24 24'); svg.setAttribute('aria-hidden', 'true'); svg.setAttribute('focusable', 'false');
  if (cls) svg.setAttribute('class', cls);
  const p = document.createElementNS(NS, 'path');
  p.setAttribute('d', path); p.setAttribute('fill', 'currentColor');
  svg.append(p);
  return svg;
}
const WA_ICON = '%s';
const CART_ICON = 'M7 18a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm10 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM5.2 4l.9 2H20a1 1 0 0 1 .9 1.4l-3.3 6.3a2 2 0 0 1-1.8 1.1H8.1l-1 1.7V17h12v2H6a1.5 1.5 0 0 1-1.3-2.3l1.4-2.4L2.6 4H1V2h2.9z';

function formatPrice(n) { return String(n).replace(/\\B(?=(\\d{3})+(?!\\d))/g, '\\u00a0'); }

function shopCard(p, i) {
  return h('article', { class: 'shop-card', id: 'shop-' + p.id },
    h('div', { class: 'shop-cover ' + p.id, 'aria-hidden': 'true' },
      h('span', { class: 'shop-cover-pdf' + (p.badge === 'WORD' ? ' word' : ''), text: p.badge || 'PDF' }),
      h('span', { class: 'shop-cover-kind', text: t('appTitle') }),
      h('span', { class: 'shop-cover-name', text: p.kind })),
    h('div', { class: 'shop-body' },
      h('span', { class: 'shop-num', text: t('shopNum', { n: i + 1 }) }),
      h('h3', { class: 'shop-title', text: p.title }),
      h('span', { class: 'shop-format', text: p.format }),
      h('p', { class: 'shop-desc', text: p.description }),
      p.contents ? h('details', { class: 'shop-toc' }, h('summary', { text: t('shopContents') }),
        h('dl', null, p.contents.flatMap(([q, works]) => [h('dt', { text: q }), h('dd', { text: works.join(' · ') })]))) : null,
      h('div', { class: 'shop-foot' },
        h('div', { class: 'shop-price' }, formatPrice(p.price), h('small', { text: t('shopCurrency') })),
        h('a', { class: 'wa-btn', href: waLink(p.message), target: '_blank', rel: 'noopener noreferrer',
          'aria-label': t('shopBuy') + ': ' + p.title }, svgIcon(WA_ICON), h('span', { text: t('shopBuy') })))));
}

function showShop() {
  const body = h('div', { class: 'shop' },
    h('div', { class: 'photo-banner photo-almaty shop-photo', 'aria-hidden': 'true' }),
    h('p', { class: 'shop-lead', text: t('shopLead') }),
    h('div', { class: 'shop-grid' }, SHOP_PRODUCTS.map(shopCard)),
    h('section', { class: 'shop-how' },
      h('h3', { text: t('shopHowTitle') }),
      h('ol', { class: 'shop-steps' }, STRINGS.shopSteps.map(x => h('li', { text: x }))),
      h('p', { text: t('shopHow') })));
  openDialog(t('shopTitle'), body, [{ label: t('close') }]);
  const box = document.querySelector('.dlg');
  if (box) {   // no primary button here: focus the window itself so Esc and Tab work at once
    box.classList.add('shop-dlg');
    box.setAttribute('tabindex', '-1');
    box.focus({ preventScroll: true });
    box.scrollTop = 0;
  }
}

/* ---- COVER — the opening window""" % WA_SVG)

# Top bar button (before «Көмек»)
rep("""    h('button', { class: 'btn help-btn', type: 'button', onclick: showHelp,""",
    """    h('button', { class: 'btn shop-btn', type: 'button', onclick: showShop, title: t('shopTitle'), 'aria-label': t('shopTitle') },
      svgIcon(CART_ICON, 'shop-ico'), h('span', { class: 'shop-label', text: t('shopBtn') })),
    h('button', { class: 'btn help-btn', type: 'button', onclick: showHelp,""")

# Cover: a third button
rep("""        h('button', { class: 'btn', type: 'button', text: t('coverHelp'), onclick: () => close(showHelp) })),""",
    """        h('button', { class: 'btn', type: 'button', text: t('coverHelp'), onclick: () => close(showHelp) }),
        h('button', { class: 'btn', type: 'button', text: t('coverShop'), onclick: () => close(showShop) })),""")

# Direct link korkemtaldau.com/#duken
rep("""loadState();
render();
showCover();""", """loadState();
render();
if (location.hash === SHOP_HASH) showShop(); else showCover();
window.addEventListener('hashchange', () => { if (location.hash === SHOP_HASH) showShop(); });""")

s = s.replace('      python3 save.py kids.html kobem-talday.html          # save as Word / PDF',
              '      python3 save.py kids.html saved.html                 # save as Word / PDF\n'
              '      python3 shop.py saved.html kobem-talday.html         # «Сатып алу» (WhatsApp orders)')
open(out, 'w', encoding='utf8').write(s)
print('shop ->', out)
