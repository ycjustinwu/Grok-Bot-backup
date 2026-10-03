# Story Search + Fusion

投資敘事分析師 (Story Search) consumes Swing GEMINI HANDOFF → 敘事報告; Fusion Formatter merges technical + story into ≤500字 MD + infographic **prompt**. Default: **no baoyu / no image generation** unless Justin asks.

## Sub-features

- `story-handoff-parse` — Contract fields from HK or US HANDOFF; MARKET label preserved.
- `story-no-upgrade` — Narrative must not change technical VERDICT (no story-driven BUY upgrade).
- `story-report` — 繁中 敘事報告 + 廣東話一句講晒; themes from knowledge + web search.
- `fusion-report` — OUTPUT① ≤500字; tech VERDICT priority; ADJUSTED STOP; EARNINGS line.
- `fusion-prompt-only` — OUTPUT② infographic prompt file; STOP — no default Fusion Swing Infographic / baoyu.

## How to get to it (user POV)

- After Swing Setup HANDOFF, 總指揮 runs Story then Fusion (or Justin asks).
- Justin receives Fusion report MD + prompt path; may generate art elsewhere.
- Work Verifier audits Story and/or Fusion artifacts before final.

## Driving it with work-verify harness

Preconditions:

- Doctor GO on story_report and/or fusion outputs cited in intake.
- Feature id `story-search-fusion`; note MARKET=HK|US from upstream.

- **Locate pair.** Open technical_report + story_report inputs (or Fusion run dir) and OUTPUT① MD; OUTPUT② prompt if claimed.
- **Story ANTI_JOBS.** Confirm VERDICT in story matches Swing; no scanner/setup redo; catalysts not invented without source.
- **Fusion fidelity.** No facts beyond the two inputs; VERDICT = technical; stop = ADJUSTED STOP; STALK wording = wait volume, don’t chase.
- **Budget.** Fusion MD ≤500字 spirit (hard budgets in skill); 一句講晒 is 廣東話.
- **Image default.** If baoyu/infographic PNG present without Justin/總指揮 GENERATE ask → NOTES or FAIL per intake (default policy = should not auto-run). If only prompt file → PASS path.
- **MARKET.** HK/US benchmark language not mixed unlabeled.
- **Proof.** Evidence lists MD + prompt paths; states image-gen skipped/allowed.

## Gotchas

- Story quality ≠ license to upgrade VERDICT — verifier FAIL if BUY appears only from narrative.
- Prompt file alone is the Fusion default success; missing PNG is not FAIL.
- Verifying Fusion without checking ADJUSTED STOP vs raw stop is incomplete.
