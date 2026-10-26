---
name: TV Abnormal Volume MCP
description: >-
  Use this when a US or HK market brief needs abnormal-volume UP/DOWN seeds —
  pull from TradingView MCP (user-Tradingview-xai mcp-tv-run-screener) with
  OpenClaw criteria before analysis; Justin paste overrides if he supplies one.
---
# TV Abnormal Volume MCP

Pull abnormal-volume **UP** and **DOWN** seed lists via **TradingView MCP** (`user-Tradingview-xai` → `mcp-tv-run-screener`) **before** brief analysis. Prefer MCP over paste, OpenClaw cron, Python scripts, or browser.

## When

- Start of **US Market Daily Brief** or **港股收市簡報** (and any job that needs AV seeds).
- Run **after the cash session is closed** for that market (US after US close; HK after 16:00 HKT). Mid-session empty/partial lists are expected — do not treat as a hard failure during RTH; for the daily brief, wait until the close bar is final.

## Override

If Justin pastes or attaches an AV list for that session, **use his list as authoritative** and skip MCP for that side. If he supplies nothing, MCP is required.

## Columns (both markets)

Return: `name`, `close`, `change`, `market_cap_basic`, `relative_volume_10d_calc`, `Value.Traded`, `exchange`, `Perf.3M`.
Sort: `relative_volume_10d_calc` desc. `symbol_types`: `["stock"]`.

## US — `market: america`

| Gate | UP | DOWN |
| --- | --- | --- |
| `close` | > 1 | > 1 |
| `change` | ≥ +5 | ≤ −5 |
| `market_cap_basic` | > 5e9 (USD) | same |
| `relative_volume_10d_calc` | > 2 | > 2 |
| `Value.Traded` | > 5e6 (USD) | same |
| `Perf.3M` | none | none |

- Filters example UP: `{ "close": [1, null], "change": [5, null], "market_cap_basic": [5000000000, null], "relative_volume_10d_calc": [2, null], "Value.Traded": [5000000, null] }`
- DOWN: `change: [null, -5]`, same other gates.
- **Post-filter:** drop `exchange == "OTC"` (MCP cannot express `≠ OTC` in filters). Keep NYSE / NASDAQ / AMEX / similar listed venues.
- Limit: 300 (MCP cap 1000 OK).

## HK — `market: hongkong` (not `hong_kong`)

| Gate | UP | DOWN |
| --- | --- | --- |
| `close` | > 1 | > 1 |
| `change` | ≥ +5 | ≤ −5 |
| `market_cap_basic` | > 1e10 (HKD) | same |
| `relative_volume_10d_calc` | > 2.0 | > 1.5 |
| `Value.Traded` | > 5e6 (HKD) | same |
| `Perf.3M` | > 1 | none |

- UP adds `"Perf.3M": [1, null]`.
- DOWN uses RelVol **1.5** (asymmetric by design).
- Limit: 200.
- No extra exchange filter (`set_markets` equivalent = `market: hongkong`).

## Output handoff

1. Build two tables: **UP** and **DOWN** (ticker, close, chg%, RelVol, Value.Traded, mcap, exchange; HK add Perf.3M for UP).
2. Save under the brief day folder if useful, e.g. `/workspace/us-brief-inputs/YYYY-MM-DD/av-tv-mcp.json` or `/workspace/hk-brief-inputs/YYYY-MM-DD/av-tv-mcp.json`.
3. Hand the seed list to the next brief skill (US Abnormal Volume linkage / HK Unusual Movers clustering). **Do not re-gate** seeds that already passed MCP filters (except the US OTC post-filter).
4. If MCP errors or returns empty **after** the session close when criteria should have hits, DATA GATE: notify 總指揮 with market, side, filters used, and error/totalCount — do not invent tickers. Empty UP with non-empty DOWN (or vice versa) can be valid for that session — say so and continue.

## Anti-jobs

- Do not run disabled Python OpenClaw scripts (`us_abnormal_volume_screener.py`, `hk_abnormal_volume_screener.py`).
- Do not use Browserless / box desktop to scrape TradingView when MCP works.
- Do not invent RelVol, mcap, or prices.
- Do not apply the old US mcap>$10B gate — OpenClaw lock is **$5B**.
