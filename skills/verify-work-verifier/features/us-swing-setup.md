# 美股 Swing Setup

美股 Swing Trade Setup (v4.7-US): authorized ticker+CSV → Setup judgment, Trade Entry, **MARKET=US** GEMINI HANDOFF. Scanner **Potential Setups ≠ Setup** — no auto-pickup after scan.

## Sub-features

- `us-swing-auth` — Runs only with explicit task id + ticker + CSV path from Justin/總指揮.
- `us-swing-csv` — Input `/workspace/us-swing-scanner/output/run-*/`; output `/workspace/us-swing-setup/output/run-*/`.
- `us-swing-handoff` — GEMINI HANDOFF with MARKET=US; RS vs SPY.
- `us-swing-potential-boundary` — Drive Pullback / Pine screener lists are Potential Setups only.
- `us-swing-verdict-lock` — Technical VERDICT locked; self-VERIFY then Work Verifier.

## How to get to it (user POV)

- Justin/總指揮 issues explicit Setup task (not “scan finished → auto Setup”).
- Producer writes Trade Entry + HANDOFF under us-swing-setup output.
- 總指揮 asks Work Verifier before treating as final.

## Driving it with work-verify harness

Preconditions:

- Doctor GO on claimed Setup outputs (not merely scanner Potential CSV).
- Feature id `us-swing-setup`.

- **Authorize scope.** Intake shows task id / ticker / CSV; if producer ran unsolicited post-scan Setup → FAIL ANTI_JOBS / process.
- **Locate Setup artifacts.** Trade Entry + HANDOFF under `us-swing-setup/output/run-*/`.
- **HANDOFF schema.** Same contract fields as HK chain with **MARKET=US**; RS vs SPY.
- **Potential ≠ Setup.** If only Potential Setups file claimed as “Setup done” → FAIL done-criteria.
- **No fabricate / ANTI_JOBS.** No Regime TOTAL; no Story upgrade; no HK CSV; no invent prices/VERDICT.
- **Proof.** Evidence distinguishes scanner vs Setup paths clearly.

- **Fleet handoff fields (2026-10-05).** Check HANDOFF for `PINNED_INPUTS`, `DECISIONS_MADE`, `OPEN_QUESTIONS`, `NEXT_GATE`. Downstream may read only pinned files; settled decisions must not be re-opened. During rollout, missing fields → PASS_WITH_NOTES (not FAIL).

## Gotchas

- Highest-frequency error: treating scanner Potential Setups as completed Setup.
- MARKET=US handoff with HSI RS language → FAIL.
- Do not verify US Setup using the HK feature file checklist.
