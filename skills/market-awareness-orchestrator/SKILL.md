---
name: Market Awareness Orchestrator
description: >-
  Use this as the daily Market Awareness Orchestrator playbook — ingest Stockbee
  xlsx + breadth + ETF CSV, score Pillars A/B, layers, stance (v6.4.6 hysteresis multi-band confirm + v6.4.5 Fast-Track /
  Change C), then emit the 繁體中文 regime daily.
---
# Market Awareness Orchestrator

Daily **Regime Scoring v6.4.6** end-to-end. Label: `v6.4.6 hysteresis multi-band confirm`. Source of truth:
`/workspace/refactored_market_awareness/docs/v6.4.3/regime-scoring-v6.4.3.txt` (scoring spine)
+ `docs/v6.4.5/fast-track-and-change-c.md` (FT / Change C / LS / FT memory)
+ `docs/CHANGELOG-v6.4.6.md` + `docs/regime-bands.md` (5B multi-band confirm).
**v6.4.6 = v6.4.3 scoring + v6.4.5 FT/CC + 5B multi-band confirm only** — do not invent scoring changes.

Default to action on the **silent** phase; complete every pillar before rendering.

## When Justin asks for today's market regime / 市場制度日報

1. [Regime Data Ingest](sand-workflow:regime-data-ingest) — Stockbee via [Stockbee T2108 Monitor](sand-workflow:stockbee-t2108-monitor) (**xlsx full history**), Breadth via [Breadth Daily Report](sand-workflow:breadth-daily-report) + [FRED VIX Term Structure](sand-workflow:fred-vix-term-structure), TradingView US-ETF CSV, **+ CUP Market Monitor self-pull from Google Drive** (always)
2. [Regime Pillar A](sand-workflow:regime-pillar-a) → /12 (floor −4)
3. [Regime Pillar B](sand-workflow:regime-pillar-b) → /9.5 (floor −6.5)
4. [Regime Layer Context](sand-workflow:regime-layer-context) → Layer 0/1/2
5. [Regime Modifiers And Stance](sand-workflow:regime-modifiers-and-stance) → modifiers, hysteresis, **Fast-Track / Change C / FT STATE**, short 5C, stance Steps 1–5
6. [Regime Daily Report](sand-workflow:regime-daily-report) → 繁體中文 deliverable

## Execution order (v6.4.6)

Silent compute: **Sections 1 → 2 → 3 → 4 → 5 → 7 → 0**, then Section 6 **Steps 1–5** (still silent).
**Only then** render Section 6 output + Section 8.
Section 6 “no raw tables / concise” applies to the **rendered** text only.

## Version guard (hard)

- **NO Pillar C.** **NO** Section 5D trade-unit table.
- Caps: Pillar A `/12` | Pillar B `/9.5` | **TOTAL `/21.5`**
- Floors: A1 −2 | Pillar A −4 | B1 −2 | B2 −3 | B3 −1.5 | Pillar B −6.5 (A −3 is NOT the floor — print `A −3 (floor −4)`)
- **Prior-day revision (2026-09-29):** if Stockbee xlsx PREV row ≠ prior run's `stockbee-1a.json` today → re-score prior day Pillar A on revised row (B unchanged) → print revised prior TOTAL + Δ vs revised (archive prior still drives 5B); write `prior_revised` / `delta_revised` in regime-summary.json
- Daily must contain literal line `MARKET=US` under the title
- TOTAL range **[−10.5, 21.5]**; all scores multiples of **0.5**
- A2 clipped **[−1, 4]**; A3 clipped **[−1, 2]**
- Section 0 ①② = **VOO EMA** from CSV (not Stockbee DMA)
- B2-i = **7** offensive names (**no MAGS**); B1-iii = **HYG vs LQD**
- P5 Defensive = **XLU, XLP, XLV only** (SCHD in P1 only)
- B3: `% = positive/found×100`; disclose `found/45`; `found=0` → B3=0 + DATA GAP
- Late Stage Warning compares B3 **%** vs 50%, not B3 score
- 0A④ = simple AND `$NYMO ≥ 0 AND $NAMO ≥ 0` — **not** priority-order state
- Section 0 Checklist Trend ≠ Section 6 Step 1 Deployment Trend (stance uses Deployment only)
- **v6.4.5 add-ons:** Fast-Track (4%≥3 + VIX drop>10% + LS volume → same-day upgrade, Day1 Exposure ≤30%); Change C (T2108<20% only, relax V-REVERSAL ② if B2-i≥+2% + LS volume); LS = Layer1 #1 (P5 → N/A); FT STATE Day2 memory (unknown → keep 30%); Q11 self-check
- **v6.4.6 5B:** upgrade pending target = today’s **raw band**; 2 consecutive same raw → effective may **jump multi-band**; fail restarts from new raw — **no one-band / adjacent ladder**. Downgrade still immediate. FT/CC unchanged.
- **v6.4.6 Step 5 add-on (2026-10-01):** Index Drawdown Gate before V-REVERSAL (dd ≥8% / 5–8% / <5%) — stance only
- Scoring math **unchanged** from v6.4.3 — do not "upgrade" A1-ii / 0A④ / Pair7 / B3 / clips

