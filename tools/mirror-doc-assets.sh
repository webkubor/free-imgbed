#!/usr/bin/env bash
# Mirror repository images into the built Pages site.
set -euo pipefail
cd "$(dirname "$0")/.."
output=docs/.vitepress/dist
test -f "$output/index.html"

for directory in */; do
  case "${directory%/}" in docs|web|tools|node_modules|design|brand) continue ;; esac
  image=$(find "$directory" -type f \( \
    -iname '*.png' -o -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.webp' -o \
    -iname '*.gif' -o -iname '*.svg' -o -iname '*.bmp' -o -iname '*.mp4' -o \
    -iname '*.mov' -o -iname '*.webm' -o -iname '*.avif' \) -print -quit)
  if [ -n "$image" ]; then
    cp -R "${directory%/}" "$output/"
  fi
done
