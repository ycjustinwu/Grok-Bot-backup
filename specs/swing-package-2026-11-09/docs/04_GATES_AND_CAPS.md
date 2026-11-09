# 04 — Gates and caps (the part that decides whether a ticket exists)

## Verdict pipeline

| Stage | Output | Meaning |
|---|---|---|
| S1–S2 `run_daily.sh` | `Summary_US.csv`, `Contract_US.csv` | facts only: levels, ADR, RS, volume, family |
| S3 `l2_prep.py` | `L2_Input.csv` | baseline verdict per name (BUY / STALK / WATCH / AVOID) |
| S4 (LLM) | `<T>_story.json`, `_search_log.json` | narrative only — no prices, no targets |
| S5 | `verdicts_<market>.jsonl` | story conviction merged with the baseline |
| S6 `check_verdict.py` | exit 0 / 2 | 0 = send, 2 = do not send |
| S7 `render_report.py` | `index.md`, 快報, image_pack | the deliverable |

## The Tradeable gate (v5.5.4 US / v6.10 HK)

A plan is only a ticket when **all** of these hold:

1. `risk <= cap_adr × ADR` — default `cap_adr = 1.2`
2. `risk% <= max(cap_pct, cap_adr × ADR%)` — default `cap_pct = 8.0`, so a high-ADR name gets a wider
   absolute allowance and a low-ADR name keeps the strict 8%
3. `room >= floor` — room from entry to the hard supply level, in R
4. `room@plan stop >= floor` — room measured against the **plan** stop, not a provisional 1×ADR

`floor` comes from the setup family: BREAKOUT 1.5R, PULLBACK 1.0R, REVERSAL 1.5R.

Failure is not a downgrade to "risky" — it removes the ticket:

- `Tradeable=FAIL` → the name is forced to **WATCH** (`l2_prep.tradeable_gate`)
- `generate_trigger` writes only `Tradeable=PASS` rows
- `check_verdict` **V4d** rejects any BUY/STALK whose `Tradeable != PASS`
- `invariants` **I30** fails the run if `Trigger_US.csv` contains a non-PASS row

Columns added by the gate: `Tradeable`, `Tradeable_Why`, `Room_At_Plan_Stop_R`, `Room_At_1_2ADR_R`.

A pending breakout is **not** exempt: the plan stop exists before the fill, so it is judged before the
fill (this is exactly how a 2.72×ADR STALK used to ship).

## Environment variables

| Var | Effect | Default |
|---|---|---|
| `SWING_RISK_ADR_CAP` | risk in ADR units | `1.2` |
| `SWING_RISK_PCT_CAP` | risk in percent (floats up to `cap_adr × ADR%`) | `8.0` |
| `SWING_ASOF` | replay a past session date | today |
| `SWING_VOL_MODE` | `REMARK` keeps low-volume breakouts as A_SETUP with a note | strict |
| `SWING_OUTPUT_FOLDER` | run directory | `runs/…` |
| `SWING_MARKET` | `us` / `hk` — selects list + verdicts file | `us` (HK script pins `hk`) |

## RS staleness

If ≥3 sessions are missing inside the 63-day RS window, every LEADER `FAIL` is downgraded to
`UNKNOWN`, `Leader_Why` is annotated `stale window — 資料不足，不作 FAIL`, and `run_daily.sh` prints

```
WARN RS-stale -> Leader UNKNOWN (n): 0700.HK, …
```

`UNKNOWN` blocks tickets exactly like `FAIL` (no BUY/STALK on an unknown leader) but the report must
say "insufficient data", never "trend broken".

## Invariants worth knowing

| ID | Claim |
|---|---|
| I11 | negative room implies `Risk_OK=FAIL` |
| I20 | `Trigger_US.csv` present, or explicitly warn that nothing is actionable |
| I28 | the Evidence long table reduces to the Contract gates |
| I30 | every ticket is `Tradeable=PASS` |
| V4c | BUY/STALK require `Risk_OK=PASS` |
| V4d | BUY/STALK require `Tradeable=PASS` |
