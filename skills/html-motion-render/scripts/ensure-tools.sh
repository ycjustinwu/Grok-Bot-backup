#!/usr/bin/env bash
# Ensure node, ffmpeg/ffprobe, a Chromium-family browser and playwright-core exist.
# Prints CHROME=<path> and TOOLS=<dir> on success. Safe to re-run.
set -euo pipefail
TOOLS="${HTML_MOTION_TOOLS:-$HOME/.local/share/html-motion-tools}"
need(){ command -v "$1" >/dev/null 2>&1 || { echo "MISSING: $1" >&2; return 1; }; }
need node; need npm
if ! need ffmpeg || ! need ffprobe; then
  (sudo -n apt-get install -y ffmpeg >/dev/null 2>&1 || apt-get install -y ffmpeg >/dev/null 2>&1) || { echo "Install ffmpeg manually" >&2; exit 1; }
fi
CHROME="${CHROME:-}"
for c in google-chrome google-chrome-stable chromium chromium-browser; do
  [ -z "$CHROME" ] && command -v "$c" >/dev/null 2>&1 && CHROME="$(command -v "$c")"
done
[ -z "$CHROME" ] && for c in /opt/pw-browsers/chromium*/chrome-linux/chrome "$HOME"/.cache/ms-playwright/chromium*/chrome-linux/chrome; do
  [ -x "$c" ] && CHROME="$c" && break; done
mkdir -p "$TOOLS"
if [ ! -d "$TOOLS/node_modules/playwright-core" ]; then
  (cd "$TOOLS" && { [ -f package.json ] || npm init -y >/dev/null; } && npm i playwright-core >/dev/null 2>&1)
fi
if [ -z "$CHROME" ]; then
  (cd "$TOOLS" && npx -y playwright-core install chromium >/dev/null 2>&1) || true
  CHROME="$(ls -d "$HOME"/.cache/ms-playwright/chromium*/chrome-linux/chrome 2>/dev/null | head -1)"
fi
[ -z "$CHROME" ] && { echo "No Chromium found" >&2; exit 1; }
echo "CHROME=$CHROME"; echo "TOOLS=$TOOLS"
