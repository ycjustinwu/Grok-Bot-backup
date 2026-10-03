# 港股收市簡報

After-close Traditional Chinese Markdown brief for Justin: tape, 三大頭條, sector rotation, unusual movers, 北水 alerts, and CUP Market Monitor — MD only by default (no PDF unless asked).

## Sub-features

- `hk-brief-schema` — 繁中 after-close skeleton; empty optional sections may skip; Monitor kept when Summary row exists.
- `hk-brief-av-seed` — Justin TV UP/DOWN seed tape is authoritative (locked 2026-09-30); do **not** FAIL on Yahoo price/%/RV/name drift.
- `hk-brief-connect` — HKEX Stock Connect 南向 buy/sell → net; ≪200億 gate labeled.
- `hk-brief-monitor` — Market Monitor Summary for session date (Up4/Down4, SMA, MLI); **same calendar day D**, not US D+1.
- `hk-brief-commodities` — Oil/gold % must be same-contract (or labeled snapshot / not like-for-like).
- `hk-brief-gaps` — Soft sources and missing non-TV lines labeled 不捏造 / 缺口 (HSTECH, VHSI, etc.).

## How to get to it (user POV)

- 總指揮 assigns Work Verifier after 港股收市簡報 delivers `HK brief-YYYY-MM-DD.md`.
- Justin flags the day’s after-close pack under `/workspace/hk-brief-inputs/YYYY-MM-DD/`.
- Producer claims MD-only delivery (~16:30 HKT target); PDF absent is OK unless Justin asked for PDF.

## Driving it with work-verify harness

Preconditions:

- Doctor GO on primary MD + claimed supports (`justin-tv-movers.csv` / day-folder AV paste, `stock360-industry.md`, `hkex-connect.md`, `market-monitor-extract.md`, commodity notes as cited). Yahoo seed/large JSON may exist as optional soft context — **not** a hard AV gate after 2026-09-30.
- Feature id `hk-after-close-brief`; session date matches folder/header.

- **Locate MD.** Open `/workspace/hk-brief-inputs/<date>/HK brief-<date>.md`. File present → continue; missing → FAIL.
- **Schema 繁中.** Confirm Tape / 三大頭條 / 板塊 / 個股 / 北水 / Market Monitor order (or documented skips). Citations + 不捏造 stance present.
- **AV seed tape (locked 2026-09-30).** Membership: names in §個股 / AV table must match Justin’s TV UP/DOWN paste for the session. **Do NOT FAIL** on Yahoo price / % / RV / name “drift” vs the seed. Producer trusts Justin’s tape; Yahoo re-verify is optional soft NOTES only if the brief itself asserts a non-TV number that contradicts disk.
- **No H-share ≥100億 market-cap gate (locked 2026-09-30).** Do not PASS/FAIL seeds on H-cap or any mcap filter. Scoring “H 股市值閘” as hard is a **verifier error**.
- **Clean-check clutter.** Identity / method / gate checks that find nothing wrong → auto-hide in NOTES; only surface real gaps or FAIL causes (mirrors producer).
- **Industry / tape / connect.** Stock360 turnover/advance/sectors match brief table when cited; Connect buy/sell rows match `hkex-connect.md`; net derived and labeled 推算 if needed. Index/北水/theme prices the brief asserts from **non-TV** sources must not be fabricated.
- **Market Monitor.** Summary row for session **D** (same calendar day — HK is **NOT** US D+1); Up4/Down4/SMA/MLI figures match extract when present.
- **Commodities (hard).** Oil/gold % = same-contract settle-to-settle, or labeled snapshot / not like-for-like. Mixing continuous (`BZ=F`) after roll vs prior-month settle without 更正註記 → FAIL.
- **ANTI_JOBS.** After-close brief only — no Regime TOTAL/21.5, no Swing VERDICT upgrade, no default PDF pipeline.
- **Research path (soft).** Producer preference Sheets→Tavily→Firecrawl→Browserless→Browser Use→desktop; absence of MCP chain log = soft NOTES only (not FAIL).
- **Soft-evidence NOTES class.** Flag without auto-FAIL when labeled: HSTECH from secondary press while gap noted; theme names absent from optional yahoo JSON but not contradicted; immaterial rounding on labeled snapshots.
- **Proof.** Evidence report lists artifact table + checklist + NOTES bullets; VERDICT PASS or PASS_WITH_NOTES when only soft class remains.

## Gotchas

- Failing a seed on Yahoo vs Justin TV price/%/RV is a **verifier error** after 2026-09-30.
- Scoring H-share ≥100億 mcap as hard PASS/FAIL is a **verifier error** after 2026-09-30.
- HSTECH soft source is NOTES if gap labeled; inventing an uncited HSTECH print is FAIL.
- Market Monitor is side-channel — do not demand a second regime score; do not apply US D+1 date offset.
- PDF missing is not FAIL under MD-only default.
- Commodity same-contract is hard; snapshot labels keep it NOTES not FAIL.
