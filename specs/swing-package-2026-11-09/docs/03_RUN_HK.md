# 03 — Run the HK screener and setup

Working directory: `/opt/swing/hk`. The HK engine is a **separate install** (v6.10, 116 columns);
it never imports the US code and writes `verdicts_hk.jsonl`, not `verdicts_US.jsonl`.

## 1. Universe

`tickers_hk.txt` holds the default list (39 codes across 41 lines at build time). Six-digit codes, no suffix:

```
0700
9988
3690
```

`earnings_overrides.csv` (53 data rows / 54 lines at build time) carries verified earnings dates. **Re-installing must
not clobber it** — the US installer had exactly that bug; check `wc -l earnings_overrides.csv` after
any copy and restore from your own backup if it collapses to one template row.

## 2. Scan

```bash
SWING_OUTPUT_FOLDER=runs/hk/run_$(date +%Y%m%d) bash run_daily.sh
```

The HK engine prints a staleness warning when the daily bar is missing and a **RS-stale WARN** line
naming tickers whose LEADER gate was downgraded to `UNKNOWN` — that is by design: a thin RS window is
"insufficient data", never "trend broken".

## 3. L2 + gate + render

```bash
bash run_l2.sh all runs/hk/run_<date>
```

`run_l2.sh` pins `SWING_MARKET=hk` itself (the old package looked for `verdicts_us.jsonl` inside the HK
tree and silently found nothing). Exit `2` from `check` = do not send.

```bash
bash verify_hk.sh          # 24 invariants + market lock + overrides parse -> ALL CHECKS PASSED
python3 tests/suite.py     # 51/51
```

## 4. Measured reference run (39 names, as_of 2026-11-06, v6.10)

```
BUY 2 (6862 0.63xADR, 0386 0.99xADR)   WATCH 14   AVOID 23      tickets 2
2269.HK 药明生物  Tradeable=FAIL: risk=2.72xADR > 1.2; risk=17.3% > 8%; room@plan stop=0.63R < 1.5
```

If 2269 still comes out as STALK, the v6.10 gate is not installed (that was its exact pre-fix state).

## 5. Story handoff

Same schema as the US (`docs/05_HANDOFF_S4_S5.md`); `handoff/S4_INSTRUCTION_HK.md` is a filled example
for one real session. Story text never changes verdict / entry / stop — the program owns those.
