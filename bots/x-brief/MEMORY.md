# X Brief memory snapshot
agent_id: 0ba0445d-a3df-4430-8a47-0eeb0cbbafcf
serverId: 156683
written_at: 2026-10-26T20:45+08:00 (Asia/Hong_Kong)
source: fleet disaster-recovery backup for 记忆管家
prior_snapshots:
- /workspace/156683-memory-backup.md (2026-09-14, 91 lines)
- /workspace/0ba0445d-a3df-4430-8a47-0eeb0cbbafcf-memory-backup.md (2026-10-03, superseded by this file)

## Identity
- Name: X Brief
- Title: (empty)
- User: Justin Wu
- User timezone (box/prompt): Asia/Hong_Kong (UTC+8). Brief timezone pref: unset.
- Harness: temporal
- ONE JOB: Read X (connector) and/or pasted handles → one concise brief Justin can skim. Never post on his behalf.
- PIPELINE: confirm handles/topics → fetch via X tools (small pulls) → cluster 3–7 themes with source links → write 繁體中文 or English to match ask (default 繁體中文 for finance days) → save `/workspace/x-brief/output/brief-YYYYMMDD-HHMM.md` + `LATEST.txt`.
- BOUNDARY: Market Awareness Orchestrator = regime score. US Market Daily Brief = ETF/themes. This bot = social/X narrative only. X Monitor = separate read-only signal bot.
- ANTI-JOBS: never post/reply/like/bookmark unless Justin explicitly orders it; do not run swing/regime analysis (hand to those bots); do not dump raw timelines — synthesize.
- VERIFY: no invented quotes or metrics; cite post URLs; if credits ~$0 or tools missing, say so and do not fabricate a brief.
- Partners / adjacent: 總指揮 (routing); X Monitor (markets/setups/AI signal, ≤8 items); Market Awareness Orchestrator / US Market Daily Brief (not this lane); Work Verifier only if Jev `needs_wv` or Justin asks (X Brief not in default WV pool); 记忆管家 (this backup).
- Output path (current profile): `/workspace/x-brief/output/brief-YYYYMMDD-HHMM.md` (Asia/Hong_Kong) and `LATEST.txt`. Directory exists. Legacy first brief still at `/home/box/x-brief/brief-2026-09-07.md`.
- Language: 繁體中文 or English to match Justin’s ask; default 繁體中文 for finance days. Delivered briefs so far have been English (Justin asked in English).
- Voice: plain, lead with the one thing worth knowing, one question at a time; never mention setup/file paths casually to Justin.
- X signed-in account (public, last read 2026-09-07): @Ycjustinwu / id 387109693 / display name Jwu.eth Ø
- X plugin 49086599: installed as of 2026-09-07; MCP `user-X` connected historically; Grok Bot shared public X namespace `x` also available for reads. Not re-probed this backup.
- Slack / Notion / Linear: not installed for this bot (user skipped optional plugins 2026-09-07).
- Usage gate (Justin via 總指揮, 2026-09-20, in agent profile memory): reuse a fresh artifact before browser/multi-source/retry/extra skill/subagent; same approach failed twice → stop and report; no tools needed → chat only; prefer connector or API over clicking a site; do not create more bots or routines to save usage. Canon: `/workspace/fleet-policies/USAGE_GATE.md`.
- Jev (B+C): TypeSafe client `/workspace/typesafe-jev/jev_client.py`; key `[REDACTED:TYPESAFE_API_KEY]`; skill `jev-fleet-decisions`. Front-door A OFF. This backup run: pre_task act=cheap_path, evidence_enough≈0.72, escalate≈0.2, cost_tier≈0.

## Historical decisions / locked rules
- 2026-09-07: Template setup. Routines Daily X brief and Weekly X recap created **paused** (`enabled=false`, provenance untrusted). Daily cron `CRON_TZ=Asia/Hong_Kong 0 9 * * 1-5`; Weekly `0 9 * * 5`. User asked to turn them on; **no yes**. They have **never run**.
- 2026-09-07: Optional plugins Slack (674), Notion (404), Linear (512) offered; user chose Skip optional plugins.
- 2026-09-07: Beat = AI, trading, finance. Starter watch list proposed and confirmed: 12 accounts + 5 topics + 5 searches. First 24h brief delivered in this chat.
- 2026-09-07: Working state lives in **files**, not memory: watch list, dated briefs, seen log. Watch list is source of truth. Same post never reported twice.
- 2026-09-07: After first brief, asked (skippable) what Justin uses the brief for — unanswered.
- 2026-09-07: Draft-by-default; never post/reply/like/DM without explicit yes.
- 2026-09-14: Agent profile rewritten (ONE JOB / PIPELINE / VERIFY / ANTI-JOBS / BOUNDARY). Output dir `/workspace/x-brief/output/`. Default language for finance days 繁體中文.
- 2026-09-14: Memory snapshot `/workspace/156683-memory-backup.md` (91 lines) reported to 记忆管家.
- 2026-10-03: Usage gate saved to agent profile memory; snapshot rewritten at this path (97 lines).
- 2026-10-04: Justin asked “give me daily X brief”. Window = **last 24h only** (not the Sep 7–Oct 4 gap). Brief saved under profile path; seen log appended; delivered in chat with attachment. Credits after pull ~$14.52 (was ~$14.67 before).
- X MCP practice locked: read x-api-mcp-guide before calls; keep pulls small; search `max_results` minimum 10; default daily window = last 24h unless Justin asks for catch-up (then estimate cost and wait for yes).
- Signal bar (default): launch/new version, funding/hiring/departure, published number/benchmark, strong claim from someone with standing, thread worth keeping, shift in the argument. Skip bait, bare reposts, unsourced screenshots, motivation, giveaways, empty drama, rehashes. Cap ~12 items. Every item needs a real URL. Quote ≤20 words.
- Skills persisted (user-created): Getting started; Build the X watch list; Daily X brief; Weekly X recap; Read a thread or post; Draft a post or reply. Plus fleet `jev-fleet-decisions`.

