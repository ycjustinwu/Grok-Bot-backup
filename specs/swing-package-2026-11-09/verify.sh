#!/usr/bin/env bash
# Prove the install: compile every module, run both regression suites, print the counts.
#   ./verify.sh /opt/swing
set -uo pipefail
TARGET="${1:-/opt/swing}"
HERE=$(cd "$(dirname "$0")" && pwd)
PY="${PYTHON:-python3}"
command -v "$PY" >/dev/null || { echo "no $PY on PATH"; exit 1; }
fail=0

echo "== 1. python compile"
find "$TARGET/us" "$TARGET/hk" -name '*.py' -not -path '*/runs/*' -print0 \
  | xargs -0 -n1 "$PY" -m py_compile || fail=1
echo "   ok"

echo "== 2. US regressions (expect ALL PASSED, 29 cases)"
( cd "$TARGET/us/02_CODE" && "$PY" tests/regressions.py ) || fail=1

echo "== 3. HK suite (expect 51/51 passed)"
( cd "$TARGET/hk" && "$PY" tests/suite.py ) || fail=1

echo
if [ "$fail" = 0 ]; then echo "VERIFY: PASS"; else echo "VERIFY: FAIL"; fi
exit "$fail"
