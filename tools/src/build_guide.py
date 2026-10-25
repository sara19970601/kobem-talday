"""Split guide.txt (pdftotext -layout) into sections; verify; write guide.json.
Usage: python3 -I build_guide.py guide.txt guide.json"""
import json, re, sys

HEADER = 'КӨРКЕМ ШЫҒАРМАНЫ ТАЛДАУ'
TOC_PAGES = {3, 4}          # 1-based
SKIP_PAGES = {1, 2}         # cover + title page (front matter, not body)
CH = re.compile(r'^\s*(\d+)-БӨЛІМ\.\s*(.*)$')
SUB = re.compile(r'^\s*(\d+\.\d+)\.\s+([А-ЯЁӘІҢҒҮҰҚӨҺ].*)$')
TABLE_GAP = re.compile(r'\S\s{3,}\S')
BULLET = re.compile('^(\\s*)(•|\\d{1,2}\\.|-)\u200b?\\s+')
CAPS_CONT = re.compile(r'^[А-ЯЁӘІҢҒҮҰҚӨҺA-Z0-9 ,:;«»\-–—/()]+$')

src, out = sys.argv[1], sys.argv[2]
pages = open(src, encoding='utf8').read().split('\f')

# 1. Strip running header (first non-empty line), page number (last non-empty
#    line), cover/title and TOC pages.
body = []
for no, page in enumerate(pages, start=1):
    if no in TOC_PAGES or no in SKIP_PAGES:
        continue
    lines = page.split('\n')
    idx = [i for i, l in enumerate(lines) if l.strip()]
    if not idx:
        continue
    if lines[idx[0]].strip() == HEADER:
        lines[idx[0]] = ''
    if re.fullmatch(r'\d+', lines[idx[-1]].strip()):
        lines[idx[-1]] = ''
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and not lines[0].strip():
        lines.pop(0)
    body.append(lines)

# Typical right edge of a full text line.
edges = sorted(len(l.rstrip()) for p in body for l in p if l.strip())
FULL = edges[int(len(edges) * 0.90)] * 0.80

# 2. Join pages. A paragraph that runs over a page break is kept together
#    when the last line of the page reaches the right edge.
lines = []
for p in body:
    if lines and lines[-1].strip() and len(lines[-1].rstrip()) < FULL \
            and not p[0].strip()[:1].islower():
        lines.append('')
    lines.extend(p)

# 3. Split at chapter / subsection headings only.
sections = [{'id': 'pre', 'level': 0, 'title': None, 'lines': []}]
i = 0
while i < len(lines):
    l = lines[i]
    m = CH.match(l) or SUB.match(l)
    if m:
        title = m.group(2).strip()
        # Heading continued on the next line(s): all-caps, no blank line between.
        while (CH.match(l) or title.isupper()) and i + 1 < len(lines) \
                and lines[i + 1].strip() and CAPS_CONT.match(lines[i + 1].strip()) \
                and not re.match(r'^\s*\d', lines[i + 1]) and len(lines[i + 1].strip()) < 60:
            i += 1
            title += ' ' + lines[i].strip()
        sections.append({'id': m.group(1), 'level': 1 if CH.match(l) else 2,
                         'title': title, 'lines': []})
    else:
        sections[-1]['lines'].append(l)
    i += 1

# 4. Paragraphs: blank-line blocks; tables kept as laid out; prose lines joined.
def paragraphs(block_lines):
    out, blocks, cur = [], [], []
    for l in block_lines + ['']:
        if l.strip():
            cur.append(l.rstrip())
        elif cur:
            blocks.append(cur); cur = []
    def is_row(l):
        return TABLE_GAP.search(l.strip()) and not BULLET.match(l)
    def in_table(l):
        return l.startswith(' ') and not BULLET.match(l)
    for b in blocks:
        rows = [i for i, l in enumerate(b) if is_row(l)]
        st = en = None
        if rows:
            # Table run: first..last column row, widened by indented lines
            # (cells wrapped onto their own lines). Needs 3+ lines.
            st, en = rows[0], rows[-1]
            while en + 1 < len(b) and in_table(b[en + 1]):
                en += 1
            while st > 0 and in_table(b[st - 1]):
                st -= 1
        if st is not None and en - st + 1 >= 3:
            out.extend(prose(b[:st]))
            ind = min(len(l) - len(l.lstrip()) for l in b[st:en + 1])
            out.append('\n'.join(l[ind:] for l in b[st:en + 1]))
            out.extend(prose(b[en + 1:]))
        else:
            out.extend(prose(b))
    return out

def prose(b):
    """Join wrapped lines. Bullets start items. A line well short of the
    block's right edge ends a paragraph, unless the next line starts in
    lowercase (then the sentence simply continues)."""
    out, para, item_indent = [], [], None
    if not b:
        return out
    full = max(len(l.rstrip()) for l in b) * 0.8
    def flush():
        if para:
            out.append(re.sub(r'\s+', ' ', ' '.join(para)).strip())
            para.clear()
    for k, l in enumerate(b):
        bm = BULLET.match(l)
        indent = len(l) - len(l.lstrip())
        if bm:
            flush()
            # Items flush at column 0 ('- …', '2. Мінез. …') continue at column 0
            # and end at a short line; indented items use a hanging indent.
            item_indent = len(bm.group(0)) if bm.group(1) and bm.group(2) != '-' else None
            para.append(bm.group(2) + ' ' + l[bm.end():].strip())
        else:
            if item_indent is not None and indent < item_indent - 2:
                flush(); item_indent = None
            para.append(l.strip())
        nxt = b[k + 1].strip() if k + 1 < len(b) else ''
        if len(l.rstrip()) < full and not nxt[:1].islower():
            flush(); item_indent = None
    flush()
    return out

result = []
for s in sections:
    paras = paragraphs(s['lines'])
    if s['id'] == 'pre' and not paras:
        continue
    result.append({'id': s['id'], 'level': s['level'], 'title': s['title'], 'text': '\n\n'.join(paras)})

# 5. Verify.
ids = [s['id'] for s in result]
dups = sorted({x for x in ids if ids.count(x) > 1})
need = [str(n) for n in range(1, 17)] + ['2.%d' % n for n in range(1, 25)]
missing = [x for x in need if x not in ids]
chapters = [s for s in result if s['level'] == 1]
subs = [s for s in result if s['level'] == 2]
print('chapters found:', len(chapters), [s['id'] for s in chapters])
print('subsections found:', len(subs), [s['id'] for s in subs])
print('lead-in section:', 'yes' if result[0]['id'] == 'pre' else 'no')
if dups:
    print('DUPLICATE ids:', dups)
if missing or dups:
    print('MISSING:', missing)
    sys.exit(1)
print('missing: none')
json.dump({'sections': result}, open(out, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