## DATA GATE (highest priority)

Missing / stale / abnormal critical input → **STOP**, notify **總指揮** (→ Justin): what failed, source, expected vs got session date, what to fix. Never invent or paper over. Never continue past a failed gate.

## Side-channel

## US Market Monitor — ADDITIONAL Observation (**always self-pull Google Drive**)

Mirror HK After-Close Brief §五. Sheet `1NMWO4-bmO8clwceamTGXZjG7rSYpljoz2jCupTk-zCQ` — playbook `docs/cup-market-monitor.md`.

1. During ingest: **always** Google Drive `read_file_content` on CUP sheet (do not wait for attachment) → Summary + History + Sector/Industry (ignore Raw). Apply D+1 stamp lock.
2. During Layer 0 / Focus Themes: direction-only vs Stockbee 4% pulse; MLI升% flags; sector tilt notes.
3. In daily report: render **### 附加觀察｜US Market Monitor（CUP／股票層）** after 重要旗號 (skeleton in playbook).
4. **Never** into Pillar A/B / TOTAL. Drive unreachable → one-line DATA GAP under 重要旗號; do **not** fail whole Regime DATA GATE. Never invent CUP from Stockbee.

## ETF RS Theme Tilt — ADDITIONAL Observation (non-scoring)

After CUP Monitor in the daily: run [ETF RS Overlay Ingest](sand-workflow:etf-rs-overlay-ingest) + [ETF RS Theme Tilt](sand-workflow:etf-rs-theme-tilt) → `### 附加觀察｜ETF RS 主題傾斜（非計分）` with Favor / Avoid / **趨勢觀察（2d+5d both-Rising；雙降且仍領先）**. Overlay only — never TOTAL / band / hysteresis / FT / Exposure. Stale US trade date → DATA GAP omit section.

## Locked learnings (2026-09-09)

Keep where they do not conflict with v6.4.6: A2 pattern checklist (zero-rejection), Pair3 near-zero fails, PRE-FOMC ≤7d, Layer2 cooling list, BUG/IGV split on short, cite 前值 only from thread archive/json.
**From v6.4.3 (still in force):** Stockbee prev/today from **xlsx**; DEGRADED = McClellan/VIX only; A1-ii parity-first; A3 NYSI-only zero-cross; B3 found-denom; Step3 EFFECTIVE (unless FT); ratchet new-floor; Pair7 improving includes CU.
**New in v6.4.5:** Fast-Track, Change C, Leading Sector volume, FT STATE Day2, Q11.
**New in v6.4.6 only:** hysteresis multi-band confirm (pending = raw band; multi-band jump on day-2).
- **Index Drawdown Gate (Justin 2026-10-01):** when T2108<20, before V-REVERSAL — SPX dd vs 252-session high from Stockbee S&P. ≥8% PASS; <5% FAIL (no V-REVERSAL, ⚠️ 非底部訊號); 5–8% NEUTRAL (V-REVERSAL OK but 首注輕試 + Exposure 10% cap). Stance-only; no TOTAL/band change. See `regime-modifiers-and-stance` Step 5 + `docs/CHANGELOG-v6.4.6.md`.

Refs: `/workspace/refactored_market_awareness/docs/` + `CHANGELOG-v6.4.6.md` + `CHANGELOG-v6.4.5.md`.

**CUP date lock (Justin forever 2026-09-18, **US-only**):** sheet stamp S = US session S−1; for Regime session D use Summary/History **label D+1**; disclose stamp→session. **HK Monitor is NOT D+1.** See `docs/cup-market-monitor.md`.
