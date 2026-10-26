---
name: HK Unusual Movers
description: >-
  Use this when screening Hong Kong unusual movers for the after-close brief —
  primary source is TradingView MCP (OpenClaw HK criteria) after 16:00 HKT;
  Justin paste overrides; no post-seed 100億 gate.
---
# HK Unusual Movers

Screen Hong Kong stocks for unusual after-close movers before headlines.

## 1. Get seeds (locked 2026-10-14)

**Primary:** run [TV Abnormal Volume MCP](sand-workflow:tv-abnormal-volume-mcp) for **HK** UP and DOWN **after 16:00 HKT** (close bar final). Mid-session empty lists are normal — wait for the after-close brief window.

**Override:** if Justin pastes/attaches an AV list for that session, treat it as authoritative and skip MCP for that side.

Do **not** run `hk_abnormal_volume_screener.py` / browser TradingView scrape when MCP works.

HK MCP gates (OpenClaw): close>$1; UP chg≥+5% / DOWN ≤−5%; mcap>$10B HKD; RelVol UP>2.0 / DOWN>1.5; Value.Traded>$5M HKD; UP only Perf.3M>1%; `market: hongkong`.

## 2. Accept seeds

- MCP seeds already passed gates — **do not** FAIL/filter again on 100億 / H-share mcap.
- Justin paste seeds: always valid; do **not** cross-check close / chg% / RV / names vs Yahoo or 披露易.
- Optional mcap note for context only, never a pass/fail column.

## 3. Steps

1. Session date = HK cash day; note 16:00 HKT close.
2. Load MCP (or Justin) UP/DOWN lists. Cluster by sector. If ≥3 names in the same sector move >5% the same way, flag **sector-driven** vs single-stock.
3. Seed table for the brief: `XXXX.HK` | Chinese name | close | % change | RV | sector | sector-linked? (Y/N). **No PASS/FAIL gate column.**
4. For **non-seed** tape (indices, mega-caps, 北水), cite public sources; never invent.

## 4. Verify (minimal)

- Confirm a seed source exists for the session (MCP result and/or Justin paste).
- MCP error after close → STOP / escalate to 總指揮.
- Empty UP or DOWN alone can be valid — continue.
- If checks find nothing wrong, auto-hide verification clutter.

## Anti-jobs

- Do not invent prices, volumes, or tickers.
- Do not FAIL seeds on market cap after they cleared MCP / Justin.
- Do not re-validate Justin’s seed tape against Yahoo / 披露易.
- Do not run disabled Python OpenClaw TV scripts.
