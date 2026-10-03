---
name: Regime Layer Context
description: >-
  Use this for Regime v6.4.5 Layer 0 anomaly scan, Layer 1 seven-group 1W excess
  ranking (+ 1D%/RelVol for Leading Sector volume), Layer 2 ACTIVE + cooling
  narratives, and US Market Monitor (CUP) ADDITIONAL Observation flags.
---
# Regime Layer Context (v6.4.5)

Silent computation for Section 7; feed Dashboard + Section 6 + **Fast-Track / Change C**. Universes: `docs/etf-universes.md`.

## Layer 0 — 1D Anomaly
Scan Tier1 + Layer2 + B1/B2 helpers: `|1D%| ≥ 5%`. Report ticker, 1D%, RelVol, group. RelVol≥2 confirmed; <1.5 weak. None → 「今日無 1D 異動」. Missing tickers → missing_ticker_protocol.

## Layer 1 — Preference (7 groups)
Rank by **1W excess vs VOO** (not 1M). Groups:
- P1 FCF/Quality: XLK, QQQ, XLF, **SCHD**, MAGS
- P2 Hardware/Infra: SOXX, SMH, XLI, PAVE, GRID, DTCR, DRAM, AIPO, HYDR
- P3 Rate-Cut/Biotech: XBI, GNOM, HEAL, OZEM, IDNA, IHI
- P4 Speculation: ARKK, MEME, IPO, WGMI, IBIT, WEED
- **P5 Defensive: XLU, XLP, XLV only** (SCHD removed from P5 — stays in P1)
- P6 Frontier Tech: WQTM, UFO, ROKT, DRNZ
- P7 Software/Cyber: IGV, BUG (2-name — lower confidence flag if #1/#2/weakest)

**Data pull (v6.4.5):** for **every** constituent extract **1D%, 1W%, 1M%, RSI14, RelVol** (1D+RelVol required for LS volume confirm).

Sustainability tags from 1M vs VOO (持續強勢 / 新興輪動 / 短期回調 / 趨勢性弱勢).
Output #1/#2 (must 1W excess >0 for Long themes else 「無明顯 long 主題」), weakest for 5C, full rank, VOO EMA alignment (info only). Include RSI14 avg for #1/#2 (Offensive Override).

### LEADING SECTOR (feeds FT + Change C)
- LS = Layer 1 **#1 by 1W excess**.
- If #1 = **P5 Defensive** → LS = **N/A** (FT/Change C auto-fail). P7 #1 = OK + low confidence.
- Volume confirm: over **present** names only — `avg(1D%) > 0` AND `avg(RelVol) ≥ 2.0`; found=0 → N/A + DATA GAP (no ÷0). Group average, not any-one-name.
- Also keep Defensive Warning when P5=#1 (DEFENSIVE ROTATION).

**Late Stage Warning:** P4=#1 AND B3 **% positive (of found)** < 50% AND McClellan reversing → SPECULATION LATE STAGE FLAG. (**Not** B3 score vs 50.)

## Layer 2 — Global narratives
ACTIVE only per N1–N4 rules in prompt (1M; VIXY Carry Unwind uses 1D — include VIXY 1D% when evaluating). One line each for Section 6. Also list narratives that **fell out** of ACTIVE vs prior session (**cooling**) — one line each.

## US Market Monitor → Layer 0 / Focus Themes (non-scoring)
After ETF Layer 0/1/2, apply CUP JSON from ingest (`us-market-monitor.json` — **must** exist from Drive self-pull unless data_gap):
1. **Pulse direction** only vs Stockbee Up4/Down4 (universes differ — never substitute counts into A1).
2. If MLI升% < ~40% while Checklist/indices look firm → flag 「領導股內部不一致」 into Layer 0 / 重要旗號.
3. Sector Top3 / Industry Top5 leader concentration → optional stock-level corroboration under Focus Themes (not a second Brief package).
4. Feed the daily **附加觀察** block; do not change TOTAL / stance math.

## CUP date lock (Justin forever 2026-09-18, US-only)
Sheet stamp **S** = US session **S−1**. For Regime session **D** → Summary/History **label D+1**. Disclose stamp→session. **HK Monitor is NOT D+1.** See `docs/cup-market-monitor.md`.
