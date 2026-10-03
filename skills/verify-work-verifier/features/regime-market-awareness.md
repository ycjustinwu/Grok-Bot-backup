# Regime / Market Awareness (v6.4.6)

Market Awareness Orchestrator daily: Regime Scoring v6.4.6 — Pillars A/12 + B/9.5 = TOTAL/21.5, layers, modifiers, **hysteresis multi-band confirm**, stance, 繁體中文 regime daily. No Pillar C; no Section 5D trade-unit table.
Label: `v6.4.6 hysteresis multi-band confirm` (scoring spine still v6.4.3 / FT from v6.4.5).

## Sub-features

- `regime-ingest` — Stockbee / breadth / FRED VIX / TradingView US-ETF CSV present or DEGRADED/DATA GATE labeled.
- `regime-caps` — A≤12, B≤9.5, TOTAL≤21.5; no Pillar C; no 5D units table.
- `regime-section0` — ①② from VOO EMA in CSV — not Stockbee DMA.
- `regime-thread` — Prior-day memory; first run DEGRADED; no invented history.
- `regime-hysteresis-5B` — **v6.4.6:** pending target = today’s **raw band** (not adjacent-only); 2 consecutive same raw + strictly above prior effective → day 2 effective may **jump multi-band**; day-2 leave pending → fail/restart from new raw — **FAIL if daily still uses one-band ladder / adjacent-only upgrade**. Downgrade immediate. FT/CC unchanged.
- `regime-index-drawdown-gate` — **2026-10-01:** if T2108<20, daily/summary must show SPX drawdown gate (PASS ≥8% / NEUTRAL 5–8% / FAIL <5%) before V-REVERSAL. FAIL → no V-REVERSAL + ⚠️ 非底部訊號. NEUTRAL + V-REVERSAL → Exposure ≤10% / 首注輕試. Window <252 → ⚠️ 窗口不足. Gate must not alter TOTAL.
- `regime-boundary` — Not a 美股市場每日簡報 theme package.

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
- **Hysteresis 5B (v6.4.6).** Pending target must equal today’s raw band when upgrading; if raw held 2 days above prior effective, effective must equal that raw (multi-band OK). Reject one-band-at-a-time / adjacent-only confirm language. Exposure: on confirm lower = new regime floor; floor wins if > +20pp ratchet upper.
- **Index Drawdown Gate (2026-10-01).** When T2108<20: verify dd math from Stockbee S&P (or labeled short window); FAIL blocks V-REVERSAL; NEUTRAL caps at 10% if V-REVERSAL claimed; TOTAL unchanged by gate.
- **DATA GATE.** Stale Stockbee/breadth/CSV → must stop or label; inventing multi-day history → FAIL.
- **ANTI_JOBS.** No competing cash-session theme brief; no position-sizing table; no English-as-main-daily.
- **Proof.** Evidence with TOTAL arithmetic line; VERDICT accordingly.

## Gotchas

- DEGRADED MODE on first thread day is correct — do not FAIL for missing prev-day memory when labeled.
- B2-i offensive average excludes MAGS — verifier must not “fix” by re-including MAGS.
- US Daily Brief boundary: themes OK to mention lightly; a full Part-1 ETF theme package belongs to the other bot.
- Pre-v6.4.6 dailies that used Bear/Avoid adjacent ladder under a Cautious raw are **superseded** by multi-band rule — do not FAIL a v6.4.6 redo for disagreeing with those old Finals.
