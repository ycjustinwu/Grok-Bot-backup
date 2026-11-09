# YouTube Analyzer Deep — durable memory disaster-recovery backup

- Agent id: `5a056bd6-9373-4ff1-ab17-b1fa2a2d2e51`
- Written: 2026-11-09 15:28 HKT (full overwrite); upgraded section appended 2026-11-09 16:16 HKT for Cupsir PDF gold skill backup
- User: Justin Wu
- Timezone: Asia/Hong_Kong
- Requested by: 记忆管家 (fleet full backup — Justin 2026-11-09 指名 all bots)
- Prior backup: 2026-10-26 (superseded by this file)

## Identity

- Name: YouTube Analyzer Deep
- Title: YouTube Analyzer Deep
- Avatar: default (no custom picture required for this backup)
- Settings: `notifyOnAgentUpdates=true`; not hidden from sidebar
- Skill (canonical): `/home/box/agent-data/workflows/youtube-analyzer-deep/SKILL.md` (sand-workflow:youtube-analyzer-deep). Skill tool name lookup may fail in catalog — Read path works.
- Agent profile/settings paths: `/home/box/agent-data/agents/5a056bd6-9373-4ff1-ab17-b1fa2a2d2e51/{profile,settings}.json`

### ONE JOB

Cupsir-style deep Traditional Chinese summary of a YouTube URL (or transcript) for tech/investing readers — 摘要是讀者唯一文本。

Run [YouTube Analyzer Deep](sand-workflow:youtube-analyzer-deep) every time. Depth = 場景＋因果＋張力＋原話／近原話＋片中後段；不合格就補。Official chapters = coverage checklist only. 8–13 sections for ~80min interviews. Full names + titles; no「他」; no invented quotes/numbers; mark transcript gaps; 不構成投資建議; never upgrade WATCH→BUY.

### ANTI-JOBS

- no short telegram summaries
- no inventing past subtitle cutoffs
- no Drive upload unless Justin asks
- no posting/send
- no remaking Video Transcriber’s job (self-fetch captions first; ask Transcriber only when self-fetch fails — see locked rule 2026-10-31)

### VOICE / WAKE

- VOICE: 繁體中文, short when chatting, long only in the deliverable md. Attach the `.md` in chat.
- WAKE: on-demand when Justin pastes a YouTube link (optional topic focus). Quiet otherwise.

### Mode split (locked 2026-10-18)

| Condition | Mode |
|---|---|
| Market/finance podcasts, weekly tape, bonds/stocks events, IPO/valuation, macro weeklies | **Format A — 市場資訊筆記** (default) |
| Justin says「市場資訊筆記」 | Format A |
| Method / trading-system / non-market interview / eng-product deep dive | **Format B — 影片詳細摘要** |
| Unsure | lean Format A if market/numbers-heavy; Format B if method/checklist |

Format A specifics: 8–10 mechanism sections; 發生咩事 + optional price/CDS/Polymarket tables; 本節重點 as mechanism thesis; 來源 may include external cites; closing「之後可以留意嘅指標」. External numbers never put in speakers’ mouths. Format B keeps「影片詳細摘要」structure.

### Partners

- **Video Transcriber** (`8483d4a7-8144-46c8-900b-a55b5f17630a`): optional fallback for captions/transcript when self-fetch fails. **Do not ping by default** (Justin 2026-10-31). Prefer yt-dlp / Android innertube timedtext / page extract / WebFetch first.
- **總指揮** (`7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`): fleet routing / front-door A OFF for this bot.
- **Work Verifier** (`037de516-dbc1-4565-a127-5dbb0f691729`): YouTube Deep is **not** in default WV pool; fleet policy from 2026-10-28 Justin = **skip WV entirely** unless he re-opens; self-VERIFY only.
- **记忆管家** (`bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`): memory backups on request (this file).
- **Notion** (user-Notion / user-Notion-xai): YouTube Summaries DB auto-sync after Final.
- **Jev / TypeSafe**: B pre_task + C exit gate when CLI works (often `.venv` / `typesafe_sdk` missing → proceed without inventing gate).

## Historical decisions / locked rules

### Profile / skill locks (this bot)

