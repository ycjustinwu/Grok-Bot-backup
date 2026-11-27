# US swing sim — script-first open helpers

中／EN · local files only · model decides · code executes · zero invented prices

## When to run (open Soft Final)

| Step | Script | Agent still does |
|------|--------|------------------|
| 1. Hermes gate + extract | `hermes_gate.py --pack … [--ticker T]` | Decide OPEN/SKIP from AUTHORIZE + 四問 |
| 2. Book crowding | `book_snapshot.py` | Respect max 7 / cash-slot |
| 3. Size R$ | `size_position.py --entry --stop [--thin-room] [--paper-probe-r]` | Choose thin_room / paper_probe_r |
| 4. Soft Final skeleton | `soft_final_stub.py --tc … --decision-json … --out …` | Fill narrative / PINNED / VERIFY |
| 5. Ledger write (optional) | `open_working_limit.py … [--dry-run]` | Confirm before non-dry write |

Track Soft Finals stay on track skill; these scripts cover **open/skip** grind.

## UNTY example chain (Hermes Nov5 pack)

```bash
PACK=/workspace/second-brain/2026-11-05/hermes-nov5
TOOLS=/workspace/us-swing-sim/tools

# 1) Gate + Contract/Trigger/verdict (expect gate PASS, warning l2_absent)
python3 $TOOLS/hermes_gate.py --pack "$PACK" --ticker UNTY --json

# 2) Book header
python3 $TOOLS/book_snapshot.py

# 3) Size — FULL (acceptance 344). Do NOT pass --thin-room unless Room∈[1.0,1.5] or Justin forces.
python3 $TOOLS/size_position.py --entry 58.10 --stop 56.654 --json
# → shares 344 · r_usd ≈497.76 · effective_r ≈497.42

# 4) Soft Final stub from agent-built decision JSON
python3 $TOOLS/soft_final_stub.py \
  --tc TC-YYYYMMDD-xx \
  --decision-json /tmp/decision.json \
  --out /workspace/us-swing-sim/_finals/TC-YYYYMMDD-xx.md

# 5) Working limit (dry-run first)
python3 $TOOLS/open_working_limit.py \
  --ticker UNTY --limit 58.1 --stop 56.654 --shares 344 --r-usd 497.42 \
  --soft-supply 58.83 --hard-room 60.28 --paper-probe \
  --source "$PACK" --tc TC-YYYYMMDD-xx --dry-run
```

## thin_room note

- Skill 四問: Room_To_Supply_R in **1.0–1.5** → half size + tag `thin_room`.
- Hermes §3.4 UNTY acceptance Room **1.5076** → **FULL 344** (default `--thin-room` OFF).
- AUTHORIZE may keep honesty tag `thin_room` while sizing full — do not auto-half from the tag alone.

## Self-test

```bash
python3 /workspace/us-swing-sim/tools/size_position.py --self-test
# or
bash /workspace/us-swing-sim/tools/test_size_position.sh
```

## Out of scope

- No Sheet MCP / TV MCP inside these scripts
- No permanent `rules.json` edits
- No Second brain edits
- Banned Soft Final tokens: `RR_` `Target_` `Setup_Type` `Adjusted_Stop`

## Justin defaults 2026-11-06
- thin_room: default OFF; pass `--thin-room` when Room∈[1.0,1.5] or forced half.
- paper_probe: Deep Bear / smaller-bet → auto `--paper-probe-r 0.5`.

## Sheet safe sync (safe-sync-v1) — ONLY update path

Root cause of messy Excel: agents hand-applied many clear/write MCP calls and sometimes patched cells.  
**Fix:** one scripted path. Build on box → agent applies MCP in fixed order → automatic verify gate.

```bash
# 1) Build payloads + print SAFE APPLY CARD (no Sheets API on box)
bash /workspace/us-swing-sim/tools/sheet_safe_sync.sh

# 2) Agent applies MCP exactly as the card says:
#    a) batch_clear_values once (6 managed ranges; Journal OUT)
#    b) write_range ×6 parseInput=true from .sheet_payloads/*_write.json
#    c) update_chart ×2
#    d) freeze/format optional
#    e) read Dashboard A1:B16 + Book A1:J30 + Positions A1:L10 + Orders A1:L15 → readback JSON
#    f) verify:
python3 /workspace/us-swing-sim/tools/verify_sheet_readback.py \
  --expect /workspace/us-swing-sim/.sheet_payloads/apply_plan.json \
  --readback /workspace/us-swing-sim/_finals/_sheet_readback_<TC>.json

# Smoke without Sheet:
python3 /workspace/us-swing-sim/tools/verify_sheet_readback.py --from-ledger
```

