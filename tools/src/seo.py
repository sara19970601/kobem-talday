"""Search and sharing: page title and description, canonical link, Open Graph / Twitter card,
icons, Schema.org data, and a <noscript> summary for readers (and crawlers) without JavaScript.
Usage: python3 -I seo.py in.html out.html   (run last, after refresh.py)"""
import json, sys

src, out = sys.argv[1:3]
s = open(src, encoding='utf8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit('seo anchor found %d times (want %d): %r' % (n, count, old[:90]))
    s = s.replace(old, new)

URL = 'https://korkemtaldau.com/'
TITLE = 'Көркем шығарманы талдауға арналған тегін платформа'
DESC = ('Көркем шығарманы талдауға арналған тегін платформа: 45 минуттық сабақ жоспары мен бағалау рубрикасы, '
        '10 талдау түрі бар Зертхана, әдеби терминдер сөздігі және балалар әдебиеті.')
data = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    'name': 'Көркем шығарманы талдау',
    'url': URL,
    'inLanguage': 'kk',
    'description': DESC,
    'author': {'@type': 'Person', 'name': 'Бекжанова Сара'},
    'audience': {'@type': 'EducationalAudience', 'educationalRole': 'teacher'},
    'about': ['Әдебиет', 'Көркем шығарманы талдау', 'Әдебиет сабағы'],
    'isAccessibleForFree': True,
}
head = '\n'.join([
    '<meta name="description" content="%s">' % DESC,
    '<meta name="author" content="Бекжанова Сара">',
    '<meta name="theme-color" content="#3A56E4">',
    '<link rel="canonical" href="%s">' % URL,
    '<link rel="icon" type="image/png" sizes="48x48" href="/favicon.png">',
    '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
    '<meta property="og:type" content="website">',
    '<meta property="og:site_name" content="Көркем шығарманы талдау">',
    '<meta property="og:locale" content="kk_KZ">',
    '<meta property="og:url" content="%s">' % URL,
    '<meta property="og:title" content="%s">' % TITLE,
    '<meta property="og:description" content="%s">' % DESC,
    '<meta property="og:image" content="%sog-image.jpg">' % URL,
    '<meta property="og:image:width" content="1200">',
    '<meta property="og:image:height" content="630">',
    '<meta property="og:image:alt" content="Көркем шығарманы талдауға арналған тегін платформа">',
    '<meta name="twitter:card" content="summary_large_image">',
    '<script type="application/ld+json">%s</script>' % json.dumps(data, ensure_ascii=False),
])
rep('<title>Көркем шығарманы талдау</title>', '<title>%s</title>\n%s' % (TITLE, head))

NOSCRIPT = """<noscript>
  <section style="max-width:720px;margin:40px auto;padding:0 16px;font-family:Georgia,serif;line-height:1.6;color:#17233B">
    <h1>Көркем шығарманы талдау</h1>
    <p>Көркем шығарманы талдауға арналған тегін платформа. Құрастырған: Бекжанова Сара.</p>
    <ul>
      <li>Шығарманы жанрына қарай кезең-кезеңімен талдау (тақырып, идея, сюжет, композиция, кейіпкер, баяндаушы, уақыт пен кеңістік, көркем тіл).</li>
      <li>Жауаптардан өзі құрылатын 45 минуттық сабақ жоспары мен бағалау рубрикасы; Word және PDF түрінде сақтау.</li>
      <li>Зертхана: кейіпкер психологиясы, сюжет пен композиция, нарратология, символдар мен мотивтер, хронотоп, мифопоэтика, салыстырмалы талдау, көркем тіл мен стиль, герменевтика, экокритика.</li>
      <li>Әдеби терминдер сөздігі (63 термин) және жас санатына қарай балалар әдебиеті.</li>
    </ul>
    <p>Сайт жұмыс істеуі үшін браузерде JavaScript қосулы болуы керек.</p>
  </section>
</noscript>"""
i = s.index('<body')
j = s.index('>', i) + 1
s = s[:j] + '\n' + NOSCRIPT + s[j:]
open(out, 'w', encoding='utf8').write(s)
print('seo ->', out)
