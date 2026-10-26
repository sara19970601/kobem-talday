#!/usr/bin/env bash
# Runs the browser tests (Playwright + Chromium) against a page, default: index.html at the repo root.
# Usage: tools/tests/run.sh [page.html]
# Needs Node.js and the `playwright` package with Chromium (npm i -D playwright && npx playwright install chromium).
set -uo pipefail
here=$(cd "$(dirname "$0")" && pwd)
page=$(cd "$(dirname "${1:-$here/../../index.html}")" && pwd)/$(basename "${1:-index.html}")
w=$(mktemp -d)
cp "$page" "$w/index.html"
port=$((8800 + RANDOM % 100))
(cd "$w" && python3 -m http.server "$port" >/dev/null 2>&1) & srv=$!
trap 'kill $srv 2>/dev/null; rm -rf "$w"' EXIT
for i in $(seq 1 50); do curl -s "localhost:$port" >/dev/null && break; sleep 0.2; done
url="http://localhost:$port/index.html"
fails=0
run() {
  local name=$1; shift
  local outp; outp=$(cd "$w" && node "$here/$name.test.js" "$@" 2>&1)
  local pass; pass=$(grep -c '^PASS' <<<"$outp")
  # The page's own request to localhost is not an outside request.
  local bad; bad=$(grep -v '^PASS' <<<"$outp" | grep -E '^FAIL|Error' | grep -v 'no network.*"http://localhost' || true)
  if [ -n "$bad" ]; then fails=$((fails + 1)); echo "✗ $name ($pass passed)"; echo "$bad" | sed 's/^/    /'; else echo "✓ $name ($pass passed)"; fi
}
for t in lab plot tutor more merge preview shop kids gloss; do run "$t" "$url" "$w"; done
run saveword "$url" "$w"
run lib "$url"
run cover "$w/index.html"
run account "$url" "$w"
echo; [ "$fails" -eq 0 ] && echo "Барлық тест өтті." || echo "$fails тест жиынтығында қате бар."
exit "$fails"
