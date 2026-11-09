#!/usr/bin/env bash
# Daily driver for the US swing screener (v5.5.2).
#   ./run_daily.sh                          # scan tickers.txt into <cwd>/runs/run_YYYYMMDD/
#   SWING_ASOF=2026-11-03 ./run_daily.sh    # replay a past session (live data, as-of date)
#   SWING_VOL_MODE=REMARK ./run_daily.sh    # keep low-volume breakouts as A_SETUP with a note
# Exit codes: 0 ok · 2 an invariant FAILED · 1 the engine itself failed.
set -uo pipefail
CALLER=$(pwd)                     # run output is relative to where you invoke it, not to the script
HERE=$(cd "$(dirname "$0")" && pwd)
cd "$HERE"

# v6.9: an install records its market in .swing_market, so the same script works in a
# HK install and a US install without a hand-edited copy of this file.
if [ -z "${SWING_MARKET:-}" ] && [ -f "$HERE/.swing_market" ]; then
  SWING_MARKET=$(cat "$HERE/.swing_market" | tr -d ' \r\n')
fi
export SWING_MARKET="${SWING_MARKET:-us}"

MARKET="${SWING_MARKET:-us}"
LIST="tickers.txt"
[ "$MARKET" = "hk" ] && [ -f tickers_hk.txt ] && LIST="tickers_hk.txt"
TICKERS=$(grep -v '^[[:space:]]*#' "$LIST" | tr -d ' \r' | grep -v '^$' | paste -sd, -)
[ -z "$TICKERS" ] && { echo "no tickers in $LIST"; exit 1; }

ENGINE=us_swing_v55.py
[ -f "$ENGINE" ] || ENGINE=us_swing_v54.py
[ -f "$ENGINE" ] || { echo "no engine (us_swing_v55.py / us_swing_v54.py)"; exit 1; }

if [ "$MARKET" = "us" ]; then
  OUT="${SWING_OUTPUT_FOLDER:-$CALLER/runs/run_$(date +%Y%m%d)}"
else
  OUT="${SWING_OUTPUT_FOLDER:-$CALLER/runs/$MARKET/run_$(date +%Y%m%d)}"
fi
mkdir -p "$OUT"
echo "== scanning $(echo "$TICKERS" | tr ',' '\n' | wc -l | tr -d ' ') tickers -> $OUT (market $MARKET, vol mode ${SWING_VOL_MODE:-WATCH})"
SWING_TICKERS="$TICKERS" SWING_OUTPUT_FOLDER="$OUT" python3 "$ENGINE" || { echo "ENGINE FAILED"; exit 1; }

# every field the layer-2 playbook names must exist in the contract
PB=$(ls PLAYBOOK_v5.4.md ../rules/PLAYBOOK_v5.4.md ../01_RULES/PLAYBOOK_v5.4.md 2>/dev/null | head -1)
[ -n "$PB" ] && python3 check_fields.py "$PB" "$OUT/Contract_US.csv" | tee "$OUT/field_check.txt" || true

python3 invariants.py "$OUT" | tee "$OUT/invariants.txt"

# v6.9 + Justin 2026-11-07: a stale RS window yields Leader_OK=UNKNOWN — always warn the operator
python3 - "$OUT/Contract_US.csv" <<'PY' || true
import csv, sys
try:
    with open(sys.argv[1], newline='', encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
    bad = [r['Ticker'] for r in rows if str(r.get('Leader_OK', '')).upper() == 'UNKNOWN']
    if bad:
        print(f"WARN RS-stale -> Leader UNKNOWN ({len(bad)}): {', '.join(bad)}"
              "  # 資料窗口過期，唔好當 FAIL 亦唔好信佢")
except Exception:
    pass
PY

# forward outcome log is OPT-IN: this system has no backtest by design (DECISION_LOG D11)
[ "${SWING_FORWARD_LOG:-0}" = "1" ] && [ -z "${SWING_ASOF:-}" ] && python3 forward_log.py "$OUT" forward_log.csv || true

if grep -qE '^FAIL ' "$OUT/invariants.txt"; then
  echo "INVARIANT FAILED — read $OUT/Invariant_Report.md before trusting the list"
  exit 2
fi
echo "handoff: $OUT/handoff_US.md"
echo "output:  $(cd "$OUT" && pwd)"        # v6.9: absolute path, for cron logs
exit 0
