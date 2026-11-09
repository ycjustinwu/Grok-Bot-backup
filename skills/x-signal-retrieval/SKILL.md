---
name: X signal retrieval
description: >-
  Use when running Weekday/Evening/Saturday X signal (or any X Monitor scan) to
  pull list posts via MCP, run the post-fetch script, and format the Signal with
  within-Signal and cross-run dedup.
---
# X signal retrieval

Goal: in one time window, surface only posts that clear Justin’s bar, are new vs the last delivery, and are worth acting on. Soft Final rung: **`x+script`** (MCP fetch + post-fetch script). Do not invent quotes, numbers, or links. Never load full acc JSON into the model context.

List-first: X list `2097092298073166050` unless Justin names another. Layout: HiTw93 Signal English (Main threads → numbered author blocks → 💡 takeaway).

## 0. Script-first pipeline (token save)

1. Plan slices (required for weekday ~12h):
```bash
python3 /workspace/x-monitor/scripts/x_signal_pipeline.py plan-window \
  --start …Z --end …Z --max-slices 4
```
   **Token cut #2 (Justin 2026-11-05):** use **≤4 slices** (default). Do **not** fixed-2h × ~7.
2. **Connector:** public `x.search_posts_all` with `list:2097092298073166050 -is:retweet` + `start_time`. Dump each page/slice JSON under `/workspace/x-monitor/{run}-page*.json` / `{run}-h*.json`. Cap 25/call.
3. **Pagination stop (hard — token cut #1):** Soft Final must **not** wait on endless `next_token`.
   - **Max 2 pages per slice** (suffix none + `b`). **No page c/d/…** — stop even if `next_token` remains and even if coverage looks thin.
   - If `_paginate_queue.json` idle **>3 min** with no new dump files → **stop waiting**, clear or ignore queue, run pipeline on whatever dumps exist, format + deliver.
   - If Exact body for this `{run}` already exists on disk / was already delivered (oneshot or parent), **do not** send a second Signal from a hung Automation wake.
4. **Script (required after dumps)** — **token cut #3:** `--top 50` (default; was 120):
```bash
python3 /workspace/x-monitor/scripts/x_signal_pipeline.py run \
  --glob '/workspace/x-monitor/{run}-page*.json' \
  --glob '/workspace/x-monitor/{run}-h*.json' \
  --seen /workspace/x-monitor/seen.json \
  --out-prefix /workspace/x-monitor/{run} \
  --top 50
```
5. **Model reads only** `{run}-barcands.txt` (and skill rules). Do **not** open `-acc.json` for formatting.
6. After deliver:
```bash
python3 /workspace/x-monitor/scripts/x_signal_pipeline.py update-seen \
  --seen /workspace/x-monitor/seen.json \
  --ids-file /tmp/{run}-delivered_ids.txt \
  --run {run}
```
Docs: `/workspace/x-monitor/scripts/README.md`. No Computer Use for this job.

## 1. Window and sources

1. Window = since sibling routine (Weekday ↔ Evening). If Evening paused, still use Evening clock (~prior day 18:15 HKT). Else ~12h.
2. Primary list search as above. Paginate / slice only under §0 stop rule (**≤4 slices × ≤2 pages**).
3. Optional thin-list supplement: targeted `search_posts_all -is:retweet`, `get_news` / `search_news`, `get_posts_counts_recent`.
4. Never replace the list with a random follow graph.

## 2. Bar (push)

Keep when it fits at least one: US regime/tape with numbers; HK/China named tape; swing/momentum process; fundamentals/earnings figures; same-day AI tools/workflow.

## 3. Skip

Opinion/jokes without numbers; engagement bait; undated screenshots; unsourced rumors (mark unconfirmed once if material); tiny version notes; already-delivered same story; bare RTs; midterms/politics unless it moves a named market print.

## 4. Novelty (seen) — cross-run

1. `/workspace/x-monitor/seen.json`: `{id, url, topic_keys[], delivered_at, run}`.
2. Script `rank` drops seen ids; still drop topic near-dupes from last 7d unless material update.
3. Topic keys = lowercase tickers + 2–4 nouns.
4. Prefer `update-seen` CLI after delivery; prune >7d.
5. **Cross-run rewrite ban (Justin 2026-11-02):** if window mostly restates prior Signal → delta-only or `沒有變化`. Full multi-block only for net-new tape.

## 5. Within-Signal dedup (hard rule) — less echo

1. **One owner per fact.** Primary post owns full numbers + link; later authors = new angle only.
2. **Main threads = thesis / opinion only (TC-20261105-04 R4).** 3–5 bullets of **theme labels** that suit Justin’s interest (regime/tape split, setups process, earnings split, AI tools) — **not** a figure dump. **Forbid** repeating any figure, %, level, or ticker print that an author block will carry. If a figure is needed once, it lives in **one** owner block only.
3. **Author blocks own detail.** No opening theme echo of Main threads.
4. **Wire/confirm** accounts (Investing.com / Barchart / pure reprint of a print already owned) → **Glance only** or drop (R5).
5. Same-author multi-posts → one block.
6. **Prefer 5–6 author blocks (R5).** Cap hard at 8. When ≥3 candidates confirm the same print, keep the best owner + push confirms to Glance — fewer unique angles beat echo.

## 6. Rank and cap

Script pre-ranks (engagement + bar boost; bar-matched first; **max 3 posts per @handle** in barcands after TC-20261105-04). Model re-filters to Justin’s bar and list relevance, then **target 5–6** author blocks (≤8). Prefer process/setup and regime angles over wire monoculture. If nothing clears → exactly `沒有變化`.

## 7. Output shape (HiTw93 Signal)

**Main threads** — thesis labels only (§5.2); no figure echo of blocks.

```
1. Display Name 🌐 @handle
- **Topic:** detail + numbers + ([original](url))

💡 one-line takeaway
```

Optional Glance row for wire confirms. Market replies end with `不構成投資建議`.

## 8. Delivery

Parent SendToUser exact body — no preamble. Never post/reply/like/repost/follow/DM on X. Softshort ≤8 Markets/Setups/AI is 總指揮/internal only.

## Source lesson

[@dotey](https://x.com/dotey/status/2110407057622904945) method + Justin list/bar. Within-Signal dedup 2026-11-03. Script rung `/workspace/x-monitor/scripts/x_signal_pipeline.py` 2026-11-03 for token save. Pagination stop 2026-11-05 after MCP stall. **TC-20261105-04:** R2–R5 (Main thesis-only + less echo). **TC-20261105-05:** token cut 1+2+3 — hard 2 pages/slice, ≤4 slices, `--top 50`. Skip R1/R6 and cuts 4–5 unless he re-asks.
