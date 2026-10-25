#!/usr/bin/env bash
# Builds the site page (index.html) from tools/src, tools/data, tools/photos and tools/fonts.
# The full guide is NOT in the repository: pass its guide.json (made from guide.pdf with
#   pdftotext -layout guide.pdf guide.txt && python3 -I tools/src/build_guide.py guide.txt guide.json).
# Usage: tools/build.sh /path/to/guide.json [out.html]   (default out: index.html at the repo root)
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
guide=${1:?"guide.json жолын көрсетіңіз: tools/build.sh /path/to/guide.json"}
out=${2:-$here/../index.html}
src=$here/src
w=$(mktemp -d)
trap 'rm -rf "$w"' EXIT
step() { python3 -I "$src/$1" "${@:2}" >/dev/null; }

step assemble.py "$src/base.html" "$here/data/worksheets.json" "$guide" "$w/01.html"
step theme.py    "$w/01.html" "$w/02.html"      # ornament theme, phone/tablet layout
step library.py  "$w/02.html" "$w/03.html"      # «Талдауларым»
step help.py     "$w/03.html" "$w/04.html"      # «Қалай қолдану керек?»
step modern.py   "$w/04.html" "$w/05.html"      # modern look, opening cover
step photos.py   "$w/05.html" "$here/photos" "$w/06.html"
step glossary.py "$w/06.html" "$here/data/glossary.txt" "$w/07.html"
step kids.py     "$w/07.html" "$here/data/kids.json" "$w/08.html"
step save.py     "$w/08.html" "$w/09.html"      # save as Word / PDF
step shop.py     "$w/09.html" "$w/10.html"      # «Сатып алу» (WhatsApp)
step lab.py      "$w/10.html" "$w/11.html"      # «Зертхана»: кейіпкер психологиясы
step plot.py     "$w/11.html" "$w/12.html"      # сюжет пен композиция
step preview.py  "$w/12.html" "$w/13.html"      # guide preview (full text only in the PDF)
step tutor.py    "$w/13.html" "$w/14.html"      # «ЖИ тәлімгері» prompt
step labmore.py  "$w/14.html" "$w/15.html"      # 8 more tools, theory step, level
step tidy.py     "$w/15.html" "$w/16.html"      # «Кеңес» toggles, «Файл ▾»
step merge.py    "$w/16.html" "$w/17.html"      # «Нұсқаулық» inside «Дәптер»
step focus.py    "$w/17.html" "$here/fonts" "$w/18.html"   # «Фокус режимі»
step seo.py      "$w/18.html" "$out"                       # search and sharing tags
echo "built: $out"