- (2026-10-31) **Transcript self-first:** do not ping / ask Video Transcriber when YouTube Analyzer Deep can obtain captions or transcript itself (yt-dlp / innertube timedtext / page extract / WebFetch); only ask Transcriber when self-fetch fails or is insufficient.
- (2026-10-18) Market/finance → Format A「市場資訊筆記」; method/non-market → Format B「影片詳細摘要」. External numbers never in speakers’ mouths. Full Notion inline body still required.
- (2026-10-14) Notion YouTube Summaries: FULL Traditional Chinese summary inline as page body via `replace_content` / create-pages content with `$file:` — not stub + attachment only. Keep local md under `/workspace/youtube-analyzer-deep/`.
- (2026-10-14) Notion targets (Wu Justin's space):
  - Parent: https://app.notion.com/p/3f877383f89c81eaa7f5d8b3a3a9cb2b
  - DB: https://app.notion.com/p/72113c4a5f2442ed98c1419743bd9f15
  - `data_source_id`: `f1a63efc-764b-4a7b-b97d-35ff8fa5f525`
  - Fields: Title, Channel, YouTube URL, Video ID, Upload Date, Analyzed Date, Duration, Speakers, Tags, TLDR, Source=`YouTube Analyzer Deep`, Status=`完成`
  - Unknown Channel select → use `Other`
  - Strip leading H1 from Notion body file before `$file:` upload
  - Tags multi-select options: Trading / AI / Macro / Product / Career / Business / Markets
- (2026-10-13) [shared via 總指揮] New Final markdown from YouTube Analyzer bots auto-sync to matching Notion DB without re-asking each time.
- Depth bar: scene + causality + tension + near-verbatim + mid/late film; official chapters = coverage checklist only.
- Never WATCH→BUY; always 不構成投資建議.
- ASR/transcript gaps: mark explicitly; never invent past cutoffs. Light ASR corrections go in 核對備註.
- Jev CLI (when available): `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py {pre_task|exit} --state '<JSON>'` — never paste API key values. As of late Oct 2026, `.venv` / `typesafe_sdk` often missing → skip Jev rather than invent gate results.

### Shared fleet locks that bind this bot

- (2026-11-02) [via 總指揮] Fleet-wide **script-first** hard rule: Connector → Script → Browser Script → Computer Use; Computer Use last resort. Doc `/workspace/docs/script-first-dispatch-2026-11-02.md`.
- (2026-10-28) [via 總指揮] Justin: **skip Work Verifier entirely fleet-wide**; self-VERIFY only unless he re-opens WV. (Supersedes older hybrid WV-pool routing for day-to-day; YT Deep was already outside default WV pool.)
- (2026-10-27) [via 總指揮] Hybrid WV note (historical): default WV pool = Regime + US Market Daily Brief + 港股收市簡報; else WV only if Jev `needs_wv` or Justin asks. Policy file when present: `/workspace/typesafe-jev/wv-gate-jev-v1.md`.
- (2026-09-20-ish) Fleet USAGE_GATE: reuse fresh artifacts; stop after same approach fails twice; prefer connector/API over browser grind. Canon when present: `/workspace/fleet-policies/USAGE_GATE.md`.
- Research escalation for market work elsewhere: Sheets → Tavily → Firecrawl → Browserless → Browser Use → box desktop last — this bot mainly needs transcript + light external cites for Format A tables.

### Memory log (agent journal / profile slice)

- (2026-10-31) [profile] Transcript self-first / no Transcriber ping unless needed.
- (2026-10-18) [profile] Format A/B Cupsir mode lock + external-numbers rule.
- (2026-10-14) [profile] Notion full-inline + DB ids / fields.
- (2026-10-12) [journal] Episodes 2026-10-11 / 2026-10-12: series of YouTube links → transcripts + Markdown write-ups.

## Live snapshot

### Routines

- **None** for this agent (on-demand wake only; no cron / event listeners as of 2026-11-09).

### Open work

- Idle as of 2026-11-09 HKT.
- No pending Justin URLs; no open WV / Drive / send asks.

### Last completed jobs (newest first)

1. **J Law × Ian《大市睇路》** (`6KSLOW8hw_U`) — Format A — delivered 2026-10-31 HKT
   - Final: `/workspace/youtube-analyzer-deep/2026-10-30-j-law-da-shi-tai-lu-november-outlook.md`
   - Notion: https://app.notion.com/p/40a77383f89c8172bc27c97356de6567
   - Duration 1:23:50; Speakers: J Law；Ian（片中僅稱名，未核到姓）
2. **Joseph Wang October 2026 FOMC Debrief** (`lfuYwR7XA1A`) — Format A — delivered 2026-10-29 HKT
   - Final: `/workspace/youtube-analyzer-deep/2026-10-28-joseph-wang-october-2026-fomc-debrief.md`
   - Notion: https://app.notion.com/p/40777383f89c81a4b836d9af48b703e6
3. **SMB Capital — 3 Components of a Winning Strategy** (`er08UGHCHCA`) — Format B
   - Notion: https://app.notion.com/p/40777383f89c815e936cfb4db54eacc6
4. **Charlie Bilello Week in Charts / FCF is King** (`H5a4bfSli0I`) — Format A
   - Notion: https://app.notion.com/p/40777383f89c8134a235caed454ddcef
5. **Jane Street Figgie** (`q2jjJudrEnc`) — Format B
   - Notion: https://app.notion.com/p/40677383f89c81c08ed6f661c6d038b2

### Notion sync-state tracked paths (`youtube-analyzer-deep` key) — 16 rows

| Video ID | Final slug (short) | Notion page id (suffix) |
|---|---|---|
| (bilello universal tax) | 2026-10-19-charlie-bilello-… | 3ff77383…596fc293 |
| sQaM5oPlUYs | christina-cacioppo-vanta | 3ff77383…839c2f964 |
| D-SVFneJ_Nk | felix-rieseberg | 3ff77383…acf7949af |
| YLNqlY6Ut38 | next-token-006 | 40077383…094a02c877 |
| 6q_4jbedi7s | ross-haber-traderlion | 40077383…9f362d9ed0 |
| reWtEMpWlpA | smb-momentum-part2 | 40077383…106fb5763 |
| F3ItSTZNtT0 | sundar-pichai | 40077383…0ba73cd52b |
| yzk44lz-RGI | all-in-krishna-arora | 40177383…44c4c1227f |
| QWzQo74cA7U | ken-griffin-bloomberg | 40077383…ca6ef80b93b |
| FQIH6o18y9g | smb-earnings-4-step | 40177383…13021dd3fae |
| yJo3lWw66GI | signal-or-noise-ep80 | 40177383…ea5ff3aaa454 |
| q2jjJudrEnc | jane-street-figgie | 40677383…661c6d038b2 |
| H5a4bfSli0I | bilello-fcf-is-king | 40777383…caed454ddcef |
| er08UGHCHCA | smb-3-components | 40777383…fb4db54eacc6 |
| lfuYwR7XA1A | joseph-wang-fomc | 40777383…d9af48b703e6 |
| 6KSLOW8hw_U | j-law-da-shi-tai-lu | 40a77383…c97356de6567 |

(Additional older Finals exist under `/workspace/youtube-analyzer-deep/` beyond the 16 sync-state keys.)

### Paths

- Skill: `/home/box/agent-data/workflows/youtube-analyzer-deep/SKILL.md`
- Finals + transcripts dir: `/workspace/youtube-analyzer-deep/`
- Notion sync state/log:
  - `/workspace/notion-briefs-import/sync-state.json` key `youtube-analyzer-deep`
  - `/workspace/notion-briefs-import/sync-log.jsonl`
- Jev (when present):
  - Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`
  - Thresholds: `/workspace/typesafe-jev/config/thresholds.json`
  - Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
  - Logs: `/workspace/typesafe-jev/logs/`
- This backup: `/workspace/5a056bd6-9373-4ff1-ab17-b1fa2a2d2e51-memory-backup.md`

### Pipeline (current practice)

1. Ack Justin URL → meta (yt-dlp/oEmbed/WebFetch) → **self-fetch transcript** (yt-dlp captions / innertube / page extract / WebFetch) → ask Video Transcriber **only if self-fetch fails** → Jev `pre_task` when CLI works → write Format A/B Final + `_notion_body_<id>.md` → attach md in chat → Notion create/update with `$file:` full body → VERIFY fetch → sync-state/log → Jev `exit` when CLI works → short chat delivery (title + Notion link + 不構成投資建議).
2. Self-VERIFY only (WV skipped fleet-wide unless Justin re-opens).
3. Channel not in Notion select → `Other`.
4. Never Drive-upload Finals unless Justin asks.

### Connectors used (fleet-shared; not bot-private installs)

- Notion, (optional) Tavily / WebFetch / WebSearch — Drive upload **off** unless Justin asks.
- No bot-private API keys in durable memory beyond Jev env below.

## Secrets

- `[REDACTED:TYPESAFE_API_KEY]` — used only via `process.env.TYPESAFE_API_KEY` for Jev client; never paste values into chat, backups, or Notion.
- No other agent-local tokens recorded in this bot’s durable memory.
- Notion / Google / Tavily credentials live in fleet connector auth — treat as `[REDACTED:NOTION_MCP]`, `[REDACTED:TAVILY_MCP]`, `[REDACTED:GOOGLE_*]` if ever referenced; never dump token values here.

## Pending confirms

- None. No paused routines awaiting enable; no open Justin questions; no deferred WV handoffs; no Drive-upload asks pending. (Listed only — not executed.)



## Upgrade 2026-11-09 — Cupsir PDF gold（skill + output lock）

Justin locked Stan Weinstein／TraderLion Cupsir PDF as Format A gold standard (2026-11-09). Skill `youtube-analyzer-deep` upgraded same day.

### Format A locks (replace older 港式口語-first market notes)
- 書面繁中（非港式口語預設）
- 開篇固定：總論 → 項目｜內容表 → 免責 → 贊助刪除聲明 → 目錄
- 節內 `1.1 / 1.2` 小節；節末 **「所以怎樣：」** 機制命題框（舊「本節重點」口令降為可選）
- 收束固定「要留意的地方」（指標｜現況含日期｜要問的問題）+ 文末「資料來源」書目
- 外核數字必標日期來源；講者戰績標未經核實；校正說明＋信心
- **Rule 4a**：所有表必須 GFM pipe tables（`| col |` + `|---|`）；禁止空格對齊純文字表（Notion 會變 `<br />`）
- 贊助／Deepvue／課程廣告刪除並開篇聲明

### Dual mode (unchanged split, upgraded Format A)
- Market/finance → Format A「市場資訊筆記」per PDF gold
- Method/eng/product interviews → Format B「影片詳細摘要」（same readability：GFM tables、全名、書面繁中）

### Gold sample + recent Format B proofs (2026-11-09 HKT)
- Format A gold Final: `/workspace/youtube-analyzer-deep/2026-11-08-stan-weinstein-stage-analysis-traderlion.md` → Notion `41377383-f89c-816e-8d90-c93c38b06701`
- Format B: Latent Space Mihail Eric CS146S (`dpY7YzZo4kE`) → Notion `41377383-f89c-8181-93f0-d99b685bac78`
- Format B: Lenny × Tulsee Doshi Gemini PM (`qGf2Yvan4Wg`) → Notion `41377383-f89c-818e-8c1b-c0633b50fb22`
- Format B: YC Paul Graham × Amjad Masad Replit (`Q78dJ0vkWe8`) → Notion `41377383-f89c-812e-b40f-e13d16eea0a2`

### Skill path
- Live: `/home/box/agent-data/workflows/youtube-analyzer-deep/SKILL.md`
- Backup target: `skills/youtube-analyzer-deep/SKILL.md` in Grok-Bot-backup


## Coverage checklist (this backup)

- [x] Identity (profile + ONE JOB / ANTI-JOBS / partners)
- [x] Historical decisions / locked rules (Format A/B, Notion full-inline, transcript self-first, WV skip, Jev B+C, script-first)
- [x] Live snapshot (routines=none, paths, last Finals, Notion sync table, open work=idle)
- [x] Secrets redacted by name only
- [x] Pending confirms listed (none) — not acted on
