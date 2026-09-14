# X Brief memory snapshot
agent_id: 0ba0445d-a3df-4430-8a47-0eeb0cbbafcf
serverId: 156683
written_at: 2026-09-14T20:32+08:00 (Asia/Hong_Kong)
source: disaster-recovery backup for 记忆管家

## Identity
- Name: X Brief
- Title: (empty)
- User: Justin Wu
- User timezone (box/prompt): Asia/Hong_Kong (UTC+8). Brief timezone pref: unset.
- ONE JOB: Read X (connector) and/or pasted handles → one concise brief Justin can skim. Never post on his behalf.
- BOUNDARY: Market Awareness Orchestrator = regime score. US Market Daily Brief = ETF/themes. This bot = social/X narrative only.
- ANTI-JOBS: never post/reply/like/bookmark unless Justin explicitly orders it; do not run swing/regime analysis; do not dump raw timelines.
- VERIFY: no invented quotes or metrics; cite post URLs; if credits ~$0 or tools missing, say so and do not fabricate a brief.
- Output path (current profile): `/workspace/x-brief/output/brief-YYYYMMDD-HHMM.md` (Asia/Hong_Kong) and `LATEST.txt`. Legacy first brief lives at `/home/box/x-brief/brief-2026-09-07.md`.
- Language: 繁體中文 or English to match Justin’s ask; default 繁體中文 for finance days. First brief was English.
- Voice: plain, lead with the one thing worth knowing, one question at a time, never mention setup or file locations in user chat.
- X signed-in account (public): @Ycjustinwu / id 387109693 / display name Jwu.eth Ø
- X plugin 49086599: installed; MCP `user-X` connected (account=default)
- Slack / Notion / Linear: not installed (user skipped 2026-09-07)

## Historical decisions
- 2026-09-07: Template setup. Routines Daily X brief and Weekly X recap created paused (`enabled=false`, provenance untrusted). Daily cron `0 9 * * 1-5`; Weekly `0 9 * * 5`. User was asked to turn them on; no yes received — they stay paused and have never run.
- 2026-09-07: Optional plugins Slack (674), Notion (404), Linear (512) offered; user chose Skip optional plugins.
- 2026-09-07: User beat set to AI, trading, finance. Starter watch list proposed and confirmed: 12 accounts + 5 topics. First 24h brief run and delivered in this chat.
- 2026-09-07: Working state lives in files, not memory: watch list, dated briefs, seen log. Watch list is source of truth. Same post never reported twice.
- 2026-09-07: After first brief, asked (skippable) what Justin uses the brief for — unanswered.
- 2026-09-07: Draft-by-default; never post/reply/like/DM without explicit yes.
- 2026-09-14: Agent profile rewritten (ONE JOB / PIPELINE / VERIFY / ANTI-JOBS / BOUNDARY). Output dir moved to `/workspace/x-brief/output/`. Default language for finance days is 繁體中文.
- Skills persisted (user-created): Getting started; Build the X watch list; Daily X brief; Weekly X recap; Read a thread or post; Draft a post or reply.

## Live snapshot
### Prefs (fill during getting started)
- beat = AI, trading, finance
- accounts = starter list tracked (see watch list)
- topics and searches = starter list tracked
- mute list = unset
- X connected = yes
- timezone = unset (box default Asia/Hong_Kong)
- brief hour = unset (routines placeholder 09:00)
- brief days = weekdays
- brief destination = this chat
- signal bar = default
- post drafts wanted = unset

### Watch list (12 accounts, 5 topics, 5 searches)
Accounts: karpathy; sama; OpenAI; AnthropicAI; demishassabis; AndrewYNg; DeItaone; LiveSquawk; unusual_whales; zerohedge; WSJ; Bloomberg.
Topics: AI model launches & agents; LLM benchmarks & evals; Quant / algo trading; Macro & Fed; Crypto markets BTC ETH.
Searches (connector): GPT/Claude/Gemini/Llama launch|release|agent; LLM benchmark|eval; quant|algo trading; Fed|FOMC|interest rate; Bitcoin|BTC|Ethereum|ETH price.
Mute list: unset
File: `/home/box/x-brief/watch-list.md`

### Routines
- Daily X brief [paused] weekdays 09:00; folder daily-x-brief; lastRunAt null
- Weekly X recap [paused] Friday 09:00; folder weekly-x-recap; lastRunAt null

### Last brief
- Date: 2026-09-07 HKT
- File: `/home/box/x-brief/brief-2026-09-07.md`
- 6 items from 5 accounts + 1 search. One thing: @sama amplified @merettm (Jakub Pachocki) “An Alien Mind”. Themes: AI next years; macro/oil; Asia equities. Quiet: karpathy, OpenAI, AnthropicAI, demishassabis, AndrewYNg, Bloomberg.

### Seen log (6 links, 2026-09-07)
- https://x.com/merettm/status/2096630018495377464
- https://x.com/sama/status/2096647371983880383
- https://x.com/unusual_whales/status/2096819247225647435
- https://x.com/LiveSquawk/status/2096914851943600132
- https://x.com/DeItaone/status/2096722845329998080
- https://x.com/zerohedge/status/2096964520514121767
File: `/home/box/x-brief/seen-log.md`

### Credits (as of 2026-09-07 session)
- total_balance last read: about $15.00 (not re-fetched this backup run)
- Secret: [REDACTED:X_API_CREDENTIALS] — OAuth via X plugin only; never stored here

## Secrets placeholders only
- [REDACTED:X_OAUTH_TOKEN]
- [REDACTED:X_API_CREDENTIALS]
- [REDACTED:SLACK_BOT_TOKEN] — plugin not installed
- [REDACTED:NOTION_TOKEN] — plugin not installed
- [REDACTED:LINEAR_API_KEY] — plugin not installed
No real tokens, keys, or session cookies in this file.

## Pending confirms (Justin)
- Turn Daily X brief / Weekly X recap on (both paused; no yes)
- Timezone + brief hour (needed before offering/arming routines)
- What the brief is used for (signal bar)
- Mute list
- Post drafts wanted yes/no
- Brief destination still this chat unless changed
- Whether to migrate saved briefs to `/workspace/x-brief/output/` per new profile
