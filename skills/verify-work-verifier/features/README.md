# Work Verifier fleet feature map

Maintained source for driving high-stakes Grok Bot deliverables the way Justin reads them. Read this index, then the matching feature file. Harness commands live in **`work-verify`** (Launch→Doctor→Drive→Evidence→Cleanup).

## Baseline preconditions

- Intake from 總指揮/Justin: producer name, claim, `/workspace/...` paths, done criteria.
- Artifacts on the shared box filesystem (not chat-only).
- Run **Doctor** before deep Drive; NO-GO → Evidence FAIL, no silent repair.
- Scratch: `/workspace/work-verifier/scratch/<run-id>/` only.
- Evidence survives Cleanup: `/workspace/work-verifier/output/verify-YYYYMMDD-HHMM.md` + `LATEST.txt`.
- Never mutate producer outputs; never invent missing quotes.

## Driving conventions

- Prefer on-disk sources (JSON, CSV, extracts, HANDOFF blocks) over narrative memory.
- Pair each checklist item with an observable (row match, field present, gap label).
- Soft evidence (secondary press, seed-absent names, rounding, soft mcap) → **NOTES**, not auto-FAIL, when labeled and not contradicted.
- Fabricate / schema break / ANTI_JOBS / missing primary → **FAIL**.
- MARKET=HK vs US must stay labeled; do not mix RS benchmarks silently.
- Fusion default: report MD + infographic **prompt** only — baoyu/image only if Justin asked.

## Proof and skip reporting

- Record feature ID + paths checked in the verify report.
- If a support file is absent but the brief labels the gap, note it — do not invent the number.
- Do not mark a skipped producer section as verified via a different section.
- VERDICT: `PASS` | `PASS_WITH_NOTES` | `FAIL`.

## Feature entry contract

Each feature file: H1 + one paragraph, then exactly four H2s:

1. `Sub-features`
2. `How to get to it (user POV)`
3. `Driving it with work-verify harness`
4. `Gotchas`

## Features

- [港股收市簡報](./hk-after-close-brief.md) — after-close MD; 繁中 schema; Yahoo/TV seed; Connect; Market Monitor
- [US Market Daily Brief](./us-market-daily-brief.md) — 美股市場每日簡報; ETF/volume CSVs; DATA GATE
- [Regime / Market Awareness](./regime-market-awareness.md) — v6.3 TOTAL/21.5; no Pillar C
- [港股 Swing Setup](./hk-swing-setup.md) — CSV → Trade Entry + GEMINI HANDOFF MARKET=HK
- [美股 Swing Setup](./us-swing-setup.md) — MARKET=US; Potential Setups ≠ Setup
- [Story Search + Fusion](./story-search-fusion.md) — narrative + Fusion MD/prompt; no default baoyu
