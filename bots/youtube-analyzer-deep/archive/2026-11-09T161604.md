# YouTube Analyzer Deep — durable memory disaster-recovery backup

- Agent id: `5a056bd6-9373-4ff1-ab17-b1fa2a2d2e51`
- Server id: `12183283`
- Written: 2026-10-26 (HKT)
- User: Justin Wu
- Timezone: Asia/Hong_Kong
- Requested by: 记忆管家 (fleet memory backup 2026-10-26)

## Identity

- Name: YouTube Analyzer Deep
- Title: empty
- Avatar: default (no custom picture required for this backup)
- Settings: `notifyOnAgentUpdates=true`; not hidden from sidebar
- Harness: temporal
- Skill (canonical): `/home/box/agent-data/workflows/youtube-analyzer-deep/SKILL.md` (sand-workflow:youtube-analyzer-deep). Skill tool name lookup may fail in catalog — Read path works.

### ONE JOB

Cupsir-style deep Traditional Chinese summary of a YouTube URL (or transcript) for tech/investing readers — 摘要是讀者唯一文本。

Run [YouTube Analyzer Deep](sand-workflow:youtube-analyzer-deep) every time. Depth = 場景＋因果＋張力＋原話／近原話＋片中後段；不合格就補。Official chapters = coverage checklist only. 8–13 sections for ~80min interviews. Full names + titles; no「他」; no invented quotes/numbers; mark transcript gaps; 不構成投資建議; never upgrade WATCH→BUY.

### ANTI-JOBS

- no short telegram summaries
- no inventing past subtitle cutoffs
- no Drive upload unless Justin asks
- no posting/send
- no remaking Video Transcriber’s job (ask it or captions for transcript, then write)

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

- **Video Transcriber** (`8483d4a7-8144-46c8-900b-a55b5f17630a`): caption/transcript source of truth; do not remake its job; may tip silently when captions land.
- **總指揮** (`7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4`): fleet routing / front-door A OFF for this bot; high-stakes WV routing stays with 總指揮 when needed.
- **Work Verifier** (`037de516-dbc1-4565-a127-5dbb0f691729`): YouTube Deep is **not** in default WV pool; route only if Jev `needs_wv` high or Justin asks.
- **Notion** (user-Notion / user-Notion-xai): YouTube Summaries DB auto-sync after Final.
- **Jev / TypeSafe**: B pre_task + C exit gate (see below).

## Historical decisions / locked rules

### Profile / skill locks

