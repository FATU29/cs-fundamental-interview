#!/bin/sh
# Render every Mermaid source (<Topic>/img/*.mmd) to a PNG next to it.
# Skips files whose PNG is newer than the source. Run: sh tools/render-diagrams.sh
# Usage: sh tools/render-diagrams.sh [path/to/file.mmd ...]
set -eu

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS="$ROOT/tools"
MMDC="$TOOLS/node_modules/.bin/mmdc"

if [ ! -x "$MMDC" ]; then
  echo "mmdc not found. Run: cd tools && PUPPETEER_SKIP_DOWNLOAD=1 npm install" >&2
  exit 1
fi

if [ "$#" -gt 0 ]; then
  FILES="$*"
else
  FILES="$(find "$ROOT" -path "$TOOLS" -prune -o -path '*/node_modules' -prune -o -name '*.mmd' -print)"
fi

[ -n "$FILES" ] || { echo "No .mmd files found."; exit 0; }

fail=0
while IFS= read -r src; do
  [ -n "$src" ] || continue
  out="${src%.mmd}.png"
  if [ -f "$out" ] && [ "$out" -nt "$src" ]; then
    echo "skip   $out (up to date)"
    continue
  fi
  # -b white: light background so labels stay readable in every site theme.
  # -s 2: 2x scale for sharp text on retina/mobile.
  if "$MMDC" -i "$src" -o "$out" -p "$TOOLS/puppeteer-config.json" -b white -s 2 -q; then
    echo "render $out"
  else
    echo "FAIL   $src" >&2
    fail=1
  fi
done <<EOF
$FILES
EOF
exit "$fail"
