"""Photos: cover background and header images (embedded as WebP data URIs).
Usage: python3 -I photos.py in.html photos_dir out.html   (run after modern.py)"""
import base64, os, sys

src, pdir, out = sys.argv[1:4]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('photos anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

def data_url(name):
    b = open(os.path.join(pdir, name + '.webp'), 'rb').read()
    return 'url("data:image/webp;base64,' + base64.b64encode(b).decode('ascii') + '")'

NAMES = ['cover', 'library', 'guide', 'plan', 'help', 'kids', 'class', 'almaty']
vars_css = '\n'.join('    --photo-%s: %s;' % (n, data_url(n)) for n in NAMES)

# A separate style block so the large image data stays out of the main stylesheet.
rep('</head>', """<style id="photos">
  /* PHOTOS — free stock photos, cropped and compressed by prep_photos.py.
     cover: Шарын шатқалы · library: жұмыс үстелі · guide: кітап сөрелері ·
     plan: ашық кітаптар · help: Бәйтерек ·
     kids: балалар кітабы · class: мұғалім мен сынып · almaty: Алматы */
  :root {
%s
  }
  .cover-art {
    background:
      linear-gradient(180deg, rgba(6, 34, 62, .35) 0%%, rgba(6, 34, 62, .15) 35%%, rgba(6, 34, 62, .88) 100%%),
      var(--photo-cover) center / cover no-repeat;
  }
  .cover-art::before { opacity: .22; }
  .cover-art-title { text-shadow: 0 1px 8px rgba(0, 0, 0, .45); }
  .photo-banner {
    height: 180px; margin: 0 0 20px; border-radius: var(--radius); box-shadow: var(--shadow-sm);
    background-position: center; background-size: cover; background-repeat: no-repeat;
  }
  .photo-library { background-image: var(--photo-library); background-position: center 60%%; }
  .photo-guide { background-image: var(--photo-guide); }
  .photo-plan { background-image: var(--photo-plan); }
  .photo-kids { background-image: var(--photo-kids); background-position: center 45%%; }
  .photo-class { background-image: var(--photo-class); background-position: center 12%%; }
  .photo-almaty { background-image: var(--photo-almaty); background-position: center 22%%; }
  .photo-help { background-image: var(--photo-help); height: 150px; margin-bottom: 4px; border-radius: 12px; background-position: center 30%%; }
  .photo-credit { margin: 14px 0 0; font-size: 12px; color: var(--ink-2); }
  @media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) .photo-banner { filter: brightness(.82); } }
  :root[data-theme="dark"] .photo-banner { filter: brightness(.82); }
  @media (max-width: 680px) {
    .cover-art { background:
      linear-gradient(90deg, rgba(6, 34, 62, .8) 0%%, rgba(6, 34, 62, .45) 100%%),
      var(--photo-cover) center 40%% / cover no-repeat; }
    .photo-banner { height: 120px; margin-bottom: 14px; }
    .photo-help { height: 110px; }
  }
  @media print { .photo-banner { display: none; } }
</style>
</head>""" % vars_css)

rep("  helpBtn: 'Көмек',", "  photoCredit: 'Фотосуреттер тегін фотостоктардан алынды.',\n  helpBtn: 'Көмек',")

# Header images: «Талдауларым», guide lead-in and chapter pages, lesson plan, rubric, help.
rep("""  return h('section', null,
    h('p', { class: 'ws-kicker', text: t('tabLibrary') }),""", """  return h('section', null,
    photoBanner('library'),
    h('p', { class: 'ws-kicker', text: t('tabLibrary') }),""")
rep("""  return h('article', { class: 'guide' },""", """  return h('article', { class: 'guide' },
    sec.level < 2 ? photoBanner('guide') : null,""")
rep("""  return h('section', null,
    h('h2', { class: 'ws-title', text: t('lessonPlan') }),""", """  return h('section', null,
    photoBanner('class'),
    h('h2', { class: 'ws-title', text: t('lessonPlan') }),""")
rep("""  const field = rubricField();
  return h('section', null, sheetHeader(ws),""", """  const field = rubricField();
  return h('section', null, photoBanner('class'), sheetHeader(ws),""")
rep("""  const body = h('div', { class: 'help-body' }, STRINGS.helpSections.map(sec => [
    h('h3', { text: sec.title }),
    h('ul', null, sec.items.map(x => h('li', { text: x }))),
  ]));""", """  const body = h('div', { class: 'help-body' }, h('div', { class: 'photo-banner photo-help', 'aria-hidden': 'true' }),
    STRINGS.helpSections.map(sec => [
      h('h3', { text: sec.title }),
      h('ul', null, sec.items.map(x => h('li', { text: x }))),
    ]),
    h('p', { class: 'photo-credit', text: t('photoCredit') }));""")
rep("""function showHelp() {""", """/** Decorative header photo (no text content, hidden from screen readers). */
function photoBanner(name) {
  return h('div', { class: 'photo-banner photo-' + name, 'aria-hidden': 'true' });
}

function showHelp() {""")

rep("      python3 modern.py helped.html kobem-talday.html   # modern look + opening cover",
    "      python3 modern.py helped.html modern.html         # modern look + opening cover\n"
    "      python3 prep_photos.py <photos> photos            # crop + compress stock photos (WebP)\n"
    "      python3 photos.py modern.html photos kobem-talday.html")

open(out, 'w', encoding='utf8').write(s)
print('wrote', out, len(s.encode('utf8')) // 1024, 'KB')
