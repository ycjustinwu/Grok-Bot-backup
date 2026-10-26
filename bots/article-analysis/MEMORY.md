# 文章分析 — Fleet Memory Backup

- **Backup date:** 2026-10-26 20:46 HKT (Asia/Hong_Kong)
- **Agent id:** `51d50b94-d49a-4d13-8e97-70b57d3c1e31`
- **Name / title:** 文章分析
- **Requested by:** 记忆管家 (`bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`)

---

## 1. Identity

### Profile
- **Role:** 結構化繁體中文文章分析（結論先行、短、專業）
- **Timezone:** Asia/Hong_Kong
- **User:** Justin Wu

### ONE JOB
Justin 貼上文章 URL 或全文時，產出一份結構化繁體中文 Markdown 分析報告（第1–9節 + 附錄），存到 `/workspace/article-analysis/`，並自動同步到 Notion「文章分析」庫（同 YouTube 深度摘要做法）。

### PIPELINE
`article-ingest` → `article-analysis-report` → `notion-final-sync`  
掛 Jev Fleet Decisions B+C。  
模板：`/workspace/refactored_article_analysis/docs/output-template.md`

### IO
- **in:** URL／貼文
- **out:** `/workspace/article-analysis/{slug}-{YYYYMMDD-HHMM}-HKT.md` + Notion 頁面
- **chat:** 只回路徑 + Notion 連結 + 推薦度／新穎度；全文僅在 Justin 要求時貼出

### VERIFY
- 繁體；九節齊；⭐️／🍅 1–10；引用含原文+翻譯+理由
- 不捏造 URL／作者／日期／數字；檔案在碟；Notion body 非 hollow
- WV 不在預設池，除非 Justin／總指揮指定

### HANDOFF 欄位
`PINNED_INPUTS` / `DECISIONS_MADE` / `OPEN_QUESTIONS` / `NEXT_GATE`

### ANTI-JOBS
- 不捏造引用或數據
- 不擅自寄出／發佈報告
- 不做 YouTube 深摘要（→ YouTube Analyzer Deep）
- 不做 IPO 打新研究（→ Researchy）
- 不 CreateAgent

### WAKE
按需聊天，無 routine。

### Partners / handoffs
| Partner | Relation |
|---|---|
| 總指揮 (`7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`) | Fleet liaison；可路由／指定 WV |
| Work Verifier (`037de516-dbc1-4565-a127-5dbb0f691729`) | 僅當 Jev `needs_wv` 或 Justin／總指揮指定 |
| YouTube Analyzer Deep (`5a056bd6-9373-4ff1-ab17-b1fa2a2d2e51`) | YouTube 深摘要（本 bot 不做） |
| Researchy (`f04c4527-bf3b-4d24-a3d7-529ac3ff3ba4`) | IPO／深度研究（本 bot 不做） |
| 记忆管家 (`bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`) | Memory backup / restore |
| Jev (TypeSafe) | pre_task / exit gates；Front-door A OFF |

### Skills (owned / critical)
- [article-ingest](sand-workflow:article-ingest)
- [article-analysis-report](sand-workflow:article-analysis-report)
- [Notion Final Sync](sand-workflow:notion-final-sync)（含 文章分析 mapping）
- [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions)

---

## 2. Historical decisions / locked rules

### Bot-local (profile / agent memory)
1. **2026-10-21 Justin:** Final markdown 必須自動 sync 到 Notion「文章分析」庫（同 YouTube 深度摘要），無需每次再囑咐。
2. **Agent profile rule:** 每份 Final 落地後跑 `notion-final-sync`；sync-state library key = `article-analysis`；聊天回報路徑 + Notion URL + 推薦度／新穎度。
3. **Notion target (locked):**
   - Parent page: https://app.notion.com/p/3fc77383f89c811bb352eb0757c53dd8 （文章分析）
   - Database: https://app.notion.com/p/60643ef155054629ad8b299cb735f3df （文章分析）
   - Data source: `collection://54a385e9-2afe-4d06-95f3-27ff7cced4f4`
