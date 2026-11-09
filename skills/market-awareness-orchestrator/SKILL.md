---
name: Market Awareness Orchestrator
description: >-
  Use this as the daily Market Awareness Orchestrator playbook — ingest Stockbee
  + breadth + ETF + Market Master (ΔLIFT/Pace trend-first), score A/B, stance
  v6.4.6, Trial carve-out / 今日動作 top bar, Rotation Delta (non-scoring), then 繁體中文 regime daily.
---
> **Canonical (2026-10-22):** Market Master `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` — tabs 美股市寬／美股行業／ETF 輪動（+ 港股市寬／形態篩選／Setup_Latest）. Doc: `/workspace/docs/market-master-canonical-2026-10-22.md`. Retired primary Monitor: `1XqUu…`.
> **動作層 (2026-10-22):** 今日動作＋linkage＋Trial carve-out — `docs/今日動作-trial-carve-out-2026-10-22.md`（唔改 TOTAL／hysteresis）。
> **Rotation Delta (2026-11-05):** non-scoring book-ETF churn — `docs/rotation-module-v1.1.md` + [rotation-delta](sand-workflow:rotation-delta).
> **Monitor 讀法 (2026-10-29):** 行業趨勢 = ΔLIFT＋Pace；|z| 顯著性 only — `docs/cup-market-monitor.md`.
# Market Awareness Orchestrator

Daily **Regime Scoring v6.4.6** end-to-end. Label: `v6.4.6 hysteresis multi-band confirm`. Source of truth:
`/workspace/refactored_market_awareness/docs/v6.4.3/regime-scoring-v6.4.3.txt` (scoring spine)
+ `docs/v6.4.5/fast-track-and-change-c.md` (FT / Change C / LS / FT memory)
+ `docs/CHANGELOG-v6.4.6.md` + `docs/regime-bands.md` (5B multi-band confirm).
**v6.4.6 = v6.4.3 scoring + v6.4.5 FT/CC + 5B multi-band confirm only** — do not invent scoring changes.

Default to action on the **silent** phase; complete every pillar before rendering.

## When Justin asks for today's market regime / 市場制度日報

1. [Regime Data Ingest](sand-workflow:regime-data-ingest) — Stockbee via [Stockbee T2108 Monitor](sand-workflow:stockbee-t2108-monitor) (**xlsx full history**), Breadth via [Breadth Daily Report](sand-workflow:breadth-daily-report) + [FRED VIX Term Structure](sand-workflow:fred-vix-term-structure), TradingView US-ETF CSV, **+ Market Master self-pull (`美股市寬`＋`美股行業`)** (always)
2. [Regime Pillar A](sand-workflow:regime-pillar-a) → /12 (floor −4)
3. [Regime Pillar B](sand-workflow:regime-pillar-b) → /9.5 (floor −6.5)
4. [Regime Layer Context](sand-workflow:regime-layer-context) → Layer 0/1/2
4.6. [Rotation Delta](sand-workflow:rotation-delta) → churn5/10/20 + 四檔判定（**non-scoring**；script `/workspace/market-awareness/rotation/rotation_calc.py`）
5. [Regime Modifiers And Stance](sand-workflow:regime-modifiers-and-stance) → modifiers, hysteresis, **Fast-Track / Change C / FT STATE**, short 5C, stance Steps 1–5, **+ Trial carve-out／今日動作／linkage／主題許可**
6. [ETF RS Overlay Ingest](sand-workflow:etf-rs-overlay-ingest) + [ETF RS Theme Tilt](sand-workflow:etf-rs-theme-tilt) — before render（主題許可要用 Favor／Avoid）
7. [Regime Daily Report](sand-workflow:regime-daily-report) → 繁體中文 deliverable（**最頂**今日動作＋中間 linkage，然後 Dashboard）

## Execution order (v6.4.6)

