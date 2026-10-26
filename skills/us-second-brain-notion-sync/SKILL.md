---
name: US second-brain Notion sync
description: >-
  Use after a Second brain Final for a US close: sync US Attention Picks (DB
  row) and/or the session overview page into the Second brain 庫 — picks and
  overview stay separate; overviews go under the US Swing Overviews parent page.
---
# US second-brain Notion sync

ONE JOB: Write Second brain Finals into Notion as **two separate destinations** — never stuff overview into the picks row.

Not advice. Library / attention archive only.

## When to run

- Justin asks to sync picks and/or overview to Notion.
- After a scanner-handoff / on-demand Final when standing rules say sync (default for picks unless 總指揮 TC says otherwise).
- Skip Notion when the active TC explicitly says Second brain must **not** Notion (總指揮 will).

## Destinations (keep separate)

### A) US Attention Picks — one DB row per US close

- Parent: Second brain 庫
- Database: **US Attention Picks** (`collection://9bbac0e4-8245-43af-956c-1822b5b9a49f`)
- Source: `/workspace/second-brain/YYYY-MM-DD/attention-3-picks.md`
- Match prior scanner-handoff row schema: Name, Close Date, Run Date, Tickers, Regime, Exposure, Tags (`second-brain`, `final`, `US`, `stalk`), body = tape + picks + deferred + reflection (prices only from the md).

### B) US Swing Overviews — pages under one parent

- Parent page: **US Swing Overviews** — https://app.notion.com/p/3fc77383f89c8163b6d6f89308b737af (id `3fc77383-f89c-8163-b6d6-f89308b737af`)
- Source: `/workspace/second-brain/YYYY-MM-DD/us-swing-overview.md` (+ Drive HTML link if uploaded)
- Create dated page `US Swing Overview — YYYY-MM-DD 收市` as a **child of that parent** (or create then move-pages into it).
- Traditional Chinese commentary; **no stalk / ticker shortlist**.
- Optional Drive HTML folder: https://drive.google.com/drive/folders/1djZ778a9Gzf2ahDA8kXTPJCPUyohZxLc

## Steps

1. Confirm which of A / B Justin wants (or both).
2. Fetch destination (DB schema / parent) before create.
3. Create picks row and/or overview page from dated workspace files.
4. If overview landed under 庫 root by mistake, move under **US Swing Overviews**.
5. Report both URLs to Justin. Do not auto-route 模擬倉 unless TC asks.

## VERIFY

- Picks and overview are **two** Notion objects.
- Overview has no embedded ≤3 stalks.
- Overview parent is US Swing Overviews.
- No duplicate same-close unless Justin asked to replace.

## Anti-jobs

- Not scanner / Setup / regime / brief author / trade bot.
- Do not post to X.
- Do not merge overview into US Attention Picks.