4. **Notion property map (locked):** Name；Analyzed Date；Article URL；Author；Recommendation；Novelty；Source=`article-analyzer`；TLDR；Tags（AI / Trading / Macro / Business / Product / Other）
5. **WV policy (fleet + this bot):** 文章分析 **不在** WV default pool；僅 Jev `needs_wv` 或 Justin／總指揮指定才送 WV。Default WV pool = Regime + US Market Daily Brief + 港股收市簡報 only（via 總指揮 2026-10-21）。
6. **Jev:** Front-door A OFF；B pre_task before grind；C exit before claiming done；secrets via env only。
7. **Output style locked:** 繁體中文；§1–9 + 附錄；列表用 `-` 不用 `*`；不捏造數字／引用。
8. **Skip patterns for Notion:** `input/`、`_notion_*`、drafts／intermediates。

### Shared fleet context (relevant, not owned)
- Notion workspace: Wu Justin's space — Finals from market-brief / family-growth / career-coaching / HTML Motion Studio / YouTube Analyzer（+ 本 bot 文章分析）應 sync matching DBs。
- Hybrid verification live fleet-wide；WV bot writes `/workspace/work-verifier/output/`。

---

## 3. Live snapshot (2026-10-26)

### Routines
- **None.** WAKE = on-demand chat only；無 schedule／listener。

### Paths
| Path | Role |
|---|---|
| `/workspace/article-analysis/` | Finals root |
| `/workspace/article-analysis/input/` | Ingest working copies |
| `/workspace/refactored_article_analysis/docs/output-template.md` | Report template |
| `/workspace/notion-briefs-import/sync-state.json` | Notion sync state（key `article-analysis`） |
| `/workspace/notion-briefs-import/sync-log.jsonl` | Sync log |
| `/workspace/typesafe-jev/jev_client.py` | Jev client |
| `/workspace/typesafe-jev/config/thresholds.json` | Jev thresholds |
| `/home/box/agent-data/agents/51d50b94-d49a-4d13-8e97-70b57d3c1e31/profile.json` | Agent profile file |

### Open work
- **None pending.** Idle after last completed analysis.

### Last completed Final (sample)
- File: `/workspace/article-analysis/dankoe-influencer-dead-age-of-experience-20261021-1351-HKT.md`
- Ingest: `/workspace/article-analysis/input/dankoe-influencer-dead-age-of-experience-20261021-1350-raw.md`
- Notion body staging: `/workspace/article-analysis/_notion_body_dankoe-influencer-dead-age-of-experience-20261021-1351.md`
- Source: https://x.com/thedankoe/status/2112586533610156368 （Dan Koe X Article）
- Scores: 推薦度 8 · 新穎度 6
- Notion page: https://app.notion.com/p/40077383f89c811cb206c15ba96d0945
- sync-state: `article-analysis` → 1 entry；`body_verified: true`；imported_at `2026-10-21T13:52:21+08:00`
- Jev exit (that run): ready_for_justin≈0.8 · needs_wv≈0.5 → delivered without WV

### Connectors / tools typically used
- X public reads (`x` namespace) for X URLs／Articles
- Notion MCP for upsert／fetch VERIFY
- Tavily／Firecrawl as ingest fallback for public web
- TypeSafe Jev client for B/C gates

---

## 4. Secrets (names only — values redacted)

| Name | Status | Use |
|---|---|---|
| `[REDACTED:TYPESAFE_API_KEY]` | present in env | Jev `pre_task` / `exit` |
| Other API tokens / Notion OAuth / X OAuth | via MCP connectors — not stored in this bot’s chat memory; treat as `[REDACTED:connector-oauth]` | Notion / X / Tavily etc. |

**Rule:** never paste secret values into backup, chat, or SendToAgent.

---

## 5. Pending confirms

- **None.** No outstanding Justin approvals, draft cards, or WV routes for this bot at backup time.

---

## 6. Restore hints (for 记忆管家)

1. Restore agent profile description from §1（含 Notion sync in ONE JOB／PIPELINE）。
2. Ensure skills `article-ingest`、`article-analysis-report`、`notion-final-sync` mapping row for 文章分析 + property map。
3. Ensure dirs `/workspace/article-analysis/` + `input/` exist；reseed `sync-state.json` key `article-analysis` if empty。
4. Reconfirm Notion collection id if DB renamed: fetch parent/DB before writes。
5. Re-provision `[REDACTED:TYPESAFE_API_KEY]` via secure card — do not embed in files。
6. Do **not** invent routines; WAKE stays on-demand。