Silent compute: **Sections 1 → 2 → 3 → 4 → 5 → 7 → 0**, then Section 6 **Steps 1–5** + **Trial carve-out** (still silent).
**Only then** render Section 6 output + Section 8（頂欄先於 Dashboard）。
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
- **v6.4.6 5B:** upgrade pending target = today’s **raw band**; 2 consecutive same raw → effective may **jump multi-band**; pending FAIL + today’s raw **>** prior effective → **Intermediate Land** (effective = today raw today; clear pending) — Justin 2026-10-23; still **no** day-1 one-band ladder. Downgrade still immediate. FT/CC unchanged. See `docs/hysteresis-intermediate-land-2026-10-23.md`.
- **v6.4.6 Step 5 add-on (2026-10-01):** Index Drawdown Gate before V-REVERSAL (dd ≥8% / 5–8% / <5%) — stance only
- **動作層 (2026-10-22):** 今日動作三選一 + linkage + Trial carve-out（三條件齊先細碼試倉）+ 主題許可 Focus∩MM **ΔLIFT/Pace**（|z| 顯著性）∩ETF Favor — **never** into TOTAL／band／hysteresis／FT／numeric Exposure ceiling
- **Monitor 趨勢軸 (2026-10-29):** IndustryGroup 主讀 **ΔLIFT＋Pace**；|z| 過濾 only — `docs/cup-market-monitor.md`
- Scoring math **unchanged** from v6.4.3 — do not "upgrade" A1-ii / 0A④ / Pair7 / B3 / clips

## DATA GATE (highest priority)

Missing / stale / abnormal critical input → **STOP**, notify **總指揮** (→ Justin): what failed, source, expected vs got session date, what to fix. Never invent or paper over. Never continue past a failed gate.

## Side-channel

## US Market Monitor — ADDITIONAL Observation (**always self-pull**; **Market Master since 2026-10-22**)

Mirror HK After-Close Brief §五. Sheet `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk` (**Market Master**) tabs **`美股市寬`＋`美股行業`** — playbook `docs/cup-market-monitor.md`. Retired primary: `1XqUuQ4Q0cj1BwORSLeUbRi6c1zjHMUt6cghy9N1BdYk` (and older `1NMWO4-…`).

1. During ingest: **always** pull Market Master (Sheets MCP preferred) → 美股市寬 + 美股行業 (Summary/History equivalents + IndustryGroup). Prefer History Date = US session D; else D+1 stamp lock + disclose.
2. Capture: **動力股佔比%**, **SPY ATR**, **QQQ ATR**, IndustryGroup **ΔLIFT + Pace (trend primary)** + lift / 季度 median / |z| (significance filter only) — still non-scoring. Reading order: `docs/cup-market-monitor.md` (Cup Sir／Justin 2026-10-29).
3. During Layer 0 / Focus Themes: direction-only vs Stockbee 4% pulse; MLI升% / 動力股佔比 / ATR stretch flags; IndustryGroup **ΔLIFT／Pace 轉強／轉弱** vs Layer1 / ETF RS — disclose ΔLIFT↔Pace divergences (e.g. share↑/price↓ or low-level turn).
4. In daily report: render **### 附加觀察｜US Market Monitor（Market Master／股票層）** after 重要旗號 — **first** ΔLIFT／Pace trend lists, **then** |z|>1.96 as significance tags (never rank “strength” by |z| alone). Skeleton in playbook.
5. **Never** into Pillar A/B / TOTAL / hysteresis / FT / Exposure. Drive unreachable → one-line DATA GAP under 重要旗號; do **not** fail whole Regime DATA GATE. Never invent from Stockbee.
6. **Also feeds** 今日動作 linkage + Trial 條件② + 主題許可交叉（Focus ∩ ΔLIFT/Pace ∩ ETF Favor；|z| 加權 only — 仍非計分）。

## ETF RS Theme Tilt — ADDITIONAL Observation (non-scoring)

