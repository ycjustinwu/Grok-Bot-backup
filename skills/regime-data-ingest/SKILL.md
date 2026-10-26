---
name: Regime Data Ingest
description: >-
  Use this to gather daily regime v6.4.5 inputs — Stockbee xlsx, StockCharts
  breadth + FRED VIX, US-ETF CSV, and self-pull Market Master 美股市寬＋美股行業 (always;
  never wait for attachment).
---
# Regime Data Ingest

Daily inputs for Market Regime Scoring **v6.4.5/v6.4.6**. Complete fully; show values. No invented history.

## DATA GATE

Missing / stale / abnormal critical input → **STOP**, notify 總指揮. Never fabricate. Empty/truncated CSV, stale Stockbee snapshot treated as live, OCR fails cross-check → gate.

## Sources

1. **Stockbee (1A)** — attach/build full Monitor **xlsx** via [Stockbee T2108 Monitor](sand-workflow:stockbee-t2108-monitor).
   - **TODAY** = row with `max(Date)`; **PREV DAY** = next most recent trading date. Sort by Date explicitly — do not assume row order.
   - Reconstruct multi-day Stockbee patterns (A1 weakness, A2 patterns, Pair 5/6, Deployment Trend S&P legs) from the **xlsx**.
   - **Thread is NOT needed for Stockbee fields.**
   - **Prior-row revision check (2026-09-29):** diff xlsx PREV row vs prior run's `regime-output/<prev>/stockbee-1a.json` `today`. Any change → disclose old→new, re-score prior-day Pillar A (A1 + A2 zone/T2108; McClellan from thread; B unchanged) → hand revised prior TOTAL + Δ to report (`prior_revised`, `delta_revised`).
   - **SPX Index Drawdown (2026-10-01, for Step 5 gate):** from xlsx **S&P** column, compute `spx_high_252` = max close over last min(252, available) sessions, `spx_drawdown` = (high − today) / high. Hand to stance with `window_n` and `window_short: true` if N<252 (`⚠️ 窗口不足`). Non-scoring; only feeds Step 5 Index Drawdown Gate when T2108<20.

2. **Breadth (1B)** — [Breadth Daily Report](sand-workflow:breadth-daily-report) + [FRED VIX Term Structure](sand-workflow:fred-vix-term-structure) (same-date VIXCLS÷VXVCLS pair; one source consistently inside any Pair 7 lookback).
   - Table: $VIX, VIX/VXVCLS, $NAMO, $NYMO, $NYSI, $NASI (+ optional $SPXA200R/50R/20R).
   - Keep **VIX_prev** (prior session) for Fast-Track drop >10% test.

3. **US-ETF-complete CSV (1C)** — Justin attaches TradingView export → extract all tickers in `docs/etf-universes.md` (**1D%/1W%/1M%/RSI14/RelVol**/VOO EMAs — 1D+RelVol required for Leading Sector volume). Never invent prices.

4. **US Market Monitor (Market Master)** — **self-pull** Google Sheet `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` tabs **`美股市寬`＋`美股行業`** every run (see section below). Not a TOTAL input. Canonical: `/workspace/docs/market-master-canonical-2026-10-22.md`.

## Thread-history rules (v6.4.5)

**Thread-only fields:** McClellan history, VIX/VXVCLS 3-day trend + Pair 7 five-day lookback, prior day's score + regime (hysteresis 5B), **Fast-Track STATE** (Day1/Day2). Reconstruct from `latest-state.json` / prior reports. Never invent. Unknown FT state → keep 30% cap + flag.

**FIRST RUN / no McClellan-VIX history:**
`⚠️ DEGRADED MODE — 無 McClellan/VIX 歷史數據`
→ skip multi-day McClellan/VIX patterns and hysteresis 2-day confirmation (apply today's band directly); list components affected.
→ **Stockbee multi-day still OK** (from xlsx).

## Protocols

- **missing_ticker_protocol:** absent CSV ticker → exclude from avg/count; list under 重要旗號 as data gap; state which score component is affected. No estimate / stale carry / invent.
- **ratio_fallback_protocol:** A1-i or A1-iii denominator = 0 → assign **MAX** sub-score + flag `EXTREME RATIO（分母=0，賦最高分）`. B3 `found=0` → B3=0 + `DATA GAP（B3 無可用 Tier 1 數據，score=0）` (do not %).

## Notes

- VOO = SPX proxy for Section 0 EMA checks and Layer 1 excess.
- P5 Defensive extraction = XLU, XLP, XLV only (SCHD stays in P1 / B3 universe).

Hand structured 1A/1B/1C extract to scoring skills.

## US Market Monitor (Market Master) — **MANDATORY self-pull**

**Every Regime ingest** (Justin forever; sheet → Market Master 2026-10-22):

1. **Yourself** pull sheet `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` tabs **`美股市寬`** + **`美股行業`** (Sheets MCP preferred) — do **not** wait for an attached export.
2. Date pick: prefer History/Summary **Date = US session D**. If only Asia stamp exists, fall back to D+1 lock and disclose.
3. Capture: sample, Up4, Down4, SMA20/50, MLI n / % / 升%, pool, leader%, **動力股佔比%**, **SPY ATR / QQQ ATR / S&P 500**, Sector Top3, Industry Top5, **IndustryGroup** rows with |z|>1.96 (lift, z, ΔLift(21), pace) — 2–3 strong + 2–3 weak, vs prior session row.
4. Prefer History Date = US session D when available; else D+1 stamp lock and disclose.
5. Write `/workspace/regime-output/YYYY-MM-DD/us-market-monitor.json` (`data_gap: false` on success; include atr_spy, atr_qqq, momentum_pct, industry_group_sig).
6. Non-scoring ADDITIONAL Observation only — never into Pillar A/B/TOTAL; never invent from Stockbee.
7. If Drive/Sheets fails after one retry → `data_gap: true` (does **not** trip main Regime DATA GATE).

Playbook: `/workspace/refactored_market_awareness/docs/cup-market-monitor.md` (Market Master since 2026-10-22).
**HK Monitor is NOT D+1.**
**Retired primary (do not pull):** `1XqUuQ4Q0cj1BwORSLeUbRi6c1zjHMUt6cghy9N1BdYk` · `1NMWO4-bmO8clwceamTGXZjG7rSYpljoz2jCupTk-zCQ`.