| Script | Role |
|--------|------|
| `sync_sheet.py --strict` | Rebuild `.sheet_payloads/*` + `apply_plan.json` (`protocol=safe-sync-v1`) |
| `sheet_safe_sync.sh` | Runs sync + prints SAFE APPLY CARD |
| `verify_sheet_readback.py` | Gate: NAV/cash/open/working + banned strings |

**Bans:** no ad-hoc cell patches · no partial tab writes · no delete tabs · Journal leave alone · no invented NAV.
See `../SHEET_CONTRACT.md`.

**sheet-sync-even-quiet-v1** (Justin t96u): run this ritual after every post-close track, even when there are no fills / cancels / exits and the book is empty. Do not skip the Sheet because nothing traded. Pre-open does not sync.

## Daily pre-open + post-close (token-save, 2026-11-14)

Biggest token burn was the model re-reading rules and hand-writing ledger/briefs.  
**Ladder:** Connector (one TradingView MCP batch) → Script → agent relays the brief + does Sheet/TV MCP apply.

```bash
TOOLS=/workspace/us-swing-sim/tools

# 0) What to fetch (open + working + observe)
python3 $TOOLS/pre_open_check.py --print-symbols
# → NASDAQ:UNTY,NYSE:CRL,NYSE:EL

# 1) Pre-open (~22:00 HKT) — never fills, never changes cash/shares
#    Save MCP mcp-tv-get-symbol-data-batch (close + premarket_*) as marks JSON:
python3 $TOOLS/pre_open_check.py --marks /tmp/preopen_marks.json          # dry-run brief
python3 $TOOLS/pre_open_check.py --marks /tmp/preopen_marks.json --apply  # write pre_open_latest + journal

# 2) Post-close (~06:00 HKT) — official 1D OHLC required (open,high,low,close). No invented prices.
python3 $TOOLS/track_session.py --marks /tmp/official_1d.json             # dry-run brief
python3 $TOOLS/track_session.py --marks /tmp/official_1d.json --apply --sync-payloads
# then: bash $TOOLS/sheet_safe_sync.sh → MCP apply → verify_sheet_readback.py
# TV us shortlist 351605193: script prints desired set; agent adds/removes.

# Self-test (tmp copies of the book; live ledger untouched)
python3 $TOOLS/test_daily_scripts.py
```

Marks JSON shape:

```json
{
  "session": "2026-11-13",
  "source": "TradingView MCP mcp-tv-get-ohlcv 1D + mcp-tv-get-symbol-data-batch",
  "checked_hkt": "2026-11-14 06:05 HKT",
  "marks": {
    "UNTY": {
      "open": 58.73, "high": 59.2, "low": 58.1, "close": 58.915,
      "volume": 33815, "ema9": 58.314453492083246, "sma20": 57.8815,
      "premarket_close": 58.68, "premarket_change_pct": 0.574, "premarket_volume": 136
    }
  }
}
```

`--apply` is required to write. Default is dry-run. Re-running the same `marks_session` is a no-op unless `--force`.

| Script still does | Agent still does |
|-------------------|------------------|
| WATCH_GAP / HOLD / TIGHT from documented precedents (≤2.20% / ≥4.25%; in-between asks, no invented cutoff) | One TV MCP batch; paste/save JSON |
| GAP_SL / HARD_SL / EMA9 grace / trim-1/3+BE / better-price fill + stop reanchor / 5% away cancel / stalk lifetime | Relay 繁中 brief to Justin |
| Ledger + journal + Soft Final stub | Sheet MCP apply + readback; TV shortlist add/remove |
| Annotate room ≤0.3R | Thesis invalid (only fills if already queued) |
| post-trim-hold-v1 (no time-stop ask) | Time-stop ask if script flags it; observe thesis-clean if list not empty |

**Hard bans in these scripts:** no invented OHLC; no supply-half (revoked); no live broker; no Second brain edits; no regime rescore; no Sheet MCP inside the script.

Accepted against TRACK-20261113 fixtures: NAV 100607.70, rooms −0.0588 / 0.2295 / 0.6937, UNTY pre-open WATCH_GAP 2.12%.
