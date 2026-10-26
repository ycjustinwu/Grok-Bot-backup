---
name: mm-gas-merge-charts
description: Use when merging friend chart axis/window ideas into Market Master v1.2.1 Visuals helpers (same-tab chartDataOn_/addChart_), not a parallel Charts page.
---

# mm-gas-merge-charts

## ONE JOB
Produce a **permanent** Apps Script patch: friend axis/window ideas merged into the multi-file Market Master project (same-tab helper cols + rebuild/day jobs).

## Steps
1. Start from pinned inbox / prior patch copies — never from memory alone.
2. Keep v1.2.1 direction: `chartDataOn_(sh, startCol, data, labelCol)` + `addChart_(…)` with `SHOW_BOTH`; chart data on **same** dashboard tab in helper columns.
3. Absorb friend `viewWindow` as **named constants** (e.g. `CHART_AXIS_PULSE_`, `CHART_AXIS_MOMENTUM_`, `CHART_AXIS_BREADTH_`) with defaults ±500 / 0–40 / 10–80; callers pass via `o.vAxis`.
4. Wire rebuild / menu paths in `90_Orchestrator.gs` (or equivalent) so redraw is repeatable — friend note: **perm fix, not one-time**.
5. Touch only chart/helper/permission/rebuild code. Leave Market Master **data and scoring** untouched.
6. Write full file outputs under `/workspace/market-master/apps-script/patches/YYYYMMDD-HKT/` — complete `.gs` files Justin can diff, plus `CHANGELOG.md` listing changed functions.

## VERIFY
- [ ] No new long-term standalone Charts-page workflow as the fix
- [ ] Helper columns + SHOW_BOTH retained
- [ ] Axis windows are constants / options, not magic scattered numbers only
- [ ] CHANGELOG names functions + how to redraw from menu
- [ ] Diffable full `.gs` paths exist on disk
- [ ] No scoring/data formula changes

## ANTI
Do not invent Sheets APIs. Do not push to live Apps Script without Justin. Do not “fix” by one-shot pasting into a demo Charts tab as the ship form.
