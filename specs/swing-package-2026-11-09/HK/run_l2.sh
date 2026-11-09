#!/usr/bin/env bash
# v5.5.2 — run after ./run_daily.sh. Steps S3, S6, S7 of WORKFLOW_v55.md.
#   ./run_l2.sh prep   runs/run_20261106 [runs/run_20261105]   # S3
#   ./run_l2.sh check  runs/run_20261106                        # S6: exit 2 = do not send
#   ./run_l2.sh render runs/run_20261106                        # S7
#   ./run_l2.sh all    runs/run_20261106 [prev]                 # prep + check + render
# Paths may be given relative to where you invoke the script.
set -uo pipefail
CALLER=$(pwd)
HERE=$(cd "$(dirname "$0")" && pwd)

# v6.9: pin the market. run_l2.sh is a sibling of run_daily.sh, so run_daily's export
# never reaches it; an install also records its market in .swing_market.
if [ -z "${SWING_MARKET:-}" ] && [ -f "$HERE/.swing_market" ]; then
  SWING_MARKET=$(cat "$HERE/.swing_market" | tr -d ' \r\n')
fi
export SWING_MARKET="${SWING_MARKET:-us}"

abs() { case "${1:-}" in ""|/*) echo "${1:-}";; *) echo "$CALLER/$1";; esac; }
RUN=$(abs "${2:-}")
PREV=$(abs "${3:-}")
cd "$HERE"

auto_prev() {
  local cur="$1" prev
  prev=$(ls -d "$CALLER"/run_* "$CALLER"/runs/run_* 2>/dev/null | grep -v "^${cur}$" | sort | while read -r d; do
           [ -f "$d/L2_Input.csv" ] && echo "$d"
         done | tail -1)
  if [ -n "${prev:-}" ]; then echo "$prev"; else
    echo "" >&2
    echo "WARN: no earlier run with L2_Input.csv; Change_vs_Prev will be BASELINE" >&2
  fi
}

case "${1:-}" in
  prep)   [ -n "$PREV" ] || PREV=$(auto_prev "$RUN")
          python3 l2_prep.py "$RUN" ${PREV:+"$PREV"} ;;
  check)  python3 check_verdict.py "$RUN" ;;
  render) python3 render_report.py "$RUN" ;;
  all)    [ -n "$PREV" ] || PREV=$(auto_prev "$RUN")
          python3 l2_prep.py "$RUN" ${PREV:+"$PREV"} \
            && python3 check_verdict.py "$RUN" \
            && python3 render_report.py "$RUN" ;;
  *) echo "usage: $0 prep|check|render|all <run> [prev_run]"; exit 1 ;;
esac
