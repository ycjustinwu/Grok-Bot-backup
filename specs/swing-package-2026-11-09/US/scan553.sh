#!/usr/bin/env bash
# Ad-hoc US swing scan (v5.5.3 package layout). No cron — Justin supplies the universe.
#   ./scan553.sh "AAPL,MSFT,NVDA"          # scan + L2 prep
#   ./scan553.sh /path/tickers.txt run_x   # tickers from a file
# Exit: 0 ok · 2 invariant FAIL · 1 engine failed
set -uo pipefail
cd "$(dirname "$0")"
export HOME="${SWING_HOME:-$HOME}"
SRC="${1:?usage: scan553.sh \"T1,T2,...\"|<file> [run_folder]}"
OUT="${2:-run_$(TZ=Asia/Hong_Kong date +%Y%m%d_%H%M)}"

if [ -f "$SRC" ]; then
  TICKERS=$(tr -s ' \t\r\n' ',' < "$SRC" | sed 's/,,*/,/g; s/^,//; s/,$//')
else
  TICKERS=$(echo "$SRC" | tr -d ' ' | tr '[:lower:]' '[:upper:]')
fi
n=$(echo "$TICKERS" | tr ',' '\n' | grep -c .)
echo "== $n tickers -> $OUT"
mkdir -p "$OUT"
cd 02_CODE
SWING_TICKERS="$TICKERS" SWING_OUTPUT_FOLDER="../$OUT" HOME=${SWING_ROOT:-$PWD} python3 us_swing_v55.py || { echo "ENGINE FAILED"; exit 1; }
python3 check_fields.py ../01_RULES/PLAYBOOK_v5.4.md "../$OUT/Contract_US.csv" | tee "../$OUT/field_check.txt"
python3 invariants.py "../$OUT" | tee "../$OUT/invariants.txt"
if grep -qE '^FAIL ' "../$OUT/invariants.txt"; then
  echo "INVARIANT FAILED — read $OUT/Invariant_Report.md; do not trust the list"
  exit 2
fi
python3 l2_prep.py "../$OUT" || true
cd ..
echo "== done: $OUT"
# Trim per-ticker intermediate dumps (keeps Contract/L2/reports).
# KEEP_RAW=1 skips cleanup. Missing scripts/clean_runs.sh soft-fails (B2 2026-11-09).
if [ "${KEEP_RAW:-0}" != "1" ]; then
  CLEAN="${SWING_ROOT:-$PWD}/scripts/clean_runs.sh"
  if [ -x "$CLEAN" ] || [ -f "$CLEAN" ]; then
    bash "$CLEAN" "$OUT" | tail -2 || echo "== clean_runs non-zero (ignored)"
  else
    echo "== skip clean_runs (no $CLEAN); KEEP_RAW=1 to silence"
  fi
fi
