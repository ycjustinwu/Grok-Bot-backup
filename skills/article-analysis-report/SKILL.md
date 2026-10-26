---
name: article-analysis-report
description: >-
  Use when writing the 文章分析 Traditional Chinese Markdown report (sections 1–9 +
  appendix) from an ingested working copy. Follow docs/output-template.md. After
  Final lands, sync to Notion 文章分析 via notion-final-sync.
---
# Article Analysis Report

## Before grind
Run Jev B `pre_task` ([Jev Fleet Decisions](sand-workflow:jev-fleet-decisions)) if hung. Then read PINNED working copy only.

## Output header
- 推薦度：⭐️ × N（1–10）
- 新穎度：🍅 × N（1–10）
- 文章URL：（or 無 URL）

## Sections (all required; Markdown `-` lists only, never `*`)
1. **核心分析** — ≥10 coherent sentences; then 關鍵要點 ×5; 創新見解 ×5
2. **重要引用與翻譯** — ≥3 quotes: 原文（第X段）+ 翻譯 + 引用理由. Translate into 繁體中文.
3. **閱讀筆記** — ≥3 categories: one-line summary + 3 bullets + hashtags each
4. **數據可視化** — text/ASCII charts from real figures in the piece; if no numbers, say 原文無可用數據並用結構圖代替 — do not invent stats
5. **思維導圖** — text mind map of the article’s logic
6. **文章核心問題問答** — ≥3 Q&As; answers cite/ paraphrase from the piece
7. **行動與改變** — one 行動建議 + one 認知升級
8. **關鍵術語解釋** — terms that appear in the piece only
9. **發散聯想** — clearly labeled as analyst extension (not claimed as author text)

## Appendix
URL · 作者信息 · 發布時間 · 發布平台（未知 if missing）

## Style
- 繁體中文; direct output; no meta chatter
- End with one line: 本報告非投資／法律建議；分析基於提供文本。

## File
Save: `/workspace/article-analysis/{slug}-{YYYYMMDD-HHMM}-HKT.md`
Chat: path + 推薦度/新穎度 line; full body only if Justin asks.

## Notion sync (required after Final)
Run [Notion Final Sync](sand-workflow:notion-final-sync) for the saved Final before ending the turn:
- Target: Notion DB **文章分析** (`collection://54a385e9-2afe-4d06-95f3-27ff7cced4f4`)
- Library key in sync-state: `article-analysis`
- Skip `input/` and `_notion_*` files
- Fill Name, Analyzed Date, Article URL, Author, Recommendation, Novelty, Source=`article-analyzer`, TLDR, Tags when clear
- Body via `$file:` expansion; VERIFY page is not hollow
- Chat: also return Notion page URL when sync succeeds

## Exit
Jev C `exit` if hung. NEXT_GATE = Justin (WV only if routed).

## VERIFY
- [ ] 繁體中文 throughout
- [ ] Header scores 1–10 present
- [ ] Sections 1–9 + appendix all present
- [ ] ≥3 quotes with 原文+翻譯+理由
- [ ] No invented URL/author/date/numbers
- [ ] File exists on disk; path reported
- [ ] Disclaimer line present
- [ ] Notion row created/updated under 文章分析; body verified; sync-state updated
