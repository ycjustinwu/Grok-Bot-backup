#!/usr/bin/env bash
# safe-sync-v1 driver — builds payloads + prints SAFE APPLY CARD.
# Does NOT call Google Sheets API (no credentials on box).
# Agent must apply MCP steps exactly, then run verify_sheet_readback.py.
set -euo pipefail

ROOT=/workspace/us-swing-sim
TOOLS="$ROOT/tools"
PAYLOAD="$ROOT/.sheet_payloads"
PLAN="$PAYLOAD/apply_plan.json"
SPREADSHEET_ID=1mtSZo10jrCC_o4x0HnjjyrCEj_3FbBCcN8pgvZkU7v4

STRICT_FLAG=--strict
if [[ "${1:-}" == "--no-strict" ]]; then
  STRICT_FLAG=--no-strict
fi

echo "==> sync_sheet.py $STRICT_FLAG"
python3 "$TOOLS/sync_sheet.py" $STRICT_FLAG

if [[ ! -f "$PLAN" ]]; then
  echo "FAIL: apply_plan.json missing after sync" >&2
  exit 1
fi

python3 - "$PLAN" "$PAYLOAD" "$SPREADSHEET_ID" <<'PY'
import json, sys
from pathlib import Path

plan_path, payload_dir, sid = sys.argv[1], Path(sys.argv[2]), sys.argv[3]
plan = json.loads(Path(plan_path).read_text())
v = plan.get("verify") or {}
ranges = plan.get("managed_clear_ranges") or []
range_a1 = [f"{r['sheet']}!{r['cells']}" for r in ranges]
if not range_a1:
    # fallback from first batch_clear_values step
    for s in plan.get("steps") or []:
        if s.get("op") == "batch_clear_values":
            range_a1 = s.get("ranges") or []
            break

writes = [s for s in plan.get("steps") or [] if s.get("op") == "write_range"]
charts = [s for s in plan.get("steps") or [] if s.get("op") == "update_chart"]

print()
print("=" * 64)
print("SAFE APPLY CARD  ·  protocol=safe-sync-v1")
print("=" * 64)
print(f"spreadsheetId: {sid}")
print(f"sync_hkt:      {plan.get('sync_hkt')}")
print(f"marks_session: {plan.get('marks_session')}")
print(f"expect NAV:    {v.get('nav')}   cash: {v.get('cash')}")
print(f"expect Open:   {v.get('open_tickers')}")
print(f"expect Working:{v.get('working')}")
print()
print("RULES: never_hand_patch_cells · journal_leave_alone · verify_required")
print("BAN:   no ad-hoc cell patches · no partial tab writes · no delete tabs")
print()
print("EXACT ORDER (agent MCP — do not reorder / skip verify):")
print()
print("a) batch_clear_values ONCE with these 6 ranges (Journal OUT):")
for r in range_a1:
    print(f"     - {r}")
print()
print("b) write_range ×6  parseInput=true  values from $file: paths:")
for w in writes:
    name = w.get("payload")
    fpath = payload_dir / name
    print(f"     - {w.get('sheet')}!{w.get('cells')}  ←  $file:{fpath}")
print()
print("c) update_chart ×2 (if listed in apply_plan):")
for c in charts:
    print(f"     - chartId={c.get('chartId')} title={c.get('title')!r}")
print()
print("d) freeze / format_header / set_column_width (optional polish from plan)")
print()
print("e) READ BACK then write JSON (sheet-readback-done-v1):")
print("     Dashboard!A1:B16")
print("     Book!A1:J30")
print("     Positions!A1:L10")
print("     Orders!A1:L15")
print("     → e.g. /workspace/us-swing-sim/_finals/_sheet_readback_<TC>.json")
print("       schema: dashboard{NAV,cash,Open,Working,marks_session,raw_A1H20?}")
print("               book{raw_A1J40?} positions_open[] orders_working[]")
print()
print("f) VERIFY (required):")
print("     python3 /workspace/us-swing-sim/tools/verify_sheet_readback.py \\")
print(f"       --expect {plan_path} \\")
print("       --readback /workspace/us-swing-sim/_finals/_sheet_readback_<TC>.json")
print()
print("ONE-LINER RITUAL (build only — agent still applies MCP):")
print("  bash /workspace/us-swing-sim/tools/sheet_safe_sync.sh")
print("=" * 64)
PY

echo
echo "==> ledger smoke verify (--from-ledger)"
python3 "$TOOLS/verify_sheet_readback.py" --from-ledger
echo
echo "DONE: payloads ready under $PAYLOAD"
echo "Agent: follow SAFE APPLY CARD above; do NOT hand-patch cells."
