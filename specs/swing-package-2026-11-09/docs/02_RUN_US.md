# 02 — Run the US screener and setup

Working directory for every command: `/opt/swing/us/02_CODE`.

## 1. Universe (US has no cron — you supply the list)

```bash
cat > tickers.txt <<'EOF'
AAPL
MSFT
NVDA
EOF
```

or scan an ad-hoc list without touching `tickers.txt`:

```bash
cd /opt/swing/us && ./scan553.sh "AAPL,MSFT,NVDA" run_adhoc
```

## 2. Scan (S1–S2) → Summary_US.csv, Contract_US.csv (113 cols), Trigger_US.csv

```bash
cd /opt/swing/us/02_CODE
SWING_OUTPUT_FOLDER=runs/us/run_$(date +%Y%m%d) bash run_daily.sh
```

Replay a past session with live data: add `SWING_ASOF=2026-11-06`.
Exit codes: `0` ok · `2` invariant failed · `1` engine failed.

## 3. L2 prep + gate + render (S3, S6, S7)

```bash
bash run_l2.sh all runs/us/run_<date> [previous_run]
```

- `prep` → `L2_Input.csv` (one row per name, the LLM's input)
- `check` → `check_verdict`; **exit 2 means do not send**
- `render` → `index.md`, per-name 快報, `<T>_image_pack.md`

Run the steps separately when debugging: `bash run_l2.sh prep|check|render <run>`.

## 4. Story handoff (S4) → verdicts (S5)

`L2_Input.csv` is the input for the story model. It must return, per name:

- `<TICKER>_story.json` — narrative fields only
- `<TICKER>_search_log.json` — the queries and URLs it used
- `verdicts_US.jsonl` — one row per name, `ticker` + `verdict`

Schema and hard rules: `docs/05_HANDOFF_S4_S5.md`.

```bash
cd /opt/swing/us/02_CODE
python3 story_search_sync.py runs/us/run_<date>     # merges stories into the run
bash run_l2.sh check runs/us/run_<date>             # must exit 0
bash run_l2.sh render runs/us/run_<date>
```

## 5. Measured reference run (44 names, as_of 2026-11-06, v5.5.4)

```
BUY 1   WATCH 26   AVOID 17      # Tradeable gate on
Trigger_US.csv = 1 ticket: DNA  entry 11.29  stop 9.92  risk 12.1% (1.09xADR)  room 1.96R
```

Before the Tradeable gate the same date produced `BUY 2 / STALK 4`; the six demotions are listed in
`PATCH_NOTES_v5.5.4.md` with their exact `Tradeable_Why` strings. A run that still shows STALK rows
with `2.4xADR` stops means the gate is not installed.
