---
name: X signal retrieval
description: >-
  Use when running Weekday/Evening X signal (or any X Monitor scan) to pull list
  posts, judge novelty and value, and format the Signal brief.
---
# X signal retrieval

Goal: in one time window, surface only posts that clear Justin’s bar, are new vs the last delivery, and are worth acting on. Prefer public X reads (`search_posts_all`, `get_users_posts`, `get_posts_by_id`, `get_news` / `search_news`, `get_posts_counts_recent`). Cap each call at 25 results; respect rate limits.

This skill is list-first. The watch source is X list `2097092298073166050` unless Justin names another list. Delivery layout stays HiTw93 Signal-style English (Main threads → numbered author blocks → 💡 takeaway). Do not invent quotes, numbers, or links.

## 1. Window and sources

1. Window = since the sibling routine last ran (Weekday ↔ Evening). If unknown, ~12h back on weekdays.
2. Primary: `search_posts_all` with `list:2097092298073166050` and a `start_time` for the window. Paginate only if the first page is clearly incomplete for the bar.
3. Optional supplement (only when the list yield is thin on a bar topic, or a major event is underway):
   - Targeted `search_posts_all` queries with `-is:retweet` and `start_time`
   - `get_news` / `search_news` for the same themes
   - `get_posts_counts_recent` when volume-spike confirmation helps
4. Never replace the list with a random follow graph. Supplemental handles belong only if Justin added them to the list or explicitly asked.

## 2. Bar (push)

Keep an item when it fits at least one:

- US regime / tape (breadth, indices, credit, rates, allocation shifts with numbers)
- HK / China tape with named names or hard prints
- Swing / momentum process (setups, screens, risk rules, failed breakouts)
- Fundamentals / earnings with concrete figures
- AI tools / agent workflow that Justin can use the same day

## 3. Skip

- Pure opinion or jokes with no number or named tape fact
- Engagement bait, undated screenshots, unsourced rumors (if truly material, mark unconfirmed once)
- Small version notes with no user-facing change
- Same story already delivered this morning/evening with no new substance
- Retweets with no added comment (prefer the original)

## 4. Novelty (seen)

1. Maintain `/workspace/x-monitor/seen.json`: array of `{id, url, topic_keys[], delivered_at, run}`.
2. Before delivering, drop any post id already in seen, and drop near-duplicates whose topic keys match an item delivered in the last 7 days unless there is a material update (rumor → official, new number, guidance change).
3. Topic keys = lowercase tickers + 2–4 content nouns (e.g. `iwm,200dma`, `anthropic,q3,revenue`).
4. After delivery, append every reported post id and its topic keys. Prune entries older than 7 days.

## 5. Rank and cap

1. Prefer: official/reliable media, high engagement inside the list, hard numbers, regime tells over single-name chatter.
2. Cap ~8 author blocks. Group by author; one block can hold several of their posts.
3. If nothing clears the bar → deliver exactly `沒有變化` and stop.

## 6. Output shape (HiTw93 Signal)

**Main threads** — short theme bullets (regime first).

Then numbered blocks:

```
1. Display Name 🌐 @handle
- **Topic:** fuller detail with numbers/tickers + why it matters. ([original](url))

💡 one-line takeaway
```

Optional one-liner glance row for near-misses that are useful but not full blocks.

## 7. Delivery

Hand the exact body to the parent to SendToUser in X Monitor’s chat — no preamble. Never post, reply, like, repost, follow, or DM on X.

## Source lesson

Method distilled from [@dotey](https://x.com/dotey/status/2110407057622904945) (account tiers + search recipes + novelty/value gates + silence when empty), adapted to Justin’s list-first market/swing bar and Signal layout.
