---
name: TV Abnormal Volume MCP
description: >-
  Use this when a US or HK market brief needs abnormal-volume UP/DOWN seeds (and
  the US mega-cap sweep) from the tvscreener script — not TradingView MCP.
  Justin paste still overrides. Market-cap gates are applied in the script.
---
# TV Abnormal Volume Screener

Pull abnormal-volume **UP** and **DOWN** seed lists with the **tvscreener script** **before** brief analysis. Do **not** use TradingView MCP (`user-Tradingview-xai` / `mcp-tv-run-screener`) for this job, and do not fall back to it if the script fails.

## Runtime

Always call through the venv:

```bash
/workspace/tvscreener-venv/bin/python /workspace/scripts/tv_av_screener.py \
  --market us \
  --session YYYY-MM-DD \
  --out-dir /workspace/us-brief-inputs/YYYY-MM-DD
```

Hong Kong (after 16:00 HKT): `--market hk` and `--out-dir /workspace/hk-brief-inputs/YYYY-MM-DD`.

Writes `av-up.csv`, `av-down.csv`, `av-tv-screener.json`, and (US only) `mega-up.csv` / `mega-down.csv`. Stdout is a short JSON receipt (`source: tvscreener`, `mcp: false`, counts, `mcap_present`). Market cap is filtered in the script; every kept row should have `market_cap_basic`.

## When

- Start of **US Market Daily Brief** or **港股收市簡報** (and any job that needs AV seeds).
- Run **after the cash session is closed** for that market (US after US close; HK after 16:00 HKT). Mid-session empty/partial lists are expected — do not treat as a hard failure during RTH; for the daily brief, wait until the close bar is final.

## Override

If Justin pastes or attaches an AV list for that session, **use his list as authoritative** and skip the script for that side. If he supplies nothing, the script is required.

## Columns (both markets)

Return: `name`, `close`, `change`, `market_cap_basic`, `relative_volume_10d_calc`, `Value.Traded`, `exchange`, `Perf.3M` (plus `symbol`, `sector`, `industry`).
Sort: `relative_volume_10d_calc` desc. Symbol type: common stock (TradingView type `stock`).

## US — `market: america` (OpenClaw AV)

| Gate | UP | DOWN |
| --- | --- | --- |
| `close` | > 1 | > 1 |
| `change` | ≥ +5 | ≤ −5 |
| `market_cap_basic` | > 5e9 (USD) | same |
| `relative_volume_10d_calc` | > 2 | > 2 |
| `Value.Traded` | > 5e6 (USD) | same |
| `Perf.3M` | none | none |

- **Post-filter:** drop `exchange == "OTC"` and any `OTC:`-prefixed symbols. Keep NYSE / NASDAQ / AMEX / similar listed venues. Report **raw count vs US-primary count** after OTC drop (in the receipt `raw` / `primary`).
- Limit: 300.

## US — mega-cap sweep (locked 2026-10-31)

**Second pass** every US brief session (in addition to OpenClaw AV):

| Gate | Value |
| --- | --- |
| `market` | `america` |
| symbol type | stock |
| `market_cap_basic` | ≥ 5e10 ($50B) |
| `change` | ≥ +3 **or** ≤ −3 (UP and DOWN sides) |
| RelVol / Value.Traded | **no** OpenClaw RelVol>2 / Value>$5M gate — cluster detection is the point |

- **Post-filter:** drop OTC.
- Read for **same-industry clusters**: 8–12 peers at −3% to −6% (or +3% to +6%) = day’s **震央** candidate for the parent brief opening / headline #1 — even if none cleared RelVol>2.
- Hand cluster summary (industry, tickers, % range, count) to [US Abnormal Volume](sand-workflow:us-abnormal-volume) / parent brief. Do not invent industry labels; use the script’s sector/industry fields or a known map.
- If this pass fails but OpenClaw AV succeeded, continue with AV and note mega-sweep OMIT under DATA GAPS.

## HK — `market: hongkong` (not `hong_kong`)

| Gate | UP | DOWN |
| --- | --- | --- |
| `close` | > 1 | > 1 |
| `change` | ≥ +5 | ≤ −5 |
| `market_cap_basic` | > 1e10 (HKD) | same |
| `relative_volume_10d_calc` | > 2.0 | > 1.5 |
| `Value.Traded` | > 5e6 (HKD) | same |
| `Perf.3M` | > 1 | none |

- The global screener returns market cap in **USD**. The script converts the 10B HKD gate at **7.80 HKD per USD** (peg mid) and records `hkd_per_usd` in the JSON. Do not call `set_currency('HKD')` — that blanks `market_cap_basic`. `Value.Traded` stays in HKD (price currency).
- DOWN uses RelVol **1.5** (asymmetric by design).
- Limit: 200.
- No extra exchange filter. Mega-cap sweep is **US-brief only** unless HK brief skill asks for an analogous pass.

## Output handoff

1. Build tables: **UP**, **DOWN**, and (US) **mega-cap sweep** cluster note from the script output (not from MCP).
2. Keep the CSV/JSON under the brief day folder (`av-tv-screener.json`).
3. Hand seeds to the next brief skill. **Do not re-gate** OpenClaw seeds that already passed the script filters (except the US OTC post-filter, already applied).
4. If the script errors or returns empty **after** the session close when criteria should have hits, DATA GATE: notify 總指揮 with market, side, command used, and error/counts — do not invent tickers, and do **not** retry via TradingView MCP. Empty UP with non-empty DOWN (or vice versa) can be valid — say so and continue.

## Anti-jobs

- Do not use TradingView MCP for AV or mega-cap seeds (no fallback).
- Do not run disabled Python OpenClaw scripts (`us_abnormal_volume_screener.py`, `hk_abnormal_volume_screener.py`).
- Do not use Browserless / box desktop to scrape TradingView when the script works.
- Do not invent RelVol, mcap, or prices.
- Do not apply the old US mcap>$10B gate — OpenClaw lock is **$5B**.
- Do not skip the US mega-cap sweep on US daily brief runs.
