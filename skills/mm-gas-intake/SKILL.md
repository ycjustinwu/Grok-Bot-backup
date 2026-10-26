---
name: mm-gas-intake
description: Use when Market Master Apps Script starts a chart/helper patch — lock which .gs files, which charts, and missing sources before editing.
---

# mm-gas-intake

## ONE JOB
Lock the patch scope for Market Master Apps Script before any `.gs` edit.

## Steps
1. Read TC / Justin ask; note canonical sheet `1Xu9VX4S3VuS3BrzW42Yf9WRSaYn8Znp3X6XC-2SFmEk`.
2. Inventory inbox under `/workspace/market-master/apps-script/inbox-*/` (and prior patches under `patches/`).
3. List **present** vs **missing** project files (e.g. `10_Breadth.gs`). If breadth charts are in scope and `10_Breadth.gs` (or live export) is missing → stop and ask Justin to paste/export or open Apps Script share — do not invent.
4. Prefer US/HK **breadth** charts first; ETF only after breadth aligned (unless Justin names ETF first).
5. Friend demo sheet (optional): `1DSYO86aAHqjqqvNIXj6_hTWYLi-kbuZNggmxEwRfc6Q` — need Justin share if unreadable.
6. Write intake note: `/workspace/market-master/apps-script/handoff/IN-YYYYMMDD-HKT.md` with PINNED_INPUTS / DECISIONS_MADE / OPEN_QUESTIONS / NEXT_GATE.

## Defaults (friend → merge targets, tunable constants — not hard-coded forever)
- 脈搏 / net advances style: `viewWindow` ≈ ±500
- 動力股佔比: 0–40
- 市寬 %: 10–80
Merge into existing `chartDataOn_` + `addChart_` + rebuild/menu path. **Do not** treat a standalone `Charts` one-shot page as the long-term fix.

## VERIFY
- [ ] Canonical sheet id recorded
- [ ] Present/missing `.gs` listed; no invent of missing files
- [ ] Chart targets named (tabs + chart titles)
- [ ] Handoff four fields written
- [ ] Scope excludes data/scoring tabs

## ANTI
No data/scoring edits. No parallel long-term Charts-only project. No live push in this skill.
