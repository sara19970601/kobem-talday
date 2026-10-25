"""Welcome page: the opening window becomes a full-screen first page in the «Фокус режимі» style.
Hero (kicker, title, the author's three lead paragraphs, actions, author line, photo), six section
cards with big numbers that open the section, and a privacy strip. The texts of the cover are
kept as they were; «Келесі жолы көрсетпеу» works as before.
Usage: python3 -I welcome.py in.html out.html   (run after focus.py)"""
import re, sys

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('welcome anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

def rep_fn(name, new):
    global s
    m = re.search(r'\nfunction ' + re.escape(name) + r'\(.*?\n\}\n', s, re.S)
    if not m:
        sys.exit('welcome: function %s not found' % name)
    s = s[:m.start()] + '\n' + new.strip('\n') + '\n' + s[m.end():]

rep('</style>\n</head>', r"""</style>
<style id="welcome">
  /* WELCOME — the first page */
  .cover-overlay.welcome { display: block; padding: 0; background: var(--bg); overflow-y: auto; backdrop-filter: none; }
  .welcome .cover { display: block; max-width: none; width: 100%; max-height: none; min-height: 100%; margin: 0; border-radius: 0; box-shadow: none;
    background: var(--bg); overflow: visible; grid-template-columns: none; }
  .wl-top { position: sticky; top: 0; z-index: 2; display: flex; align-items: center; gap: 12px; padding: 12px 24px;
    background: var(--surface); border-bottom: 1px solid var(--line); }
  .wl-top::after { content: ""; position: absolute; left: 0; right: 0; bottom: -7px; height: 6px; background: var(--orn-band) repeat-x left bottom / 24px 6px; opacity: .55; }
  .wl-brand { display: flex; align-items: center; gap: 10px; font-family: var(--display); font-weight: 700; font-size: 18px; color: var(--ink); }
  .wl-brand .brand-mark { width: 32px; height: 32px; }
  .wl-top .btn { margin-left: auto; }
  .wl-wrap { max-width: 1140px; margin: 0 auto; padding: 40px 24px 32px; }
  .wl-hero { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, .85fr); gap: 40px; align-items: center; }
  .wl-kicker { margin: 0 0 10px; font-size: 13px; font-weight: 700; letter-spacing: .14em; color: var(--gold-ink); }
  .welcome .cover h1 { margin: 0 0 18px; font-family: var(--display); font-size: clamp(34px, 4.6vw, 56px); line-height: 1.08; letter-spacing: -.01em; color: var(--ink); }
  .wl-lead p { margin: 0 0 12px; font-size: 17px; line-height: 1.65; color: var(--ink-2); }
  .wl-lead p:first-child { font-family: var(--display); font-size: 20px; line-height: 1.5; color: var(--ink); padding-left: 16px; border-left: 3px solid var(--gold); }
  .wl-lead p:last-child { color: var(--ink); font-weight: 600; }
  .wl-actions { display: flex; flex-wrap: wrap; gap: 10px; margin: 22px 0 14px; }
  .wl-actions .btn { min-height: 48px; padding: 0 22px; font-size: 16px; font-weight: 600; }
  .wl-actions .btn.primary { padding: 0 30px; }
  .wl-author { margin: 0; font-size: 14px; color: var(--ink-2); }
  .wl-photo { position: relative; min-height: 440px; border-radius: 20px; overflow: hidden; background: var(--photo-cover) center 40% / cover no-repeat;
    box-shadow: 0 18px 40px rgba(23, 35, 59, .18); }
  .wl-photo::before { content: ""; position: absolute; inset: 12px; border: 1px solid rgba(255, 255, 255, .55); border-radius: 12px; pointer-events: none; }
  .wl-photo::after { content: ""; position: absolute; inset: 0; background: linear-gradient(180deg, rgba(23, 35, 59, 0) 45%, rgba(23, 35, 59, .82) 100%); }
  .wl-photo-cap { position: absolute; z-index: 1; left: 28px; right: 28px; bottom: 24px; color: #fff; }
  .wl-photo-cap b { display: block; font-family: var(--display); font-size: 22px; line-height: 1.25; }
  .wl-photo-cap span { font-size: 13px; letter-spacing: .08em; opacity: .9; }
  .wl-feats-title { margin: 48px 0 14px; font-family: var(--display); font-size: 24px; color: var(--ink); }
  .wl-cards { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }
  .wl-card { display: grid; grid-template-columns: auto 1fr; gap: 4px 14px; align-items: start; text-align: left; padding: 18px; min-height: 120px;
    border: 1px solid var(--line); border-radius: 16px; background: var(--surface); color: var(--ink); transition: border-color .15s, box-shadow .15s, transform .15s; }
  .wl-card:hover { border-color: var(--accent); box-shadow: 0 8px 22px rgba(35, 74, 143, .12); transform: translateY(-1px); }
  .wl-num { grid-row: span 2; min-width: 58px; font-family: var(--display); font-size: 34px; font-weight: 700; line-height: 1; color: var(--gold-ink); }
  .wl-card b { font-size: 16px; }
  .wl-desc { font-size: 14px; line-height: 1.5; color: var(--ink-2); }
  .wl-card .wl-go { color: var(--accent); font-weight: 700; }
  .wl-trust { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 18px; margin: 18px 0 0; padding: 14px 18px; border-radius: 14px;
    background: var(--ok-soft); color: var(--ok); font-weight: 600; font-size: 14.5px; }
  .wl-trust::before { content: "✓"; display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; background: var(--ok); color: #fff; font-size: 13px; }
  .wl-foot { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px; margin-top: 28px; padding-top: 16px; border-top: 1px solid var(--line); }
  .welcome .cover-hide { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; font-size: 14px; color: var(--ink-2); cursor: pointer; }
  .welcome .cover-hide input { width: 18px; height: 18px; }
  .wl-foot .link-btn { font-size: 14px; }
  @media (max-width: 980px) { .wl-cards { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
  @media (max-width: 760px) {
    .wl-hero { grid-template-columns: minmax(0, 1fr); gap: 22px; }
    .wl-photo { order: -1; min-height: 190px; }
    .wl-photo-cap b { font-size: 18px; }
    .wl-wrap { padding: 22px 16px 24px; }
    .wl-top { padding: 10px 16px; }
    .wl-lead p { font-size: 16px; } .wl-lead p:first-child { font-size: 18px; }
    .wl-actions .btn { flex: 1 1 100%; }
    .wl-cards { grid-template-columns: minmax(0, 1fr); }
    .wl-card { min-height: 0; }
    .wl-feats-title { margin-top: 32px; }
  }
  @media (prefers-reduced-motion: reduce) { .wl-card { transition: none; } .wl-card:hover { transform: none; } }
</style>
</head>""")

rep("  coverHide: 'Келесі жолы көрсетпеу',", """  coverHide: 'Келесі жолы көрсетпеу',
  coverClose: 'Сайтқа өту →',
  coverGo: 'Ашу →',
  coverCards: [
    { n: '✎', title: 'Дәптер', text: 'Шығарманы жанрына қарай кезең-кезеңімен талдау' },
    { n: '10', title: 'Зертхана', text: 'Кейіпкер, сюжет, нарратология, символ, хронотоп, мифопоэтика т.б.; мектеп және университет деңгейі, ЖИ тәлімгеріне дайын сұрау' },
    { n: '45′', title: 'Сабақ жоспары мен рубрика', text: '45 минуттық сабақ жоспары мен бағалау рубрикасы жауаптарыңыздан өзі құрылады' },
    { n: '§', title: 'Әдістемелік нұсқаулық', text: 'Кіріспе мен алғашқы бөлімдер, әр параққа қысқа кеңес; толық нұсқасы PDF-те' },
    { n: '63', title: 'Әдеби терминдер сөздігі', text: '63 термин, 6 бөлім, іздеу' },
    { n: '38', title: 'Балалар әдебиеті', text: 'Жас санатына қарай іріктелген 38 кітап' },
  ],
  coverTrust: 'Талдаулар осы браузерде сақталады, интернетсіз де жұмыс істейді, оқушы деректері жиналмайды',""")

rep_fn('showCover', r"""
function showCover(force) {
  let hidden = false;
  try { hidden = !!window.localStorage.getItem(COVER_HIDDEN_KEY); } catch (e) { hidden = false; }
  if (hidden && !force) return;
  const prev = document.activeElement;
  const hide = h('input', { type: 'checkbox', id: 'cover-hide' });
  hide.checked = hidden;
  const overlay = h('div', { class: 'cover-overlay welcome' });
  const close = then => {
    try {
      if (hide.checked) window.localStorage.setItem(COVER_HIDDEN_KEY, '1');
      else window.localStorage.removeItem(COVER_HIDDEN_KEY);
    } catch (e) { /* storage blocked */ }
    overlay.remove();
    if (then) then(); else if (prev && prev.focus) prev.focus();
  };
  // Each card opens its section.
  const goto = [
    () => switchTab('book'),
    () => switchTab('lab'),
    () => { switchTab('book'); goTo('plan'); },
    () => switchTab('guide'),
    () => switchTab('glossary'),
    () => switchTab('kids'),
  ];
  const start = h('button', { class: 'btn primary', type: 'button', text: t('coverStart'), onclick: () => close() });
  overlay.append(h('div', { class: 'cover', role: 'dialog', 'aria-modal': 'true', 'aria-labelledby': 'cover-title' },
    h('div', { class: 'wl-top' },
      h('div', { class: 'wl-brand' }, h('span', { class: 'brand-mark', 'aria-hidden': 'true' }), h('span', { text: t('appTitle') })),
      h('button', { class: 'btn', type: 'button', text: t('coverClose'), onclick: () => close() })),
    h('div', { class: 'wl-wrap' },
      h('section', { class: 'wl-hero' },
        h('div', null,
          h('p', { class: 'wl-kicker', text: t('coverKicker') }),
          h('h1', { id: 'cover-title', text: t('appTitle') }),
          h('div', { class: 'wl-lead' }, STRINGS.coverLead.map(x => h('p', { text: x }))),
          h('div', { class: 'wl-actions cover-actions' },
            start,
            h('button', { class: 'btn', type: 'button', text: t('coverHelp'), onclick: () => close(showHelp) })),
          h('p', { class: 'wl-author', text: t('coverAuthor') })),
        h('div', { class: 'wl-photo', role: 'img', 'aria-label': t('coverArtTitle') },
          h('div', { class: 'wl-photo-cap' }, h('b', { text: t('coverArtTitle') }), h('span', { text: 'korkemtaldau.com' })))),
      h('h2', { class: 'wl-feats-title', text: t('coverFeatsTitle') }),
      h('div', { class: 'wl-cards' }, STRINGS.coverCards.map((c, i) => h('button', { class: 'wl-card', type: 'button', onclick: () => close(goto[i]) },
        h('span', { class: 'wl-num', 'aria-hidden': 'true', text: c.n }),
        h('b', { text: c.title }),
        h('span', { class: 'wl-desc' }, c.text, ' ', h('span', { class: 'wl-go', text: t('coverGo') }))))),
      h('p', { class: 'wl-trust', text: t('coverTrust') }),
      h('div', { class: 'wl-foot' },
        h('label', { class: 'cover-hide', for: 'cover-hide' }, hide, t('coverHide')),
        h('button', { class: 'link-btn', type: 'button', text: t('coverShop'), onclick: () => close(showShop) })))));
  overlay.addEventListener('keydown', e => { if (e.key === 'Escape') close(); });
  document.body.append(overlay);
  start.focus({ preventScroll: true });
  overlay.scrollTop = 0;
}
""")
open(out, 'w', encoding='utf8').write(s)
print('welcome ->', out)
