#!/usr/bin/env bash
# Install the US + HK swing screeners. Idempotent: re-running replaces code, keeps your runs/.
#   ./install.sh /opt/swing            # US -> /opt/swing/us, HK -> /opt/swing/hk
set -euo pipefail
TARGET="${1:-/opt/swing}"
HERE=$(cd "$(dirname "$0")" && pwd)

mkdir -p "$TARGET"
for part in US HK; do
  low=$(echo "$part" | tr 'A-Z' 'a-z')
  dest="$TARGET/$low"
  mkdir -p "$dest"
  if [ -d "$dest/runs" ]; then
    echo "keeping existing $dest/runs"
  fi
  tar -C "$HERE/$part" -cf - . | tar -C "$dest" -xf -
  # B1: pin market marker so HK never falls back to US when SWING_MARKET unset
  printf '%s\n' "$low" > "$dest/.swing_market"
  echo "installed $part -> $dest (marker=$low)"
done

# M5: chmod every .sh under the install (nested 02_CODE runners included)
find "$TARGET/us" "$TARGET/hk" -type f -name '*.sh' -exec chmod +x {} +
echo
echo "next:  python3 -m pip install -r $HERE/requirements.txt"
echo "       bash $HERE/verify.sh $TARGET"