After US Market Monitor in the daily: run [ETF RS Overlay Ingest](sand-workflow:etf-rs-overlay-ingest) + [ETF RS Theme Tilt](sand-workflow:etf-rs-theme-tilt) → `### 附加觀察｜ETF RS 主題傾斜（非計分）` with Favor / Avoid / **趨勢觀察（2d+5d both-Rising；雙降且仍領先）**. Prefer Market Master tab **`ETF 輪動`**; legacy Drive `1cgrNJ…` only if Justin says. Overlay only — never TOTAL / band / hysteresis / FT / Exposure. Stale US trade date → DATA GAP omit section. **Favor／Avoid also feed 主題許可／禁止.**

## Rotation Delta — ADDITIONAL Observation (non-scoring) — Justin adopt 2026-11-05

After Layer Context, before Index Drawdown Gate / stance Steps: run [Rotation Delta](sand-workflow:rotation-delta). Script-first: `python3 /workspace/market-awareness/rotation/rotation_calc.py --matrix <PH_MT|ETF_Prices.csv>`. Prefer RS `PH_MT` then Market Master hidden tab **`ETF_Prices`**. Canon `/workspace/docs/rotation-module-v1.1.md`.

- Output: `rot_state` ∈ {制度輪動, 輪動中, 已定格, 延續} + churn5/10/20 + top8/old8. **Never** into TOTAL / band / hysteresis / FT / Change C / Exposure.
- Render via [Regime Daily Report](sand-workflow:regime-daily-report): daily `### 附加觀察｜輪動位移（非計分）` after ETF RS; escalate top-bar / 重要旗號 / 三、操作立場 only for ②③ per skill.
- Fallback: 5-day `S` proxy + `⚠️ 輪動數據代理`; never invent churn.

## Locked learnings (2026-09-09)

Keep where they do not conflict with v6.4.6: A2 pattern checklist (zero-rejection), Pair3 near-zero fails, PRE-FOMC ≤7d, Layer2 cooling list, BUG/IGV split on short, cite 前值 only from thread archive/json.
**From v6.4.3 (still in force):** Stockbee prev/today from **xlsx**; DEGRADED = McClellan/VIX only; A1-ii parity-first; A3 NYSI-only zero-cross; B3 found-denom; Step3 EFFECTIVE (unless FT); ratchet new-floor; Pair7 improving includes CU.
**New in v6.4.5:** Fast-Track, Change C, Leading Sector volume, FT STATE Day2, Q11.
**New in v6.4.6 only:** hysteresis multi-band confirm (pending = raw band; multi-band jump on day-2).
- **Intermediate Land (Justin 2026-10-23):** pending FAIL but raw > prior effective → land effective at raw today (升一級／落地中間帶); not day-1 ladder.
- **Index Drawdown Gate (Justin 2026-10-01):** when T2108<20, before V-REVERSAL — SPX dd vs 252-session high from Stockbee S&P. ≥8% PASS; <5% FAIL (no V-REVERSAL, ⚠️ 非底部訊號); 5–8% NEUTRAL (V-REVERSAL OK but 首注輕試 + Exposure 10% cap). Stance-only; no TOTAL/band change. See `regime-modifiers-and-stance` Step 5 + `docs/CHANGELOG-v6.4.6.md`.
- **今日動作＋Trial (Justin 2026-10-22):** top-bar action layer; Trial three-gate carve-out; skill challenged **once** then follow rules — do not re-litigate philosophy in each daily.

Refs: `/workspace/refactored_market_awareness/docs/` + `CHANGELOG-v6.4.6.md` + `CHANGELOG-v6.4.5.md` + `今日動作-trial-carve-out-2026-10-22.md`.

**US Monitor date lock (Justin forever 2026-09-18; sheet→Market Master 2026-10-22, **US-only**):** sheet stamp S = US session S−1; for Regime session D use Summary/History **label D+1**; disclose stamp→session. Prefer exact session Date when tab is session-dated. **HK Monitor is NOT D+1.** See `docs/cup-market-monitor.md`.
