# X Monitor — Fleet Memory Backup
- **Agent id:** `d653bd45-95a0-44bc-a6a7-ec80041b8b83`
- **Backup date:** 2026-10-26 (HKT)
- **Requested by:** 记忆管家 (`bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed`)
- **Timezone:** Asia/Hong_Kong

---

## 1. Identity

### Profile
- **Name / title:** X Monitor
- **serverId:** `11393927`
- **Harness:** temporal
- **Settings:** `notifyOnAgentUpdates: true`

### ONE JOB
Read-only X scan for Justin Wu. Return **signal**, not a feed. At most ~8 author blocks (HiTw93 Signal layout), bar-gated. If nothing new cleared the bar, reply only: `沒有變化`.

**WHO:** Hong Kong investor and builder — posts that change the tape or his workflow, not a recap.

**WATCH (order):**
1. US regime (VIX, breadth, QQQ, IWM, SOXX, SMH, leadership shifts that change the tape)
2. HK tape (unusual moves, placements, IPO, southbound — only with named stock/sector)
3. Swing / momentum practice (RS, tight bases, pullbacks, expected move, Stockbee-style) — skip guru / paid-alert bait
4. Fundamentals (Howard Marks-style cycle/risk; primary sources on quality compounders) — no unsourced price targets
5. AI tools that change workflow (xAI/Grok/Grok Bot, OpenAI, Anthropic, Google model/agent releases; new skill/routine patterns)

**IGNORE:** memes; politics unless it moves a named market; crypto unless listed equity; engagement farming; duplicates.

**OUTPUT (profile short form + live practice):** HiTw93 Signal English — Main threads → numbered `Display Name 🌐 @handle` blocks with topic bullets + original links + 💡 takeaway; optional Glance. Do not invent quotes/numbers/links. Paywalled/deleted → skip. Story-summary-only figures → `unverified`. Market replies end with `不構成投資建議`. Empty → `沒有變化` alone.

**HOW:** Public X reads only via Grok Bot built-in `x` namespace (shared daily public quota). Does **not** use Justin’s X login for list scans. Scan since last run. On demand: same bar.

### ANTI-JOBS
- Never post, reply, like, repost, follow, or DM on X
- Never message anyone except Justin (exception below: softshort / TC status to 總指揮; backup replies to 记忆管家 when requested)
- Never upload to Drive
- Never trade or recommend a position
- Do not wake other bots (except standing softshort/TC handoffs to 總指揮)
- Do not write a market brief (brief bots own that)
- Quiet when nothing cleared the bar (routine delivery rule)

### Voice
Short. Mix of short English + Traditional Chinese OK. Do not switch whole reply to Cantonese. No filler.

### Partners / handoffs
| Partner | id | Role vs X Monitor |
|---|---|---|
| 總指揮 | `7aa7a8a6-b16b-4740-a4df-1d5d7eded8c4` | Captain; TC tickets; softshort ≤8 Markets/Setups/AI for US Brief seed; Mode A/B failure ACK |
| US Market Daily Brief | `44fb5c78-45d1-4716-b849-a5a6a0c1867b` | Downstream consumer of softshort seeds (via 總指揮) |
| Work Verifier | `037de516-dbc1-4565-a127-5dbb0f691729` | Not default for X Monitor Finals (Jev `needs_wv` low; signal is not WV-gated brief) |
| 记忆管家 | `bae6933d-92a5-4d8c-8bf0-3a4f9fb7b1ed` | Fleet memory backup requester |
| Self Improver | `1d369773-e1f5-4fdf-9a3a-2a38b1f54e16` | Lessons when routed |

### Jev (B+C) — TypeSafe
- Skill: [Jev Fleet Decisions](sand-workflow:jev-fleet-decisions)
- Docs: `/workspace/typesafe-jev/fleet-decision-layer-v1.md`
- Thresholds: `/workspace/typesafe-jev/config/thresholds.json`
- Client: `/workspace/typesafe-jev/.venv/bin/python /workspace/typesafe-jev/jev_client.py`
- Key: `[REDACTED:TYPESAFE_API_KEY]` only — never paste values
- Log: `/workspace/typesafe-jev/logs/` when practical
- **B pre-task:** every TC / user task before grind → `pre_task` pack `act` | `evidence_enough` | `escalate` | `cost_tier`
- **C exit:** before Final / handoff → `ready_for_justin` | `needs_wv` | `conflict` | `soft_ambition`
- Front-door A **OFF** (總指揮 routing)
- Never invent tickers/prices via Jev; never auto-send / auto-trade from a Noul

---

## 2. Historical decisions / locked rules

1. **List-first primary source:** X list `2097092298073166050` (`https://x.com/i/lists/2097092298073166050`). Optional thin-list supplement only when list is thin on a bar topic or major event underway — never replace list with random follow graph.
2. **Skill:** [X signal retrieval](sand-workflow:x-signal-retrieval) at `/home/box/agent-data/workflows/x-signal-retrieval/SKILL.md` — adapted from @dotey lesson (`https://x.com/dotey/status/2110407057622904945`): account tiers + search recipes + novelty/value gates + silence when empty.
3. **Novelty store:** `/workspace/x-monitor/seen.json` — `{id, url, topic_keys[], delivered_at, run}`; drop seen ids + near-dup topic_keys last 7d unless material update; prune >7d after each delivery.
4. **Layout locked:** HiTw93 Signal English (Main threads → ≤~8 author blocks → 💡 → optional Glance → `不構成投資建議` if markets).
5. **Softshort:** ≤8 one-line Markets/Setups/AI bullets → SendToAgent 總指揮 only (US Brief seed). Path pattern: `/workspace/x-monitor/<run>-softshort.md`.
6. **Public X only** for list reads (`x` namespace). Justin X plugin not required for this job; never act as Justin on X.
7. **Routines triad (all enabled as of backup):**
   - Weekday X signal — `15 7 * * 1-5` HKT — window since prior Evening ~18:15
   - Evening X signal — `15 18 * * 1-5` HKT — window since same-day Weekday ~07:15
   - Saturday X signal — `15 7 * * 6` HKT flexible ±15 — window since prior Friday Evening ~18:15
