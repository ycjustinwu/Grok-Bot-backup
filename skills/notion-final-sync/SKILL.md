---
name: Notion Final Sync
description: >-
  Use when new Final markdown (or Motion HTML/MP4) from market briefs, family
  growth, career coaching, HTML Motion Studio, YouTube Analyzer, or 文章分析 should
  be upserted into the matching Notion database without waiting for the user to
  ask. Market Awareness and US Market Daily Brief run this themselves after Soft
  Final (create-new default). 總指揮 still syncs 港股收市簡報 and other libraries, and
  runs the catch-up safety net.
---
# Notion Final Sync

## When
After a Final deliverable lands on the box, or on a catch-up scan: upsert one row per Final into the mapped Notion DB. Skip drafts, intermediates (`abnormal-volume`, `inputs/`, `input/`, `_notion_body_*`, `cases/`), and duplicates for the same date/title.

**Owners (Justin 2026-11-24 AUTHORIZE, widget t1132s4841):**
- Market Awareness Orchestrator (`e4e8d80f-26c5-48c1-bd11-f56c0a9cc077`) and US Market Daily Brief (`44fb5c78-45d1-4716-b849-a5a6a0c1867b`) run this skill **themselves** after Soft Final + self-VERIFY (WV still skipped unless Justin re-opens). They deliver the Notion link in their own chats. They do **not** hand off routine sync to 總指揮, and they send no success FYI to 總指揮.
- 總指揮 still syncs 港股收市簡報 and the other libraries below, still takes MA/US Brief **failure** escalations (path, md5, error), and still runs catch-up routine `notion-finals-catch-up-sync`.
- Default is **create a new page**. Never `--update` / `--page-id` unless Justin explicitly asked to revise that same page. Never overwrite older Notion pages.

## Mapping (Justin / Wu Justin's space)
Keep collection ids current via Notion fetch if renamed.

| Bot / source | Final pattern on box | Notion parent | Data source | Who upserts |
|---|---|---|---|---|
| Market Awareness | `/workspace/market-awareness/YYYY-MM-DD/regime-daily-YYYY-MM-DD.md` | Market Awareness 制度日報庫 | `collection://ee81c980-05aa-4971-93d7-58b2ef01bc79` | **that bot** (`--library regime`; state key `market-awareness`) |
| US Market Daily Brief | `/workspace/us-market-daily-brief/YYYY-MM-DD/US brief-YYYY-MM-DD.md` (filename uses the **session** date; prefer this tree over `us-brief-output/` / `us-brief/`) | 美股市場每日簡報庫 | `collection://b65fa2ce-b87b-4547-9993-b12c60b1dee0` | **that bot** (`--library us-brief`; state key `us-market-brief`) |
| 港股收市簡報 | `/workspace/hk-brief/YYYY-MM-DD/HK brief-YYYY-MM-DD.md` (else `hk-brief-inputs/`) | 港股收市簡報庫 | `collection://803e4190-3dc3-4863-a15a-fbd0d9875ee4` | **總指揮** (`--library hk-brief`) |
| 家庭成長副手 | `/workspace/family-growth/*.md` | 家庭成長副手庫 | `collection://f20abc00-8111-49da-a9c1-19a7d171544a` | 總指揮 / owning bot (`--library family-growth`) |
| Career Coaching | `/workspace/career/*.md` | Career Coaching 庫 | `collection://6ecc93bd-b9b2-43ab-baed-4cd0f2159259` | 總指揮 / owning bot (`--library career`) |
| HTML Motion Studio | project folder under `/workspace/html-motion-bot/*` or `/workspace/html-motion/*` with `index.html` / render MP4 | HTML Motion Studio 庫 | `collection://35bcc267-637c-4952-9108-ca697c3334a6` | 總指揮 / owning bot (`--library html-motion`) |
| YouTube Analyzer Deep | `/workspace/youtube-analyzer-deep/YYYY-MM-DD-*.md` (not `_notion_*`) | YouTube 深度摘要庫 | `collection://f1a63efc-764b-4a7b-b97d-35ff8fa5f525` | 總指揮 / owning bot (`--library youtube`) |
| 文章分析 | `/workspace/article-analysis/{slug}-{YYYYMMDD-HHMM}-HKT.md` (not `input/` or `_notion_*`) | 文章分析 | `collection://54a385e9-2afe-4d06-95f3-27ff7cced4f4` | 總指揮 / owning bot (`--library article-analysis`) |

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

