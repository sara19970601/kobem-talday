"""Check guide.json against guide.txt word for word; list table blocks."""
import json, re, sys
txt, gj = sys.argv[1], sys.argv[2]
g = json.load(open(gj, encoding='utf8'))['sections']
pages = open(txt, encoding='utf8').read().split('\f')
src = []
for no, p in enumerate(pages, 1):
    if no < 5:
        continue
    ls = [l for l in p.split('\n') if l.strip()]
    if ls and ls[0].strip() == 'КӨРКЕМ ШЫҒАРМАНЫ ТАЛДАУ': ls = ls[1:]
    if ls and re.fullmatch(r'\d+', ls[-1].strip()): ls = ls[:-1]
    src += ' '.join(ls).replace('​', ' ').split()
out = []
for s in g:
    if s['title']:
        out += (s['id'] + ('-БӨЛІМ.' if s['level'] == 1 else '.')).split() + s['title'].split()
    out += s['text'].replace('​', ' ').split()
print('words in body:', len(src), '| words extracted:', len(out), '| identical order:', src == out)
for s in g:
    for i, q in enumerate(s['text'].split('\n\n')):
        if '\n' in q:
            print('  table block:', s['id'], 'para', i, '|', q.split('\n')[0].strip()[:60])
