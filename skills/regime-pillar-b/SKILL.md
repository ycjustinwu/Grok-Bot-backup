---
name: Regime Pillar B
description: >-
  Use this when scoring Regime Pillar B (ETF structure) for v6.4.5 — B1 HYG−LQD
  floors, B2 7-name offensive no MAGS, B3 % of found/45 with DATA GAP if found=0
  and Late Stage uses % not score; max /9.5 floor −6.5.
---
# Regime Pillar B (v6.4.5)

> Scoring math identical to v6.4.3. Version bump tracks orchestrator; do not invent new B rules.

Pillar B ETF Market Structure — **max /9.5**, floor **−6.5** (B1−2 + B2−3 + B3−1.5). From US-ETF CSV. Show every calc. Universes: `docs/etf-universes.md`. Half-open intervals unless noted.

## B1 Macro Liquidity /2 (floor −2; each 0.5)

- **B1-i** UUP 1W: <−0.5% → +0.5 | [−0.5%, +1.0%) → 0 | ≥+1.0% → −0.5
- **B1-ii** TLT 1W: ≥+0.5% → +0.5 | [−1.5%, +0.5%) → 0 | <−1.5% → −0.5
- **B1-iii** Spread = **HYG 1W − LQD 1W** (NOT VOO): ≥+0.5% → +0.5 | [−0.5%, +0.5%) → 0 | <−0.5% → −0.5
- **B1-iv** BKLN 1M: ≥0% → +0.5 | [−2%, 0%) → 0 | <−2% → −0.5
- GLD interpretation = **flag only** (no score)

## B2 Risk Appetite /5 (floor −3)

- **B2-i** Offensive 1W avg of **exactly 7**: QQQ, XLK, SOXX, IWM, MDY, XLI, ARKK (**no MAGS**) vs Defensive mean(XLU, XLP, XLV). Spread: ≥+2%→3 | [+1,+2)→2 | [0,+1)→1 | [−1,0)→0 | <−1%→−1
- **B2-ii** XLF 1W: ≥+1%→+1 | [−2%, +1%)→0 | <−2%→−1
- **B2-iii** SPHB−SPLV 1W: ≥+1%→+1 | [−1%, +1%)→0 | <−1%→−1
- Breadth quality flags (RSP/VOO/MAGS/MTUM) = no score. **RSP vs VOO ±0.5 flag logic still runs — never skip** (ops lock).

## B3 Thematic Breadth /2.5 (floor −1.5)

45 Tier 1 names (see universes / prompt).
`found` = count present in CSV (≤45).
- If **found = 0** → B3 = **0** + `DATA GAP（B3 無可用 Tier 1 數據，score=0）` — do **not** compute %.
- Else: missing tickers via missing_ticker_protocol; `positive_count` = found with 1W% > 0; **`% = positive ÷ found × 100`** (never ÷45 fixed).
  %≥70→2 | [50,70)→1 | [30,50)→0 | <30→−1; then apply RSP−VOO bonus/penalty ±0.5 per prompt (show found/45, positive, %).
- RSI14 >75 among found: count ≥3 → overheat flag (no score).

**Late Stage Warning** (Layer 1 skill): compares this B3 **%** to 50%, **not** the B3 score.

**Pillar B = B1+B2+B3 /9.5**. Never add Pillar C.
