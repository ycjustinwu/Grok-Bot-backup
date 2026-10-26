---
name: Notion Final Sync
description: >-
  Use when new Final markdown (or Motion HTML/MP4) from market briefs, family
  growth, career coaching, HTML Motion Studio, YouTube Analyzer, or 文章分析 should
  be upserted into the matching Notion database without waiting for the user to
  ask.
---
# Notion Final Sync

## When
After a Final deliverable lands on the box, or on a catch-up scan: upsert one row per Final into the mapped Notion DB. Skip drafts, intermediates (`abnormal-volume`, `inputs/`, `input/`, `_notion_body_*`, `cases/`), and duplicates for the same date/title.

## Mapping (Justin / Wu Justin's space)
Keep collection ids current via Notion fetch if renamed.

| Bot / source | Final pattern on box | Notion parent | Data source |
|---|---|---|---|
| Market Awareness | `/workspace/market-awareness/YYYY-MM-DD/regime-daily-YYYY-MM-DD.md` | Market Awareness 制度日報庫 | `collection://ee81c980-05aa-4971-93d7-58b2ef01bc79` |
| US Market Daily Brief | `/workspace/us-brief-output/YYYY-MM-DD/US brief-YYYY-MM-DD.md` (prefer output over `us-brief/`) | 美股市場每日簡報庫 | `collection://b65fa2ce-b87b-4547-9993-b12c60b1dee0` |
| 港股收市簡報 | `/workspace/hk-brief/YYYY-MM-DD/HK brief-YYYY-MM-DD.md` (else `hk-brief-inputs/`) | 港股收市簡報庫 | `collection://803e4190-3dc3-4863-a15` (confirm full id from parent) |
| 家庭成長副手 | `/workspace/family-growth/*.md` | 家庭成長副手庫 | `collection://f20abc00-8111-49da-a9c1-19a7d171544a` |
| Career Coaching | `/workspace/career/*.md` | Career Coaching 庫 | `collection://6ecc93bd-b9b2-43ab-baed-4cd0f2159259` |
| HTML Motion Studio | project folder under `/workspace/html-motion-bot/*` or `/workspace/html-motion/*` with `index.html` / render MP4 | HTML Motion Studio 庫 | `collection://35bcc267-637c-4952-9108-ca697c3334a6` |
| YouTube Analyzer Deep | `/workspace/youtube-analyzer-deep/YYYY-MM-DD-*.md` (not `_notion_*`) | YouTube 深度摘要庫 | `collection://f1a63efc-764b-4a7b-b97d-35ff8fa5f525` |
| 文章分析 | `/workspace/article-analysis/{slug}-{YYYYMMDD-HHMM}-HKT.md` (not `input/` or `_notion_*`) | 文章分析 | `collection://54a385e9-2afe-4d06-95f3-27ff7cced4f4` |

### 文章分析 property map
Parent page: https://app.notion.com/p/3fc77383f89c811bb352eb0757c53dd8 — DB: https://app.notion.com/p/60643ef155054629ad8b299cb735f3df

| Notion property | Source |
|---|---|
| Name (title) | Article title from report/header |
| Analyzed Date | Stamp date (Asia/Hong_Kong) |
| Article URL | Header `文章URL` (omit if 無 URL) |
| Author | Appendix 作者（未知 → leave empty） |
| Recommendation | 推薦度 1–10 |
| Novelty | 新穎度 1–10 |
| Source | `article-analyzer` |
| TLDR | One-line core takeaway from §1 |
| Tags | Multi-select when clear: AI / Trading / Macro / Business / Product / Other |

State file: `/workspace/notion-briefs-import/sync-state.json` — map `library → { path → { page_url, mtime, imported_at } }`. Use library key `article-analysis` for this bot.

## Steps
1. Discover candidates newer than sync-state (or missing from it) matching Final patterns only.
2. Dedupe by date/title: search Notion (or query data source if quota allows). If a row already exists for that date/title and file mtime is unchanged, skip. If mtime newer, update page content + Attachments.
3. Create or update page in the data source: Name/Title, Date when applicable, Status/Tags=Final when that property exists, Source path note (plain path string — no markdown links). For 文章分析 fill the property map above.
4. **Body (critical):** pass `$file:/absolute/path/to/body.md` as the **entire** `content` (create) or `new_str` (replace_content) argument so CallDynamicTool expands the file. Never embed `$file:` inside markdown link/text — that stores a hollow path and leaves the page empty (bug 2026-10-15). Strip leading `#`/`##` title lines that duplicate the Notion Name property. Upload `.md` (and Motion `.html`/`.mp4` ≤ upload cap) to Attachments when possible.
5. **VERIFY body:** fetch the page after write; content must show real report prose (not a `$file:`/`file://` stub). If hollow, `replace_content` with expanded `$file:` body immediately.
6. Append successes to `sync-state.json` and `/workspace/notion-briefs-import/sync-log.jsonl`.
7. Report: count created / updated / skipped / failed + sample URLs. On catch-up with zero new Finals, stay silent to the user.

## VERIFY
- One row per Final date/title (no dupes).
- Page body is real markdown (fetch check), not a literal `$file:` path.
- Attachments present when upload succeeded.
- State file updated for every success.
- 文章分析 rows carry Recommendation/Novelty when the Final header has scores.

## Notes
- Prefer Notion MCP over browser.
- Do not import corpora under `cases/` or `article-analysis/input/`.
- If Query Data Source is usage-capped, fall back to search + sync-state.
- Immediate path: when delivering a Final in chat, run this for that file before ending the turn.