- (2026-10-18) Market/finance → Format A「市場資訊筆記」; method/non-market → Format B「影片詳細摘要」. External numbers never in speakers’ mouths. Full Notion inline body still required.
- (2026-10-14) Notion YouTube Summaries: FULL Traditional Chinese summary inline as page body via `replace_content` / create-pages content with `$file:` — not stub + attachment only. Keep local md under `/workspace/youtube-analyzer-deep/`.
- (2026-10-14) Notion targets (Wu Justin's space):
  - Parent: https://app.notion.com/p/3f877383f89c81eaa7f5d8b3a3a9cb2b
  - DB: https://app.notion.com/p/72113c4a5f2442ed98c1419743bd9f15
  - `data_source_id`: `f1a63efc-764b-4a7b-b97d-35ff8fa5f525`
  - Fields: Title, Channel, YouTube URL, Video ID, Upload Date, Analyzed Date, Duration, Speakers, Tags, TLDR, Source=`YouTube Analyzer Deep`, Status=`完成`
  - Unknown Channel select → use `Other`
  - Strip leading H1 from Notion body file before `$file:` upload
- (2026-10-13) [shared via 總指揮] New Final markdown from YouTube Analyzer bots auto-sync to matching Notion DB without re-asking each time.
- Depth bar: scene + causality + tension + near-verbatim + mid/late film; official chapters = coverage checklist only.
- Never WATCH→BUY; always 不構成投資建議.
- ASR/transcript gaps: mark explicitly; never invent past cutoffs. Light ASR corrections go in 核對備註 (e.g. real GP→GDP).
- yt-dlp / oEmbed / Tavily extract / Video Transcriber captions OK for transcript; Transcriber definitive when it lands after a draft path.
- Jev CLI: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py {pre_task|exit} --state '<JSON>'` — mode positional required; never paste API key values.

### Shared fleet locks that bind this bot

- (2026-10-21) [via 總指揮] Work Verifier default pool = Regime + US Market Daily Brief + 港股收市簡報 only. YouTube Analyzer Deep uses WV only if Jev `needs_wv` or Justin asks.
- (2026-09-20-ish) Fleet USAGE_GATE: reuse fresh artifacts; stop after same approach fails twice; prefer connector/API over browser grind; do not spawn extra bots/routines just to save usage. Canon when present: `/workspace/fleet-policies/USAGE_GATE.md`.
- Research escalation for market work elsewhere: Sheets → Tavily → Firecrawl → Browserless → Browser Use → box desktop last — prefer MCP; this bot mainly needs transcript + light external cites for Format A tables.

### Memory log (agent journal / profile slice)

- (2026-10-12) [journal] Episodes 2026-10-11 / 2026-10-12: series of YouTube links → transcripts + Markdown write-ups.
- Profile facts: Format A/B mode lock (2026-10-18); Notion full-inline + DB ids (2026-10-14).

## Live snapshot

### Routines

- **None** for this agent (on-demand wake only; no cron / event listeners).

### Open work

- Idle as of 2026-10-26 HKT.
- Last completed job: Creative Planning *Signal or Noise* Ep 80 (`yJo3lWw66GI`) — Format A 市場資訊筆記.
  - Final: `/workspace/youtube-analyzer-deep/2026-10-22-signal-or-noise-ep80-biggest-myths.md`
  - Notion body: `/workspace/youtube-analyzer-deep/_notion_body_yJo3lWw66GI.md`
  - Transcript: `/workspace/youtube-analyzer-deep/yJo3lWw66GI-transcript.txt`
  - Notion page: https://app.notion.com/p/40177383f89c814bb8acea5ff3aaa454
  - Speakers: Charlie Bilello; Peter Mallouk (Creative Planning)
  - Delivered to Justin in chat + Notion synced (2026-10-23 HKT); Jev exit previously `ready_for_justin` high / `needs_wv` low → no WV.

### Paths

- Skill: `/home/box/agent-data/workflows/youtube-analyzer-deep/SKILL.md`
- Finals + transcripts dir: `/workspace/youtube-analyzer-deep/`
  - Dated Finals (`2026-*.md`): **32** files on disk (incl. one `.body.md` companion)
  - Recent Finals (sample): Ken Griffin Bloomberg; All-In Krishna/Arora; SMB earnings 4-step; Signal or Noise Ep80
- Notion sync state/log (shared import harness):
  - `/workspace/notion-briefs-import/sync-state.json` key `youtube-analyzer-deep` (recent tracked ~11 paths) + `libraries.youtube` (~31 seeded/imported)
  - `/workspace/notion-briefs-import/sync-log.jsonl`
- Jev:
  - Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`
  - Thresholds: `/workspace/typesafe-jev/config/thresholds.json`
  - Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
  - Logs: `/workspace/typesafe-jev/logs/`
- Agent profile/settings: `/home/box/agent-data/agents/5a056bd6-9373-4ff1-ab17-b1fa2a2d2e51/{profile,settings}.json`
- This backup: `/workspace/5a056bd6-9373-4ff1-ab17-b1fa2a2d2e51-memory-backup.md`

### Pipeline (current practice)

1. Ack Justin URL → meta (yt-dlp/oEmbed) → transcript (Transcriber and/or captions/Tavily) → Jev `pre_task` → write Format A/B → attach md → Notion create/update with `$file:` full body → VERIFY fetch → sync-state/log → Jev `exit` → short chat delivery (title + Notion link + 不構成投資建議).
2. Tags typically include Trading and/or Markets (+ show-specific).
3. Channel not in Notion select → `Other`.

### Connectors used (fleet-shared; not bot-private installs)

- Notion, Tavily, (optional) Google Drive — Drive upload **off** unless Justin asks.
- No bot-private API keys in durable memory beyond Jev env below.

## Secrets

- `[REDACTED:TYPESAFE_API_KEY]` — used only via `process.env.TYPESAFE_API_KEY` for Jev client; never paste values into chat, backups, or Notion.
- No other agent-local tokens recorded in this bot’s durable memory.
- Notion / Google / Tavily credentials live in fleet connector auth — treat as `[REDACTED:NOTION_MCP]`, `[REDACTED:TAVILY_MCP]`, `[REDACTED:GOOGLE_*]` if ever referenced; never dump token values here.

## Pending confirms

- None. No paused routines awaiting enable; no open Justin questions; no deferred WV handoffs; no Drive-upload asks pending.

## Coverage checklist (this backup)

- [x] Identity (profile + ONE JOB / ANTI-JOBS / partners)
- [x] Historical decisions / locked rules (Format A/B, Notion full-inline, WV pool exclusion, Jev B+C)
- [x] Live snapshot (routines=none, paths, last Final, open work=idle)
- [x] Secrets redacted by name only
- [x] Pending confirms listed (none) — not acted on
