"""Children's books list (docx) -> kids.json. Stops if a book lacks a field.
Usage: python3 -I kids_extract.py books.docx kids.json"""
import json, re, sys
import docx

src, out = sys.argv[1:3]
paras = [(p.style.name, p.text.strip()) for p in docx.Document(src).paragraphs]
groups, book, intro = [], None, []
FIELDS = {'Автор': 'author', 'Басылым': 'edition', 'Жас (каталог бойынша)': 'age'}
for style, text in paras:
    if not text:
        continue
    if style == 'Heading 1':
        groups.append({'title': text, 'intro': '', 'books': []}); book = None; continue
    if not groups:
        intro.append(text); continue
    if style == 'Heading 2':
        m = re.match(r'^(\d+)\.\s+(.+)$', text)
        book = {'n': int(m[1]), 'title': m[2], 'desc': []}
        groups[-1]['books'].append(book); continue
    if book is None:
        groups[-1]['intro'] = (groups[-1]['intro'] + ' ' + text).strip(); continue
    m = re.match(r'^(Автор|Басылым|Жас \(каталог бойынша\)):\s*(.+)$', text)
    if m:
        book[FIELDS[m[1]]] = m[2]; continue
    m = re.match(r'^Тақырып:\s*(.+?)\s+·\s+Дереккөз:\s*(.+)$', text)
    if m:
        book['topics'] = [x.strip() for x in m[1].split(',')]; book['source'] = m[2]; continue
    book['desc'].append(text)

bad = [(g['title'], b['n'], k) for g in groups for b in g['books']
       for k in ('author', 'edition', 'age', 'topics', 'source') if k not in b] + \
      [(g['title'], b['n'], 'desc') for g in groups for b in g['books'] if not b['desc']]
if bad:
    sys.exit('missing fields: %r' % bad)
for g in groups:
    for b in g['books']:
        b['desc'] = '\n\n'.join(b['desc'])
json.dump({'intro': intro, 'groups': groups}, open(out, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(' · '.join('%s: %d' % (g['title'], len(g['books'])) for g in groups),
      '| total', sum(len(g['books']) for g in groups))