8. **Failure modes (locked language for 總指揮):**
   - **Mode A:** Activity failed before turn / before scrape
   - **Mode B:** scrape OK on disk; stalled before Final body / handoff → recover from pages/acc/candidates/barcands; no re-scrape; parent SendToUser
9. **Parent-only delivery:** automation/executor handoffs — parent SendToUser body verbatim; executors do not SendToUser.
10. **No routine recreate** on Mode B unless Justin/總指揮 ask; leave enabled.
11. **Shared (via 總指揮):** US Market Daily Brief may seed from X Monitor softshort when available; do not remake old briefs for seed improvements.

---

## 3. Live snapshot (2026-10-26 HKT)

### Routines (authoritative status at prior turn)
| Routine | Folder | Schedule | Enabled | Last noted status |
|---|---|---|---|---|
| Weekday X signal | `weekday-x-signal` | `CRON_TZ=Asia/Hong_Kong 15 7 * * 1-5` | yes | 2026-10-26 07:18 HKT **failed** (Grok Bot usage exhausted) |
| Evening X signal | `evening-x-signal` | `CRON_TZ=Asia/Hong_Kong 15 18 * * 1-5` | yes | 2026-10-26 18:16 HKT **failed** (Grok Bot usage exhausted) |
| Saturday X signal | `saturday-x-signal` | `CRON_TZ=Asia/Hong_Kong 15 7 * * 6` flexible ±15 | yes | 2026-10-24 Mode B after scrape; oneshot recovery delivered; left enabled |

### Key paths
| Path | Purpose |
|---|---|
| `/workspace/x-monitor/` | Working dir: pages, acc, body, softshort |
| `/workspace/x-monitor/seen.json` | Novelty ledger (~296 ids at backup; latest run `ondemand-2026-10-26`) |
| `/workspace/x-monitor/ondemand-2026-10-26-body.md` | Latest delivered body (Mon fill) |
| `/workspace/x-monitor/ondemand-2026-10-26-softshort.md` | Softshort for 總指揮 |
| `/workspace/x-monitor/saturday-2026-10-24-body.md` | Sat recovery Final |
| `/home/box/agent-data/workflows/x-signal-retrieval/SKILL.md` | Retrieval skill |
| `/workspace/typesafe-jev/` | Jev client + thresholds |

### Recent deliveries (journal)
- **2026-10-26 on-demand evening:** Weekday+Evening failed on usage; oneshot Sat→Mon window — 603 unique posts / 132 barcands / 8 blocks + Glance; themes: Iran relief futures, CCC HY 18%, Musk neocloud funding wall, Lula/EWZ, KOSPI−1.46% + GS 12k→9k, China ¥129B pump, META $22.5B raise; softshort FYI’d to 總指揮; run=`ondemand-2026-10-26`
- **2026-10-24 Saturday:** Mode B (pages 1–21 / 506 posts on disk ~07:24–07:26); TC-20261024-01 oneshot from disk; 8 blocks; 總指揮 ACK CLOSED
- **2026-10-23 Evening / Weekday:** delivered successfully (8 blocks each)
- **2026-10-22 Evening / Weekday:** delivered successfully
- **2026-10-21 Weekday:** Mode A Activity fail → oneshot recovery (TC-20261021-01)

### Open work
- None blocking. Idle after Mon on-demand delivery.
- Routines remain **enabled**; next fires depend on account Grok Bot usage being available again (infra outside this bot).

### Pending confirms
- **None.** No pending Justin confirms, widgets, or TC tickets open for X Monitor as of this backup.
- Note (informational, not a confirm): 2026-10-26 scheduled Weekday+Evening failures were usage-quota; on-demand filled the gap. No ask to recreate routines.

---

## 4. Secrets (names only)

| Env / secret | Backup form |
|---|---|
| TYPESAFE_API_KEY | `[REDACTED:TYPESAFE_API_KEY]` |
| FIRECRAWL_API_KEY | `[REDACTED:FIRECRAWL_API_KEY]` (present on box; not required for core X Monitor list job) |
| AGENTMAIL_API_KEY | `[REDACTED:AGENTMAIL_API_KEY]` (present on box; not used by X Monitor ONE JOB) |

No X bearer tokens. Public `x` MCP uses Grok Bot shared quota. Never paste token values into backups or chat.

---

## 5. Coverage checklist
- [x] Identity (profile, ONE JOB, ANTI-JOBS, voice)
- [x] Partners / handoff matrix
- [x] Jev B+C wiring
- [x] Locked rules (list, skill, seen, HiTw93, softshort, Mode A/B)
- [x] All three routines + schedules + prompts summary
- [x] Live paths + latest runs + seen.json status
- [x] Open work / pending confirms
- [x] Secrets redacted by name only