## Live snapshot
### Prefs
- beat = AI, trading, finance
- accounts / topics / searches = starter list tracked
- mute list = unset
- X connected = yes (as of 2026-09-07; not re-probed 2026-10-26)
- timezone = unset (box default Asia/Hong_Kong)
- brief hour = unset (routines placeholder 09:00)
- brief days = weekdays
- brief destination = this chat
- signal bar = default
- post drafts wanted = unset

### Watch list (12 accounts, 5 topics, 5 searches)
Accounts (ids from 2026-09-07): karpathy `33836629`; sama `1605`; OpenAI `4398626122`; AnthropicAI `1353836358901501952`; demishassabis `1482581556`; AndrewYNg `216939636`; DeItaone `2704294333`; LiveSquawk `59393368`; unusual_whales `1200616796295847936`; zerohedge `18856867`; WSJ `3108351`; Bloomberg `104237736`.
Topics: AI model launches & agents; LLM benchmarks & evals; Quant / algo trading; Macro & Fed; Crypto markets BTC ETH.
Searches: GPT/Claude/Gemini/Llama launch|release|agent; LLM benchmark|eval; quant|algo trading; Fed|FOMC|interest rate; Bitcoin|BTC|Ethereum|ETH price.
Mute list: unset
File: `/home/box/x-brief/watch-list.md` (unchanged since 2026-09-07)

### Routines (both paused, never run — automation_status 2026-10-26)
- Daily X brief: weekdays 09:00 HKT (`0 9 * * 1-5`); runtime folder `9c9dd386-86b2-5e8b-a81d-7d1371d4cad5`; on-disk slug `daily-x-brief`; enabled false; never run
- Weekly X recap: Friday 09:00 HKT (`0 9 * * 5`); runtime folder `963e75cd-7c86-5d57-9203-7b19bcd53cac`; on-disk slug `weekly-x-recap`; enabled false; never run

### Briefs delivered
1. **2026-09-07** — `/home/box/x-brief/brief-2026-09-07.md` — 6 items. One thing: @sama amplified @merettm (Jakub Pachocki) “An Alien Mind”. Themes: AI next years; macro/oil; Asia equities. Quiet: karpathy, OpenAI, AnthropicAI, demishassabis, AndrewYNg, Bloomberg. Credits then ~$15.00.
2. **2026-10-04 ~13:37 HKT** — `/workspace/x-brief/output/brief-20261004-1337.md` (also pointed by `LATEST.txt`) — 2 items, English. One thing: @sama on religious force / human judgment as safety issue. Other: @DeItaone Lukoil oil deal in Ukraine talks. Quiet: karpathy, OpenAI, AnthropicAI, demishassabis, AndrewYNg, LiveSquawk, Bloomberg. Below bar: unusual_whales, zerohedge, WSJ; launch-search rumors skipped. Credits after ~$14.52.
- No brief since 2026-10-04 as of this snapshot.

### Seen log (8 links)
File: `/home/box/x-brief/seen-log.md`
- 2026-09-07 https://x.com/merettm/status/2096630018495377464
- 2026-09-07 https://x.com/sama/status/2096647371983880383
- 2026-09-07 https://x.com/unusual_whales/status/2096819247225647435
- 2026-09-07 https://x.com/LiveSquawk/status/2096914851943600132
- 2026-09-07 https://x.com/DeItaone/status/2096722845329998080
- 2026-09-07 https://x.com/zerohedge/status/2096964520514121767
- 2026-10-04 https://x.com/sama/status/2106388373221118198
- 2026-10-04 https://x.com/DeItaone/status/2106397175773040657

### Paths
- Watch list: `/home/box/x-brief/watch-list.md`
- Seen log: `/home/box/x-brief/seen-log.md`
- Output dir: `/workspace/x-brief/output/`
- LATEST: `/workspace/x-brief/output/LATEST.txt` → `brief-20261004-1337.md`
- Usage gate: `/workspace/fleet-policies/USAGE_GATE.md`
- Profile: `/home/box/agent-data/agents/0ba0445d-a3df-4430-8a47-0eeb0cbbafcf/profile.json`

### Open work
- None in flight. Routines remain paused. No catch-up of Sep 7–Oct 3 gap unless Justin asks (cost estimate + yes required).

### Credits
- Last observed after 2026-10-04 brief: about $14.52 (not re-fetched 2026-10-26)
- Secret: [REDACTED:X_API_CREDENTIALS] — OAuth via X plugin / shared X tools only; never stored here

## Secrets placeholders only
- [REDACTED:TYPESAFE_API_KEY]
- [REDACTED:X_OAUTH_TOKEN]
- [REDACTED:X_API_CREDENTIALS]
- [REDACTED:SLACK_BOT_TOKEN] — plugin not installed for this bot
- [REDACTED:NOTION_TOKEN] — plugin not installed for this bot
- [REDACTED:LINEAR_API_KEY] — plugin not installed for this bot
No real tokens, keys, or session cookies in this file.

## Pending confirms (Justin) — list only; do not act
- Turn Daily X brief / Weekly X recap on (both paused; no yes)
- Timezone + brief hour (needed before arming routines)
- What the brief is used for (custom signal bar)
- Mute list
- Post drafts wanted yes/no
- Brief destination still this chat unless changed
- Whether catch-up of long quiet gaps is ever wanted (default remains last-24h only)
