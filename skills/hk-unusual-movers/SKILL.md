---
name: HK Unusual Movers
description: >-
  Use this when screening Hong Kong stocks for unusual movers from Justin’s
  manual TradingView AV paste (or heatmaps) before writing an after-close brief.
  No 100億 market-cap gate; Justin’s seed tape is authoritative.
---
# HK Unusual Movers

Screen Hong Kong stocks for unusual after-close movers. Use this before writing headlines.

## Criteria (for Justin's TradingView AV paste — locked 2026-09-30)

Justin’s pasted UP/DOWN list is **always valid**. Treat seed close / chg% / RV / names / sectors as given.

- **No market-cap gate** — do **not** FAIL or filter on 100億 / H-share / whole-company mcap (removed 2026-09-30). Optional mcap note for context only, never a pass/fail column.
- Do **not** cross-check seed close / chg% / RV / Chinese names vs Yahoo or 披露易 for validation.
- Day change and RV thresholds are whatever Justin’s paste already applied (his TV screen). Do not re-gate.

## Discovery sources

1. **Justin manual abnormal-volume list (PRIMARY — locked 2026-09-18; TV trust locked 2026-09-30)** — Justin pastes UP/DOWN movers (chat table, CSV, or files under `/workspace/hk-brief-inputs/YYYY-MM-DD/`). **Do NOT** run `/workspace/tools/hk-abnormal-volume/hk_abnormal_volume_screener.py`, `tradingview_screener`, or any TradingView scanner API. Scripts are disabled.
2. **HKEJ Stock360 Industry（行業熱圖）** — https://stock360.hkej.com/marketWatch/Industry — secondary discovery only after Justin list is in (for sector colour / non-seed mega-caps).
3. **HKEJ Stock360 Spot** — lower priority (many small-caps).
4. Futu / other heatmaps if needed for non-seed tape only.

If Justin has not provided abnormal-volume yet, **STOP** and ask 總指揮 / Justin — do not scrape TV.

## Steps

1. Pull the session date and note HKT close (16:00). Load Justin’s abnormal-volume paste/CSVs only.
2. Accept every seed as listed. Cluster by sector from his tags (or obvious business). If ≥3 names in the same sector move >5% the same way, flag **sector-driven** vs single-stock.
3. Output a seed table for the brief: `XXXX.HK` | Chinese name (from Justin / common usage) | close | % change | RV | sector | sector-linked? (Y/N). **No PASS/FAIL/SOFT FAIL gate column.**
4. Optional mcap may appear as context in prose, never as a filter.
5. For **non-seed** tape (indices, mega-caps, 北水 names), cite public sources; never invent. If sources conflict on non-seed figures, prefer HKEX / HKEJ and note gaps `[來源，日期]`.

## Verify (minimal)

- Confirm Justin’s list is present for the session date.
- If something is missing or unreadable → STOP / escalate.
- **If checks find nothing wrong, auto-hide verification clutter** in the brief (no identity/RV cross-tables, no method dumps).

## Anti-jobs

- Do not invent prices, volumes, or tickers.
- Do not FAIL seeds on market cap.
- Do not re-validate Justin’s seed tape against Yahoo / 披露易.
- Do not keep mega-caps with small moves in the seed table — this skill is the AV seed list + light sector clustering.
- Do not run Python TradingView abnormal-volume screener (disabled 2026-09-18).
- Do not create or re-enable a cron for TV scanner fetch.
- If Justin’s movers list is missing, STOP and escalate — never invent or scrape.
