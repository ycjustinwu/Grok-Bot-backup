# Regime / Market Awareness (v6.4.6)

Market Awareness Orchestrator daily: Regime Scoring v6.4.6 — Pillars A/12 + B/9.5 = TOTAL/21.5, layers, modifiers, **hysteresis multi-band confirm**, stance, 繁體中文 regime daily. No Pillar C; no Section 5D trade-unit table.
Label: `v6.4.6 hysteresis multi-band confirm` (scoring spine still v6.4.3 / FT from v6.4.5).

## Sub-features

- `regime-ingest` — Stockbee / breadth / FRED VIX / TradingView US-ETF CSV present or DEGRADED/DATA GATE labeled.
- `regime-caps` — A≤12, B≤9.5, TOTAL≤21.5; no Pillar C; no 5D units table.
- `regime-section0` — ①② from VOO EMA in CSV — not Stockbee DMA.
- `regime-thread` — Prior-day memory; first run DEGRADED; no invented history.
- `regime-hysteresis-5B` — **v6.4.6 + Intermediate Land (2026-10-23):** pending target = today’s **raw band** (not adjacent-only); 2 consecutive same raw + strictly above prior effective → day 2 effective may **jump multi-band**. On pending FAIL (day-2 raw leaves T): compare today raw R to prior effective E — `R < E` → downgrade to R; `R == E` → hold E, clear pending; **`R > E` → Intermediate Land**: effective = R today, clear pending (**FAIL if daily still requires restart `pending R 1/2` while leaving effective at old E**). Still **FAIL** day-1 one-band ladder / adjacent-only upgrade. Downgrade immediate. FT/CC unchanged. Canon: `docs/hysteresis-intermediate-land-2026-10-23.md` + `regime-bands.md`.
- `regime-index-drawdown-gate` — **2026-10-01:** if T2108<20, daily/summary must show SPX drawdown gate (PASS ≥8% / NEUTRAL 5–8% / FAIL <5%) before V-REVERSAL. FAIL → no V-REVERSAL + ⚠️ 非底部訊號. NEUTRAL + V-REVERSAL → Exposure ≤10% / 首注輕試. Window <252 → ⚠️ 窗口不足. Gate must not alter TOTAL.
- `regime-boundary` — Not a 美股市場每日簡報 theme package.
- `regime-today-action` — **2026-10-22:** daily must open with ### 今日動作 (准 swing 試倉／觀望／收手) + 主題許可 + Exposure 旁註 (`字面 0%`／`試倉例外開`／`試倉例外唔開`) and ### 中間 linkage (effective vs Checklist／Deployment; MM 動力股／|z| 撐反). Trial carve-out: 准試倉 only if pending升級中 ∧ 動力股↑ ∧ 風險胃納略改善 — else FAIL if top bar says 准試倉. Does **not** change TOTAL. Canon: `docs/今日動作-trial-carve-out-2026-10-22.md`.

## How to get to it (user POV)

- Justin pastes Stockbee / attaches US-ETF-complete CSV / asks for 市場制度日報 or regime score.
- 總指揮 sends Work Verifier the regime daily path + supporting extracts.
- Refs: `/workspace/refactored_market_awareness/docs/` (+ `CHANGELOG-v6.4.6.md`, `regime-bands.md`).

## Driving it with work-verify harness

Preconditions:

- Doctor GO on regime daily + cited inputs.
- Feature id `regime-market-awareness`.

- **Locate daily.** Open claimed 繁中 regime report path.
- **Version guard.** Confirm no Pillar C, no 5D units; TOTAL formula A+B=/21.5 and arithmetic matches stated pillar scores; version string cites v6.4.6 when 5B multi-band in force.
- **Section 0.** EMA/VOO claims tied to CSV (or gap labeled) — reject Stockbee-DMA substitution if present.
- **Pillars / stance.** Spot-check one A and one B input against ingest artifacts; modifiers/hysteresis consistent with thread or DEGRADED note.
- **Hysteresis 5B (v6.4.6 + Intermediate Land 2026-10-23).** Pending target must equal today’s raw band when upgrading; if raw held 2 days above prior effective, effective must equal that raw (multi-band OK). On pending FAIL: R vs E — R<E downgrade; R==E hold E clear pending; **R>E Land** → effective=R today, clear pending (do **not** require restart `pending R 1/2` at old E). Reject day-1 one-band-at-a-time / adjacent-only confirm language. Exposure: on confirm lower = new regime floor; floor wins if > +20pp ratchet upper.
- **Index Drawdown Gate (2026-10-01).** When T2108<20: verify dd math from Stockbee S&P (or labeled short window); FAIL blocks V-REVERSAL; NEUTRAL caps at 10% if V-REVERSAL claimed; TOTAL unchanged by gate.
- **DATA GATE.** Stale Stockbee/breadth/CSV → must stop or label; inventing multi-day history → FAIL.
- **今日動作／頂欄自洽 (2026-10-22).** Confirm ### 今日動作 + ### 中間 linkage exist above Dashboard. If action=准 swing 試倉: verify Trial three conditions cited with numbers/state (pending升級中; 動力股↑ vs昨或vs P50 disclosed; B2↑或B2-i差改善). Missing any condition + 准試倉 → **FAIL**. Tension days (Checklist/Deployment Uptrend vs effective Deep Bear) must be explained in linkage — bare juxtaposition → NOTES or FAIL. Exposure 旁註 must match Trial outcome. Do **not** judge P&L / whether the trade would have worked.
- **ANTI_JOBS.** No competing cash-session theme brief; no position-sizing table; no English-as-main-daily.
- **Proof.** Evidence with TOTAL arithmetic line; VERDICT accordingly.

## Gotchas

- DEGRADED MODE on first thread day is correct — do not FAIL for missing prev-day memory when labeled.
- B2-i offensive average excludes MAGS — verifier must not “fix” by re-including MAGS.
- US Daily Brief boundary: themes OK to mention lightly; a full Part-1 ETF theme package belongs to the other bot.
- Pre-v6.4.6 dailies that used Bear/Avoid adjacent ladder under a Cautious raw are **superseded** by multi-band rule — do not FAIL a v6.4.6 redo for disagreeing with those old Finals.
- Intermediate Land (2026-10-23): a correct Land Final (pending FAIL + raw > prior effective → effective lands on raw) must **PASS** — do not FAIL for skipping a fresh `pending R 1/2` at the old effective. Day-1 one-band ladder still FAIL.
- Trial carve-out does **not** rewrite numeric Exposure ceiling or effective band — only top-bar action + 旁註. Do not FAIL a Deep Bear 0% ceiling that also says `試倉例外開` when Trial gates pass.