State file: `/workspace/notion-briefs-import/sync-state.json` — map `library → { path → { page_url, mtime, imported_at } }`. Catch-up routine `notion-finals-catch-up-sync` reads this file. Bots that self-push **must** let `upsert_final.py` write state so catch-up sees NOTHING_NEW.

## Steps
1. Discover the Final path and confirm self-VERIFY (WV skipped unless Justin re-opens). Never invent tickers, prices, scores, or Verdicts; read them from the file. For US Brief, Verdict character is 冇 (U+5187), never typo 冊 (U+518A).
2. **Preferred path — script:** `python3 /workspace/notion-briefs-import/upsert_final.py --library <canon> --path <abs.md> --name "<Name>" --date YYYY-MM-DD --md5 <digest>` plus file-accurate `--prop` / `--close-date` as needed. Token from process.env `NOTION_API_KEY` or `NOTION_TOKEN` only — never paste, never write the secret to disk or chat, never pass it as a flag. README: `/workspace/notion-briefs-import/README-upsert-final.md`.
3. Default **create-new**. Same path + same md5 already in `sync-state.json` is skipped (exit 0). The script refuses a duplicate Name without `--update --page-id`. Use `--update` only for an explicit wording revision of that same page. Do not `--dry-run` as a substitute for the real push.
4. Confirm the JSON receipt: `ok`, `action` (`created` / `skipped`), `body_verified`, `attachment`, `page_url`, `page_id`. State must be written. If the script fails (nonzero / `ok: false`) or leaves a half-written page, **escalate to 總指揮** with path, md5, and the error; do not silently continue. A Source Path autolink in Notion fetch (filename shown as a markdown link) is handled inside the script (fix 2026-11-24) and must not block attachment + state when the body otherwise verifies.
5. For `regime` / `us-brief` / `hk-brief`, also write the short vault index (no 14–18k paste): `python3 /workspace/obsidian-captain/scripts/add_final_note.py --library <regime|us-brief|hk-brief> --date YYYY-MM-DD --name "<Name>" --path <abs.md> --md5 <digest> --notion <page_url> ...`
6. **MA / US Brief delivery:** in **that bot’s own chat**, Notion-only — short status + Notion link. No full markdown paste/attach once synced. No routine success FYI to 總指揮.
7. **Fallback (MCP)** only if the script cannot run: search / query to dedupe; create or (explicit revise only) update; pass `$file:/absolute/path/to/body.md` as the **entire** `content` / `new_str` argument; never embed `$file:` inside markdown text (hollow-page bug 2026-10-15). Strip leading `#`/`##` title lines that duplicate Name. Then VERIFY by fetching the page (real prose, not a `$file:` stub), upload the `.md` attachment, and append `sync-state.json` + `/workspace/notion-briefs-import/sync-log.jsonl` yourself. Prefer not to use this fallback for MA / US Brief.
8. On catch-up with zero new Finals, stay silent to the user.

## VERIFY
- One row per Final date/title (no dupes; older pages left untouched).
- Page body is real markdown (receipt `body_verified` or fetch check), not a literal `$file:` path.
- Attachments present when upload succeeded.
- State file updated for every success so catch-up sees NOTHING_NEW.
- 文章分析 rows carry Recommendation/Novelty when the Final header has scores.

## Notes
- Prefer `upsert_final.py` over ad-hoc Notion MCP or browser.
- Do not import corpora under `cases/` or `article-analysis/input/`.
- If Query Data Source is usage-capped, fall back to search + sync-state.
- Immediate path: when delivering a Final in chat, run this for that file before ending the turn.
