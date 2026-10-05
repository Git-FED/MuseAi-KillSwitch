#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"; test -s favicon.svg || { echo 'missing favicon.svg'; exit 1; }
command -v rsvg-convert >/dev/null 2>&1 || { echo 'Install librsvg (rsvg-convert) to generate PNGs'; exit 1; }
for size in 180 192 512; do rsvg-convert -w "$size" -h "$size" favicon.svg -o "assets/icon-${size}.png"; done
cp assets/icon-180.png assets/apple-touch-icon.png
printf 'favicon assets generated\n'
