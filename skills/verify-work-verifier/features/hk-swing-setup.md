# 港股 Swing Setup

港股 Swing Trade Setup (v4.7-HK): Python CSV → Setup/止損驗證 → Trade Entry CSV → labeled GEMINI HANDOFF with **MARKET=HK** for 投資敘事分析師. RS = Stock%−HSI%; ADR = 20日.

## Sub-features

- `hk-swing-csv` — Input under `/workspace/hk-swing-scanner/output/run-*/`; validate before publish.
- `hk-swing-trade-entry` — Trade Entry CSV under `/workspace/hk-swing-setup/output/run-*/`.
- `hk-swing-handoff` — GEMINI HANDOFF block: VERDICT/SETUP/STOP/ENTRY/TARGETS/EARNINGS/RS/MARKET=HK.
- `hk-swing-verdict-lock` — Technical VERDICT locked for downstream Story/Fusion.
- `hk-swing-invalid` — STOP INVALID must not publish as final.

## How to get to it (user POV)

- Justin or 總指揮 assigns HK CSV path / run id to 港股 Swing Setup.
- After self-VERIFY, 總指揮 routes outputs to Work Verifier.
- Downstream expects HANDOFF usable by 投資敘事分析師 (not US rules).

## Driving it with work-verify harness

Preconditions:

- Doctor GO on Trade Entry path + HANDOFF artifact (file or pasted block saved under run dir).
- Feature id `hk-swing-setup`; MARKET must be HK.

- **Locate outputs.** Confirm `hk-swing-setup/output/run-*/` artifacts exist per claim.
- **Schema HANDOFF.** Required fields present: VERDICT, SETUP, STOP TYPE, STOP ANCHOR, SCENARIO ENTRY, ENTRY ZONE, ADJUSTED STOP, PRIMARY TARGET+RR, EARNINGS, KEY SUPPORT, TECHNICAL CONCERN, CLAUDE CONVICTION, RS_SCORE, **MARKET=HK**.
- **Market rules.** RS framing vs HSI (not SPY); ADR 20-day language consistent.
- **No fabricate.** OHLC/volume/VERDICT traceable to CSV; INVALID runs not marked final.
- **ANTI_JOBS.** No US CSV analysis; no name 「港美股 Swing Setup」; no investment-advice framing; no Story upgrade inside Setup.
- **Reversibility.** Entry/stop levels are analysis — flag if producer language implies live order placement without Justin.
- **Proof.** Evidence lists run paths + field checklist.

- **Fleet handoff fields (2026-10-05).** Check HANDOFF for `PINNED_INPUTS`, `DECISIONS_MADE`, `OPEN_QUESTIONS`, `NEXT_GATE`. Downstream may read only pinned files; settled decisions must not be re-opened. During rollout, missing fields → PASS_WITH_NOTES (not FAIL).

## Gotchas

- Missing MARKET=HK or HK handoff with SPY RS → FAIL consistency.
- Scanner Potential list ≠ Setup deliverable — verifying scanner scoreboard alone is wrong surface (use this feature only for Setup outputs).
- Do not upgrade WATCH/STALK → BUY during verify.
